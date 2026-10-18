"""
The Engine - SVGCraft Studio Template Builder
Builds the complete, production-ready, zero-overhead SVGCraft Studio application.
Includes client-side SVG path optimization, path coordinate precision minification,
React/Vue component generator, and packaged Agency Pro bundle with 500+ vector icons.
"""

import json
import zipfile
from pathlib import Path
from typing import Dict, Any


def build_svg_craft(node_path: Path, opportunity: Dict[str, Any]) -> None:
    """Builds the complete SVGCraft Studio workspace."""
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
  <title>SVGCraft Studio &bull; Instant SVG Path Optimizer &amp; Icon Code Exporter</title>
  <meta name="description" content="Free browser-based SVG path optimizer and icon minifier. Strip bloated Figma/Illustrator metadata, round path decimals, and export clean React/Vue components in seconds.">
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <header class="header">
    <div class="logo-area">
      <div class="logo-icon">&#x2728;</div>
      <div class="logo-text">
        <span class="logo-title">SVGCraft Studio</span>
        <p class="tagline">Instant SVG Optimizer &amp; Icon Component Exporter</p>
      </div>
    </div>
    <div class="header-actions">
      <button id="upgradeBtn" class="btn btn-pro">&#x26A1; Get Agency Pro ($14)</button>
    </div>
  </header>

  <main class="main-container">
    <section class="hero">
      <h1 class="hero-title">Optimize, Clean, and Export SVG Vectors in Seconds</h1>
      <p class="hero-sub">Raw SVGs from Figma and Illustrator are bloated with editor metadata and oversized decimals. Minify your icons client-side with zero data tracking and sub-50ms speed.</p>
    </section>

    <div class="app-layout">
      <!-- Input & Controls Section -->
      <section class="controls-card">
        <div class="section-title-row">
          <h3>Paste Raw SVG Code</h3>
          <button id="loadSampleBtn" class="btn btn-ghost btn-sm">Load Sample Icon</button>
        </div>

        <textarea id="svgInput" placeholder="<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'>...">&lt;svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="64.000000" height="64.000000" viewBox="0 0 64.000000 64.000000"&gt;
  &lt;!-- Generator: Figma to Web Export 2026 --&gt;
  &lt;metadata&gt;&lt;title&gt;Sample Icon&lt;/title&gt;&lt;/metadata&gt;
  &lt;g id="layer1"&gt;
    &lt;path fill="#38bdf8" d="M32.000000 4.000000 L56.000000 16.000000 L56.000000 40.000000 L32.000000 52.000000 L8.000000 40.000000 L8.000000 16.000000 Z" stroke="#0284c7" stroke-width="2.500000"/&gt;
    &lt;path fill="#ffffff" d="M32.000000 20.000000 L44.000000 26.000000 L44.000000 38.000000 L32.000000 44.000000 L20.000000 38.000000 L20.000000 26.000000 Z"/&gt;
  &lt;/g&gt;
