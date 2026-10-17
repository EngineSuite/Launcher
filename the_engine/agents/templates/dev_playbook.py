"""
The Engine - Template: DevOps & Cloud Zero-Cost Architecture Playbook (CloudZero)
Generates high-converting interactive web matrix, savings calculator, and Pro Kit assets.
"""

import json
from pathlib import Path
from typing import Dict, Any


def build_dev_playbook(node_path: Path, opp: Dict[str, Any]) -> None:
    public_dir = node_path / "public"
    src_dir = node_path / "src"
    mon_dir = node_path / "monetization"

    public_dir.mkdir(exist_ok=True)
    src_dir.mkdir(exist_ok=True)
    mon_dir.mkdir(exist_ok=True)

    # 1. index.html
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>CloudZero | The $0/Month Cloud Architecture Playbook</title>
  <meta name="description" content="Production-ready $0/month cloud infrastructure architecture matrix for SaaS up to 50k MAU. Stop paying AWS/GCP bills.">
  <link rel="stylesheet" href="styles.css">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet">
</head>
<body>
  <header class="navbar">
    <div class="nav-container">
      <div class="logo">
        <span class="logo-icon">&#x269B;</span>
        <span>CloudZero<span class="badge-accent">PLAYBOOK</span></span>
      </div>
      <div class="nav-links">
        <a href="#matrix">Stack Matrix</a>
        <a href="#calculator">Savings Calc</a>
        <button id="upgradeBtn" class="btn btn-primary">Get Production Kit ($12)</button>
      </div>
    </div>
  </header>

  <section class="hero">
    <div class="pill">&#x1F4A5; Cut AWS &amp; Cloud Bills to Exactly $0.00</div>
    <h1>Scale to 50k MAU on <span class="gradient-text">100% Free Cloud Tiers</span></h1>
    <p class="hero-sub">The battle-tested infrastructure blueprint combining Cloudflare, Oracle Always-Free, Supabase, and Resend. Zero monthly bills.</p>
  </section>

  <!-- Interactive Savings Calculator -->
  <section id="calculator" class="calc-section">
    <div class="card calc-card">
      <h2>&#x1F4B8; Cloud Cost Reduction Calculator</h2>
      <p class="card-sub">See how much you save by switching from traditional AWS/GCP to the CloudZero stack.</p>
      
      <div class="calc-grid">
        <div class="slider-group">
          <label for="mauSlider">Monthly Active Users (MAU): <span id="mauVal" class="val-display">15,000</span></label>
          <input type="range" id="mauSlider" min="1000" max="60000" step="1000" value="15000">

          <label for="dbSlider">Database Storage (GB): <span id="dbVal" class="val-display">5 GB</span></label>
          <input type="range" id="dbSlider" min="1" max="50" step="1" value="5">

          <label for="bandwidthSlider">Monthly Outbound Bandwidth (GB): <span id="bwVal" class="val-display">150 GB</span></label>
          <input type="range" id="bandwidthSlider" min="10" max="1000" step="10" value="150">
        </div>

        <div class="result-box">
          <div class="comparison-row">
            <span class="comp-label">Standard AWS/GCP Cost:</span>
            <span id="awsCost" class="comp-val aws-strike">$185.00/mo</span>
          </div>
          <div class="comparison-row highlight-row">
            <span class="comp-label">CloudZero Free Stack:</span>
            <span class="comp-val zero-cost">$0.00/mo</span>
          </div>
          <div class="annual-savings">
            Annual Savings: <strong id="annualSavings">$2,220.00/year</strong>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Architecture Matrix -->
  <section id="matrix" class="matrix-section">
    <div class="section-title">
      <h2>Battle-Tested Free Tier Component Matrix</h2>
      <p>Every tool below has a permanent free tier capable of handling real production workloads.</p>
    </div>

    <div class="category-tabs">
      <button class="tab-btn active" data-cat="all">All Layers</button>
      <button class="tab-btn" data-cat="hosting">Hosting &amp; Edge</button>
      <button class="tab-btn" data-cat="db">Database &amp; Cache</button>
      <button class="tab-btn" data-cat="auth">Auth &amp; Users</button>
      <button class="tab-btn" data-cat="compute">Compute &amp; Containers</button>
    </div>

    <div id="matrixGrid" class="matrix-grid">
      <!-- Populated by app.js -->
    </div>
  </section>

  <!-- Pro Kit Upgrade Section -->
  <section class="pro-section">
    <div class="pro-card">
      <div class="pro-tag">Instant Download</div>
      <h2>CloudZero Production Kit</h2>
      <p class="pro-sub">Stop spending hours configuring infrastructure. Get copy-paste, production-grade templates.</p>
      
      <div class="pro-grid">
        <ul class="pro-features">
          <li>&#x2714; <strong>Docker Compose Suite</strong>: Caddy reverse proxy with auto-HTTPS + Node/Python backends</li>
          <li>&#x2714; <strong>Terraform Modules</strong>: Automated Cloudflare DNS + Pages + Supabase IaC setup</li>
          <li>&#x2714; <strong>Oracle Always-Free Script</strong>: Automated 4 OCPU / 24GB RAM Ampere instance deployer</li>
          <li>&#x2714; <strong>GitHub Actions CI/CD</strong>: Zero-downtime blue/green deployment workflow</li>
          <li>&#x2714; <strong>65-Page PDF Guide</strong>: Hardening, rate-limiting, and zero-bill guardrails</li>
        </ul>
        <div class="buy-box">
          <div class="buy-price">$12 <span class="one-time">/ one-time</span></div>
          <p class="guarantee">&#x1F512; Instant ZIP delivery. 30-day money-back guarantee.</p>
          <button id="buyNowBtn" class="btn btn-full btn-pro">Download Production Kit ($12)</button>
        </div>
      </div>
    </div>
  </section>

  <!-- Checkout Modal -->
  <div id="checkoutModal" class="modal-backdrop">
    <div class="modal-box">
      <div class="modal-header">
        <h3>Get CloudZero Production Kit ($12)</h3>
        <button id="closeModal" class="close-modal">&times;</button>
      </div>
      <div class="modal-body">
        <p>Choose your preferred zero-fee checkout method. Instant digital ZIP download delivered immediately upon payment.</p>
        <div class="checkout-links">
          <a href="https://gumroad.com" target="_blank" class="pay-btn gumroad-btn">&#x1F4B3; Pay with Card / PayPal (Gumroad)</a>
          <a href="https://payhip.com" target="_blank" class="pay-btn payhip-btn">&#x26A1; Pay with Payhip ($12)</a>
        </div>
        <p class="guarantee-note" style="margin-top: 12px; font-size: 0.8rem; color: #10b981; text-align: center;">&#x1F6E1;&#xFE0F; 30-Day No-Hassle Money-Back Guarantee. Instant digital delivery.</p>
      </div>
    </div>
  </div>

  <footer class="footer">
    <p>&copy; 2026 CloudZero Playbook. Maintained by The Engine. 100% Free Tier Compliant.</p>
  </footer>

  <script src="app.js"></script>
