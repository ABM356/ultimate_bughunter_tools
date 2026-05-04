"""Initial schema.

Revision ID: 001_initial
Revises:
Create Date: 2026-01-01 00:00:00.000000
"""
from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "001_initial"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _ts_columns() -> list[sa.Column]:
    return [
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    ]


def upgrade() -> None:
    op.execute('CREATE EXTENSION IF NOT EXISTS "pgcrypto"')

    # tenants ---------------------------------------------------------
    op.create_table(
        "tenants",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("slug", sa.String(64), nullable=False, unique=True),
        sa.Column("tier", sa.Integer, nullable=False, server_default="1"),
        sa.Column("status", sa.String(32), nullable=False, server_default="active"),
        sa.Column("billing_email", sa.String(255), nullable=True),
        sa.Column("stripe_customer_id", sa.String(255), nullable=True),
        sa.Column("settings", postgresql.JSONB, nullable=False, server_default="{}"),
        *_ts_columns(),
    )

    # users ----------------------------------------------------------
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("email", sa.String(255), nullable=False, unique=True),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("full_name", sa.String(255), nullable=False, server_default=""),
        sa.Column("role", sa.String(32), nullable=False, server_default="client"),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default=sa.true()),
        sa.Column("last_login_at", sa.DateTime(timezone=True), nullable=True),
        *_ts_columns(),
    )
    op.create_index("ix_users_tenant_id", "users", ["tenant_id"])

    # bounty programs / submissions ----------------------------------
    op.create_table(
        "bounty_programs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), nullable=True, index=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("description", sa.Text, nullable=False, server_default=""),
        sa.Column("scope", postgresql.JSONB, nullable=False, server_default="{}"),
        sa.Column("rewards", postgresql.JSONB, nullable=False, server_default="{}"),
        sa.Column("rules", sa.Text, nullable=False, server_default=""),
        sa.Column("status", sa.String(32), nullable=False, server_default="draft"),
        *_ts_columns(),
    )
    op.create_table(
        "bounty_submissions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), nullable=True, index=True),
        sa.Column(
            "program_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("bounty_programs.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "hunter_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("description", sa.Text, nullable=False, server_default=""),
        sa.Column("severity", sa.String(16), nullable=False, server_default="medium"),
        sa.Column("status", sa.String(32), nullable=False, server_default="submitted"),
        sa.Column("evidence", postgresql.JSONB, nullable=False, server_default="{}"),
        sa.Column("reward_amount", sa.Numeric(12, 2), nullable=True),
        sa.Column("paid_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("triaged_at", sa.DateTime(timezone=True), nullable=True),
        *_ts_columns(),
    )

    # vulnerabilities ----------------------------------------------
    op.create_table(
        "vulnerabilities",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), nullable=True, index=True),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("description", sa.Text, nullable=False, server_default=""),
        sa.Column("cvss_base", sa.Float, nullable=False, server_default="0"),
        sa.Column("cvss_exploitability", sa.Float, nullable=False, server_default="0"),
        sa.Column("cvss_impact", sa.Float, nullable=False, server_default="0"),
        sa.Column("cvss_vector", sa.String(128), nullable=True),
        sa.Column("severity", sa.String(16), nullable=False, server_default="info"),
        sa.Column("status", sa.String(32), nullable=False, server_default="open"),
        sa.Column("cwe", sa.String(32), nullable=True, index=True),
        sa.Column("cve", sa.String(32), nullable=True, index=True),
        sa.Column(
            "evidence_urls",
            postgresql.ARRAY(sa.String),
            nullable=False,
            server_default="{}",
        ),
        sa.Column("remediation", sa.Text, nullable=False, server_default=""),
        sa.Column("metadata", postgresql.JSONB, nullable=False, server_default="{}"),
        *_ts_columns(),
    )

    # scans ---------------------------------------------------------
    op.create_table(
        "scans",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), nullable=True, index=True),
        sa.Column("target", sa.String(512), nullable=False, index=True),
        sa.Column("scan_type", sa.String(32), nullable=False, server_default="web"),
        sa.Column("scan_level", sa.String(16), nullable=False, server_default="fast"),
        sa.Column("tier", sa.Integer, nullable=False, server_default="1"),
        sa.Column("status", sa.String(32), nullable=False, server_default="queued"),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("findings_count", sa.Integer, nullable=False, server_default="0"),
        sa.Column("raw_output", postgresql.JSONB, nullable=False, server_default="{}"),
        sa.Column(
            "tools_used", postgresql.ARRAY(sa.String), nullable=False, server_default="{}"
        ),
        sa.Column("error_message", sa.Text, nullable=True),
        *_ts_columns(),
    )

    # alerts --------------------------------------------------------
    op.create_table(
        "alerts",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), nullable=True, index=True),
        sa.Column("severity", sa.String(16), nullable=False, server_default="medium"),
        sa.Column("source", sa.String(64), nullable=False, server_default="siem"),
        sa.Column("message", sa.Text, nullable=False, server_default=""),
        sa.Column("ip", sa.String(64), nullable=True, index=True),
        sa.Column("user_identifier", sa.String(255), nullable=True),
        sa.Column("status", sa.String(32), nullable=False, server_default="new"),
        sa.Column("correlation_id", postgresql.UUID(as_uuid=True), nullable=True, index=True),
        sa.Column("raw_event", postgresql.JSONB, nullable=False, server_default="{}"),
        *_ts_columns(),
    )

    # incidents -----------------------------------------------------
    op.create_table(
        "incidents",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), nullable=True, index=True),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("description", sa.Text, nullable=False, server_default=""),
        sa.Column("severity", sa.String(16), nullable=False, server_default="medium"),
        sa.Column("status", sa.String(32), nullable=False, server_default="open"),
        sa.Column("timeline", postgresql.JSONB, nullable=False, server_default="[]"),
        sa.Column("affected_assets", postgresql.JSONB, nullable=False, server_default="[]"),
        sa.Column("response_actions", postgresql.JSONB, nullable=False, server_default="[]"),
        sa.Column("detected_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("resolved_at", sa.DateTime(timezone=True), nullable=True),
        *_ts_columns(),
    )

    # assets --------------------------------------------------------
    op.create_table(
        "assets",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), nullable=True, index=True),
        sa.Column("name", sa.String(255), nullable=False, index=True),
        sa.Column("asset_type", sa.String(32), nullable=False, server_default="domain"),
        sa.Column("identifier", sa.String(512), nullable=False, index=True),
        sa.Column("attributes", postgresql.JSONB, nullable=False, server_default="{}"),
        sa.Column("criticality", sa.Integer, nullable=False, server_default="1"),
        sa.Column("owner", sa.String(255), nullable=True),
        sa.Column("status", sa.String(32), nullable=False, server_default="active"),
        *_ts_columns(),
    )

    # training ------------------------------------------------------
    op.create_table(
        "training_modules",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), nullable=True, index=True),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("description", sa.Text, nullable=False, server_default=""),
        sa.Column("difficulty", sa.String(16), nullable=False, server_default="beginner"),
        sa.Column("duration_minutes", sa.Integer, nullable=False, server_default="30"),
        sa.Column("content", postgresql.JSONB, nullable=False, server_default="{}"),
        sa.Column("tags", postgresql.JSONB, nullable=False, server_default="[]"),
        *_ts_columns(),
    )
    op.create_table(
        "user_progress",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), nullable=True, index=True),
        sa.Column(
            "user_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "module_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("training_modules.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("status", sa.String(32), nullable=False, server_default="enrolled"),
        sa.Column("progress_pct", sa.Integer, nullable=False, server_default="0"),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("score", sa.Integer, nullable=True),
        *_ts_columns(),
    )
    op.create_table(
        "lab_sessions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), nullable=True, index=True),
        sa.Column(
            "user_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "module_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("training_modules.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("container_id", sa.String(128), nullable=True),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("ended_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("status", sa.String(32), nullable=False, server_default="pending"),
        sa.Column("metadata", postgresql.JSONB, nullable=False, server_default="{}"),
        *_ts_columns(),
    )

    # reports -------------------------------------------------------
    op.create_table(
        "reports",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), nullable=True, index=True),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("report_type", sa.String(32), nullable=False, server_default="executive"),
        sa.Column("audience_role", sa.String(32), nullable=False, server_default="ciso"),
        sa.Column("status", sa.String(32), nullable=False, server_default="draft"),
        sa.Column("generated_html", sa.Text, nullable=True),
        sa.Column("generated_pdf_url", sa.String(1024), nullable=True),
        sa.Column("parameters", postgresql.JSONB, nullable=False, server_default="{}"),
        sa.Column("summary", sa.Text, nullable=True),
        *_ts_columns(),
    )

    # scheduled jobs -----------------------------------------------
    op.create_table(
        "scheduled_jobs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), nullable=True, index=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("description", sa.Text, nullable=False, server_default=""),
        sa.Column("cron_expression", sa.String(64), nullable=False),
        sa.Column("job_type", sa.String(64), nullable=False, server_default="scan"),
        sa.Column("payload", postgresql.JSONB, nullable=False, server_default="{}"),
        sa.Column("status", sa.String(32), nullable=False, server_default="active"),
        sa.Column("next_run", sa.DateTime(timezone=True), nullable=True),
        sa.Column("last_run", sa.DateTime(timezone=True), nullable=True),
        sa.Column("last_result", sa.String(32), nullable=True),
        *_ts_columns(),
    )


def downgrade() -> None:
    for table in (
        "scheduled_jobs",
        "reports",
        "lab_sessions",
        "user_progress",
        "training_modules",
        "assets",
        "incidents",
        "alerts",
        "scans",
        "vulnerabilities",
        "bounty_submissions",
        "bounty_programs",
        "users",
        "tenants",
    ):
        op.drop_table(table)
