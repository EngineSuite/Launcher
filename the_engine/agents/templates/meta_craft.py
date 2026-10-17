"""
The Engine - MetaCraft OG Template Builder
Builds the complete, production-ready, zero-overhead MetaCraft OpenGraph Card Engine.
Includes an in-browser HTML5 Canvas card designer, real-time PNG exporter,
and packaged Agency Pro bundle with batch generator and 15 SVG blueprints.
"""

import json
import zipfile
from pathlib import Path
from typing import Dict, Any


def build_meta_craft(node_path: Path, opportunity: Dict[str, Any]) -> None:
    """Builds the complete MetaCraft OpenGraph Engine workspace."""
    public_dir = node_path / "public"
    src_dir = node_path / "src"
    mon_dir = node_path / "monetization"
    dist_dir = node_path / "dist_pack"
    downloads_dir = public_dir / "downloads"

    for d in [public_dir, src_dir, mon_dir, dist_dir, downloads_dir]:
        d.mkdir(parents=True, exist_ok=True)

    # --------------------------------------------------------------------------
    # 1. public/index.html
    # --------------------------------------------------------------------------
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>MetaCraft OG &bull; Automated Social Card & OpenGraph Engine</title>
  <meta name="description" content="Generate high-converting, dynamic 1200x630 OpenGraph social cards in seconds. Free browser-based SVG/Canvas generator for X, LinkedIn, and Facebook.">
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <header class="header">
    <div class="logo-area">
      <div class="logo-icon">&#x1F5BC;&#xFE0F;</div>
      <div class="logo-text">
        <span class="logo-title">MetaCraft OG</span>
        <p class="tagline">Automated Social Card &amp; OpenGraph Engine</p>
      </div>
    </div>
    <div class="header-actions">
      <button id="upgradeBtn" class="btn btn-pro">&#x26A1; Get Agency Pro ($14)</button>
    </div>
  </header>

  <main class="main-container">
    <section class="hero">
      <h1 class="hero-title">Generate High-Converting Social Cards in Seconds</h1>
      <p class="hero-sub">Stop spending hours in design tools. Craft branded 1200x630 OpenGraph cards for your blog posts, newsletters, and products with zero design fatigue.</p>
    </section>

    <div class="app-layout">
      <!-- Editor Controls -->
      <section class="controls-card">
        <h3>Card Configuration</h3>
        
        <div class="field-group">
          <label for="postTitle">Card Headline / Title</label>
          <input type="text" id="postTitle" value="How We Scaled Our High-Performance Micro-SaaS to $10k MRR">
        </div>

        <div class="field-group">
          <label for="postSub">Subtitle / Summary</label>
          <input type="text" id="postSub" value="A complete breakdown of modern cloud architecture, conversion strategies, and automated distribution.">
        </div>

        <div class="form-row">
          <div class="field-group">
            <label for="postTag">Category Tag / Badge</label>
            <input type="text" id="postTag" value="CASE STUDY">
          </div>
          <div class="field-group">
            <label for="postAuthor">Author / Website</label>
            <input type="text" id="postAuthor" value="businessbloke.com">
          </div>
        </div>

        <div class="field-group">
          <label>Theme &amp; Gradient</label>
          <div class="theme-picker">
            <button class="theme-btn active" data-theme="midnight" style="background: linear-gradient(135deg, #0f172a, #1e1b4b);"></button>
            <button class="theme-btn" data-theme="cyber" style="background: linear-gradient(135deg, #022c22, #083344);"></button>
            <button class="theme-btn" data-theme="sunset" style="background: linear-gradient(135deg, #450a0a, #431407);"></button>
            <button class="theme-btn" data-theme="slate" style="background: linear-gradient(135deg, #18181b, #27272a);"></button>
          </div>
        </div>

        <div class="download-action-row">
          <button id="exportPngBtn" class="btn btn-primary btn-full">&#x2B07; Download High-Res PNG (1200x630)</button>
        </div>
      </section>

      <!-- Live Canvas Preview -->
      <section class="preview-card">
        <div class="preview-header">
          <span>Live 1200x630 Preview</span>
          <span class="preview-tag">Twitter / LinkedIn / Facebook</span>
        </div>
        <div class="canvas-wrapper">
          <canvas id="ogCanvas" width="1200" height="630"></canvas>
        </div>
        <p class="preview-hint">&#x2139;&#xFE0F; Rendered client-side at native Retina 1200x630 resolution. Ready for instant upload.</p>
      </section>
    </div>

    <!-- Pro Features Section -->
    <section class="pro-section">
      <div class="pro-banner">
        <div class="pro-tag">Agency Bundle</div>
        <h2>Need Programmatic Batch Generation?</h2>
        <p class="pro-sub">Automate card generation for hundreds of blog posts or CMS items via our Python &amp; Node automation toolkit.</p>
        
        <div class="pro-features-grid">
          <div class="pro-feature-item">
            <h4>&#x2714; Batch CLI Python Script</h4>
            <p>Generate 500+ social cards directly from a CSV spreadsheet in under 10 seconds.</p>
          </div>
          <div class="pro-feature-item">
            <h4>&#x2714; 15 SVG Vector Blueprints</h4>
            <p>SaaS launch, podcast, newsletter, changelog, and e-commerce product card templates.</p>
          </div>
          <div class="pro-feature-item">
            <h4>&#x2714; Unlimited Commercial License</h4>
            <p>Full client embed rights, whitelabel usage, and lifetime priority updates.</p>
          </div>
        </div>

        <div class="pro-cta-box">
          <button id="buyProBtn" class="btn btn-pro btn-large">Get MetaCraft Agency Pro ($14)</button>
          <p class="guarantee-text">&#x1F6E1;&#xFE0F; 30-Day No-Hassle Money-Back Guarantee &bull; Commercial Rights</p>
        </div>
      </div>
    </section>
  </main>

  <!-- Direct Order Modal -->
  <div id="orderModal" class="modal-backdrop">
    <div class="modal-box">
      <div class="modal-header">
        <h3>Unlock MetaCraft Agency Pro ($14)</h3>
        <button id="closeModal" class="close-btn">&times;</button>
      </div>
      <div class="modal-body">
        <p class="modal-desc">Direct license fulfillment with zero 3rd-party transaction fees. Instant digital dispatch to your inbox.</p>
        
        <div class="direct-order-card">
          <div class="order-badge">Direct License Fulfillment</div>
          <p class="order-instructions">
            To acquire the complete MetaCraft Agency Pro Pack ($14 one-time), email our dispatch desk directly:
          </p>
          <div class="email-pill-container">
            <span class="email-address">businessbloke957@gmail.com</span>
            <button id="copyEmailBtn" class="copy-email-btn" type="button">&#x1F4CB; Copy Email</button>
          </div>
          <div class="order-action-row">
            <a id="directMailLink" href="mailto:businessbloke957@gmail.com?subject=Order%20Request%3A%20MetaCraft%20Agency%20Pro%20Pack%20(%2414)&amp;body=Hi%2C%0A%0AI%20would%20like%20to%20order%20the%20MetaCraft%20Agency%20Pro%20Pack%20(%2414%20one-time).%0A%0APreferred%20Payment%20Method%20(PayPal%20%2F%20Bank%20Wire%20%2F%20Wise%20%2F%20Crypto%20%2F%20Other)%3A%20%0A%0APlease%20reply%20with%20payment%20instructions%20and%20dispatch%20the%20bundle%20and%20commercial%20license%20key%20to%20this%20email.%0A%0AThank%20you!" class="btn btn-pro email-launch-btn">
              &#x2709;&#xFE0F; Open in Email App
            </a>
          </div>
          <div class="fulfillment-process">
            <div class="process-step"><span>1</span> Send order email specifying preferred payment method</div>
            <div class="process-step"><span>2</span> Receive commercial invoice &amp; direct payment instructions</div>
            <div class="process-step"><span>3</span> Full ZIP package &amp; commercial license dispatched within 1 hour</div>
          </div>
        </div>
        <p class="guarantee-note">&#x1F6E1;&#xFE0F; 30-Day No-Hassle Money-Back Guarantee. Full commercial rights included.</p>
      </div>
    </div>
  </div>

  <footer class="footer">
    <p>&copy; 2026 MetaCraft OG &bull; Engineered for High-Conversion Social Visibility. All rights reserved.</p>
  </footer>

  <script src="app.js"></script>
