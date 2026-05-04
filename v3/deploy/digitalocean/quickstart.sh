#!/bin/bash
# ─────────────────────────────────────────────────────────────
# HopeUp Quickstart — One-shot deployment to DigitalOcean
# Run this from your local machine after configuring doctl
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
NC="\033[0m"

echo -e "${GREEN}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║       HopeUp Platform — DigitalOcean Quickstart         ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════╝${NC}"

# Pre-flight
command -v doctl > /dev/null 2>&1 || {
    echo -e "${RED}[!] doctl is required. Install: brew install doctl${NC}"
    exit 1
}

doctl auth list > /dev/null 2>&1 || {
    echo -e "${YELLOW}[*] Run: doctl auth init${NC}"
    exit 1
}

# Get SSH key
SSH_KEY_ID=$(doctl compute ssh-key list --format ID --no-header | head -1)
if [[ -z "$SSH_KEY_ID" ]]; then
    echo -e "${RED}[!] No SSH key found. Add one: https://cloud.digitalocean.com/account/security${NC}"
    exit 1
fi

# Create droplet
if doctl compute droplet get "$DROPLET_NAME" > /dev/null 2>&1; then
    echo -e "${YELLOW}[*] Droplet $DROPLET_NAME already exists${NC}"
else
    echo -e "${GREEN}[*] Creating droplet $DROPLET_NAME ($DROPLET_SIZE in $DROPLET_REGION)...${NC}"
    doctl compute droplet create "$DROPLET_NAME" \
        --image "$DROPLET_IMAGE" \
        --size "$DROPLET_SIZE" \
        --region "$DROPLET_REGION" \
        --ssh-keys "$SSH_KEY_ID" \
        --enable-monitoring \
        --enable-ipv6 \
        --enable-backups \
        --wait
fi

DROPLET_IP=$(doctl compute droplet get "$DROPLET_NAME" --format PublicIPv4 --no-header)
DROPLET_IP6=$(doctl compute droplet get "$DROPLET_NAME" --format PublicIPv6 --no-header || echo "")

echo -e "${GREEN}[+] Droplet IP: $DROPLET_IP${NC}"

# Set up DNS if domain is managed by DigitalOcean
if doctl compute domain get "$DOMAIN" > /dev/null 2>&1; then
    echo -e "${YELLOW}[*] Domain $DOMAIN already on DigitalOcean${NC}"
else
    echo -e "${GREEN}[*] Adding $DOMAIN to DigitalOcean DNS...${NC}"
    doctl compute domain create "$DOMAIN" --ip-address "$DROPLET_IP" || true
fi

echo -e "${GREEN}[*] Creating subdomain records...${NC}"
for sub in app api admin docs status www staging; do
    EXISTING=$(doctl compute domain records list "$DOMAIN" --format Name,Data --no-header | grep "^$sub " || echo "")
    if [[ -n "$EXISTING" ]]; then
        echo -e "  ${YELLOW}- $sub.$DOMAIN already exists${NC}"
    else
        doctl compute domain records create "$DOMAIN" \
            --record-type A \
            --record-name "$sub" \
            --record-data "$DROPLET_IP" \
            --record-ttl 3600 > /dev/null
        echo -e "  ${GREEN}+ $sub.$DOMAIN -> $DROPLET_IP${NC}"
    fi
done

# Wait for SSH
echo -e "${GREEN}[*] Waiting for SSH...${NC}"
for i in {1..30}; do
    if ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 root@"$DROPLET_IP" "echo ok" > /dev/null 2>&1; then
        break
    fi
    sleep 5
done

# Run setup
echo -e "${GREEN}[*] Running server setup...${NC}"
scp -o StrictHostKeyChecking=no setup.sh root@"$DROPLET_IP":/tmp/
ssh -o StrictHostKeyChecking=no root@"$DROPLET_IP" "bash /tmp/setup.sh"

# Copy app files
echo -e "${GREEN}[*] Copying application files...${NC}"
ssh -o StrictHostKeyChecking=no root@"$DROPLET_IP" "mkdir -p /opt/hopeup && chown hopeup:hopeup /opt/hopeup"
scp -o StrictHostKeyChecking=no docker-compose.production.yml Caddyfile deploy.sh root@"$DROPLET_IP":/opt/hopeup/
ssh -o StrictHostKeyChecking=no root@"$DROPLET_IP" "chown hopeup:hopeup /opt/hopeup/* && chmod +x /opt/hopeup/deploy.sh"

echo ""
echo -e "${GREEN}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                  Setup Complete                          ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════╝${NC}"
echo ""
echo "Droplet:    $DROPLET_NAME"
echo "IPv4:       $DROPLET_IP"
echo "IPv6:       $DROPLET_IP6"
echo ""
echo "Next steps (manual — needs your secrets):"
echo ""
echo "  1. SSH in and create .env with secrets:"
echo "     ssh hopeup@$DROPLET_IP"
echo "     cd /opt/hopeup"
echo "     cp .env.example .env && nano .env"
echo ""
echo "  2. Build and push Docker images (from your local machine):"
echo "     doctl registry create hopeup --region $DROPLET_REGION"
echo "     doctl registry login"
echo "     docker build -t registry.digitalocean.com/hopeup/hopeup-backend:latest ../backend && docker push registry.digitalocean.com/hopeup/hopeup-backend:latest"
echo "     docker build -t registry.digitalocean.com/hopeup/hopeup-frontend:latest ../frontend && docker push registry.digitalocean.com/hopeup/hopeup-frontend:latest"
echo ""
echo "  3. Deploy:"
echo "     ssh hopeup@$DROPLET_IP"
echo "     cd /opt/hopeup"
echo "     doctl auth init"
echo "     ./deploy.sh"
echo ""
echo "  4. Verify:"
echo "     curl -I https://app.hopeuptech.ca"
echo "     curl -I https://api.hopeuptech.ca/health"
echo ""
echo "Estimated time to live: 30-60 min"
echo "Estimated cost: ~\$60/month"