</body>
</html>
"""
    with open(public_dir / "index.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    # 2. styles.css
    css_content = """/* CloudZero Dark Terminal Stylesheet */
:root {
  --bg: #090d16;
  --bg-card: #131b2e;
  --border: #1e293b;
  --text: #f8fafc;
  --text-muted: #94a3b8;
  --cyan: #38bdf8;
  --accent: #10b981;
  --neon-blue: #6366f1;
}

* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: 'Space Grotesk', -apple-system, sans-serif;
  background-color: var(--bg);
  color: var(--text);
  line-height: 1.6;
}

/* Navbar */
.navbar {
  border-bottom: 1px solid var(--border);
  background: rgba(9, 13, 22, 0.85);
  backdrop-filter: blur(8px);
  position: sticky;
  top: 0;
  z-index: 100;
}
.nav-container {
  max-width: 1100px;
  margin: 0 auto;
  padding: 16px 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.logo { font-size: 1.3rem; font-weight: 700; display: flex; align-items: center; gap: 8px; }
.logo-icon { color: var(--cyan); }
.badge-accent {
  background: rgba(56, 189, 248, 0.15);
  color: var(--cyan);
  font-size: 0.65rem;
  padding: 2px 8px;
  border-radius: 4px;
  margin-left: 8px;
  font-family: 'JetBrains Mono', monospace;
}
.nav-links { display: flex; align-items: center; gap: 20px; }
.nav-links a { color: var(--text-muted); text-decoration: none; font-size: 0.95rem; }
.nav-links a:hover { color: var(--text); }

/* Buttons */
.btn {
  padding: 8px 16px;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  border: none;
  transition: all 0.2s ease;
  font-size: 0.9rem;
}
.btn-primary { background: var(--cyan); color: #000; }
.btn-primary:hover { filter: brightness(1.15); }
.btn-pro {
  background: linear-gradient(135deg, #38bdf8 0%, #6366f1 100%);
  color: #fff;
  box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4);
}
.btn-pro:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(99, 102, 241, 0.6); }
.btn-full { width: 100%; padding: 12px; margin-top: 14px; }

/* Hero */
.hero { text-align: center; padding: 60px 24px 30px; max-width: 800px; margin: 0 auto; }
.pill {
  display: inline-block;
  background: rgba(16, 185, 129, 0.1);
  color: var(--accent);
  border: 1px solid rgba(16, 185, 129, 0.3);
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.8rem;
  padding: 4px 12px;
  border-radius: 20px;
  margin-bottom: 20px;
}
.hero h1 { font-size: 2.8rem; font-weight: 700; line-height: 1.15; margin-bottom: 16px; }
.gradient-text {
  background: linear-gradient(135deg, #38bdf8 0%, #a855f7 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.hero-sub { color: var(--text-muted); font-size: 1.15rem; }

/* Calculator */
.calc-section { max-width: 900px; margin: 40px auto; padding: 0 24px; }
.card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 32px;
}
.card h2 { font-size: 1.4rem; margin-bottom: 6px; }
.card-sub { color: var(--text-muted); font-size: 0.9rem; margin-bottom: 24px; }
.calc-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 32px; align-items: center; }
@media (max-width: 768px) { .calc-grid { grid-template-columns: 1fr; } }
.slider-group { display: flex; flex-direction: column; gap: 14px; }
.slider-group label { font-size: 0.9rem; display: flex; justify-content: space-between; font-weight: 500; }
.val-display { font-family: 'JetBrains Mono', monospace; color: var(--cyan); }
input[type=range] { width: 100%; accent-color: var(--cyan); }

.result-box {
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 24px;
}
.comparison-row { display: flex; justify-content: space-between; margin-bottom: 12px; font-size: 0.95rem; }
.aws-strike { color: #f87171; text-decoration: line-through; font-family: 'JetBrains Mono', monospace; }
.highlight-row { font-size: 1.1rem; font-weight: 700; border-top: 1px solid var(--border); padding-top: 12px; }
.zero-cost { color: var(--accent); font-family: 'JetBrains Mono', monospace; font-size: 1.4rem; }
.annual-savings {
  margin-top: 16px;
  background: rgba(16, 185, 129, 0.1);
  border-left: 3px solid var(--accent);
  padding: 10px;
  font-size: 0.9rem;
}
.annual-savings strong { color: var(--accent); font-family: 'JetBrains Mono', monospace; }

/* Matrix */
.matrix-section { max-width: 1100px; margin: 60px auto; padding: 0 24px; }
.section-title { text-align: center; margin-bottom: 30px; }
.section-title h2 { font-size: 2rem; margin-bottom: 8px; }
.section-title p { color: var(--text-muted); }
.category-tabs { display: flex; justify-content: center; gap: 8px; margin-bottom: 24px; flex-wrap: wrap; }
.tab-btn {
  background: var(--bg-card);
  color: var(--text-muted);
  border: 1px solid var(--border);
  padding: 6px 14px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.85rem;
}
.tab-btn.active, .tab-btn:hover { background: var(--cyan); color: #000; border-color: var(--cyan); font-weight: 600; }

.matrix-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 16px; }
.service-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}
.service-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px; }
.service-name { font-weight: 700; font-size: 1.1rem; }
.service-tier {
  background: rgba(16, 185, 129, 0.1);
  color: var(--accent);
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.75rem;
  padding: 2px 6px;
  border-radius: 4px;
}
.service-desc { color: var(--text-muted); font-size: 0.85rem; margin-bottom: 12px; }
.service-limits {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.8rem;
  background: rgba(0, 0, 0, 0.25);
  padding: 8px;
  border-radius: 4px;
  color: #cbd5e1;
}

