#!/bin/bash
# ============================================================
# Guardrail.ai VPS Auto-Setup Script
# Server: 72.61.241.106 | Domain: guardrail.ai
# Run this on your VPS as root
# ============================================================

set -e  # Exit on any error
echo ""
echo "============================================"
echo " GUARDRAIL.AI VPS SETUP — Starting..."
echo "============================================"
echo ""

# ── 1. System Update ─────────────────────────────────────────
echo "[1/7] Updating system packages..."
apt-get update -y && apt-get upgrade -y
echo "✓ System updated"

# ── 2. Install Node.js 20 ────────────────────────────────────
echo "[2/7] Installing Node.js 20..."
curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
apt-get install -y nodejs
echo "✓ Node.js $(node --version) installed"

# ── 3. Install PM2, Nginx, Certbot ──────────────────────────
echo "[3/7] Installing PM2, Nginx, Certbot..."
npm install -g pm2
apt-get install -y nginx certbot python3-certbot-nginx
echo "✓ PM2, Nginx, Certbot installed"

# ── 4. Create app directory ──────────────────────────────────
echo "[4/7] Creating app directory..."
mkdir -p /var/www/guardrail
echo "✓ Directory /var/www/guardrail created"

# ── 5. Configure Nginx ───────────────────────────────────────
echo "[5/7] Configuring Nginx..."
cat > /etc/nginx/sites-available/guardrail.ai << 'NGINX_CONF'
server {
    listen 80;
    server_name guardrail.ai www.guardrail.ai;

    # Gzip compression
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        proxy_read_timeout 86400;
    }

    # Cache static assets
    location /_next/static/ {
        proxy_pass http://localhost:3000;
        add_header Cache-Control "public, max-age=31536000, immutable";
    }
}
NGINX_CONF

# Enable site
ln -sf /etc/nginx/sites-available/guardrail.ai /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# Test and reload Nginx
nginx -t && systemctl reload nginx
echo "✓ Nginx configured and running"

# ── 6. Configure firewall ────────────────────────────────────
echo "[6/7] Configuring firewall..."
ufw allow ssh
ufw allow 80
ufw allow 443
ufw --force enable
echo "✓ Firewall configured (SSH, HTTP, HTTPS allowed)"

# ── 7. Setup PM2 startup ─────────────────────────────────────
echo "[7/7] Configuring PM2 startup on reboot..."
pm2 startup systemd -u root --hp /root | tail -1 | bash
echo "✓ PM2 startup configured"

echo ""
echo "============================================"
echo " BASE SETUP COMPLETE!"
echo " Next: Upload your app files, then run:"
echo " cd /var/www/guardrail && npm install"
echo " pm2 start 'npm run start' --name guardrail"
echo " pm2 save"
echo " certbot --nginx -d guardrail.ai -d www.guardrail.ai"
echo "============================================"
echo ""