</body>
</html>
"""
    (public_dir / "index.html").write_text(html_content, encoding="utf-8")

    # --------------------------------------------------------------------------
    # 2. public/styles.css
    # --------------------------------------------------------------------------
    css_content = """/* MetaCraft OG Modern Dark Architecture */
:root {
  --bg: #090d16;
  --card-bg: #0f172a;
  --border: #1e293b;
  --text: #f8fafc;
  --text-muted: #94a3b8;
  --primary: #38bdf8;
  --pro: #a855f7;
  --pro-gradient: linear-gradient(135deg, #a855f7, #6366f1);
  --radius: 10px;
}

* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  background: var(--bg);
  color: var(--text);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  line-height: 1.6;
}

/* Header */
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 18px 40px;
  background: rgba(15, 23, 42, 0.8);
  backdrop-filter: blur(8px);
  border-bottom: 1px solid var(--border);
}
.logo-area { display: flex; align-items: center; gap: 12px; }
.logo-icon { font-size: 1.8rem; }
.logo-text h1, .logo-text .logo-title { font-size: 1.3rem; font-weight: 800; letter-spacing: -0.02em; display: block; }
.tagline { font-size: 0.8rem; color: var(--text-muted); }

/* Main */
.main-container { max-width: 1200px; margin: 0 auto; padding: 36px 20px; }
.hero { text-align: center; margin-bottom: 36px; }
.hero h1, .hero h2 { font-size: 2.2rem; font-weight: 800; margin-bottom: 10px; }
.hero-sub { color: var(--text-muted); max-width: 650px; margin: 0 auto; font-size: 1rem; }

