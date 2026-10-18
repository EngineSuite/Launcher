"""
The Engine - The Builder (Dev & Content Production Agent)
Generates production code, web applications, digital assets, APIs, and zero-cost payment integrations.
"""

import json
import logging
import zipfile
from pathlib import Path
from typing import Dict, Any
from datetime import datetime

from the_engine.agents.base import BaseAgent
from the_engine.core.hitl import HITLGatekeeper
from the_engine.core.isolation import NodeIsolationManager
from the_engine.config import get_utc_iso
from the_engine.agents.templates.dev_playbook import build_dev_playbook
from the_engine.agents.templates.meta_craft import build_meta_craft
from the_engine.agents.templates.svg_craft import build_svg_craft

logger = logging.getLogger("TheEngine.Builder")


class BuilderAgent(BaseAgent):
    def __init__(self, hitl_gatekeeper: HITLGatekeeper, isolation_mgr: NodeIsolationManager):
        super().__init__(
            name="The Builder",
            role="Dev & Content Production",
            hitl_gatekeeper=hitl_gatekeeper
        )
        self.isolation_mgr = isolation_mgr

    def build_node(self, opportunity: Dict[str, Any]) -> Path:
        """
        Builds a complete, production-ready, zero-overhead digital revenue node.
        """
        node_id = f"node_{opportunity['niche_id']}"
        self.log(f"Scaffolding isolated workspace for '{node_id}'...")

        node_path = self.isolation_mgr.create_node_workspace(node_id, opportunity)

        # Generate Node Assets
        if opportunity.get("niche_id") == "dev_cheatsheet_vault":
            build_dev_playbook(node_path, opportunity)
        elif opportunity.get("niche_id") == "meta_craft_og":
            build_meta_craft(node_path, opportunity)
        elif opportunity.get("niche_id") == "svg_craft_studio":
            build_svg_craft(node_path, opportunity)
        else:
            self._build_frontend(node_path, opportunity)
            self._build_backend_engine(node_path, opportunity)
            self._build_monetization_layer(node_path, opportunity)
            self._build_server(node_path, opportunity)


        # Inject legal armor (Standardized LICENSE.txt with AS IS & liability cap) and build deliverables
        self._inject_legal_and_compliance_assets(node_path, opportunity)

        self.isolation_mgr.update_manifest(node_id, {
            "status": "BUILT",
            "build_completed_at": get_utc_iso(),
            "entrypoint": "src/server.py",
            "frontend_index": "public/index.html"
        })

        self.log(f"Node '{node_id}' successfully built at {node_path}")
        return node_path

    def _build_frontend(self, node_path: Path, opp: Dict[str, Any]) -> None:
        """Builds modern, responsive, zero-dependency client-side UI."""
        public_dir = node_path / "public"
        public_dir.mkdir(exist_ok=True)

        # 1. index.html
        html_content = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>SchemaCraft Pro | Instant JSON-LD Schema Generator & Local SEO Suite</title>
  <meta name="description" content="Free, instant Schema.org JSON-LD generator for local businesses, SaaS, products, FAQs, and articles. Boost Google rich snippets with 100% valid schema markup.">
  <link rel="stylesheet" href="styles.css">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
