#!/bin/bash
# ─────────────────────────────────────────────────────────────
# HopeUp Initial Server Setup — Run ONCE on a fresh DigitalOcean Droplet
# Tested on Ubuntu 22.04 LTS
# Usage: ssh root@DROPLET_IP "bash -s" < setup.sh
# ─────────────────────────────────────────────────────────────

set -euo pipefail

DEPLOY_USER="hopeup"
DEPLOY_DIR="/opt/hopeup"

echo "[*] Updating system packages..."
apt-get update
apt-get upgrade -y

echo "[*] Installing dependencies..."
apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    ufw \
    fail2ban \
    git \
    htop \
    unattended-upgrades

echo "[*] Installing Docker..."
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
chmod a+r /etc/apt/keyrings/docker.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
    https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
    tee /etc/apt/sources.list.d/docker.list > /dev/null

apt-get update
apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

echo "[*] Creating deploy user..."
if ! id -u "$DEPLOY_USER" > /dev/null 2>&1; then
    adduser --disabled-password --gecos "" "$DEPLOY_USER"
    usermod -aG docker "$DEPLOY_USER"
fi

echo "[*] Creating deploy directory..."
mkdir -p "$DEPLOY_DIR"
chown -R "$DEPLOY_USER":"$DEPLOY_USER" "$DEPLOY_DIR"

echo "[*] Configuring firewall..."
ufw default deny incoming
ufw default allow outgoing
ufw allow 22/tcp comment 'SSH'
ufw allow 80/tcp comment 'HTTP'
ufw allow 443/tcp comment 'HTTPS'
ufw --force enable

echo "[*] Configuring fail2ban..."
systemctl enable --now fail2ban

echo "[*] Configuring automatic security updates..."
dpkg-reconfigure --priority=low unattended-upgrades

echo "[*] Configuring sysctl for production..."
cat >> /etc/sysctl.conf <<'EOF'

# HopeUp tuning
vm.max_map_count=262144
fs.file-max=2097152
net.core.somaxconn=65535
net.ipv4.tcp_max_syn_backlog=65535
EOF
sysctl -p

echo ""
echo "[+] Server setup complete"
echo ""
echo "Next steps:"
echo "  1. SSH as the deploy user: ssh $DEPLOY_USER@<droplet_ip>"
echo "  2. Clone the repo to $DEPLOY_DIR"
echo "  3. Copy .env.example to .env and fill in secrets"
echo "  4. Run ./deploy.sh"
echo ""