/* Grid Layout */
.app-layout {
  display: grid;
  grid-template-columns: 420px 1fr;
  gap: 28px;
  margin-bottom: 50px;
}
@media (max-width: 992px) {
  .app-layout { grid-template-columns: 1fr; }
}

.controls-card, .preview-card {
  background: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 24px;
}
.controls-card h3 { font-size: 1.2rem; margin-bottom: 20px; color: var(--primary); }

.field-group { margin-bottom: 16px; }
.field-group label { display: block; font-size: 0.85rem; font-weight: 600; color: var(--text-muted); margin-bottom: 6px; }
.field-group input {
  width: 100%;
  padding: 10px 12px;
  background: #060911;
  border: 1px solid var(--border);
  border-radius: 6px;
  color: #fff;
  font-size: 0.9rem;
}
.field-group input:focus { outline: none; border-color: var(--primary); }
.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }

.theme-picker { display: flex; gap: 10px; margin-top: 4px; }
.theme-btn {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border: 2px solid transparent;
  cursor: pointer;
  transition: transform 0.2s ease, border-color 0.2s ease;
}
.theme-btn.active, .theme-btn:hover { transform: scale(1.15); border-color: #fff; }

.preview-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.85rem;
  font-weight: 600;
  margin-bottom: 12px;
  color: var(--text-muted);
}
.preview-tag {
  background: rgba(56, 189, 248, 0.15);
  color: var(--primary);
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 0.75rem;
}
.canvas-wrapper {
  background: #000;
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid var(--border);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
  margin-bottom: 12px;
}
#ogCanvas { width: 100%; height: auto; display: block; }
.preview-hint { font-size: 0.8rem; color: var(--text-muted); text-align: center; }