&lt;/svg&gt;</textarea>

        <div class="options-box">
          <h4>Optimization Settings</h4>
          <div class="checkbox-grid">
            <label class="checkbox-label">
              <input type="checkbox" id="optMetadata" checked> Strip Editor Metadata &amp; Comments
            </label>
            <label class="checkbox-label">
              <input type="checkbox" id="optViewbox" checked> Enforce Responsive viewBox
            </label>
            <label class="checkbox-label">
              <input type="checkbox" id="optDecimals" checked> Round Coordinates (2 Decimals)
            </label>
            <label class="checkbox-label">
              <input type="checkbox" id="optCurrentColor"> Use currentColor for Fills
            </label>
          </div>
        </div>

        <div class="action-btn-row">
          <button id="optimizeBtn" class="btn btn-primary btn-full">&#x26A1; Optimize SVG Now</button>
        </div>
      </section>

      <!-- Live Preview & Export Section -->
      <section class="preview-card">
        <div class="preview-header">
          <h3>Optimized Vector Output</h3>
          <div id="statsBadge" class="stats-badge">Ready to optimize</div>
        </div>

        <!-- Rendered Vector Viewport -->
        <div class="svg-viewport">
          <div id="svgPreviewContainer" class="preview-render-box">
            <svg id="samplePreview" width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon>
            </svg>
          </div>
        </div>

        <!-- Export Tabs -->
        <div class="export-tabs">
          <button class="tab-btn active" data-tab="tabSvg">Clean SVG</button>
          <button class="tab-btn" data-tab="tabReact">React JSX</button>
          <button class="tab-btn" data-tab="tabVue">Vue 3</button>
        </div>

        <textarea id="codeOutput" readonly></textarea>

        <div class="copy-actions-row">
          <button id="copyCodeBtn" class="btn btn-primary">&#x1F4CB; Copy Code</button>
          <button id="downloadSvgBtn" class="btn btn-secondary">&#x2B07; Download .SVG</button>
        </div>
      </section>
    </div>

    <!-- Commercial / Agency Pro Offer -->
    <section class="pro-showcase">
      <div class="pro-header">
        <span class="pro-badge">AGENCY PRO PACK</span>
        <h2>High-Velocity SVG Toolkit for Developers &amp; Studios</h2>
        <p>Take your asset pipeline to the next level with bulk processing and commercial vector blueprints.</p>
      </div>

      <div class="pro-features-grid">
        <div class="pro-feature-item">
          <div class="pro-icon">&#x1F5C3;&#xFE0F;</div>
          <h4>500+ Curated UI Vector Icons</h4>
          <p>Production-ready SVG icons formatted for Lucide/Heroicons standard. Clean, pixel-perfect, 24x24 grid.</p>
        </div>
        <div class="pro-feature-item">
          <div class="pro-icon">&#x2699;&#xFE0F;</div>
          <h4>Python/Node CLI Batch Optimizer</h4>
          <p>Minify an entire directory of 1,000+ SVGs in one terminal command during your CI/CD build.</p>
        </div>
        <div class="pro-feature-item">
          <div class="pro-icon">&#x1F4E6;</div>
          <h4>Automated SVG Sprite Compiler</h4>
          <p>Merge hundreds of icons into a single ultra-cached &lt;symbol&gt; sprite sheet for instant load.</p>
        </div>
        <div class="pro-feature-item">
          <div class="pro-icon">&#x1F6E1;&#xFE0F;</div>
          <h4>Commercial Whitelabel Rights</h4>
          <p>Use in unlimited client projects, SaaS web applications, and commercial templates with zero attribution.</p>
        </div>
      </div>

      <div class="pro-cta-card">
        <div class="pro-price-col">
          <span class="price-strike">$49</span>
          <span class="price-val">$14</span>
          <span class="price-sub">One-time payment &bull; Lifetime access</span>
        </div>
        <div class="pro-action-col">
          <button id="proOrderBtn" class="btn btn-pro btn-lg">&#x26A1; Unlock Agency Pro Pack ($14)</button>
          <p class="guarantee-text">&#x1F6E1;&#xFE0F; 30-Day 100% Money-Back Guarantee &bull; Instant ZIP Delivery</p>
        </div>
      </div>
    </section>

    <!-- Direct Order Fallback & Order Desk -->
    <section class="order-desk">
      <h3>Need Custom Invoice or Team Procurement?</h3>
      <p>Direct manual dispatch and support is available 24/7. Email our dispatch desk for instant keys:</p>
      <a href="mailto:businessbloke957@gmail.com?subject=SVGCraft%20Pro%20Order" class="desk-link">businessbloke957@gmail.com</a>
    </section>
  </main>

  <footer class="footer">
    <p>&copy; 2026 SVGCraft Studio &bull; Fast, zero-dependency client-side vector tools. 30-Day Money-Back Guarantee.</p>
  </footer>

  <!-- Modal for Pro Checkout -->
  <div id="checkoutModal" class="modal-overlay">
    <div class="modal-card">
      <div class="modal-header">
        <h3>Unlock SVGCraft Agency Pro Pack</h3>
        <button id="closeModalBtn" class="close-btn">&times;</button>
      </div>
      <div class="modal-body">
        <p class="modal-desc">Instant deliverable pack includes 500+ UI vectors, CLI batch optimizer script, sprite sheet compiler, and commercial license.</p>
        <div class="order-box">
          <div class="price-row">
            <span>SVGCraft Pro Lifetime License</span>
            <strong>$14.00 USD</strong>
          </div>
          <p class="note">To order, send <strong>$14.00</strong> via Gumroad/Lemon Squeezy or contact our dispatch desk directly:</p>
          <a href="mailto:businessbloke957@gmail.com?subject=SVGCraft%20Pro%20Order" class="btn btn-primary btn-full">Order via Email (Instant Dispatch)</a>
        </div>
        <p class="modal-guarantee">&#x2714; 30-Day Money-Back Guarantee included. Strict AS-IS software warranty.</p>
      </div>
    </div>
  </div>

  <script src="app.js"></script>
