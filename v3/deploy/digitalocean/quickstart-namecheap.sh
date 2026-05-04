#!/bin/bash
# ─────────────────────────────────────────────────────────────
# HopeUp Quickstart — DigitalOcean Droplet + Namecheap DNS
# Domain: hopeuptech.ca (registered at Namecheap)
# ─────────────────────────────────────────────────────────────

set -euo pipefail

DOMAIN="hopeuptech.ca"
DROPLET_NAME="hopeup-prod"
DROPLET_SIZE="s-4vcpu-8gb"
DROPLET_REGION="tor1"
DROPLET_IMAGE="ubuntu-22-04-x64"

GREEN="\033[0;32m"
YELLOW="\033[0;33m"
RED="\033[0;31m"
CYAN="\033[0;36m"
BOLD="\033[1m"
NC="\033[0m"

echo -e "${CYAN}${BOLD}"
cat <<'EOF'
╔══════════════════════════════════════════════════════════════╗
║   HopeUp Platform — Quickstart                               ║
║   DigitalOcean Droplet + Namecheap DNS                       ║
╚══════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# ─── Pre-flight ───
command -v doctl > /dev/null 2>&1 || {
    echo -e "${RED}[!] doctl not found. Install: brew install doctl${NC}"
    exit 1
}

doctl account get > /dev/null 2>&1 || {
    echo -e "${RED}[!] doctl not authenticated. Run: doctl auth init${NC}"
    exit 1
}

SSH_KEY_ID=$(doctl compute ssh-key list --format ID --no-header | head -1)
if [[ -z "$SSH_KEY_ID" ]]; then
    echo -e "${RED}[!] No SSH key in DigitalOcean. Add one:${NC}"
    echo -e "    https://cloud.digitalocean.com/account/security"
    exit 1
fi

echo -e "${GREEN}[+] Pre-flight checks passed${NC}"
echo ""

# ─── Step 1: Create Droplet ───
echo -e "${CYAN}${BOLD}Step 1/5 — Droplet${NC}"
if doctl compute droplet get "$DROPLET_NAME" > /dev/null 2>&1; then
    echo -e "  ${YELLOW}[*] Droplet $DROPLET_NAME already exists, reusing${NC}"
else
    echo -e "  ${GREEN}[*] Creating droplet ($DROPLET_SIZE in $DROPLET_REGION)...${NC}"
    doctl compute droplet create "$DROPLET_NAME" \
        --image "$DROPLET_IMAGE" \
        --size "$DROPLET_SIZE" \
        --region "$DROPLET_REGION" \
        --ssh-keys "$SSH_KEY_ID" \
        --enable-monitoring \
        --enable-ipv6 \
        --enable-backups \
        --wait \
        --format ID,Name,Status \
        --no-header
fi

DROPLET_IP=$(doctl compute droplet get "$DROPLET_NAME" --format PublicIPv4 --no-header)
DROPLET_IP6=$(doctl compute droplet get "$DROPLET_NAME" --format PublicIPv6 --no-header || echo "")
echo -e "  ${GREEN}[+] Droplet IP: ${BOLD}$DROPLET_IP${NC}"
echo ""

# ─── Step 2: DNS Instructions ───
echo -e "${CYAN}${BOLD}Step 2/5 — DNS at Namecheap${NC}"
echo -e "  ${YELLOW}You must add these records at Namecheap manually.${NC}"
echo ""
echo -e "  Open: ${CYAN}https://ap.www.namecheap.com/Domains/DomainControlPanel/$DOMAIN/advancedns${NC}"
echo ""
echo -e "  Add these ${BOLD}A Records${NC} (Host field is just the prefix, not the full domain):"
echo ""
echo "  ┌─────────┬──────────┬──────────────────┐"
echo "  │ Type    │ Host     │ Value            │"
echo "  ├─────────┼──────────┼──────────────────┤"
for sub in @ www app api admin docs status staging; do
    printf "  │ %-7s │ %-8s │ %-16s │\n" "A" "$sub" "$DROPLET_IP"
done
echo "  └─────────┴──────────┴──────────────────┘"
echo ""
echo -e "  ${YELLOW}TTL: Automatic for all records${NC}"
echo ""
echo -e "  ${BOLD}Delete${NC} any default URL Redirect Records or parking-page records first."
echo ""
read -p "  Press ENTER once you've added the DNS records and clicked save... "
echo ""

