# HopeUp Deployment Guide — DigitalOcean

Production deployment of the HopeUp Security Platform to DigitalOcean for the domain **hopeuptech.ca**.

---

## Architecture

```
                    ┌──────────────────────────────┐
                    │    hopeuptech.ca DNS         │
                    └──────────────┬───────────────┘
                                   │
          ┌────────────────────────┼─────────────────────────┐
          │             │          │          │              │
       app.        api.        admin.       docs.        status.
          │             │          │          │              │
          └─────────────┴────┬─────┴──────────┴──────────────┘
                             │ HTTPS (443)
                  ┌──────────▼──────────┐
                  │   DigitalOcean      │
                  │   Droplet           │
                  │   ┌──────────────┐  │
                  │   │   Caddy      │  │ ← Auto-HTTPS via Let's Encrypt
                  │   └──────┬───────┘  │
                  │          │          │
                  │  ┌───────┼───────┐  │
                  │  │       │       │  │
                  │ ┌▼┐    ┌─▼─┐   ┌─▼─┐│
                  │ │FE│   │API│   │WS ││
                  │ └──┘   └─┬─┘   └───┘│
                  │          │          │
                  │  ┌───────┼───────┐  │
                  │  │       │       │  │
                  │ ┌▼┐    ┌─▼┐    ┌─▼─┐│
                  │ │PG│   │RD│    │ES ││
                  │ └──┘   └──┘    └───┘│
                  └─────────────────────┘
```

---

## Prerequisites

- [ ] DigitalOcean account with billing enabled
- [ ] Domain `hopeuptech.ca` registered (anywhere)
- [ ] Anthropic API key (for AI features)
- [ ] Stripe account (for payments)
- [ ] `doctl` CLI installed locally: `brew install doctl`
- [ ] SSH key added to DigitalOcean: https://cloud.digitalocean.com/account/security

---

## Step 1: Create the Droplet

### Option A: Using doctl (recommended)
```bash
# Authenticate
doctl auth init

# Create droplet (8GB RAM, 4 vCPUs, ~$48/month)
doctl compute droplet create hopeup-prod \
  --image ubuntu-22-04-x64 \
  --size s-4vcpu-8gb \
  --region tor1 \
  --ssh-keys $(doctl compute ssh-key list --format ID --no-header | head -1) \
  --enable-monitoring \
  --enable-ipv6 \
  --enable-backups \
  --wait

# Get the IP
doctl compute droplet get hopeup-prod --format PublicIPv4 --no-header
```

### Option B: Using the web console
1. Go to https://cloud.digitalocean.com/droplets/new
2. Choose: Ubuntu 22.04 LTS
3. Plan: CPU-Optimized → 4 vCPUs / 8GB RAM ($48/month)
4. Region: Toronto (tor1) or closest to your users
5. Authentication: SSH key
6. Hostname: `hopeup-prod`
7. Enable: Backups, Monitoring, IPv6
8. Click "Create Droplet"

**Note your droplet's IPv4 and IPv6 addresses.**

---

## Step 2: Configure DNS

Point all subdomains at your droplet — see [dns-records.txt](dns-records.txt).

Quick version (if domain is on DigitalOcean):
```bash
DROPLET_IP=$(doctl compute droplet get hopeup-prod --format PublicIPv4 --no-header)

doctl compute domain create hopeuptech.ca --ip-address $DROPLET_IP

for sub in app api admin docs status www staging; do
  doctl compute domain records create hopeuptech.ca \
    --record-type A --record-name $sub --record-data $DROPLET_IP
done
```

---

## Step 3: Initial Server Setup

```bash
# Copy the setup script and run it
DROPLET_IP=<your-droplet-ip>
scp setup.sh root@$DROPLET_IP:/tmp/
ssh root@$DROPLET_IP "bash /tmp/setup.sh"
```

This installs Docker, configures the firewall, creates a `hopeup` user, and tunes the system.

---

## Step 4: Build and Push Docker Images

### Option A: Using DigitalOcean Container Registry
```bash
# Create registry
doctl registry create hopeup --region tor1

# Login locally
doctl registry login

# Build and push backend
cd v3/backend
docker build -t registry.digitalocean.com/hopeup/hopeup-backend:latest .
docker push registry.digitalocean.com/hopeup/hopeup-backend:latest

# Build and push frontend
cd ../frontend
docker build -t registry.digitalocean.com/hopeup/hopeup-frontend:latest .
docker push registry.digitalocean.com/hopeup/hopeup-frontend:latest
```

### Option B: Using Docker Hub
Same as above but with `docker.io/your-username/hopeup-backend:latest`.

---

## Step 5: Deploy the Application

