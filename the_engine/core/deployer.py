"""
The Engine - Cloud Deployment & Static Distribution Manager
Compiles and optimizes all active revenue nodes into a unified, zero-cost static distribution package.
Ready for 100% free hosting on GitHub Pages, Cloudflare Pages, or Vercel Hobby.
"""

import shutil
import json
import re
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime, timezone

from the_engine.core.isolation import NodeIsolationManager
from the_engine.config import get_utc_iso, BASE_DIR


class DeploymentManager:
    """
    Builds the production-ready distribution bundle in /dist:
    1. Aggregates all active nodes into clean URL paths (/schemacraft, /cloudzero, /metacraft).
    2. Generates an enterprise-grade multi-product Portal Hub at dist/index.html.
    3. Adds Cloudflare Pages (_redirects, _headers) and GitHub Pages (.nojekyll) configurations.
    4. Enforces strict zero-cost, zero-CDN performance standards.
    """

    def __init__(self, root_dir: Path = None):
        self.root_dir = root_dir or BASE_DIR
        self.isolation_mgr = NodeIsolationManager(nodes_dir=self.root_dir / "nodes")
        self.dist_dir = self.root_dir / "dist"


    def build_distribution(self) -> Dict[str, Any]:
        """Compiles all active nodes into the dist/ directory."""
        if self.dist_dir.exists():
            for item in self.dist_dir.iterdir():
                if item.name == ".git":
                    continue
                if item.is_dir():
                    shutil.rmtree(item, ignore_errors=True)
                else:
                    item.unlink(missing_ok=True)
        else:
            self.dist_dir.mkdir(parents=True)

        active_nodes = self.isolation_mgr.list_active_nodes()
        deployed_nodes: List[Dict[str, Any]] = []

        for node_id in active_nodes:
            node_path = self.isolation_mgr.get_node_path(node_id)
            public_dir = node_path / "public"

            # Destination slug (e.g. node_schemacraft_pro -> schemacraft)
            slug = node_id.replace("node_", "").replace("_pro", "").replace("_vault", "").replace("_studio", "")
            dest_dir = self.dist_dir / slug

            if public_dir.exists():
                shutil.copytree(public_dir, dest_dir, dirs_exist_ok=True)

                # Read manifest for metadata
                manifest = self.isolation_mgr.read_manifest(node_id) or {}
                meta = manifest.get("metadata", {})
                deployed_nodes.append({
                    "node_id": node_id,
                    "slug": slug,
                    "name": meta.get("name", slug.title()),
                    "category": meta.get("category", "Developer Utility"),
                    "problem": meta.get("core_problem", "High utility digital tool."),
                    "path": f"/{slug}/"
                })

        # Generate Master Portal Hub (dist/index.html)
        self._generate_portal_hub(deployed_nodes)

        # Generate Programmatic SEO Landing Pages
        programmatic_pages = self._generate_programmatic_landing_pages(deployed_nodes)

        # Generate Platform Configs
        self._generate_platform_configs(deployed_nodes)

        # Generate Production Sitemap, RSS Feed & Robots.txt
        self._generate_seo_metadata(deployed_nodes, programmatic_pages)
        self._generate_rss_feed(deployed_nodes, programmatic_pages)

        # Calculate asset stats
        total_kb = sum(f.stat().st_size for f in self.dist_dir.rglob("*.*") if f.is_file()) / 1024.0

        return {
            "status": "DEPLOYMENT_PACKAGE_BUILT",
            "dist_dir": str(self.dist_dir),
            "deployed_nodes": deployed_nodes,
            "total_assets_kb": round(total_kb, 1),
            "free_hosting_platforms": ["GitHub Pages", "Cloudflare Pages", "Vercel Hobby"],
            "generated_at": get_utc_iso()
        }

    def _generate_portal_hub(self, deployed_nodes: List[Dict[str, Any]]) -> None:
        """Generates a sleek, high-converting product directory landing page."""
        node_cards_html = ""
        for n in deployed_nodes:
            node_cards_html += f"""
        <div class="product-card">
          <div class="product-badge">{n['category']}</div>
          <h3>{n['name']}</h3>
          <p>{n['problem']}</p>
          <div class="card-action">
            <a href="./{n['slug']}/" class="launch-btn">Launch Free Tool &rarr;</a>
          </div>
        </div>
            """

        hub_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>The Digital Suite &bull; High-Performance Developer & Business Tools</title>
  <meta name="description" content="Free-to-use developer and business utilities: SEO schema generators, zero-cost cloud architecture matrices, and automated OpenGraph card engines.">
  <style>
    :root {{
      --bg: #030712;
      --card-bg: #0f172a;
      --border: #1e293b;
      --text: #f8fafc;
      --muted: #94a3b8;
      --primary: #38bdf8;
      --accent: #6366f1;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background: var(--bg);
      color: var(--text);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      line-height: 1.6;
      padding: 40px 20px;
    }}
    .container {{ max-width: 960px; margin: 0 auto; }}
    header {{ text-align: center; margin-bottom: 50px; }}
    .badge {{
      display: inline-block;
      background: rgba(56, 189, 248, 0.15);
      color: var(--primary);
      border: 1px solid rgba(56, 189, 248, 0.3);
      padding: 4px 12px;
      border-radius: 20px;
      font-size: 0.8rem;
      font-weight: 600;
      margin-bottom: 16px;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }}
    h1 {{ font-size: 2.5rem; font-weight: 800; margin-bottom: 14px; letter-spacing: -0.02em; }}
    .hero-sub {{ color: var(--muted); font-size: 1.15rem; max-width: 620px; margin: 0 auto; }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 24px;
      margin-bottom: 60px;
    }}
    .product-card {{
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 28px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: transform 0.2s ease, border-color 0.2s ease;
    }}
    .product-card:hover {{ transform: translateY(-4px); border-color: var(--primary); }}
    .product-badge {{
      font-size: 0.75rem;
      font-weight: 700;
      color: var(--primary);
      margin-bottom: 12px;
      text-transform: uppercase;
    }}
    .product-card h3 {{ font-size: 1.3rem; margin-bottom: 10px; }}
    .product-card p {{ color: var(--muted); font-size: 0.9rem; margin-bottom: 24px; flex-grow: 1; }}
    .launch-btn {{
      display: inline-block;
      width: 100%;
      text-align: center;
      background: var(--primary);
      color: #000;
      font-weight: 700;
      font-size: 0.95rem;
      padding: 12px 18px;
      border-radius: 8px;
      text-decoration: none;
      transition: background 0.2s ease;
    }}
    .launch-btn:hover {{ background: #7dd3fc; }}
    .support-box {{
      background: rgba(15, 23, 42, 0.7);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 24px;
      text-align: center;
      margin-top: 40px;
    }}
    .support-box h4 {{ margin-bottom: 8px; font-size: 1.1rem; }}
    .support-box p {{ color: var(--muted); font-size: 0.9rem; margin-bottom: 12px; }}
    .support-box a {{ color: var(--primary); font-weight: 600; text-decoration: none; }}
    footer {{ text-align: center; color: var(--muted); font-size: 0.85rem; margin-top: 60px; }}
  </style>
</head>
<body>
  <div class="container">
    <header>
      <div class="badge">100% Free Tier Compliant &bull; Instant Utility</div>
      <h1>High-Performance Micro-Tools</h1>
      <p class="hero-sub">Production-grade client-side utilities engineered for SEO, cloud cost-cutting, and social card generation. No ads, no paywalls for essential tools.</p>
    </header>

    <div class="grid">
      {node_cards_html}
    </div>

    <div class="support-box">
      <h4>Direct License Fulfillment & Custom Agency Rights</h4>
      <p>Need whitelabel rights, bulk CSV licenses, or team packs? Contact our dispatch desk directly:</p>
      <a href="mailto:businessbloke957@gmail.com">businessbloke957@gmail.com</a>
    </div>

    <footer>
      <p>&copy; 2026 Digital Suite. Verified zero-dependency architecture. All rights reserved.</p>
      <div style="margin-top: 12px; display: flex; justify-content: center; align-items: center; gap: 8px;">
        <img src="https://api.visitorbadge.io/api/visitors?path=https%3A%2F%2Fenginesuite.github.io%2FLauncher%2F&label=Total%20Hits&countColor=%232563eb&style=flat" alt="Realtime Hits Counter" loading="lazy" />
      </div>
    </footer>
  </div>
</body>
</html>
"""
        (self.dist_dir / "index.html").write_text(hub_html, encoding="utf-8")

    def _generate_platform_configs(self, deployed_nodes: List[Dict[str, Any]]) -> None:
        """Generates platform-specific hosting configuration files."""
        # 1. GitHub Pages (.nojekyll)
        (self.dist_dir / ".nojekyll").write_text("", encoding="utf-8")

        # 2. Cloudflare Pages (_headers)
        headers_content = """/*
  X-Frame-Options: SAMEORIGIN
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  Cache-Control: public, max-age=3600
"""
        (self.dist_dir / "_headers").write_text(headers_content, encoding="utf-8")

        # 3. Cloudflare Pages (_redirects)
        redirects_content = "# Cloudflare Pages Edge Redirects\n"
        for n in deployed_nodes:
            redirects_content += f"/{n['slug']}  /{n['slug']}/  301\n"
        (self.dist_dir / "_redirects").write_text(redirects_content, encoding="utf-8")

        # 4. Search Engine IndexNow Key File
        indexnow_key = "6cdf85c5687c477186f04a2e8638ead3"
        (self.dist_dir / f"{indexnow_key}.txt").write_text(indexnow_key, encoding="utf-8")

    def _generate_programmatic_landing_pages(self, deployed_nodes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Generates high-intent, long-tail programmatic SEO landing sub-pages for active tools.
        Directly targets organic searches like 'Local Business JSON-LD Generator',
        'Convert SVG to React Component', 'FAQ Schema Markup Generator', etc.
        """
        base_url = "https://enginesuite.github.io/Launcher"
        programmatic_pages = []

        # 1. SchemaCraft Programmatic Pages
        schemacraft_dir = self.dist_dir / "schemacraft"
        schemacraft_index = schemacraft_dir / "index.html"
        if schemacraft_index.exists():
            base_html = schemacraft_index.read_text(encoding="utf-8")
            adapted_html = base_html.replace('href="styles.css"', 'href="../styles.css"').replace('src="app.js"', 'src="../app.js"')

            schema_niches = [
                {
                    "slug": "local-seo",
                    "title": "Free Local Business JSON-LD Schema Generator | Google Maps Rich Snippets",
                    "desc": "Generate 100% valid LocalBusiness JSON-LD schema for dentists, restaurants, lawyers, and local shops. Boost Google Maps rankings and local SERP rich snippets.",
                    "h1": 'Generate Local Business Schema for <span class="gradient-text">Google Maps &amp; Local SEO</span>',
                    "sub": 'Create Google-compliant LocalBusiness structured data in seconds. Boost local pack visibility with zero code.',
                    "type": "LocalBusiness"
                },
                {
                    "slug": "faq-schema",
                    "title": "Free FAQ Schema Generator | Expand Google SERP Rich Snippets",
                    "desc": "Generate verified FAQPage JSON-LD schema to double your search result footprint. Expand Google SERP accordions and increase organic CTR.",
                    "h1": 'Generate FAQ Page Schema for <span class="gradient-text">Instant Google Snippets</span>',
                    "sub": 'Format FAQs into Google-recognized structured data to trigger rich accordion dropdowns on search results.',
                    "type": "FAQPage"
                },
                {
                    "slug": "product-schema",
                    "title": "Free Product Schema Markup Generator | Rich Price &amp; Star Ratings",
                    "desc": "Generate Google Product schema with prices, availability, and review ratings. Maximize e-commerce search click-through rates.",
                    "h1": 'Generate Product Schema for <span class="gradient-text">Google Search Rich Snippets</span>',
                    "sub": 'Embed verified price, stock status, and star rating schema into your product pages in seconds.',
                    "type": "Product"
                },
                {
                    "slug": "howto-schema",
                    "title": "Free How-To Schema Generator | Google Step-by-Step Rich Snippets",
                    "desc": "Generate Google HowTo schema for step-by-step guides, tutorials, and DIY instructions. Rank with image and carousel rich results.",
                    "h1": 'Generate How-To Schema for <span class="gradient-text">Step-by-Step Rich Snippets</span>',
                    "sub": 'Turn instructional guides into interactive Google step-by-step cards with zero coding.',
                    "type": "HowTo"
                }
            ]

            for niche in schema_niches:
                page_dir = schemacraft_dir / niche["slug"]
                page_dir.mkdir(parents=True, exist_ok=True)
                
                page_html = adapted_html
                page_html = re.sub(r'<title>.*?</title>', f'<title>{niche["title"]}</title>', page_html)
                page_html = re.sub(r'<meta name="description" content=".*?">', f'<meta name="description" content="{niche["desc"]}">', page_html)
                page_html = re.sub(r'<h1>.*?</h1>', f'<h1>{niche["h1"]}</h1>', page_html, flags=re.DOTALL)
                page_html = re.sub(r'<p class="hero-sub">.*?</p>', f'<p class="hero-sub">{niche["sub"]}</p>', page_html, flags=re.DOTALL)
                canonical_tag = f'<link rel="canonical" href="{base_url}/schemacraft/{niche["slug"]}/">\n</head>'
                page_html = page_html.replace('</head>', canonical_tag)
                
                inject_script = f"""
<script>
  window.addEventListener('DOMContentLoaded', function() {{
    var sel = document.getElementById('schemaType');
    if (sel) {{
      sel.value = '{niche["type"]}';
      sel.dispatchEvent(new Event('change'));
    }}
  }});
</script>
</body>"""
                page_html = page_html.replace('</body>', inject_script)
                (page_dir / "index.html").write_text(page_html, encoding="utf-8")

                programmatic_pages.append({
                    "url": f"{base_url}/schemacraft/{niche['slug']}/",
                    "title": niche["title"],
                    "priority": "0.9"
                })

        # 2. SVGCraft Programmatic Pages
        svg_dir = self.dist_dir / "svg_craft"
        svg_index = svg_dir / "index.html"
        if svg_index.exists():
            base_html = svg_index.read_text(encoding="utf-8")
            adapted_html = base_html.replace('href="styles.css"', 'href="../styles.css"').replace('src="app.js"', 'src="../app.js"')

            svg_niches = [
                {
                    "slug": "svg-to-react",
                    "title": "Convert SVG to React Component Online (Free JSX Code Exporter)",
                    "desc": "Instantly convert raw SVG code into production-ready React JSX components with zero setup. Strips junk metadata and normalizes attributes.",
                    "h1": 'Convert SVG to React Component <span class="gradient-text">Instantly in Browser</span>',
                    "sub": 'Client-side SVG to JSX code exporter. Clean attributes, viewBox scaling, and TypeScript-ready code.',
                    "active_tab": "tabReact"
                },
                {
                    "slug": "svg-to-vue",
                    "title": "Convert SVG to Vue Component Online (Free Vue 3 Template Exporter)",
                    "desc": "Instantly convert SVG code into clean Vue 3 Single File Components (SFC). Clean props, scoped styling, and lightweight payload.",
                    "h1": 'Convert SVG to Vue Component <span class="gradient-text">Instantly in Browser</span>',
                    "sub": 'Client-side SVG to Vue template generator. Ready for Vue 3 and Nuxt.js projects.',
                    "active_tab": "tabVue"
                },
                {
                    "slug": "svg-optimizer",
                    "title": "Free Online SVG Optimizer &amp; Minifier | Strip Bloat &amp; Compress",
                    "desc": "Shrink SVG file sizes by up to 70% in your browser. Strip Inkscape/Illustrator metadata, round decimal coordinates, and minify markup.",
                    "h1": 'Optimize &amp; Compress SVG Code <span class="gradient-text">Directly in Browser</span>',
                    "sub": 'High-performance SVG optimizer. Eliminate wasted bytes, clean paths, and boost website load speed.',
                    "active_tab": "tabSvg"
                }
            ]

            for niche in svg_niches:
                page_dir = svg_dir / niche["slug"]
                page_dir.mkdir(parents=True, exist_ok=True)
                page_html = adapted_html
                page_html = re.sub(r'<title>.*?</title>', f'<title>{niche["title"]}</title>', page_html)
                page_html = re.sub(r'<meta name="description" content=".*?">', f'<meta name="description" content="{niche["desc"]}">', page_html)
                page_html = re.sub(r'<h1>.*?</h1>', f'<h1>{niche["h1"]}</h1>', page_html, flags=re.DOTALL)
                page_html = re.sub(r'<p class="hero-sub">.*?</p>', f'<p class="hero-sub">{niche["sub"]}</p>', page_html, flags=re.DOTALL)
                canonical_tag = f'<link rel="canonical" href="{base_url}/svg_craft/{niche["slug"]}/">\n</head>'
                page_html = page_html.replace('</head>', canonical_tag)

                inject_script = f"""
<script>
  window.addEventListener('DOMContentLoaded', function() {{
    var tab = document.getElementById('{niche["active_tab"]}');
    if (tab) tab.click();
  }});
</script>
</body>"""
                page_html = page_html.replace('</body>', inject_script)
                (page_dir / "index.html").write_text(page_html, encoding="utf-8")

                programmatic_pages.append({
                    "url": f"{base_url}/svg_craft/{niche['slug']}/",
                    "title": niche["title"],
                    "priority": "0.9"
                })

        return programmatic_pages

    def _generate_rss_feed(self, deployed_nodes: List[Dict[str, Any]], programmatic_pages: List[Dict[str, Any]] = None) -> None:
        """Generates RSS 2.0 XML feed for aggregators, RSS subscribers, and search bots."""
        base_url = "https://enginesuite.github.io/Launcher"
        build_date = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S +0000")
        items_xml = []
        for n in deployed_nodes:
            items_xml.append(f"""    <item>
      <title>{n['name']} - {n['category']}</title>
      <link>{base_url}/{n['slug']}/</link>
      <guid>{base_url}/{n['slug']}/</guid>
      <description>{n['problem']}</description>
      <pubDate>{build_date}</pubDate>
    </item>""")
        if programmatic_pages:
            for p in programmatic_pages:
                items_xml.append(f"""    <item>
      <title>{p['title']}</title>
      <link>{p['url']}</link>
      <guid>{p['url']}</guid>
      <description>{p['title']} - 100% free client-side browser utility.</description>
      <pubDate>{build_date}</pubDate>
    </item>""")
        rss_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>EngineSuite - Free Developer Utilities &amp; Cloud Tools</title>
    <link>{base_url}/</link>
    <description>Free high-performance developer utilities for SEO, SVGs, and cloud architectures.</description>
    <language>en-us</language>
    <lastBuildDate>{build_date}</lastBuildDate>
    <atom:link href="{base_url}/feed.xml" rel="self" type="application/rss+xml"/>
{chr(10).join(items_xml)}
  </channel>
</rss>
"""
        (self.dist_dir / "feed.xml").write_text(rss_xml, encoding="utf-8")

    def _generate_seo_metadata(self, deployed_nodes: List[Dict[str, Any]], programmatic_pages: List[Dict[str, Any]] = None) -> None:
        """Generates production sitemap.xml and robots.txt for search engines."""
        base_url = "https://enginesuite.github.io/Launcher"
        today = get_utc_iso()[:10]

        sitemap_entries = [
            f"""  <url>
    <loc>{base_url}/</loc>
    <lastmod>{today}</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>"""
        ]

        for n in deployed_nodes:
            sitemap_entries.append(
                f"""  <url>
    <loc>{base_url}/{n['slug']}/</loc>
    <lastmod>{today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>"""
            )

        if programmatic_pages:
            for p in programmatic_pages:
                sitemap_entries.append(
                    f"""  <url>
    <loc>{p['url']}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>{p.get('priority', '0.9')}</priority>
  </url>"""
                )

        sitemap_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(sitemap_entries)}
</urlset>
"""
        (self.dist_dir / "sitemap.xml").write_text(sitemap_xml, encoding="utf-8")

        robots_txt = f"""User-agent: *
Allow: /
Sitemap: {base_url}/sitemap.xml
"""
        (self.dist_dir / "robots.txt").write_text(robots_txt, encoding="utf-8")