# ─── Step 3: Wait for DNS propagation ───
echo -e "${CYAN}${BOLD}Step 3/5 — Waiting for DNS propagation${NC}"
echo -e "  ${GREEN}[*] Checking app.$DOMAIN...${NC}"
for i in {1..60}; do
    RESOLVED=$(dig +short app."$DOMAIN" @8.8.8.8 | head -1)
    if [[ "$RESOLVED" == "$DROPLET_IP" ]]; then
        echo -e "  ${GREEN}[+] DNS propagated (took $((i*10))s)${NC}"
        break
    fi
    if [[ $i -eq 60 ]]; then
        echo -e "  ${YELLOW}[!] DNS still propagating after 10 min. Continuing anyway.${NC}"
        echo -e "  ${YELLOW}    Verify later: dig +short app.$DOMAIN${NC}"
    fi
    sleep 10
done
echo ""

# ─── Step 4: Wait for SSH ───
echo -e "${CYAN}${BOLD}Step 4/5 — SSH access${NC}"
echo -e "  ${GREEN}[*] Waiting for SSH...${NC}"
for i in {1..30}; do
    if ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 -o BatchMode=yes root@"$DROPLET_IP" "echo ok" > /dev/null 2>&1; then
        echo -e "  ${GREEN}[+] SSH ready${NC}"
        break
    fi
    sleep 5
done
echo ""

# ─── Step 5: Server setup + file copy ───
echo -e "${CYAN}${BOLD}Step 5/5 — Server hardening + file copy${NC}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo -e "  ${GREEN}[*] Running setup.sh on droplet (Docker, firewall, fail2ban)...${NC}"
scp -o StrictHostKeyChecking=no "$SCRIPT_DIR/setup.sh" root@"$DROPLET_IP":/tmp/
ssh -o StrictHostKeyChecking=no root@"$DROPLET_IP" "bash /tmp/setup.sh" 2>&1 | sed 's/^/    /'

echo -e "  ${GREEN}[*] Copying compose, Caddyfile, deploy.sh...${NC}"
ssh -o StrictHostKeyChecking=no root@"$DROPLET_IP" "mkdir -p /opt/hopeup && chown hopeup:hopeup /opt/hopeup"
scp -o StrictHostKeyChecking=no \
    "$SCRIPT_DIR/docker-compose.production.yml" \
    "$SCRIPT_DIR/Caddyfile" \
    "$SCRIPT_DIR/deploy.sh" \
    "$SCRIPT_DIR/.env.example" \
    root@"$DROPLET_IP":/opt/hopeup/
ssh -o StrictHostKeyChecking=no root@"$DROPLET_IP" "chown hopeup:hopeup /opt/hopeup/* && chmod +x /opt/hopeup/deploy.sh"
echo ""

# ─── Done ───
echo -e "${GREEN}${BOLD}"
cat <<'EOF'
╔══════════════════════════════════════════════════════════════╗
║                      Setup Complete                          ║
╚══════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"
echo "  Droplet:    $DROPLET_NAME"
echo "  IPv4:       $DROPLET_IP"
echo "  IPv6:       $DROPLET_IP6"
echo ""
echo -e "${BOLD}Remaining steps (need YOUR API keys):${NC}"
echo ""
echo -e "${CYAN}1. Build and push Docker images${NC} (from your laptop):"
echo ""
echo "   doctl registry create hopeup --region $DROPLET_REGION"
echo "   doctl registry login"
echo "   cd ../../backend"
echo "   docker build -t registry.digitalocean.com/hopeup/hopeup-backend:latest ."
echo "   docker push registry.digitalocean.com/hopeup/hopeup-backend:latest"
echo "   cd ../frontend"
echo "   docker build -t registry.digitalocean.com/hopeup/hopeup-frontend:latest ."
echo "   docker push registry.digitalocean.com/hopeup/hopeup-frontend:latest"
echo ""
echo -e "${CYAN}2. Configure secrets on the droplet:${NC}"
echo ""
echo "   ssh hopeup@$DROPLET_IP"
echo "   cd /opt/hopeup"
echo "   cp .env.example .env"
echo "   nano .env  # fill in ANTHROPIC_API_KEY, STRIPE_SECRET_KEY, generate passwords"
echo ""
echo -e "${CYAN}3. Authenticate registry on the droplet and deploy:${NC}"
echo ""
echo "   doctl auth init"
echo "   ./deploy.sh"
echo ""
echo -e "${CYAN}4. Visit your live platform:${NC}"
echo ""
echo "   https://app.hopeuptech.ca       — Main app"
echo "   https://api.hopeuptech.ca/docs  — API docs"
echo "   https://admin.hopeuptech.ca     — Admin panel"
echo ""
echo -e "${YELLOW}Caddy will auto-issue Let's Encrypt SSL on first hit. Allow 30-60s on first request.${NC}"
echo ""
