#!/usr/bin/env python3
"""
HopeUp Security Platform — Web Dashboard
Full web-based operating system for cybersecurity assessments.
"""

import os
import sys
import json
import uuid
import secrets
from datetime import datetime, timezone
from functools import wraps

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import (
    Flask, render_template, request, redirect, url_for,
    jsonify, session, flash, send_file, abort,
)
from werkzeug.security import generate_password_hash, check_password_hash

from platform.tools_registry import TOOL_REGISTRY, CATEGORIES, get_tools_by_team, get_tool_count
from platform.tiers import BUSINESS_TIERS, list_tiers, get_tier, get_tier_tools
from platform.scanner import Assessment, OUTPUT_DIR
from platform.report_generator import generate_report
from webapp.ai_engine import AIEngine
from webapp.role_reports import generate_role_report, REPORT_ROLES

app = Flask(__name__)
app.secret_key = os.environ.get("HOPEUP_SECRET_KEY", secrets.token_hex(32))

DATA_DIR = os.path.join(os.path.expanduser("~"), ".hopeup_platform")
DB_FILE = os.path.join(DATA_DIR, "database.json")
os.makedirs(DATA_DIR, exist_ok=True)

ai_engine = AIEngine()


# ─── Database (JSON-based for portability) ───

def _load_db():
    if os.path.isfile(DB_FILE):
        with open(DB_FILE) as f:
            return json.load(f)
    return {"users": {}, "clients": {}, "assessments": {}, "invoices": {}}


def _save_db(db):
    with open(DB_FILE, "w") as f:
        json.dump(db, f, indent=2, default=str)


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return wrapper