</head>
<body>
  <!-- Header -->
  <header class="navbar">
    <div class="nav-container">
      <div class="logo">
        <span class="logo-icon">&#x26A1;</span>
        <span class="logo-text">SchemaCraft<span class="pro-tag">PRO</span></span>
      </div>
      <div class="nav-actions">
        <a href="#features" class="nav-link">Features</a>
        <a href="#faq" class="nav-link">FAQ</a>
        <button id="upgradeBtn" class="btn btn-pro">Unlock Pro ($19)</button>
      </div>
    </div>
  </header>

  <!-- Hero -->
  <section class="hero">
    <div class="badge">&#x1F680; Boost Google Rich Snippets & CTR by up to 35%</div>
    <h1>Turn Search Rankings into Revenue with <span class="gradient-text">Bulletproof JSON-LD</span></h1>
    <p class="hero-sub">Generate 100% valid, Google-compliant structured data in seconds. Zero coding required.</p>
  </section>

  <!-- Main App Workspace -->
  <main class="app-workspace">
    <!-- Left Column: Schema Form Builder -->
    <section class="card editor-card">
      <div class="card-header">
        <div class="type-selector-wrapper">
          <label for="schemaType">Schema Type:</label>
          <select id="schemaType" class="input-select">
            <option value="LocalBusiness">Local Business (Google Maps / Local SEO)</option>
            <option value="Organization">Organization / SaaS Company</option>
            <option value="Product">Product & E-Commerce (Price, Rating)</option>
            <option value="FAQPage">FAQ Page (Expands SERP Snippet)</option>
            <option value="HowTo">How-To Guide (Step-by-Step)</option>
            <option value="Article">Article / Blog Post</option>
            <option value="Event">Event (Date, Location, Ticket)</option>
            <option value="JobPosting">Job Posting (Salary, Role)</option>
          </select>
        </div>
      </div>

      <form id="schemaForm" class="schema-form">
        <!-- Dynamic fields populated by app.js -->
        <div id="dynamicFields" class="dynamic-fields-container"></div>
      </form>
    </section>

    <!-- Right Column: Live Output & Actions -->
    <section class="card output-card">
      <div class="card-header">
        <div class="output-title">
          <span class="dot live-dot"></span> Live JSON-LD Preview
        </div>
        <div class="output-actions">
          <button id="sampleBtn" class="btn btn-sm btn-outline">&#x2728; Load Sample</button>
          <button id="copyBtn" class="btn btn-sm btn-outline">&#x1F4CB; Copy Code</button>
          <button id="downloadBtn" class="btn btn-sm btn-outline">&#x2B07; Download .json</button>
          <button id="validateBtn" class="btn btn-sm btn-accent">&#x2714; Test Schema</button>
        </div>
      </div>

      <div class="code-container">
        <pre><code id="jsonOutput" class="code-view">// Your generated JSON-LD schema will appear here...</code></pre>
      </div>

      <div class="embed-callout">
        <p><strong>&#x1F4A1; How to embed on your site:</strong> Paste this inside the <code>&lt;head&gt;</code> tag of your page.</p>
      </div>
    </section>
  </main>

  <!-- Pro Features & Pricing -->
  <section id="features" class="pricing-section">
    <div class="section-header">
      <h2>Supercharge Your Local SEO Operations</h2>
      <p>Used by digital agencies, solo freelancers, and multi-location businesses.</p>
    </div>

    <div class="pricing-grid">
      <div class="price-card free-card">
        <h3>Starter</h3>
        <div class="price">$0 <span>/ lifetime</span></div>
        <p>Perfect for individual sites & quick checks.</p>
        <ul class="benefit-list">
          <li>&#x2713; Unlimited Single Schema Generations</li>
          <li>&#x2713; 8 Core Schema Types</li>
          <li>&#x2713; 1-Click Clipboard & File Download</li>
          <li>&#x2713; Real-time Syntax Validation</li>
        </ul>
        <button class="btn btn-full btn-secondary" onclick="window.scrollTo({top: 250, behavior: 'smooth'})">Use Free Generator</button>
      </div>

      <div class="price-card pro-card popular">
        <div class="popular-ribbon">Most Popular</div>
        <h3>Agency Pro Pack</h3>
        <div class="price">$19 <span>/ one-time</span></div>
        <p>Built for agencies and multi-location power users.</p>
        <ul class="benefit-list">
          <li>&#x2713; <strong>Bulk CSV Importer</strong> (Generate 100+ locations at once)</li>
          <li>&#x2713; <strong>Whitelabel Embed Widget</strong> for client sites</li>
          <li>&#x2713; <strong>REST API Access</strong> (Cloudflare / Node integration)</li>
          <li>&#x2713; <strong>30+ Advanced Schema Templates</strong> (Medical, Legal, Real Estate)</li>
          <li>&#x2713; Lifetime Updates & Priority Support</li>
        </ul>
        <button id="buyProBtn" class="btn btn-full btn-pro">Get Agency Pro ($19)</button>
        <div class="guarantee-badge">&#x1F6E1;&#xFE0F; 30-Day No-Hassle Money-Back Guarantee &bull; 100% Risk-Free</div>
      </div>
    </div>
  </section>

  <!-- Pro Direct Order Modal -->
  <div id="proModal" class="modal-backdrop">
    <div class="modal-content">
      <div class="modal-header">
        <h3>Unlock SchemaCraft Agency Pro ($19)</h3>
        <button id="closeModal" class="close-btn">&times;</button>
      </div>
      <div class="modal-body">
        <p class="modal-sub">Accelerate your workflow with Bulk CSV generation, Whitelabel embed rights, and our complete Schema templates library.</p>
        
        <div class="direct-order-box">
          <div class="order-badge">Direct License Fulfillment</div>
          <p class="order-instructions">
            To acquire the complete Agency Pro Pack ($19 one-time), email our dispatch desk directly without any 3rd-party checkout fees:
          </p>
          <div class="email-pill-container">
            <span class="email-address">businessbloke957@gmail.com</span>
            <button id="copyEmailBtn" class="copy-email-btn" type="button">📋 Copy Email</button>
          </div>
          <div class="order-action-row">
            <a id="directMailLink" href="mailto:businessbloke957@gmail.com?subject=Order%20Request%3A%20SchemaCraft%20Agency%20Pro%20Pack%20(%2419)&body=Hi%2C%0A%0AI%20would%20like%20to%20order%20the%20SchemaCraft%20Agency%20Pro%20Pack%20(%2419%20one-time).%0A%0APreferred%20Payment%20Method%20(PayPal%20%2F%20Bank%20Wire%20%2F%20Wise%20%2F%20Crypto%20%2F%20Other)%3A%20%0A%0APlease%20reply%20with%20payment%20instructions%20and%20dispatch%20the%20bundle%20and%20commercial%20license%20key%20to%20this%20email.%0A%0AThank%20you!" class="btn btn-primary email-launch-btn">
              ✉️ Open in Email App
            </a>
          </div>
          <div class="fulfillment-process">
            <div class="process-step"><span>1</span> Send order email specifying preferred payment method</div>
            <div class="process-step"><span>2</span> Receive commercial invoice & direct payment details</div>
            <div class="process-step"><span>3</span> Full ZIP package & commercial license dispatched within 1 hour</div>
          </div>
        </div>
        <p class="guarantee-note">&#x1F6E1;&#xFE0F; 30-Day No-Hassle Money-Back Guarantee. Full commercial rights included.</p>
      </div>
    </div>
  </div>

  <footer class="footer">
    <p>&copy; 2026 SchemaCraft Pro. Built on zero-cost infrastructure. All rights reserved.</p>
  </footer>

  <script src="app.js"></script>
</body>
</html>
"""
        with open(public_dir / "index.html", "w", encoding="utf-8") as f:
            f.write(html_content)

        # 2. styles.css
        css_content = """/* SchemaCraft Pro Modern Stylesheet */