```bash
DROPLET_IP=<your-droplet-ip>

# Copy deployment files to the droplet
scp docker-compose.production.yml Caddyfile deploy.sh hopeup@$DROPLET_IP:/opt/hopeup/

# SSH into the droplet
ssh hopeup@$DROPLET_IP

# On the droplet:
cd /opt/hopeup

# Generate strong secrets
cat > .env <<EOF
REGISTRY=registry.digitalocean.com/hopeup
VERSION=latest
POSTGRES_USER=hopeup
POSTGRES_PASSWORD=$(openssl rand -base64 32 | tr -d '/+=')
POSTGRES_DB=hopeup_prod
REDIS_PASSWORD=$(openssl rand -base64 32 | tr -d '/+=')
JWT_SECRET=$(openssl rand -base64 64 | tr -d '/+=')
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
STRIPE_SECRET_KEY=sk_live_...
EOF

chmod 600 .env

# Login to registry on the droplet
doctl auth init  # or: docker login

# Run the deploy script
chmod +x deploy.sh
./deploy.sh
```

---

## Step 6: Verify Deployment

```bash
# Check services are running
ssh hopeup@$DROPLET_IP "cd /opt/hopeup && docker compose -f docker-compose.production.yml ps"

# Test endpoints
curl -I https://app.hopeuptech.ca
curl -I https://api.hopeuptech.ca/health
curl https://api.hopeuptech.ca/docs
```

Caddy will automatically request Let's Encrypt certificates on first request to each subdomain.

---

## Step 7: Create Initial Admin User

```bash
ssh hopeup@$DROPLET_IP

cd /opt/hopeup

docker compose -f docker-compose.production.yml exec backend python -c "
import asyncio
from app.core.database import async_session_maker
from app.core.security import hash_password
from app.models.user import User
import uuid

async def create_admin():
    async with async_session_maker() as session:
        admin = User(
            id=uuid.uuid4(),
            email='admin@hopeuptech.ca',
            password_hash=hash_password('CHANGE_ME_IMMEDIATELY'),
            full_name='HopeUp Admin',
            role='admin',
            is_active=True,
        )
        session.add(admin)
        await session.commit()
        print(f'Admin created: {admin.email}')

asyncio.run(create_admin())
"
```

Login at https://app.hopeuptech.ca with `admin@hopeuptech.ca` / `CHANGE_ME_IMMEDIATELY` and **change the password immediately**.

---

## Operations

### View logs
```bash
ssh hopeup@$DROPLET_IP "cd /opt/hopeup && docker compose -f docker-compose.production.yml logs -f --tail 100"
```

### Update to new version
```bash
# Push new images, then:
ssh hopeup@$DROPLET_IP "cd /opt/hopeup && ./deploy.sh"
```

### Backup database
```bash
ssh hopeup@$DROPLET_IP "cd /opt/hopeup && docker compose exec -T postgres pg_dump -U hopeup hopeup_prod | gzip > /opt/hopeup/backups/db_$(date +%F).sql.gz"
```

### Restart services
```bash
ssh hopeup@$DROPLET_IP "cd /opt/hopeup && docker compose -f docker-compose.production.yml restart"
```

---

## Cost Estimate

| Item | Cost |
|------|------|
| Droplet (s-4vcpu-8gb) | $48/mo |
| Backups | $9.60/mo (20% of droplet) |
| Container Registry (basic) | $5/mo |
| Domain (annual, prorated) | ~$1.50/mo |
| **Total** | **~$64/mo** |

Plus usage-based:
- Bandwidth above 5TB: $0.01/GB
- Anthropic API: pay-per-token

---

## Scaling Path

When you outgrow the single droplet:

1. **Move PostgreSQL to managed database** ($15/mo) — DigitalOcean Managed Postgres
2. **Move Redis to managed** ($15/mo) — DigitalOcean Managed Redis
3. **Add a second droplet** for the application tier (load balanced)
4. **Upgrade to DOKS** (Kubernetes) — use the manifests in `v3/infrastructure/kubernetes/`

---

## Troubleshooting

**Services won't start:**
```bash
docker compose -f docker-compose.production.yml logs <service-name>
```

**SSL certificates not issuing:**
- Verify DNS has propagated: `dig +short app.hopeuptech.ca`
- Check Caddy logs: `docker compose logs caddy`
- Caddy needs port 80 open to validate domain

**Out of memory:**
- Reduce Elasticsearch heap: change `ES_JAVA_OPTS=-Xms256m -Xmx256m`
- Or upgrade droplet to 16GB

**Database migrations failing:**
```bash
docker compose exec backend alembic current
docker compose exec backend alembic upgrade head
```
