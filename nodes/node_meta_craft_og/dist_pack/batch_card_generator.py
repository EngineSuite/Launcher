#!/usr/bin/env python3
"""
MetaCraft OG - Automated Headless SVG/HTML Social Card Batch Generator
Generates high-resolution social card assets from a CSV spreadsheet.
Zero external pip dependencies required.
"""

import csv
import sys
from pathlib import Path


def generate_svg_card(title: str, subtitle: str, tag: str, author: str) -> str:
    """Generates a standards-compliant SVG OpenGraph card (1200x630)."""
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