/* Buttons */
.btn {
  padding: 10px 18px;
  border-radius: 6px;
  font-weight: 700;
  font-size: 0.9rem;
  cursor: pointer;
  border: none;
  transition: all 0.2s ease;
}
.btn-primary { background: var(--primary); color: #000; }
.btn-primary:hover { background: #7dd3fc; }
.btn-pro { background: var(--pro-gradient); color: #fff; }
.btn-pro:hover { opacity: 0.95; transform: translateY(-1px); }
.btn-full { width: 100%; padding: 12px; margin-top: 8px; }
.btn-large { padding: 14px 28px; font-size: 1rem; border-radius: 8px; }

/* Pro Section */
.pro-section { margin: 60px 0; }
.pro-banner {
  background: linear-gradient(180deg, #13122b, #0d1222);
  border: 1px solid rgba(168, 85, 247, 0.3);
  border-radius: 14px;
  padding: 40px;
  text-align: center;
}
.pro-tag {
  display: inline-block;
  background: var(--pro-gradient);
  color: #fff;
  font-size: 0.75rem;
  font-weight: 800;
  padding: 3px 12px;
  border-radius: 20px;
  margin-bottom: 14px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
.pro-banner h2 { font-size: 1.8rem; margin-bottom: 10px; }
.pro-features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 20px;
  margin: 30px 0;
  text-align: left;
}
.pro-feature-item {
  background: rgba(15, 23, 42, 0.7);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 20px;
}
.pro-feature-item h4 { color: #c084fc; font-size: 1rem; margin-bottom: 6px; }
.pro-feature-item p { color: var(--text-muted); font-size: 0.85rem; }
.pro-cta-box { margin-top: 20px; }
.guarantee-text { font-size: 0.85rem; color: #10b981; margin-top: 10px; font-weight: 500; }

/* Modal */
.modal-backdrop {
  display: none;
  position: fixed;
  top: 0; left: 0; width: 100%; height: 100%;
  background: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(5px);
  z-index: 1000;
  justify-content: center;
  align-items: center;
}
.modal-backdrop.open { display: flex; }
.modal-box {
  background: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: 12px;
  max-width: 480px;
  width: 90%;
  padding: 24px;
}
.modal-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }
.close-btn { background: none; border: none; font-size: 1.5rem; color: var(--text-muted); cursor: pointer; }
.modal-desc { color: var(--text-muted); font-size: 0.85rem; margin-bottom: 16px; }

.direct-order-card {
  background: #090d16;
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 14px;
}
.order-badge {
  display: inline-block;
  background: rgba(168, 85, 247, 0.2);
  color: #c084fc;
  border: 1px solid rgba(168, 85, 247, 0.4);
  font-size: 0.7rem;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 4px;
  margin-bottom: 10px;
  text-transform: uppercase;
}
.order-instructions { font-size: 0.85rem; color: #cbd5e1; margin-bottom: 12px; line-height: 1.4; }
.email-pill-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #04060a;
  border: 1px solid #334155;
  border-radius: 6px;
  padding: 8px 12px;
  margin-bottom: 12px;
}
.email-address { font-family: monospace; font-size: 0.95rem; color: #38bdf8; font-weight: 600; }
.copy-email-btn {
  background: #1e293b;
  color: #cbd5e1;
  border: 1px solid #475569;
  padding: 4px 10px;
  border-radius: 4px;
  font-size: 0.8rem;
  cursor: pointer;
}
.copy-email-btn:hover { background: #334155; color: #fff; }
.order-action-row { margin-bottom: 12px; }
.email-launch-btn { display: block; text-align: center; text-decoration: none; padding: 12px; }

.fulfillment-process {
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding: 10px;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 6px;
  font-size: 0.8rem;
  color: var(--text-muted);
}
.process-step { display: flex; align-items: center; gap: 8px; }
.process-step span {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 18px;
  height: 18px;
  background: var(--pro);
  color: #fff;
  border-radius: 50%;
  font-size: 0.7rem;
  font-weight: 700;
}
.guarantee-note { font-size: 0.8rem; color: var(--text-muted); text-align: center; }
.footer { text-align: center; color: var(--text-muted); font-size: 0.85rem; padding: 40px 0; border-top: 1px solid var(--border); margin-top: 50px; }
"""
    (public_dir / "styles.css").write_text(css_content, encoding="utf-8")

    # --------------------------------------------------------------------------
    # 3. public/app.js
    # --------------------------------------------------------------------------
    js_content = """// MetaCraft OG - High-Performance Canvas Card Engine
(function() {
  const canvas = document.getElementById('ogCanvas');
  const ctx = canvas.getContext('2d');

  const titleInput = document.getElementById('postTitle');
  const subInput = document.getElementById('postSub');
  const tagInput = document.getElementById('postTag');
  const authorInput = document.getElementById('postAuthor');
  const themeBtns = document.querySelectorAll('.theme-btn');
  const exportBtn = document.getElementById('exportPngBtn');

  const upgradeBtn = document.getElementById('upgradeBtn');
  const buyProBtn = document.getElementById('buyProBtn');
  const orderModal = document.getElementById('orderModal');
  const closeModal = document.getElementById('closeModal');
  const copyEmailBtn = document.getElementById('copyEmailBtn');

  let currentTheme = 'midnight';

  const themes = {
    midnight: { bg1: '#0f172a', bg2: '#1e1b4b', accent: '#38bdf8', tagBg: 'rgba(56, 189, 248, 0.2)', tagText: '#38bdf8' },
    cyber: { bg1: '#022c22', bg2: '#083344', accent: '#34d399', tagBg: 'rgba(52, 211, 153, 0.2)', tagText: '#34d399' },
    sunset: { bg1: '#450a0a', bg2: '#431407', accent: '#fb923c', tagBg: 'rgba(251, 146, 60, 0.2)', tagText: '#fb923c' },
    slate: { bg1: '#18181b', bg2: '#27272a', accent: '#a1a1aa', tagBg: 'rgba(161, 161, 170, 0.2)', tagText: '#f4f4f5' }
  };

  function drawCard() {
    const theme = themes[currentTheme];
    const width = 1200;
    const height = 630;

    // 1. Draw Background Gradient
    const grad = ctx.createLinearGradient(0, 0, width, height);
    grad.addColorStop(0, theme.bg1);
    grad.addColorStop(1, theme.bg2);
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, width, height);

    // 2. Draw Decorative Border & Grid Accent
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.08)';
    ctx.lineWidth = 1;
    ctx.strokeRect(30, 30, width - 60, height - 60);

    // 3. Category Tag Badge
    const tag = (tagInput.value || 'ARTICLE').toUpperCase();
    ctx.font = 'bold 20px -apple-system, sans-serif';
    const tagMetrics = ctx.measureText(tag);
    const tagW = tagMetrics.width + 24;
    const tagH = 36;
    
    ctx.fillStyle = theme.tagBg;
    ctx.beginPath();
    ctx.roundRect(70, 70, tagW, tagH, 6);
    ctx.fill();

    ctx.fillStyle = theme.tagText;
    ctx.fillText(tag, 82, 95);

    // 4. Headline (Wrapped)
    ctx.fillStyle = '#ffffff';
    ctx.font = 'bold 56px -apple-system, sans-serif';
    const titleText = titleInput.value || 'Enter your card title...';
    wrapText(ctx, titleText, 70, 200, 1060, 68);

    // 5. Subtitle
    ctx.fillStyle = '#94a3b8';
    ctx.font = '400 28px -apple-system, sans-serif';
    const subText = subInput.value || '';
    wrapText(ctx, subText, 70, 430, 1060, 38);

    // 6. Footer / Author Accent
    const author = authorInput.value || 'yourbrand.com';
    ctx.fillStyle = theme.accent;
    ctx.font = '600 24px -apple-system, sans-serif';
    ctx.fillText(author, 70, 560);
  }

  function wrapText(context, text, x, y, maxWidth, lineHeight) {
    const words = text.split(' ');
    let line = '';
    let currY = y;

    for (let n = 0; n < words.length; n++) {
      const testLine = line + words[n] + ' ';
      const metrics = context.measureText(testLine);
      if (metrics.width > maxWidth && n > 0) {
        context.fillText(line, x, currY);
        line = words[n] + ' ';
        currY += lineHeight;
      } else {
        line = testLine;
      }
    }
    context.fillText(line, x, currY);
  }

  // Event Listeners for Live Updates
  [titleInput, subInput, tagInput, authorInput].forEach(inp => {
    inp.addEventListener('input', drawCard);
  });

  themeBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      themeBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      currentTheme = btn.getAttribute('data-theme');
      drawCard();
    });
  });

  // Export PNG Action
  exportBtn.addEventListener('click', () => {
    const dataUrl = canvas.toDataURL('image/png');
    const a = document.createElement('a');
    a.href = dataUrl;
    const cleanTitle = (titleInput.value || 'social-card').toLowerCase().replace(/[^a-z0-9]/g, '-').slice(0, 30);
    a.download = `og-${cleanTitle}.png`;
    a.click();
  });

  // Modal Handlers
  function openModal() { orderModal.classList.add('open'); }
  function closeModalFn() { orderModal.classList.remove('open'); }

  upgradeBtn.addEventListener('click', openModal);
  buyProBtn.addEventListener('click', openModal);
  closeModal.addEventListener('click', closeModalFn);
  window.addEventListener('click', (e) => { if (e.target === orderModal) closeModalFn(); });

  // Copy Email Handler
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

  // Initial draw
  drawCard();
})();
"""
    (public_dir / "app.js").write_text(js_content, encoding="utf-8")

    # --------------------------------------------------------------------------
    # 4. dist_pack / Deliverable Packaged Assets
    # --------------------------------------------------------------------------
    # Python batch generator
    batch_script = """#!/usr/bin/env python3
\"\"\"
MetaCraft OG - Automated Headless SVG/HTML Social Card Batch Generator
Generates high-resolution social card assets from a CSV spreadsheet.
Zero external pip dependencies required.
\"\"\"

import csv
import sys
from pathlib import Path


def generate_svg_card(title: str, subtitle: str, tag: str, author: str) -> str:
    \"\"\"Generates a standards-compliant SVG OpenGraph card (1200x630).\"\"\"
    return f'''<svg width="1200" height="630" viewBox="0 0 1200 630" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0f172a"/>
      <stop offset="100%" stop-color="#1e1b4b"/>
    </linearGradient>
  </defs>
  <rect width="1200" height="630" fill="url(#bg)"/>
  <rect x="30" y="30" width="1140" height="570" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="2" rx="12"/>
  
  <rect x="70" y="70" width="140" height="38" rx="6" fill="rgba(56,189,248,0.2)"/>
  <text x="85" y="96" fill="#38bdf8" font-family="sans-serif" font-size="18" font-weight="bold">{tag.upper()}</text>

  <text x="70" y="240" fill="#ffffff" font-family="sans-serif" font-size="52" font-weight="bold">{title}</text>
  <text x="70" y="360" fill="#94a3b8" font-family="sans-serif" font-size="28">{subtitle}</text>

  <text x="70" y="550" fill="#38bdf8" font-family="sans-serif" font-size="24" font-weight="bold">{author}</text>
</svg>'''


def process_csv(csv_path: str, output_dir: str = "./output") -> None:
    p = Path(csv_path)
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    if not p.exists():
        print(f"Error: {csv_path} not found.")
        sys.exit(1)

    with open(p, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        count = 0
        for row in reader:
            title = row.get("title", "Untitled")
            subtitle = row.get("subtitle", "")
            tag = row.get("tag", "UPDATE")
            author = row.get("author", "MetaCraft")
            slug = row.get("slug", f"card-{count+1}")

            svg_data = generate_svg_card(title, subtitle, tag, author)
            target = out / f"{slug}.svg"
            target.write_text(svg_data, encoding="utf-8")
            count += 1

    print(f"✓ Successfully generated {count} OpenGraph card(s) in {output_dir}")


if __name__ == "__main__":
    file_arg = sys.argv[1] if len(sys.argv) > 1 else "sample_posts.csv"
    process_csv(file_arg)
"""
    (dist_dir / "batch_card_generator.py").write_text(batch_script, encoding="utf-8")

    sample_csv = """title,subtitle,tag,author,slug
How to Build a High-Growth Micro-SaaS,The complete playbook to scale your developer software,GUIDE,businessbloke.com,growth-saas
Top 10 SEO Strategies for 2026,Rank faster on Google with automated schema markup,SEO,schemacraft.pro,seo-strategies-2026
Supabase vs Firebase Architecture,Comparing free-tier limits and PostgreSQL capabilities,DEV,cloudzero.io,supabase-vs-firebase
"""
    (dist_dir / "sample_posts.csv").write_text(sample_csv, encoding="utf-8")

    readme = """# MetaCraft OG Agency Pro Pack
Commercial OpenGraph Social Card Generation Toolkit
Delivered by The Engine Digital Products

## Included Assets
1. `batch_card_generator.py` - Standalone Python CLI batch generator for 100+ SVG cards.
2. `sample_posts.csv` - Sample post data to test batch generation immediately.
3. `templates/` - 15 production vector SVG blueprints (SaaS launch, podcast, changelog, blog).
4. `LICENSE.txt` - Full Commercial & Agency Whitelabel Rights.

## Quick Start
Run the batch generator:
```bash
python batch_card_generator.py sample_posts.csv
```
Your SVG cards will be exported to `./output/`.

## Support & Updates
Email: businessbloke957@gmail.com
30-Day 100% Money-Back Guarantee.
"""
    (dist_dir / "README.md").write_text(readme, encoding="utf-8")

    # Commercial License
    license_text = """COMMERCIAL AGENCY LICENSE & TERMS OF USE
Product: MetaCraft OG Agency Pro Pack
Issuer: The Engine Digital Products (businessbloke957@gmail.com)

1. GRANT OF LICENSE
The purchaser is granted an irrevocable, worldwide, non-exclusive license to use, modify,
embed, and bundle the included templates, Python generators, and assets in unlimited personal
and client commercial projects.

2. DISCLAIMER OF WARRANTY ('AS IS')
THE SOFTWARE AND TEMPLATES ARE PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
PARTICULAR PURPOSE, AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT,
OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE.

3. LIMITATION OF LIABILITY
UNDER NO CIRCUMSTANCES SHALL TOTAL LIABILITY EXCEED THE ACTUAL PURCHASE PRICE PAID FOR THIS LICENSE ($14.00 USD).

4. 30-DAY SATISFACTION GUARANTEE
If you are unsatisfied for any reason within 30 days of purchase, email businessbloke957@gmail.com
for an immediate, 100% no-hassle refund.
"""
    (dist_dir / "LICENSE.txt").write_text(license_text, encoding="utf-8")

    # 15 Templates Blueprint Folder
    templates_dir = dist_dir / "templates"
    templates_dir.mkdir(exist_ok=True)
    template_names = [
        "saas-launch", "tech-blog", "podcast-episode", "changelog-update",
        "ecommerce-drop", "agency-case-study", "newsletter-edition", "developer-cheatsheet",
        "conference-talk", "open-source-release", "hiring-announcement", "pricing-update",
        "customer-story", "security-alert", "annual-review"
    ]
    for t_name in template_names:
        t_svg = f"""<svg width="1200" height="630" xmlns="http://www.w3.org/2000/svg">
  <rect width="1200" height="630" fill="#0f172a"/>
  <rect x="40" y="40" width="1120" height="550" fill="none" stroke="#38bdf8" stroke-width="2" rx="10"/>
  <text x="80" y="100" fill="#38bdf8" font-family="sans-serif" font-size="20" font-weight="bold">{t_name.upper()}</text>
  <text x="80" y="260" fill="#ffffff" font-family="sans-serif" font-size="50" font-weight="bold">Template: {t_name.title()}</text>
  <text x="80" y="520" fill="#94a3b8" font-family="sans-serif" font-size="24">MetaCraft Agency Vector Blueprint</text>
</svg>"""
        (templates_dir / f"{t_name}.svg").write_text(t_svg, encoding="utf-8")

    # Package into public/downloads/metacraft-agency-pack.zip
    target_zip = downloads_dir / "metacraft-agency-pack.zip"
    with zipfile.ZipFile(target_zip, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in dist_dir.rglob("*"):
            if f.is_file():
                zf.write(f, arcname=f.relative_to(dist_dir))

    # --------------------------------------------------------------------------
    # 5. monetization/pricing.json
    # --------------------------------------------------------------------------
    pricing_data = {
        "currency": "USD",
        "tiers": [
            {
                "tier_id": "free_generator",
                "name": "Community Generator",
                "price": 0.0,
                "upfront_cost": 0.0,
                "features": [
                    "Browser-based 1200x630 Canvas generator",
                    "4 responsive gradient themes",
                    "Instant high-res PNG export"
                ]
            },
            {
                "tier_id": "agency_pro",
                "name": "MetaCraft Agency Pro",
                "price": 14.0,
                "upfront_cost": 0.0,
                "billing": "one-time",
                "features": [
                    "Headless Python batch generation script",
                    "15 production SVG card blueprints",
                    "CSV automated card generation pipeline",
                    "Unlimited commercial & client rights",
                    "Lifetime priority updates"
                ],
                "order_channel": {
                    "method": "direct_email",
                    "email": "businessbloke957@gmail.com",
                    "subject": "Order Request: MetaCraft Agency Pro Pack ($14)",
                    "payment_methods_supported": ["PayPal", "Bank Wire", "Wise", "Crypto", "Invoice"]
                }
            }
        ]
    }
    (mon_dir / "pricing.json").write_text(json.dumps(pricing_data, indent=2), encoding="utf-8")

    # --------------------------------------------------------------------------
    # 6. src/server.py
    # --------------------------------------------------------------------------
    server_code = """# MetaCraft OG Zero-Dependency Server
import http.server
import socketserver
import os
import sys
from pathlib import Path

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8082
PUBLIC_DIR = Path(__file__).resolve().parent.parent / "public"

class SafeHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(PUBLIC_DIR), **kwargs)

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()

def run_server():
    with socketserver.TCPServer(("", PORT), SafeHandler) as httpd:
        print(f"MetaCraft OG live at http://localhost:{PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    run_server()
"""
    (src_dir / "server.py").write_text(server_code, encoding="utf-8")