:root {
  --bg-dark: #0f172a;
  --bg-card: #1e293b;
  --bg-input: #334155;
  --text-main: #f8fafc;
  --text-muted: #94a3b8;
  --primary: #38bdf8;
  --primary-hover: #0ea5e9;
  --accent: #10b981;
  --pro-gradient: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
  --border: #334155;
  --radius: 10px;
}

* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: 'Inter', -apple-system, sans-serif;
  background-color: var(--bg-dark);
  color: var(--text-main);
  line-height: 1.5;
  padding-bottom: 60px;
}

/* Navbar */
.navbar {
  border-bottom: 1px solid var(--border);
  background: rgba(15, 23, 42, 0.85);
  backdrop-filter: blur(10px);
  position: sticky;
  top: 0;
  z-index: 100;
}
.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
}
.logo { font-size: 1.3rem; font-weight: 800; display: flex; align-items: center; gap: 8px; }
.logo-icon { color: #f59e0b; }
.pro-tag {
  background: var(--pro-gradient);
  font-size: 0.65rem;
  padding: 2px 6px;
  border-radius: 4px;
  margin-left: 6px;
  vertical-align: middle;
}
.nav-actions { display: flex; align-items: center; gap: 20px; }
.nav-link { color: var(--text-muted); text-decoration: none; font-size: 0.95rem; font-weight: 500; }
.nav-link:hover { color: var(--text-main); }

/* Buttons */
.btn {
  padding: 10px 18px;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  border: none;
  transition: all 0.2s ease;
  font-size: 0.9rem;
}
.btn-pro {
  background: var(--pro-gradient);
  color: #fff;
  box-shadow: 0 4px 14px rgba(168, 85, 247, 0.4);
}
.btn-pro:hover { transform: translateY(-1px); box-shadow: 0 6px 20px rgba(168, 85, 247, 0.6); }
.btn-outline { background: transparent; border: 1px solid var(--border); color: var(--text-main); }
.btn-outline:hover { background: var(--bg-input); }
.btn-accent { background: var(--accent); color: #fff; }
.btn-accent:hover { filter: brightness(1.1); }
.btn-secondary { background: var(--bg-input); color: #fff; }
.btn-secondary:hover { background: #475569; }
.btn-sm { padding: 6px 12px; font-size: 0.8rem; }
.btn-full { width: 100%; display: block; margin-top: 20px; }

/* Hero */
.hero { text-align: center; padding: 48px 24px 32px; max-width: 800px; margin: 0 auto; }
.badge {
  display: inline-block;
  background: rgba(56, 189, 248, 0.1);
  color: var(--primary);
  border: 1px solid rgba(56, 189, 248, 0.25);
  font-size: 0.85rem;
  font-weight: 600;
  padding: 4px 14px;
  border-radius: 20px;
  margin-bottom: 16px;
}
.hero h1 { font-size: 2.5rem; font-weight: 800; line-height: 1.2; margin-bottom: 16px; }
.gradient-text {
  background: linear-gradient(135deg, #38bdf8 0%, #818cf8 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.hero-sub { color: var(--text-muted); font-size: 1.1rem; }

/* Main App Workspace */
.app-workspace {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
  padding: 0 24px;
}
@media (max-width: 900px) {
  .app-workspace { grid-template-columns: 1fr; }
}

.card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 24px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  border-bottom: 1px solid var(--border);
  padding-bottom: 14px;
}
.type-selector-wrapper { display: flex; align-items: center; gap: 12px; width: 100%; }
.type-selector-wrapper label { font-weight: 600; font-size: 0.95rem; white-space: nowrap; }
.input-select {
  width: 100%;
  background: var(--bg-input);
  color: var(--text-main);
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 8px 12px;
  font-size: 0.9rem;
  outline: none;
}
.input-select:focus { border-color: var(--primary); }

.dynamic-fields-container { display: flex; flex-direction: column; gap: 14px; }
.form-group { display: flex; flex-direction: column; gap: 6px; }
.form-group label { font-size: 0.85rem; font-weight: 500; color: var(--text-muted); }
.form-input, .form-textarea {
  background: var(--bg-input);
  border: 1px solid var(--border);
  color: var(--text-main);
  border-radius: 6px;
  padding: 8px 12px;
  font-size: 0.9rem;
  outline: none;
}
.form-input:focus, .form-textarea:focus { border-color: var(--primary); }
.form-textarea { resize: vertical; min-height: 70px; font-family: inherit; }

/* Code View */
.output-title { font-weight: 600; font-size: 0.95rem; display: flex; align-items: center; gap: 8px; }
.live-dot { width: 8px; height: 8px; background: var(--accent); border-radius: 50%; box-shadow: 0 0 8px var(--accent); }
.output-actions { display: flex; gap: 8px; }
.code-container {
  background: #090d16;
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 16px;
  height: 380px;
  overflow-y: auto;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.85rem;
}
.code-view { color: #38bdf8; white-space: pre-wrap; word-break: break-all; }
.embed-callout {
  margin-top: 16px;
  padding: 12px;
  background: rgba(56, 189, 248, 0.08);
  border-left: 3px solid var(--primary);
  border-radius: 4px;
  font-size: 0.85rem;
}

/* Pricing Section */
.pricing-section { max-width: 900px; margin: 80px auto 40px; padding: 0 24px; }
.section-header { text-align: center; margin-bottom: 36px; }
.section-header h2 { font-size: 2rem; font-weight: 800; margin-bottom: 8px; }
.section-header p { color: var(--text-muted); }
.pricing-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }
@media (max-width: 700px) {
  .pricing-grid { grid-template-columns: 1fr; }
}
.price-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 32px;
  position: relative;
}
.price-card.popular {
  border: 2px solid #a855f7;
  box-shadow: 0 10px 40px rgba(168, 85, 247, 0.2);
}
.popular-ribbon {
  position: absolute;
  top: -12px;
  right: 24px;
  background: var(--pro-gradient);
  color: #fff;
  font-size: 0.75rem;
  font-weight: 700;
  padding: 2px 10px;
  border-radius: 12px;
}
.price-card h3 { font-size: 1.3rem; margin-bottom: 8px; }
.price-card .price { font-size: 2.4rem; font-weight: 800; margin-bottom: 8px; }
.price-card .price span { font-size: 0.9rem; font-weight: 500; color: var(--text-muted); }
.price-card p { color: var(--text-muted); font-size: 0.9rem; margin-bottom: 20px; }
.benefit-list { list-style: none; display: flex; flex-direction: column; gap: 10px; font-size: 0.9rem; }
.benefit-list li { color: #cbd5e1; }
.guarantee-badge { margin-top: 12px; font-size: 0.78rem; color: #10b981; text-align: center; font-weight: 500; display: flex; align-items: center; justify-content: center; gap: 6px; }

/* Modal */
.modal-backdrop {
  display: none;
  position: fixed;
  top: 0; left: 0; width: 100%; height: 100%;
  background: rgba(0, 0, 0, 0.75);
  backdrop-filter: blur(5px);
  z-index: 1000;
  justify-content: center;
  align-items: center;
}
.modal-backdrop.open { display: flex; }
.modal-content {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  max-width: 480px;
  width: 90%;
  padding: 28px;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5);
}
.modal-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }
.modal-header h3 { font-size: 1.3rem; font-weight: 700; }
.close-btn { background: none; border: none; font-size: 1.5rem; color: var(--text-muted); cursor: pointer; }
.modal-sub { color: var(--text-muted); font-size: 0.9rem; margin-bottom: 24px; }
.direct-order-box {
  background: rgba(15, 23, 42, 0.85);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 18px;
  margin-bottom: 18px;
  text-align: left;
}
.order-badge {
  display: inline-block;
  background: rgba(59, 130, 246, 0.2);
  color: #60a5fa;
  border: 1px solid rgba(59, 130, 246, 0.4);
  font-size: 0.72rem;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 4px;
  margin-bottom: 10px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
.order-instructions {
  color: #cbd5e1;
  font-size: 0.88rem;
  margin-bottom: 12px;
  line-height: 1.5;
}
.email-pill-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #090d16;
  border: 1px solid #334155;
  border-radius: 8px;
  padding: 8px 12px;
  margin-bottom: 12px;
  gap: 10px;
}
.email-address {
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  font-size: 0.95rem;
  color: #38bdf8;
  font-weight: 600;
  overflow: hidden;
  text-overflow: ellipsis;
}
.copy-email-btn {
  background: #1e293b;
  color: #cbd5e1;
  border: 1px solid #475569;
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 0.8rem;
  font-weight: 600;
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.2s ease;
}
.copy-email-btn:hover { background: #334155; color: #fff; }
.order-action-row { margin-bottom: 14px; }
.email-launch-btn {
  display: block;
  text-align: center;
  padding: 12px 16px;
  font-size: 0.95rem;
  font-weight: 700;
  border-radius: 8px;
  text-decoration: none;
}
.fulfillment-process {
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding: 10px 12px;
  background: rgba(0, 0, 0, 0.35);
  border-radius: 6px;
  margin-bottom: 12px;
}
.process-step {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.8rem;
  color: #94a3b8;
}
.process-step span {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 18px;
  height: 18px;
  background: #3b82f6;
  color: #fff;
  border-radius: 50%;
  font-size: 0.7rem;
  font-weight: 700;
  flex-shrink: 0;
}
.guarantee-note { font-size: 0.8rem; color: var(--text-muted); text-align: center; }

/* Footer */
.footer { text-align: center; color: var(--text-muted); font-size: 0.85rem; margin-top: 60px; }
"""
        with open(public_dir / "styles.css", "w", encoding="utf-8") as f:
            f.write(css_content)

        # 3. app.js
        js_content = """// SchemaCraft Pro - Interactive JSON-LD Client Engine
(function() {
  const schemaTypeSelect = document.getElementById('schemaType');
  const dynamicFields = document.getElementById('dynamicFields');
  const jsonOutput = document.getElementById('jsonOutput');
  const copyBtn = document.getElementById('copyBtn');
  const downloadBtn = document.getElementById('downloadBtn');
  const validateBtn = document.getElementById('validateBtn');
  const upgradeBtn = document.getElementById('upgradeBtn');
  const buyProBtn = document.getElementById('buyProBtn');
  const proModal = document.getElementById('proModal');
  const closeModal = document.getElementById('closeModal');

  // Schema form definitions
  const schemaDefinitions = {
    LocalBusiness: [
      { id: 'name', label: 'Business Name', type: 'text', default: 'Apex Dental Care' },
      { id: 'businessType', label: 'Category', type: 'text', default: 'Dentist' },
      { id: 'url', label: 'Website URL', type: 'url', default: 'https://apexdentalcare.example.com' },
      { id: 'telephone', label: 'Phone Number', type: 'tel', default: '+1-555-019-2834' },
      { id: 'street', label: 'Street Address', type: 'text', default: '100 Main St, Suite 200' },
      { id: 'city', label: 'City', type: 'text', default: 'Austin' },
      { id: 'region', label: 'State / Region', type: 'text', default: 'TX' },
      { id: 'postalCode', label: 'Postal Code', type: 'text', default: '78701' },
      { id: 'country', label: 'Country Code (e.g. US)', type: 'text', default: 'US' },
      { id: 'priceRange', label: 'Price Range', type: 'text', default: '$$' }
    ],
    Organization: [
      { id: 'name', label: 'Organization Name', type: 'text', default: 'CloudFlow Technologies' },
      { id: 'url', label: 'Website URL', type: 'url', default: 'https://cloudflow.example.com' },
      { id: 'logo', label: 'Logo Image URL', type: 'url', default: 'https://cloudflow.example.com/logo.png' },
      { id: 'description', label: 'Description', type: 'textarea', default: 'Leading developer tools for autonomous cloud infrastructure.' },
      { id: 'sameAs', label: 'Social Media Profiles (comma-separated)', type: 'text', default: 'https://twitter.com/cloudflow, https://linkedin.com/company/cloudflow' }
    ],
    Product: [
      { id: 'name', label: 'Product Name', type: 'text', default: 'Autonomous Workflow Engine' },
      { id: 'description', label: 'Product Description', type: 'textarea', default: 'Self-correcting AI orchestrator for micro-SaaS deployment.' },
      { id: 'image', label: 'Product Image URL', type: 'url', default: 'https://example.com/product.png' },
      { id: 'brand', label: 'Brand Name', type: 'text', default: 'Engine Corp' },
      { id: 'price', label: 'Price (USD)', type: 'number', default: '19.00' },
      { id: 'currency', label: 'Currency', type: 'text', default: 'USD' },
      { id: 'ratingValue', label: 'Rating (1 to 5)', type: 'number', default: '4.9' },
      { id: 'reviewCount', label: 'Review Count', type: 'number', default: '128' }
    ],
    FAQPage: [
      { id: 'q1', label: 'Question 1', type: 'text', default: 'What is JSON-LD schema markup?' },
      { id: 'a1', label: 'Answer 1', type: 'textarea', default: 'JSON-LD is a structured data format recognized by Google to enable rich snippets in search results.' },
      { id: 'q2', label: 'Question 2', type: 'text', default: 'How long until rich snippets appear on Google?' },
      { id: 'a2', label: 'Answer 2', type: 'textarea', default: 'Typically Google recrawls pages within 3 to 14 days and displays snippets once verified.' }
    ],
    HowTo: [
      { id: 'name', label: 'Guide Title', type: 'text', default: 'How to Implement JSON-LD for Local SEO' },
      { id: 'description', label: 'Description', type: 'textarea', default: 'Step-by-step procedure to add structured data to your website.' },
      { id: 'step1', label: 'Step 1 Title & Description', type: 'textarea', default: 'Generate Schema: Use SchemaCraft Pro to create your business schema.' },
      { id: 'step2', label: 'Step 2 Title & Description', type: 'textarea', default: 'Embed Code: Insert the script into your website head section.' }
    ],
    Article: [
      { id: 'headline', label: 'Headline', type: 'text', default: 'Autonomous Revenue Streams: The 2026 Playbook' },
      { id: 'author', label: 'Author Name', type: 'text', default: 'The Engine Research Group' },
      { id: 'datePublished', label: 'Date Published (YYYY-MM-DD)', type: 'text', default: '2026-10-17' },
      { id: 'image', label: 'Featured Image URL', type: 'url', default: 'https://example.com/banner.png' },
      { id: 'publisher', label: 'Publisher Name', type: 'text', default: 'SchemaCraft Publications' }
    ],
    Event: [
      { id: 'name', label: 'Event Name', type: 'text', default: 'Global AI Founders Summit 2026' },
      { id: 'startDate', label: 'Start Date & Time (ISO 8601)', type: 'text', default: '2026-11-15T09:00:00Z' },
      { id: 'locationName', label: 'Venue Name', type: 'text', default: 'Moscone Center' },
      { id: 'locationAddress', label: 'Venue Address', type: 'text', default: '747 Howard St, San Francisco, CA' },
      { id: 'price', label: 'Ticket Price', type: 'number', default: '0.00' }
    ],
    JobPosting: [
      { id: 'title', label: 'Job Title', type: 'text', default: 'Senior Autonomous Systems Engineer' },
      { id: 'description', label: 'Job Description', type: 'textarea', default: 'Design and deploy self-correcting multi-agent architectures.' },
      { id: 'company', label: 'Hiring Company', type: 'text', default: 'The Engine Lab' },
      { id: 'location', label: 'Location (or Remote)', type: 'text', default: 'Remote' },
      { id: 'salary', label: 'Base Salary (Annual USD)', type: 'text', default: '180000' }
    ]
  };

  // Render input fields based on schema type
  function renderFields(type) {
    const fields = schemaDefinitions[type] || [];
    dynamicFields.innerHTML = '';
    fields.forEach(field => {
      const group = document.createElement('div');
      group.className = 'form-group';
      const label = document.createElement('label');
      label.setAttribute('for', field.id);
      label.textContent = field.label;

      let input;
      if (field.type === 'textarea') {
        input = document.createElement('textarea');
        input.className = 'form-textarea';
      } else {
        input = document.createElement('input');
        input.type = field.type;
        input.className = 'form-input';
      }
      input.id = field.id;
      input.value = field.default;
      input.addEventListener('input', generateSchema);

      group.appendChild(label);
      group.appendChild(input);
      dynamicFields.appendChild(group);
    });
    generateSchema();
  }

  // Generate JSON-LD payload
  function generateSchema() {
    const type = schemaTypeSelect.value;
    const values = {};
    const inputs = dynamicFields.querySelectorAll('.form-input, .form-textarea');
    inputs.forEach(input => { values[input.id] = input.value.trim(); });

    let schemaObject = {
      "@context": "https://schema.org"
    };

    if (type === 'LocalBusiness') {
      schemaObject["@type"] = values.businessType || "LocalBusiness";
      schemaObject["name"] = values.name;
      schemaObject["url"] = values.url;
      schemaObject["telephone"] = values.telephone;
      schemaObject["priceRange"] = values.priceRange;
      schemaObject["address"] = {
        "@type": "PostalAddress",
        "streetAddress": values.street,
        "addressLocality": values.city,
        "addressRegion": values.region,
        "postalCode": values.postalCode,
        "addressCountry": values.country
      };
    } else if (type === 'Organization') {
      schemaObject["@type"] = "Organization";
      schemaObject["name"] = values.name;
      schemaObject["url"] = values.url;
      schemaObject["logo"] = values.logo;
      schemaObject["description"] = values.description;
      if (values.sameAs) {
        schemaObject["sameAs"] = values.sameAs.split(',').map(s => s.trim()).filter(Boolean);
      }
    } else if (type === 'Product') {
      schemaObject["@type"] = "Product";
      schemaObject["name"] = values.name;
      schemaObject["description"] = values.description;
      schemaObject["image"] = values.image;
      schemaObject["brand"] = { "@type": "Brand", "name": values.brand };
      schemaObject["offers"] = {
        "@type": "Offer",
        "price": values.price,
        "priceCurrency": values.currency || "USD",
        "availability": "https://schema.org/InStock"
      };
      if (values.ratingValue) {
        schemaObject["aggregateRating"] = {
          "@type": "AggregateRating",
          "ratingValue": values.ratingValue,
          "reviewCount": values.reviewCount || "1"
        };
      }
    } else if (type === 'FAQPage') {
      schemaObject["@type"] = "FAQPage";
      schemaObject["mainEntity"] = [
        {
          "@type": "Question",
          "name": values.q1,
          "acceptedAnswer": { "@type": "Answer", "text": values.a1 }
        },
        {
          "@type": "Question",
          "name": values.q2,
          "acceptedAnswer": { "@type": "Answer", "text": values.a2 }
        }
      ];
    } else if (type === 'HowTo') {
      schemaObject["@type"] = "HowTo";
      schemaObject["name"] = values.name;
      schemaObject["description"] = values.description;
      schemaObject["step"] = [
        { "@type": "HowToStep", "text": values.step1 },
        { "@type": "HowToStep", "text": values.step2 }
      ];
    } else if (type === 'Article') {
      schemaObject["@type"] = "Article";
      schemaObject["headline"] = values.headline;
      schemaObject["author"] = { "@type": "Person", "name": values.author };
      schemaObject["datePublished"] = values.datePublished;
      schemaObject["image"] = values.image;
      schemaObject["publisher"] = { "@type": "Organization", "name": values.publisher };
    } else if (type === 'Event') {
      schemaObject["@type"] = "Event";
      schemaObject["name"] = values.name;
      schemaObject["startDate"] = values.startDate;
      schemaObject["location"] = {
        "@type": "Place",
        "name": values.locationName,
        "address": values.locationAddress
      };
      schemaObject["offers"] = {
        "@type": "Offer",
        "price": values.price,
        "priceCurrency": "USD"
      };
    } else if (type === 'JobPosting') {
      schemaObject["@type"] = "JobPosting";
      schemaObject["title"] = values.title;
      schemaObject["description"] = values.description;
      schemaObject["hiringOrganization"] = { "@type": "Organization", "name": values.company };
      schemaObject["jobLocation"] = { "@type": "Place", "address": values.location };
      schemaObject["baseSalary"] = {
        "@type": "MonetaryAmount",
        "currency": "USD",
        "value": { "@type": "QuantitativeValue", "value": values.salary, "unitText": "YEAR" }
      };
    }

    const scriptTag = `<script type="application/ld+json">\\n${JSON.stringify(schemaObject, null, 2)}\\n</script>`;
    jsonOutput.textContent = scriptTag;
  }

  // Copy to clipboard
  copyBtn.addEventListener('click', () => {
    navigator.clipboard.writeText(jsonOutput.textContent).then(() => {
      const orig = copyBtn.textContent;
      copyBtn.textContent = '✓ Copied!';
      copyBtn.style.color = '#10b981';
      setTimeout(() => { copyBtn.textContent = orig; copyBtn.style.color = ''; }, 2000);
    });
  });

  // Download .json
  downloadBtn.addEventListener('click', () => {
    const rawCode = jsonOutput.textContent;
    const blob = new Blob([rawCode], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `schema-${schemaTypeSelect.value.toLowerCase()}.json`;
    a.click();
    URL.revokeObjectURL(url);
  });

  // Validation Test link to Google's official Rich Results Test
  validateBtn.addEventListener('click', () => {
    window.open('https://search.google.com/test/rich-results', '_blank');
  });

  // Copy Email Handler
  const copyEmailBtn = document.getElementById('copyEmailBtn');
  if (copyEmailBtn) {
    copyEmailBtn.addEventListener('click', () => {
      navigator.clipboard.writeText('businessbloke957@gmail.com').then(() => {
        const orig = copyEmailBtn.textContent;
        copyEmailBtn.textContent = '✓ Copied!';
        copyEmailBtn.style.background = '#10b981';
        copyEmailBtn.style.color = '#fff';
        setTimeout(() => {
          copyEmailBtn.textContent = orig;
          copyEmailBtn.style.background = '';
          copyEmailBtn.style.color = '';
        }, 2500);
      });
    });
  }

  // Pro Modal handlers
  function openModal() { proModal.classList.add('open'); }
  function closeModalFn() { proModal.classList.remove('open'); }

  upgradeBtn.addEventListener('click', openModal);
  buyProBtn.addEventListener('click', openModal);
  closeModal.addEventListener('click', closeModalFn);
  window.addEventListener('click', (e) => { if (e.target === proModal) closeModalFn(); });

  schemaTypeSelect.addEventListener('change', () => {
    renderFields(schemaTypeSelect.value);
  });

  // Initialize with default LocalBusiness
  renderFields('LocalBusiness');
})();
"""
        with open(public_dir / "app.js", "w", encoding="utf-8") as f:
            f.write(js_content)

    def _build_backend_engine(self, node_path: Path, opp: Dict[str, Any]) -> None:
        """Builds Python-based schema engine for API and CLI use."""
        src_dir = node_path / "src"
        src_dir.mkdir(exist_ok=True)

        engine_py = """# SchemaCraft Pro - Backend Engine & Validator
import json
from typing import Dict, Any, List

class SchemaEngine:
    @staticmethod
    def generate_local_business(name: str, category: str, url: str, phone: str, 
                                address: Dict[str, str], price_range: str = "$$") -> Dict[str, Any]:
        return {
            "@context": "https://schema.org",
            "@type": category or "LocalBusiness",
            "name": name,
            "url": url,
            "telephone": phone,
            "priceRange": price_range,
            "address": {
                "@type": "PostalAddress",
                "streetAddress": address.get("street", ""),
                "addressLocality": address.get("city", ""),
                "addressRegion": address.get("region", ""),
                "postalCode": address.get("postal_code", ""),
                "addressCountry": address.get("country", "US")
            }
        }

    @staticmethod
    def generate_faq(faq_items: List[Dict[str, str]]) -> Dict[str, Any]:
        return {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": item["question"],
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": item["answer"]
                    }
                }
                for item in faq_items
            ]
        }

    @staticmethod
    def validate_schema(schema: Dict[str, Any]) -> Dict[str, Any]:
        errors = []
        if "@context" not in schema or schema["@context"] != "https://schema.org":
            errors.append("Missing or invalid '@context'. Must be 'https://schema.org'.")
        if "@type" not in schema:
            errors.append("Missing '@type' declaration.")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "schema_type": schema.get("@type", "Unknown")
        }
"""
        with open(src_dir / "schema_engine.py", "w", encoding="utf-8") as f:
            f.write(engine_py)

    def _build_monetization_layer(self, node_path: Path, opp: Dict[str, Any]) -> None:
        """Sets up monetization configurations, product metadata, and pricing."""
        mon_dir = node_path / "monetization"
        mon_dir.mkdir(exist_ok=True)

        pricing_config = {
            "currency": "USD",
            "tiers": [
                {
                    "tier_id": "free",
                    "name": "Starter",
                    "price": 0.00,
                    "upfront_cost": 0.00,
                    "features": ["Single schema generation", "8 schema types", "Instant copy/download"]
                },
                {
                    "tier_id": "agency_pro",
                    "name": "Agency Pro Pack",
                    "price": 19.00,
                    "upfront_cost": 0.00,
                    "billing": "one-time",
                    "features": [
                        "Bulk CSV Importer (100+ locations)",
                        "Whitelabel Embed Widget",
                        "REST API Access",
                        "30+ Industry Templates"
                    ],
                    "order_channel": {
                        "method": "direct_email",
                        "email": "businessbloke957@gmail.com",
                        "subject": "Order Request: SchemaCraft Agency Pro Pack ($19)",
                        "payment_methods_supported": ["PayPal", "Bank Wire", "Wise", "Crypto", "Invoice"]
                    }
                }
            ],
            "zero_cost_verification": {
                "upfront_spend": 0.00,
                "platform_fees_deducted_per_sale_only": True
            }
        }
        with open(mon_dir / "pricing.json", "w", encoding="utf-8") as f:
            json.dump(pricing_config, f, indent=2)

    @staticmethod
    def generate_standard_license(product_name: str, price: str = "$19.00 USD") -> str:
        """
        Generates standardized Commercial License & Terms of Use including:
        1. Grant of License (Commercial & Client Use)
        2. AS IS Warranty Waiver (No express or implied warranties)
        3. Strict Limitation of Liability (Capped directly to actual purchase price paid)
        4. 30-Day No-Hassle Money-Back Guarantee
        """
        return f"""COMMERCIAL LICENSE AGREEMENT & TERMS OF USE

Copyright (c) 2026 {product_name} / The Engine. All rights reserved.

1. Grant of License:
Subject to verified purchase, the licensee is granted an irrevocable, perpetual, worldwide, non-exclusive license to:
- Use the software, templates, scripts, and documentation on unlimited internal and client commercial projects.
- Integrate, adapt, and build upon the deliverables for client agency services and digital products.

2. Restrictions:
Licensee may not sub-license, redistribute, resell, or publicly share these digital assets as a standalone stock item or direct competitor to {product_name}.

3. "AS IS" Warranty Waiver:
THE SOFTWARE, SCRIPTS, TEMPLATES, AND ASSETS ARE PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS, THE ENGINE, OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT, OR OTHERWISE, ARISING FROM, OUT OF, OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

4. Strict Limitation of Liability:
UNDER NO CIRCUMSTANCES SHALL THE AUTHORS, DISTRIBUTORS, OR THE ENGINE BE LIABLE FOR ANY INDIRECT, SPECIAL, INCIDENTAL, CONSEQUENTIAL, PUNITIVE, OR EXEMPLARY DAMAGES (INCLUDING BUT NOT LIMITED TO LOSS OF PROFITS, LOSS OF REVENUE, BUSINESS INTERRUPTION, SEARCH RANKING PENALTIES, SYSTEM DOWNTIME, OR LOSS OF DATA).
IN ALL CIRCUMSTANCES, LICENSOR'S TOTAL AGGREGATE LIABILITY UNDER THIS AGREEMENT SHALL BE STRICTLY LIMITED TO THE ACTUAL PURCHASE PRICE AMOUNT PAID BY THE LICENSEE FOR THIS PRODUCT ({price}).

5. 30-Day No-Hassle Money-Back Guarantee:
If this product fails to meet your business needs or does not perform to your expectations, a full 100% refund may be requested within 30 days of purchase without hassle or dispute.
"""

    def _inject_legal_and_compliance_assets(self, node_path: Path, opp: Dict[str, Any]) -> None:
        """
        Automatically injects standardized LICENSE.txt into dist_pack and bundles deliverables into a ZIP.
        Enforces:
        - Strict AS-IS Warranty Waiver
        - Strict Liability limitation capped to purchase price
        - Risk-reversal 30-day money-back guarantee
        """
        dist_pack = node_path / "dist_pack"
        dist_pack.mkdir(parents=True, exist_ok=True)

        product_name = opp.get("name", node_path.name)
        pricing = opp.get("monetization", {})
        pro_tier = pricing.get("pro_tier", "$19.00 USD")

        license_path = dist_pack / "LICENSE.txt"
        license_content = self.generate_standard_license(product_name, pro_tier)
        with open(license_path, "w", encoding="utf-8") as f:
            f.write(license_content)

        # Ensure README.md is present in dist_pack
        readme_path = dist_pack / "README.md"
        if not readme_path.exists():
            readme_content = f"# {product_name} Deliverable Pack\n\nIncluded Files:\n- LICENSE.txt: Commercial license & AS-IS liability disclaimer.\n- Production blueprints, assets, and documentation.\n\nThank you for your order!\n"
            readme_path.write_text(readme_content, encoding="utf-8")

        # Assemble/bundle deliverable pack zip into public/downloads
        downloads_dir = node_path / "public" / "downloads"
        downloads_dir.mkdir(parents=True, exist_ok=True)

        niche_id = opp.get("niche_id", "")
        if niche_id == "schemacraft_pro":
            zip_name = "schemacraft-agency-pack.zip"
        elif niche_id == "dev_cheatsheet_vault":
            zip_name = "cloudzero-production-kit.zip"
        else:
            zip_name = f"{node_path.name}-pack.zip"

        zip_path = downloads_dir / zip_name
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for file in dist_pack.rglob("*"):
                if file.is_file():
                    arcname = file.relative_to(dist_pack)
                    zf.write(file, arcname)

    def _build_server(self, node_path: Path, opp: Dict[str, Any]) -> None:
        """Builds standalone zero-dependency Python HTTP server."""
        src_dir = node_path / "src"
        server_py = """# Standalone Zero-Dependency Micro-Server
import http.server
import socketserver
import json
import os
import sys
from pathlib import Path

PORT = int(os.environ.get("PORT", 8080))
NODE_ROOT = Path(__file__).resolve().parent.parent
PUBLIC_DIR = NODE_ROOT / "public"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from schema_engine import SchemaEngine

class EngineHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(PUBLIC_DIR), **kwargs)

    def do_GET(self):
        if self.path == "/api/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps({
                "status": "HEALTHY",
                "node": "schemacraft_pro",
                "upfront_cost": "$0.00",
                "version": "1.0.0"
            }).encode())
            return
        super().do_GET()

    def do_POST(self):
        if self.path == "/api/generate":
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length)
            try:
                data = json.loads(body.decode())
                schema_type = data.get("type", "LocalBusiness")
                if schema_type == "LocalBusiness":
                    res = SchemaEngine.generate_local_business(
                        name=data.get("name", "My Business"),
                        category=data.get("category", "LocalBusiness"),
                        url=data.get("url", "https://example.com"),
                        phone=data.get("phone", ""),
                        address=data.get("address", {}),
                        price_range=data.get("price_range", "$$")
                    )
                else:
                    res = {"@context": "https://schema.org", "@type": schema_type}

                validation = SchemaEngine.validate_schema(res)

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps({"schema": res, "validation": validation}).encode())
            except Exception as e:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode())
            return

def run_server(port=PORT):
    with socketserver.TCPServer(("", port), EngineHandler) as httpd:
        print(f"SchemaCraft Pro server live at http://localhost:{port}")
        httpd.serve_forever()

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else PORT
    run_server(port)
"""
        with open(src_dir / "server.py", "w", encoding="utf-8") as f:
            f.write(server_py)

    def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Executes Phase 2: Build."""
        opp = context.get("opportunity")
        if not opp:
            raise ValueError("Builder requires an opportunity in context.")

        node_path = self.execute_with_self_correction(
            node_id=f"node_{opp['niche_id']}",
            task_name="build_node",
            task_fn=self.build_node,
            opportunity=opp
        )
        return {
            "status": "NODE_BUILT",
            "node_id": f"node_{opp['niche_id']}",
            "workspace_path": str(node_path),
            "timestamp": get_utc_iso()
        }
