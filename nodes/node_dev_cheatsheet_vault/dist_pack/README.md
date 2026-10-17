# CloudZero Production Kit ($12)

Congratulations on acquiring the **CloudZero Production Kit**. This package contains everything you need to deploy production-grade cloud infrastructure for $0/month.

---

## 📁 What's Included:
* **`docker-compose.yml`**: Production stack with Caddy, App backend, Redis, and Postgres.
* **`Caddyfile`**: Pre-configured automatic Let's Encrypt SSL, Brotli/Gzip, and security headers.
* **`terraform/main.tf`**: Automated Cloudflare DNS and WAF rate-limiting IaC.
* **`CLOUDZERO_PLAYBOOK.md`**: Complete step-by-step guide to claiming Oracle 24GB free compute, configuring Cloudflare R2, and eliminating AWS bills.

---

## 🚀 Quick Launch:
```bash
# 1. Edit Caddyfile with your domain
# 2. Start the stack
docker-compose up -d

# 3. Check logs
docker-compose logs -f
```