# ─── Auth Routes ───

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        db = _load_db()
        user = db["users"].get(email)
        if user and check_password_hash(user["password_hash"], password):
            session["user_id"] = email
            session["user_name"] = user["name"]
            session["user_role"] = user.get("role", "analyst")
            return redirect(url_for("dashboard"))
        flash("Invalid credentials", "error")
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        role = request.form.get("role", "analyst")
        if not all([name, email, password]):
            flash("All fields are required", "error")
            return render_template("register.html")
        db = _load_db()
        if email in db["users"]:
            flash("Email already registered", "error")
            return render_template("register.html")
        db["users"][email] = {
            "name": name,
            "email": email,
            "password_hash": generate_password_hash(password),
            "role": role,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        _save_db(db)
        flash("Account created. Please log in.", "success")
        return redirect(url_for("login"))
    return render_template("register.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ─── Dashboard ───

@app.route("/")
@login_required
def dashboard():
    counts = get_tool_count()
    tiers = list_tiers()
    db = _load_db()
    recent = sorted(
        db["assessments"].values(),
        key=lambda a: a.get("created_at", ""),
        reverse=True,
    )[:5]
    return render_template("dashboard.html",
        tool_counts=counts,
        tiers=tiers,
        recent_assessments=recent,
        user_name=session.get("user_name"),
        user_role=session.get("user_role"),
    )


# ─── Tools Registry ───

@app.route("/tools")
@login_required
def tools():
    team = request.args.get("team")
    tier = request.args.get("tier", type=int)
    filtered = TOOL_REGISTRY
    if team:
        filtered = {k: v for k, v in filtered.items() if v["team"] in (team, "both")}
    if tier:
        filtered = {k: v for k, v in filtered.items() if v["tier"] <= tier}
    return render_template("tools.html",
        tools=filtered,
        categories=CATEGORIES,
        team_filter=team,
        tier_filter=tier,
    )


# ─── Tier System ───

@app.route("/tiers")
@login_required
def tiers():
    tier_data = {}
    for num, tier in BUSINESS_TIERS.items():
        tools = get_tier_tools(num, TOOL_REGISTRY)
        tier_data[num] = {
            **tier,
            "tool_count": len(tools),
            "red_count": len({k: v for k, v in tools.items() if v["team"] in ("red", "both")}),
            "blue_count": len({k: v for k, v in tools.items() if v["team"] in ("blue", "both")}),
        }
    return render_template("tiers.html", tiers=tier_data)


# ─── Assessments ───

@app.route("/assessments")
@login_required
def assessments():
    db = _load_db()
    return render_template("assessments.html",
        assessments=sorted(
            db["assessments"].values(),
            key=lambda a: a.get("created_at", ""),
            reverse=True,
        )
    )


@app.route("/assessments/new", methods=["GET", "POST"])
@login_required
def new_assessment():
    if request.method == "POST":
        target = request.form.get("target", "").strip()
        tier = int(request.form.get("tier", 1))
        scope = request.form.get("scope", "red+blue")
        client_id = request.form.get("client_id", "")

        if not target:
            flash("Target is required", "error")
            return render_template("new_assessment.html", tiers=BUSINESS_TIERS)

        assessment = Assessment(target, tier, scope=scope)
        assessment.prepare()

        db = _load_db()
        db["assessments"][assessment.id] = {
            "id": assessment.id,
            "target": target,
            "tier": tier,
            "tier_name": BUSINESS_TIERS[tier]["name"],
            "scope": scope,
            "client_id": client_id,
            "status": "prepared",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "created_by": session.get("user_id"),
            "output_dir": assessment.output_dir,
        }
        _save_db(db)

        flash(f"Assessment {assessment.id} created", "success")
        return redirect(url_for("view_assessment", assessment_id=assessment.id))

    db = _load_db()
    return render_template("new_assessment.html",
        tiers=BUSINESS_TIERS,
        clients=db.get("clients", {}),
    )


@app.route("/assessments/<assessment_id>")
@login_required
def view_assessment(assessment_id):
    db = _load_db()
    assessment = db["assessments"].get(assessment_id)
    if not assessment:
        abort(404)

    summary_file = os.path.join(assessment.get("output_dir", ""), "summary.json")
    summary = None
    if os.path.isfile(summary_file):
        with open(summary_file) as f:
            summary = json.load(f)

    return render_template("view_assessment.html",
        assessment=assessment,
        summary=summary,
        report_roles=REPORT_ROLES,
    )


@app.route("/assessments/<assessment_id>/run", methods=["POST"])
@login_required
def run_assessment(assessment_id):
    db = _load_db()
    assessment_data = db["assessments"].get(assessment_id)
    if not assessment_data:
        abort(404)

    assessment = Assessment(
        assessment_data["target"],
        assessment_data["tier"],
        scope=assessment_data["scope"],
    )
    assessment.id = assessment_id
    assessment.output_dir = assessment_data["output_dir"]

    assessment.run_assessment()
    generate_report(assessment)

    db["assessments"][assessment_id]["status"] = "completed"
    db["assessments"][assessment_id]["completed_at"] = datetime.now(timezone.utc).isoformat()
    _save_db(db)

    flash("Assessment completed. Report generated.", "success")
    return redirect(url_for("view_assessment", assessment_id=assessment_id))


# ─── AI-Powered Analysis ───

@app.route("/ai/analyze", methods=["POST"])
@login_required
def ai_analyze():
    assessment_id = request.form.get("assessment_id")
    db = _load_db()
    assessment_data = db["assessments"].get(assessment_id)
    if not assessment_data:
        return jsonify({"error": "Assessment not found"}), 404

    summary_file = os.path.join(assessment_data.get("output_dir", ""), "summary.json")
    if not os.path.isfile(summary_file):
        return jsonify({"error": "No scan results found"}), 400

    with open(summary_file) as f:
        summary = json.load(f)

    analysis = ai_engine.analyze_results(summary, assessment_data["tier"])
    return jsonify(analysis)


@app.route("/ai/recommend", methods=["POST"])
@login_required
def ai_recommend():
    data = request.get_json()
    findings = data.get("findings", [])
    tier = data.get("tier", 1)
    recommendations = ai_engine.generate_recommendations(findings, tier)
    return jsonify({"recommendations": recommendations})


# ─── Role-Based Reports ───

@app.route("/assessments/<assessment_id>/report/<role>")
@login_required
def role_report(assessment_id, role):
    if role not in REPORT_ROLES:
        abort(400)

    db = _load_db()
    assessment_data = db["assessments"].get(assessment_id)
    if not assessment_data:
        abort(404)

    summary_file = os.path.join(assessment_data.get("output_dir", ""), "summary.json")
    summary = None
    if os.path.isfile(summary_file):
        with open(summary_file) as f:
            summary = json.load(f)

    report_html = generate_role_report(assessment_data, summary, role)
    report_path = os.path.join(
        assessment_data.get("output_dir", ""),
        f"report_{role}.html"
    )
    with open(report_path, "w") as f:
        f.write(report_html)

    return report_html


# ─── Client Management ───

@app.route("/clients")
@login_required
def clients():
    db = _load_db()
    return render_template("clients.html", clients=db.get("clients", {}))


@app.route("/clients/new", methods=["GET", "POST"])
@login_required
def new_client():
    if request.method == "POST":
        client_id = str(uuid.uuid4())[:8]
        db = _load_db()
        db["clients"][client_id] = {
            "id": client_id,
            "name": request.form.get("name", "").strip(),
            "company": request.form.get("company", "").strip(),
            "email": request.form.get("email", "").strip(),
            "tier": int(request.form.get("tier", 1)),
            "industry": request.form.get("industry", ""),
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        _save_db(db)
        flash("Client added", "success")
        return redirect(url_for("clients"))
    return render_template("new_client.html", tiers=BUSINESS_TIERS)


# ─── Payment / Invoicing ───

@app.route("/invoices")
@login_required
def invoices():
    db = _load_db()
    return render_template("invoices.html", invoices=db.get("invoices", {}))


@app.route("/invoices/new", methods=["GET", "POST"])
@login_required
def new_invoice():
    if request.method == "POST":
        invoice_id = f"INV-{datetime.now(timezone.utc).strftime('%Y%m%d')}-{str(uuid.uuid4())[:4].upper()}"
        db = _load_db()

        tier = int(request.form.get("tier", 1))
        tier_pricing = {1: 500, 2: 2500, 3: 10000, 4: 50000}
        amount = float(request.form.get("amount") or tier_pricing.get(tier, 0))

        db["invoices"][invoice_id] = {
            "id": invoice_id,
            "client_id": request.form.get("client_id", ""),
            "client_name": request.form.get("client_name", ""),
            "assessment_id": request.form.get("assessment_id", ""),
            "tier": tier,
            "amount": amount,
            "currency": request.form.get("currency", "USD"),
            "status": "pending",
            "description": request.form.get("description", f"Tier {tier} Security Assessment"),
            "created_at": datetime.now(timezone.utc).isoformat(),
            "payment_method": request.form.get("payment_method", ""),
            "stripe_payment_link": "",
        }
        _save_db(db)
        flash(f"Invoice {invoice_id} created for ${amount:.2f}", "success")
        return redirect(url_for("invoices"))

    db = _load_db()
    return render_template("new_invoice.html",
        clients=db.get("clients", {}),
        tiers=BUSINESS_TIERS,
        tier_pricing={1: 500, 2: 2500, 3: 10000, 4: 50000},
    )


@app.route("/invoices/<invoice_id>/pay", methods=["POST"])
@login_required
def pay_invoice(invoice_id):
    db = _load_db()
    invoice = db["invoices"].get(invoice_id)
    if not invoice:
        abort(404)

    payment_method = request.form.get("payment_method", "stripe")

    if payment_method == "stripe":
        # Stripe integration placeholder — replace with real Stripe keys
        stripe_key = os.environ.get("STRIPE_SECRET_KEY", "")
        if stripe_key:
            try:
                import stripe
                stripe.api_key = stripe_key
                checkout = stripe.checkout.Session.create(
                    payment_method_types=["card"],
                    line_items=[{
                        "price_data": {
                            "currency": invoice["currency"].lower(),
                            "product_data": {"name": invoice["description"]},
                            "unit_amount": int(invoice["amount"] * 100),
                        },
                        "quantity": 1,
                    }],
                    mode="payment",
                    success_url=request.host_url + f"invoices/{invoice_id}/success",
                    cancel_url=request.host_url + f"invoices/{invoice_id}",
                )
                return redirect(checkout.url)
            except Exception as e:
                flash(f"Stripe error: {e}", "error")
        else:
            flash("Stripe not configured. Set STRIPE_SECRET_KEY environment variable.", "warning")

    elif payment_method == "paypal":
        flash("PayPal integration: Set PAYPAL_CLIENT_ID and PAYPAL_SECRET environment variables.", "warning")

    elif payment_method == "manual":
        db["invoices"][invoice_id]["status"] = "paid"
        db["invoices"][invoice_id]["paid_at"] = datetime.now(timezone.utc).isoformat()
        _save_db(db)
        flash("Invoice marked as paid", "success")

    return redirect(url_for("invoices"))


@app.route("/invoices/<invoice_id>/success")
@login_required
def invoice_success(invoice_id):
    db = _load_db()
    if invoice_id in db["invoices"]:
        db["invoices"][invoice_id]["status"] = "paid"
        db["invoices"][invoice_id]["paid_at"] = datetime.now(timezone.utc).isoformat()
        _save_db(db)
    flash("Payment successful!", "success")
    return redirect(url_for("invoices"))


# ─── Training ───

@app.route("/training")
@login_required
def training():
    from training.curriculum import CURRICULUM, get_learning_path
    paths = {
        "red": get_learning_path("red"),
        "blue": get_learning_path("blue"),
        "deployment": get_learning_path("deployment"),
    }
    return render_template("training.html", curriculum=CURRICULUM, paths=paths)


# ─── API Endpoints ───

@app.route("/api/v1/status")
def api_status():
    return jsonify({
        "platform": "HopeUp Security Platform",
        "version": "2.0.0",
        "status": "operational",
        "tools": get_tool_count(),
        "tiers": len(BUSINESS_TIERS),
    })


@app.route("/api/v1/tools")
def api_tools():
    return jsonify(TOOL_REGISTRY)


@app.route("/api/v1/tiers")
def api_tiers():
    return jsonify(BUSINESS_TIERS)


def create_app():
    return app


if __name__ == "__main__":
    port = int(os.environ.get("HOPEUP_PORT", 5000))
    debug = os.environ.get("HOPEUP_DEBUG", "false").lower() == "true"
    print(f"\n  HopeUp Security Platform — Web Dashboard")
    print(f"  Running on http://localhost:{port}")
    print(f"  Press Ctrl+C to stop\n")
    app.run(host="0.0.0.0", port=port, debug=debug)