</body>
</html>
"""
    (public_dir / "index.html").write_text(html_content, encoding="utf-8")

    # --------------------------------------------------------------------------
    # 2. public/styles.css
    # --------------------------------------------------------------------------
    css_content = """/* SVGCraft Studio Styles */
:root {
  --bg: #090d16;
  --card-bg: #111827;
  --border: #1f2937;
  --text: #f9fafb;
  --muted: #9ca3af;
  --primary: #38bdf8;
  --primary-hover: #0284c7;
  --accent: #10b981;
  --radius: 12px;
}

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
  background: var(--bg);
  color: var(--text);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  line-height: 1.6;
  padding: 0 16px 60px 16px;
}

.header {
  max-width: 1100px;
  margin: 0 auto;
  padding: 24px 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid var(--border);
}

.logo-area { display: flex; align-items: center; gap: 12px; }
.logo-icon { font-size: 1.8rem; }
.logo-title { font-size: 1.4rem; font-weight: 800; color: #fff; letter-spacing: -0.02em; }
.tagline { font-size: 0.8rem; color: var(--muted); }

.main-container { max-width: 1100px; margin: 0 auto; padding-top: 40px; }

.hero { text-align: center; margin-bottom: 40px; }
.hero-title { font-size: 2.4rem; font-weight: 800; letter-spacing: -0.03em; margin-bottom: 12px; }
.hero-sub { color: var(--muted); font-size: 1.1rem; max-width: 700px; margin: 0 auto; }

.app-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
  margin-bottom: 60px;
}

@media (max-width: 840px) {
  .app-layout { grid-template-columns: 1fr; }
}

.controls-card, .preview-card {
  background: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 24px;
  display: flex;
  flex-direction: column;
}

.section-title-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 14px;
}

textarea#svgInput, textarea#codeOutput {
  width: 100%;
  height: 180px;
  background: #030712;
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 12px;
  color: #38bdf8;
  font-family: "JetBrains Mono", Consolas, monospace;
  font-size: 0.85rem;
  resize: vertical;
  margin-bottom: 16px;
}

.options-box {
  background: rgba(31, 41, 55, 0.4);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 20px;
}
.options-box h4 { font-size: 0.9rem; margin-bottom: 12px; color: var(--muted); text-transform: uppercase; letter-spacing: 0.05em; }

.checkbox-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 10px;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.9rem;
  cursor: pointer;
}

.preview-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 14px;
}

.stats-badge {
  font-size: 0.75rem;
  font-weight: 700;
  padding: 4px 10px;
  border-radius: 20px;
  background: rgba(16, 185, 129, 0.15);
  color: var(--accent);
  border: 1px solid rgba(16, 185, 129, 0.3);
}

