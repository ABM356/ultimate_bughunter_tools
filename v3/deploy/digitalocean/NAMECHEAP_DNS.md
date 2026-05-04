# Namecheap DNS Setup for hopeuptech.ca

Your domain is at **Namecheap**, your server is at **DigitalOcean**. This guide walks you through pointing the right subdomains at your droplet.

You have two options. **Option A is simpler — pick that.**

---

## Option A — Keep DNS at Namecheap (recommended)

Add A records at Namecheap pointing to your DigitalOcean droplet IP.

### Step 1: Get your droplet IP
After running `./quickstart.sh`, the script prints your IPv4. If you've already created the droplet:
```bash
doctl compute droplet get hopeup-prod --format PublicIPv4 --no-header
```

Save this IP — you'll paste it 7 times in the next step.

### Step 2: Open Namecheap dashboard
1. Go to https://ap.www.namecheap.com/Domains/DomainControlPanel/hopeuptech.ca/advancedns
2. (Or: Sign in → Domain List → click "Manage" next to hopeuptech.ca → "Advanced DNS" tab)

### Step 3: Set NAMESERVERS to "Namecheap BasicDNS"
At the top of the Advanced DNS page, make sure **NAMESERVERS** is set to:
- `Namecheap BasicDNS` (the default)

If it shows custom nameservers, change it back to BasicDNS.

### Step 4: Delete any existing default records
Namecheap adds parking page records by default. Delete:
- Any URL Redirect Records
- Any CNAME for `www` pointing to parking
- Any A record for `@` pointing to Namecheap parking IPs (162.255.119.x or similar)

### Step 5: Add these A records

Click **"ADD NEW RECORD"** and create each one. Replace `<DROPLET_IP>` with your actual droplet IP.

| Type | Host | Value | TTL |
|------|------|-------|-----|
| A Record | `@` | `<DROPLET_IP>` | Automatic |
| A Record | `www` | `<DROPLET_IP>` | Automatic |
| A Record | `app` | `<DROPLET_IP>` | Automatic |
| A Record | `api` | `<DROPLET_IP>` | Automatic |
| A Record | `admin` | `<DROPLET_IP>` | Automatic |
| A Record | `docs` | `<DROPLET_IP>` | Automatic |
| A Record | `status` | `<DROPLET_IP>` | Automatic |
| A Record | `staging` | `<DROPLET_IP>` | Automatic |

**Important:** In Namecheap's `Host` field, you type just `app` (NOT `app.hopeuptech.ca`). Namecheap appends the domain automatically.

### Step 6: Click the green checkmark to save

Each record has a checkmark icon — click it. If you don't, the record won't save.

### Step 7: Wait for propagation
DNS propagates in **5-30 minutes** for Namecheap.

Verify from your terminal:
```bash
dig +short app.hopeuptech.ca
dig +short api.hopeuptech.ca
```
Should return your droplet IP. If it returns nothing or wrong IP, wait longer.

Or check globally: https://dnschecker.org/#A/app.hopeuptech.ca

---

## Option B — Move DNS to DigitalOcean (advanced)

If you want to manage DNS via `doctl` and have it auto-update, change the nameservers at Namecheap to point to DigitalOcean.

### Step 1: Add domain to DigitalOcean
```bash
DROPLET_IP=$(doctl compute droplet get hopeup-prod --format PublicIPv4 --no-header)

doctl compute domain create hopeuptech.ca --ip-address $DROPLET_IP

for sub in app api admin docs status www staging; do
  doctl compute domain records create hopeuptech.ca \
    --record-type A --record-name $sub --record-data $DROPLET_IP
done
```

### Step 2: Get DigitalOcean nameservers
DigitalOcean uses these nameservers (always the same):
- `ns1.digitalocean.com`
- `ns2.digitalocean.com`
- `ns3.digitalocean.com`

### Step 3: Update Namecheap nameservers
1. Go to https://ap.www.namecheap.com/Domains/DomainControlPanel/hopeuptech.ca/domain
2. Click "Domain" tab
3. Find **NAMESERVERS** section
4. Change from `Namecheap BasicDNS` to `Custom DNS`
5. Add these three:
   - `ns1.digitalocean.com`
   - `ns2.digitalocean.com`
   - `ns3.digitalocean.com`
6. Click the green checkmark to save

### Step 4: Wait for propagation
Nameserver changes take **30 minutes to 24 hours** to propagate globally. Usually 1-2 hours.

Verify:
```bash
dig +short NS hopeuptech.ca
```
Should return the three DigitalOcean nameservers.

---

## Verification

Once DNS is set (either option), test:

```bash
# Should all return your droplet IP
dig +short app.hopeuptech.ca
dig +short api.hopeuptech.ca
dig +short admin.hopeuptech.ca

# Test reverse — should reach your droplet
ping -c 1 app.hopeuptech.ca
```

If those work, you can proceed to deploy.

---

## Troubleshooting

**"DNS not propagating after an hour"**
- Check at https://dnschecker.org/#A/app.hopeuptech.ca
- Clear your local DNS cache: `sudo dscacheutil -flushcache && sudo killall -HUP mDNSResponder` (macOS)
- Some ISPs cache aggressively — try from your phone hotspot

**"www.hopeuptech.ca shows Namecheap parking page"**
- You forgot to delete the default URL Redirect Record at Namecheap
- Go back to Advanced DNS and delete it

**"SSL cert not issuing"**
- DNS must point to your droplet BEFORE Caddy can get the certificate
- Verify with `dig` first, then restart Caddy: `docker compose restart caddy`

**"Domain doesn't show up in DigitalOcean DNS list"**
- That's only if you chose Option B (moved nameservers). Option A keeps DNS at Namecheap.