/* Pro Section */
.pro-section { max-width: 900px; margin: 80px auto; padding: 0 24px; }
.pro-card {
  background: linear-gradient(180deg, #131b2e 0%, #0d1322 100%);
  border: 2px solid #6366f1;
  border-radius: 12px;
  padding: 36px;
  position: relative;
  box-shadow: 0 20px 40px rgba(99, 102, 241, 0.15);
}
.pro-tag {
  position: absolute;
  top: -12px;
  left: 36px;
  background: #6366f1;
  color: #fff;
  font-size: 0.75rem;
  font-weight: 700;
  padding: 2px 10px;
  border-radius: 12px;
  font-family: 'JetBrains Mono', monospace;
}
.pro-card h2 { font-size: 1.8rem; margin-bottom: 8px; }
.pro-sub { color: var(--text-muted); margin-bottom: 24px; }
.pro-grid { display: grid; grid-template-columns: 3fr 2fr; gap: 32px; align-items: center; }
@media (max-width: 768px) { .pro-grid { grid-template-columns: 1fr; } }
.pro-features { list-style: none; display: flex; flex-direction: column; gap: 10px; font-size: 0.95rem; }
.buy-box {
  background: rgba(0, 0, 0, 0.35);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 24px;
  text-align: center;
}
.buy-price { font-size: 2.5rem; font-weight: 700; font-family: 'JetBrains Mono', monospace; }
.one-time { font-size: 0.9rem; color: var(--text-muted); font-family: sans-serif; font-weight: 400; }
.guarantee { font-size: 0.8rem; color: var(--text-muted); margin-top: 8px; }

/* Modal */
.modal-backdrop {
  display: none;
  position: fixed;
  top: 0; left: 0; width: 100%; height: 100%;
  background: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(4px);
  z-index: 1000;
  justify-content: center;
  align-items: center;
}
.modal-backdrop.open { display: flex; }
.modal-box {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 10px;
  max-width: 440px;
  width: 90%;
  padding: 24px;
}
.modal-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }
.close-modal { background: none; border: none; font-size: 1.4rem; color: var(--text-muted); cursor: pointer; }
.checkout-links { display: flex; flex-direction: column; gap: 10px; margin-top: 20px; }
.pay-btn {
  padding: 12px;
  border-radius: 6px;
  text-align: center;
  text-decoration: none;
  font-weight: 700;
  font-size: 0.9rem;
}
.gumroad-btn { background: #ff90e8; color: #000; }
.payhip-btn { background: #38bdf8; color: #000; }

.footer { text-align: center; color: var(--text-muted); font-size: 0.85rem; padding: 40px 0; border-top: 1px solid var(--border); margin-top: 60px; }
"""
    with open(public_dir / "styles.css", "w", encoding="utf-8") as f:
        f.write(css_content)

    # 3. app.js
    js_content = """// CloudZero Interactive Engine
(function() {
  const mauSlider = document.getElementById('mauSlider');
  const dbSlider = document.getElementById('dbSlider');
  const bwSlider = document.getElementById('bandwidthSlider');
  const mauVal = document.getElementById('mauVal');
  const dbVal = document.getElementById('dbVal');
  const bwVal = document.getElementById('bwVal');
  const awsCost = document.getElementById('awsCost');
  const annualSavings = document.getElementById('annualSavings');
  const matrixGrid = document.getElementById('matrixGrid');
  const tabBtns = document.querySelectorAll('.tab-btn');
  const upgradeBtn = document.getElementById('upgradeBtn');
  const buyNowBtn = document.getElementById('buyNowBtn');
  const checkoutModal = document.getElementById('checkoutModal');
  const closeModal = document.getElementById('closeModal');

  const services = [
    { name: "Cloudflare Pages", cat: "hosting", tier: "$0 Forever", desc: "Unlimited static site hosting & edge redirects.", limits: "Unlimited Bandwidth, 100 Custom Domains" },
    { name: "Oracle Always-Free", cat: "compute", tier: "$0 Forever", desc: "Full Ampere ARM virtual machines.", limits: "4 OCPUs, 24 GB RAM, 200 GB NVMe Storage" },
    { name: "Supabase Database", cat: "db", tier: "$0 Forever", desc: "Hosted PostgreSQL with real-time API.", limits: "500 MB DB, 50k Monthly Active Users Auth" },
    { name: "Cloudflare R2", cat: "hosting", tier: "$0 Forever", desc: "S3-compatible object storage with ZERO egress fees.", limits: "10 GB Storage / Month, Zero Egress Charges" },
    { name: "Upstash Redis", cat: "db", tier: "$0 Forever", desc: "Serverless Redis for caching & rate-limiting.", limits: "10,000 Commands / Day, Rest API" },
    { name: "Resend", cat: "compute", tier: "$0 Forever", desc: "Developer-first transactional email API.", limits: "3,000 Emails / Month, 100 Emails / Day" },
    { name: "Neon Serverless Postgres", cat: "db", tier: "$0 Forever", desc: "Branchable serverless PostgreSQL with auto-suspend.", limits: "0.5 GB Storage, Instant DB Branching" },
    { name: "Clerk Auth", cat: "auth", tier: "$0 Forever", desc: "Drop-in authentication & user management.", limits: "10,000 Monthly Active Users Free" },
    { name: "GitHub Actions", cat: "compute", tier: "$0 Forever", desc: "Automated CI/CD pipelines and cron runners.", limits: "2,000 Build Minutes / Month Free" }
  ];

  function renderMatrix(filterCat = 'all') {
    matrixGrid.innerHTML = '';
    const filtered = filterCat === 'all' ? services : services.filter(s => s.cat === filterCat);
    filtered.forEach(s => {
      const card = document.createElement('div');
      card.className = 'service-card';
      card.innerHTML = `
        <div>
          <div class="service-header">
            <span class="service-name">${s.name}</span>
            <span class="service-tier">${s.tier}</span>
          </div>
          <p class="service-desc">${s.desc}</p>
        </div>
        <div class="service-limits">${s.limits}</div>
      `;
      matrixGrid.appendChild(card);
    });
  }

  function updateSavings() {
    const mau = parseInt(mauSlider.value, 10);
    const db = parseInt(dbSlider.value, 10);
    const bw = parseInt(bwSlider.value, 10);

    mauVal.textContent = mau.toLocaleString();
    dbVal.textContent = db + ' GB';
    bwVal.textContent = bw + ' GB';

    // Estimate AWS bill
    const awsMonthly = Math.round(35 + (mau * 0.005) + (db * 1.5) + (bw * 0.09));
    const annual = awsMonthly * 12;

    awsCost.textContent = '$' + awsMonthly.toLocaleString() + '.00/mo';
    annualSavings.textContent = '$' + annual.toLocaleString() + '.00/year';
  }

  mauSlider.addEventListener('input', updateSavings);
  dbSlider.addEventListener('input', updateSavings);
  bwSlider.addEventListener('input', updateSavings);

  tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      tabBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      renderMatrix(btn.getAttribute('data-cat'));
    });
  });

  function openCheckout() { checkoutModal.classList.add('open'); }
  function closeCheckout() { checkoutModal.classList.remove('open'); }

  upgradeBtn.addEventListener('click', openCheckout);
  buyNowBtn.addEventListener('click', openCheckout);
  closeModal.addEventListener('click', closeCheckout);
  window.addEventListener('click', (e) => { if (e.target === checkoutModal) closeCheckout(); });

  updateSavings();
  renderMatrix();
})();
"""
    with open(public_dir / "app.js", "w", encoding="utf-8") as f:
        f.write(js_content)

    # 4. monetization/pricing.json
    pricing = {
        "currency": "USD",
        "tiers": [
            {
                "tier_id": "free_playbook",
                "name": "Community Playbook",
                "price": 0.00,
                "upfront_cost": 0.00,
                "features": ["Interactive Architecture Matrix", "Savings Calculator", "Free Tier Limit References"]
            },
            {
                "tier_id": "production_kit",
                "name": "CloudZero Production Kit",
                "price": 12.00,
                "upfront_cost": 0.00,
                "billing": "one-time",
                "features": [
                    "Production Docker Compose + Caddy Reverse Proxy",
                    "Terraform IaC Modules for Cloudflare & Supabase",
                    "Oracle Always-Free Automated Deployer",
                    "GitHub Actions CI/CD Blueprint",
                    "65-Page Hardening & Guardrails PDF Cheatsheet"
                ],
                "checkout_channels": {
                    "gumroad": "https://gumroad.com",
                    "payhip": "https://payhip.com"
                }
            }
        ]
    }
    with open(mon_dir / "pricing.json", "w", encoding="utf-8") as f:
        json.dump(pricing, f, indent=2)

    # 5. server.py
    server_code = """# CloudZero Zero-Dependency Micro-Server
import http.server
import socketserver
import json
import os
import sys
from pathlib import Path

PORT = int(os.environ.get("PORT", 8081))
PUBLIC_DIR = Path(__file__).resolve().parent.parent / "public"

class PlaybookHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(PUBLIC_DIR), **kwargs)

    def do_GET(self):
        if self.path == "/api/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "HEALTHY", "node": "dev_cheatsheet_vault", "cost": "$0.00"}).encode())
            return
        super().do_GET()

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else PORT
    with socketserver.TCPServer(("", port), PlaybookHandler) as httpd:
        print(f"CloudZero server live at http://localhost:{port}")
        httpd.serve_forever()
"""
    with open(src_dir / "server.py", "w", encoding="utf-8") as f:
        f.write(server_code)