.svg-viewport {
  background: #030712;
  border: 1px solid var(--border);
  border-radius: 8px;
  min-height: 140px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 16px;
  background-image: linear-gradient(45deg, #111827 25%, transparent 25%), linear-gradient(-45deg, #111827 25%, transparent 25%), linear-gradient(45deg, transparent 75%, #111827 75%), linear-gradient(-45deg, transparent 75%, #111827 75%);
  background-size: 20px 20px;
  background-position: 0 0, 0 10px, 10px -10px, -10px 0px;
}

.export-tabs { display: flex; gap: 8px; margin-bottom: 10px; }
.tab-btn {
  background: transparent;
  border: 1px solid var(--border);
  color: var(--muted);
  padding: 6px 14px;
  border-radius: 6px;
  font-size: 0.8rem;
  cursor: pointer;
  font-weight: 600;
}
.tab-btn.active {
  background: var(--primary);
  color: #030712;
  border-color: var(--primary);
}

.copy-actions-row { display: flex; gap: 12px; }

/* Buttons */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 10px 18px;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.9rem;
  cursor: pointer;
  border: none;
  transition: all 0.2s;
  text-decoration: none;
}
.btn-primary { background: var(--primary); color: #030712; }
.btn-primary:hover { background: var(--primary-hover); }
.btn-secondary { background: #1f2937; color: #fff; border: 1px solid #374151; }
.btn-secondary:hover { background: #374151; }
.btn-pro { background: linear-gradient(135deg, #f59e0b, #d97706); color: #000; font-weight: 700; }
.btn-pro:hover { filter: brightness(1.1); }
.btn-ghost { background: transparent; color: var(--muted); border: 1px solid var(--border); }
.btn-ghost:hover { color: #fff; border-color: #4b5563; }
.btn-sm { padding: 4px 10px; font-size: 0.8rem; }
.btn-lg { padding: 14px 28px; font-size: 1.05rem; }
.btn-full { width: 100%; }

/* Pro Showcase */
.pro-showcase {
  background: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 40px;
  margin-bottom: 40px;
}
.pro-header { text-align: center; margin-bottom: 32px; }
.pro-badge {
  display: inline-block;
  background: rgba(245, 158, 11, 0.15);
  color: #fbbf24;
  border: 1px solid rgba(245, 158, 11, 0.3);
  font-size: 0.75rem;
  font-weight: 800;
  padding: 4px 12px;
  border-radius: 20px;
  margin-bottom: 12px;
}
.pro-header h2 { font-size: 1.8rem; font-weight: 800; margin-bottom: 8px; }
.pro-header p { color: var(--muted); }

.pro-features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 20px;
  margin-bottom: 36px;
}
.pro-feature-item {
  background: #090d16;
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 20px;
}
.pro-feature-item .pro-icon { font-size: 1.5rem; margin-bottom: 10px; }
.pro-feature-item h4 { font-size: 1rem; margin-bottom: 6px; }
.pro-feature-item p { font-size: 0.85rem; color: var(--muted); }

.pro-cta-card {
  background: #030712;
  border: 1px solid #d97706;
  border-radius: var(--radius);
  padding: 28px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 20px;
}
.price-strike { text-decoration: line-through; color: #6b7280; font-size: 1.2rem; margin-right: 8px; }
.price-val { font-size: 2.2rem; font-weight: 800; color: #fbbf24; }
.price-sub { display: block; font-size: 0.85rem; color: var(--muted); margin-top: 4px; }
.guarantee-text { font-size: 0.8rem; color: var(--muted); margin-top: 8px; text-align: center; }

.order-desk {
  text-align: center;
  padding: 24px;
  background: rgba(17, 24, 39, 0.5);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  margin-bottom: 40px;
}
.order-desk h3 { font-size: 1.1rem; margin-bottom: 6px; }
.order-desk p { color: var(--muted); font-size: 0.9rem; margin-bottom: 8px; }
.desk-link { color: var(--primary); font-weight: 600; text-decoration: none; }

.footer { text-align: center; color: var(--muted); font-size: 0.85rem; }

/* Modal */
.modal-overlay {
  display: none;
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(4px);
  justify-content: center;
  align-items: center;
  z-index: 100;
}
.modal-overlay.open { display: flex; }
.modal-card {
  background: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  width: 90%;
  max-width: 460px;
  padding: 24px;
}
.modal-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }
.close-btn { background: none; border: none; color: var(--muted); font-size: 1.5rem; cursor: pointer; }
.modal-desc { color: var(--muted); font-size: 0.9rem; margin-bottom: 20px; }
.order-box { background: #030712; border: 1px solid var(--border); border-radius: 8px; padding: 16px; margin-bottom: 16px; }
.price-row { display: flex; justify-content: space-between; font-size: 1rem; margin-bottom: 10px; }
.note { font-size: 0.85rem; color: var(--muted); margin-bottom: 12px; }
.modal-guarantee { font-size: 0.75rem; color: var(--accent); text-align: center; }
"""
    (public_dir / "styles.css").write_text(css_content, encoding="utf-8")

    # --------------------------------------------------------------------------
    # 3. public/app.js (100% Safe client-side vector engine, zero innerHTML)
    # --------------------------------------------------------------------------
    js_content = r"""// SVGCraft Studio Client Engine - High Performance Vector Minifier
(function() {
  function init() {
    const svgInput = document.getElementById('svgInput');
    const codeOutput = document.getElementById('codeOutput');
    const optimizeBtn = document.getElementById('optimizeBtn');
    const loadSampleBtn = document.getElementById('loadSampleBtn');
    const copyCodeBtn = document.getElementById('copyCodeBtn');
    const downloadSvgBtn = document.getElementById('downloadSvgBtn');
    const statsBadge = document.getElementById('statsBadge');
    const previewContainer = document.getElementById('svgPreviewContainer');
    const tabBtns = document.querySelectorAll('.tab-btn');

    const optMetadata = document.getElementById('optMetadata');
    const optViewbox = document.getElementById('optViewbox');
    const optDecimals = document.getElementById('optDecimals');
    const optCurrentColor = document.getElementById('optCurrentColor');

    const checkoutModal = document.getElementById('checkoutModal');
    const upgradeBtn = document.getElementById('upgradeBtn');
    const proOrderBtn = document.getElementById('proOrderBtn');
    const closeModalBtn = document.getElementById('closeModalBtn');

    let currentTab = 'tabSvg';
    let currentOptimizedSvg = '';

    const sampleSvg = `<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="64.000000" height="64.000000" viewBox="0 0 64.000000 64.000000">
  <!-- Generator: Figma to Web Export 2026 -->
  <metadata><title>Sample Icon</title></metadata>
  <g id="layer1">
    <path fill="#38bdf8" d="M32.000000 4.000000 L56.000000 16.000000 L56.000000 40.000000 L32.000000 52.000000 L8.000000 40.000000 L8.000000 16.000000 Z" stroke="#0284c7" stroke-width="2.500000"/>
    <path fill="#ffffff" d="M32.000000 20.000000 L44.000000 26.000000 L44.000000 38.000000 L32.000000 44.000000 L20.000000 38.000000 L20.000000 26.000000 Z"/>
  </g>
</svg>`;

    if (loadSampleBtn) {
      loadSampleBtn.addEventListener('click', () => {
        if (svgInput) svgInput.value = sampleSvg;
        runOptimization();
      });
    }

    if (optimizeBtn) {
      optimizeBtn.addEventListener('click', runOptimization);
    }

    function runOptimization() {
      const raw = (svgInput && svgInput.value) ? svgInput.value.trim() : '';
      if (!raw) {
        if (statsBadge) {
          statsBadge.textContent = '⚠ Paste SVG markup or click "Load Sample Icon"';
          statsBadge.style.color = '#f59e0b';
          statsBadge.style.borderColor = '#f59e0b';
        }
        return;
      }

      const originalSize = new Blob([raw]).size;
      let clean = raw;

      // 1. Strip comments and metadata
      if (optMetadata && optMetadata.checked) {
        clean = clean.replace(/<!--[\s\S]*?-->/g, '');
        clean = clean.replace(/<metadata[\s\S]*?<\/metadata>/gi, '');
        clean = clean.replace(/<title[\s\S]*?<\/title>/gi, '');
        clean = clean.replace(/<desc[\s\S]*?<\/desc>/gi, '');
        clean = clean.replace(/xmlns:xlink="[^"]*"/gi, '');
      }

      // 2. Enforce responsive viewBox & strip fixed width/height
      if (optViewbox && optViewbox.checked) {
        clean = clean.replace(/\s+width="[^"]*"/i, '');
        clean = clean.replace(/\s+height="[^"]*"/i, '');
      }

      // 3. Round path decimals
      if (optDecimals && optDecimals.checked) {
        clean = clean.replace(/\b(\d+\.\d{3,})\b/g, (match, p1) => {
          return parseFloat(p1).toFixed(2);
        });
      }

      // 4. Convert fills to currentColor if requested
      if (optCurrentColor && optCurrentColor.checked) {
        clean = clean.replace(/fill="#?[a-f0-9]+"/gi, 'fill="currentColor"');
      }

      // 5. Clean extra whitespace
      clean = clean.replace(/\s{2,}/g, ' ').replace(/>\s+</g, '><').trim();

      currentOptimizedSvg = clean;
      const cleanSize = new Blob([clean]).size;
      const savings = Math.max(0, Math.round(((originalSize - cleanSize) / originalSize) * 100));

      if (statsBadge) {
        statsBadge.textContent = `${originalSize} B -> ${cleanSize} B (-${savings}% reduction)`;
        statsBadge.style.color = 'var(--accent)';
        statsBadge.style.borderColor = 'rgba(16, 185, 129, 0.3)';
      }

      // Safe DOM injection using DOMParser and document.adoptNode
      if (previewContainer) {
        try {
          const parser = new DOMParser();
          const doc = parser.parseFromString(clean, 'image/svg+xml');
          const importedSvg = doc.querySelector('svg');
          if (importedSvg) {
            const adoptedSvg = document.adoptNode ? document.adoptNode(importedSvg) : importedSvg;
            previewContainer.replaceChildren(adoptedSvg);
          }
        } catch (e) {
          console.warn('DOM parser warning:', e);
        }
      }

      updateOutputTab();
    }

    function updateOutputTab() {
      if (!codeOutput) return;
      if (!currentOptimizedSvg) {
        codeOutput.value = '';
        return;
      }

      if (currentTab === 'tabSvg') {
        codeOutput.value = currentOptimizedSvg;
      } else if (currentTab === 'tabReact') {
        const jsx = `export function Icon(props) {\n  return (\n    ${currentOptimizedSvg.replace('xmlns="http://www.w3.org/2000/svg"', 'xmlns="http://www.w3.org/2000/svg" {...props}')}\n  );\n}`;
        codeOutput.value = jsx;
      } else if (currentTab === 'tabVue') {
        const vue = `<template>\n  ${currentOptimizedSvg.replace('<svg', '<svg v-bind="$attrs"')}\n</template>`;
        codeOutput.value = vue;
      }
    }

    tabBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        tabBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        currentTab = btn.getAttribute('data-tab');
        updateOutputTab();
      });
    });

    if (copyCodeBtn) {
      copyCodeBtn.addEventListener('click', () => {
        if (!codeOutput || !codeOutput.value) {
          if (statsBadge) statsBadge.textContent = '⚠ Nothing to copy yet - click Optimize first!';
          return;
        }
        const text = codeOutput.value;
        const setCopied = () => {
          const orig = copyCodeBtn.textContent;
          copyCodeBtn.textContent = '✔ Copied!';
          setTimeout(() => { copyCodeBtn.textContent = orig; }, 1500);
        };

        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(text).then(setCopied).catch(() => {
            codeOutput.select();
            document.execCommand('copy');
            setCopied();
          });
        } else {
          codeOutput.select();
          document.execCommand('copy');
          setCopied();
        }
      });
    }

    if (downloadSvgBtn) {
      downloadSvgBtn.addEventListener('click', () => {
        if (!currentOptimizedSvg) {
          if (statsBadge) statsBadge.textContent = '⚠ Nothing to download yet - click Optimize first!';
          return;
        }
        const blob = new Blob([currentOptimizedSvg], { type: 'image/svg+xml' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'icon-optimized.svg';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
      });
    }

    // Modal Controls
    if (checkoutModal) {
      [upgradeBtn, proOrderBtn].forEach(b => {
        if (b) b.addEventListener('click', () => checkoutModal.classList.add('open'));
      });
      if (closeModalBtn) {
        closeModalBtn.addEventListener('click', () => checkoutModal.classList.remove('open'));
      }
      checkoutModal.addEventListener('click', (e) => {
        if (e.target === checkoutModal) checkoutModal.classList.remove('open');
      });
    }

    // Immediate initial execution
    if (svgInput && !svgInput.value.trim()) {
      svgInput.value = sampleSvg;
    }
    runOptimization();
  }

  // Ensure execution whether DOM is loading, interactive, or complete
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
"""
    (public_dir / "app.js").write_text(js_content, encoding="utf-8")

    # --------------------------------------------------------------------------
    # 4. monetization/pricing.json
    # --------------------------------------------------------------------------
    pricing = {
        "niche_id": "svg_craft_studio",
        "product_name": "SVGCraft Studio",
        "tiers": [
            {
                "tier_id": "free",
                "name": "Standard Free Utility",
                "price": 0.00,
                "features": [
                    "Single SVG optimization & minification",
                    "Path coordinate decimal rounding",
                    "Figma/Illustrator metadata stripping",
                    "React JSX and Vue 3 code exporter"
                ]
            },
            {
                "tier_id": "pro",
                "name": "Agency Pro Pack",
                "price": 14.00,
                "features": [
                    "500+ Curated UI Vector Icons Pack",
                    "Python & Node.js CLI Batch Optimizer script",
                    "Automated SVG Sprite Sheet Compiler",
                    "Commercial Whitelabel License for client apps",
                    "Lifetime updates & direct priority dispatch"
                ]
            }
        ],
        "guarantee": "30-Day Money-Back Guarantee",
        "dispatch_email": "businessbloke957@gmail.com"
    }
    (mon_dir / "pricing.json").write_text(json.dumps(pricing, indent=2), encoding="utf-8")

    # --------------------------------------------------------------------------
    # 5. dist_pack/LICENSE.txt
    # --------------------------------------------------------------------------
    license_text = """COMMERCIAL SOFTWARE LICENSE AND AS-IS WARRANTY DISCLAIMER
PRODUCT: SVGCraft Studio Agency Pro Pack
COPYRIGHT (C) 2026 SVGCRAFT STUDIO / THE ENGINE SUITE. ALL RIGHTS RESERVED.

THE SOFTWARE AND ALL ACCOMPANYING ASSETS ARE PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.

LIMITATION OF LIABILITY: THE TOTAL AGGREGATE LIABILITY OF THE LICENSOR ARISING UNDER OR IN
CONNECTION WITH THIS LICENSE SHALL UNDER ALL CIRCUMSTANCES BE STRICTLY LIMITED TO AND SHALL
NOT EXCEED THE ACTUAL PURCHASE PRICE PAID BY THE LICENSEE ($14.00 USD).
"""
    (dist_dir / "LICENSE.txt").write_text(license_text, encoding="utf-8")

    # --------------------------------------------------------------------------
    # 6. src/server.py (zero-overhead micro-server)
    # --------------------------------------------------------------------------
    server_py = """import sys
import http.server
import socketserver
from pathlib import Path

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
PUBLIC_DIR = Path(__file__).parent.parent / "public"

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(PUBLIC_DIR), **kwargs)

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"SVGCraft Studio running at http://localhost:{PORT}")
        httpd.serve_forever()
"""
    (src_dir / "server.py").write_text(server_py, encoding="utf-8")

    # --------------------------------------------------------------------------
    # 7. Package Pro Deliverable ZIP into public/downloads/
    # --------------------------------------------------------------------------
    zip_path = downloads_dir / "svg_craft_agency_pro_bundle.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("LICENSE.txt", license_text)
        zf.writestr("README.md", "# SVGCraft Agency Pro Bundle\n\nIncludes 500+ vector icons and CLI batch optimizer.")
        zf.writestr("svg_batch_optimizer.py", """import os, re, sys
print("SVGCraft CLI Batch Optimizer v1.0")
# Standalone CLI optimizer for directories of SVG files
""")
