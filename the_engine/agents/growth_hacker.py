"""
The Engine - The Growth Hacker (Marketing & Traffic Agent)
Executes programmatic SEO generation, automates zero-cost social distribution,
and orchestrates multi-channel outreach campaigns.
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime

from the_engine.agents.base import BaseAgent
from the_engine.core.hitl import HITLGatekeeper
from the_engine.config import get_utc_iso

logger = logging.getLogger("TheEngine.GrowthHacker")


class GrowthHackerAgent(BaseAgent):
    def __init__(self, hitl_gatekeeper: HITLGatekeeper):
        super().__init__(
            name="The Growth Hacker",
            role="Marketing, Traffic & Distribution",
            hitl_gatekeeper=hitl_gatekeeper
        )

    def deploy_growth_campaign(self, node_path: Path, node_metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        Deploys programmatic SEO, social copy, and directory submission packages for the node.
        """
        dist_dir = node_path / "distribution"
        dist_dir.mkdir(exist_ok=True)

        node_id = node_metadata.get("niche_id") or node_path.name
        slug = node_id.replace("node_", "").replace("_pro", "").replace("_vault", "").replace("_studio", "")
        live_url = f"https://enginesuite.github.io/Launcher/{slug}/"

        seo_assets = self._generate_programmatic_seo(dist_dir, node_metadata, live_url)
        social_assets = self._generate_social_campaigns(dist_dir, node_metadata, live_url)
        directory_assets = self._generate_directory_submissions(dist_dir, node_metadata, live_url)

        # Generate human-readable & automatable Markdown Launch Kit
        self._generate_launch_kit_markdown(dist_dir, node_metadata, live_url, social_assets, directory_assets)

        campaign_manifest = {
            "node_id": node_id,
            "slug": slug,
            "live_url": live_url,
            "status": "CAMPAIGN_READY",
            "generated_at": get_utc_iso(),
            "seo_pages_count": len(seo_assets.get("pages", [])),
            "distribution_channels": ["Google Organic (Programmatic SEO)", "X / Twitter", "Reddit", "Dev.to / Hashnode", "Dev Directories"],
            "total_spend": 0.00  # Strictly $0 upfront
        }

        with open(dist_dir / "campaign_manifest.json", "w", encoding="utf-8") as f:
            json.dump(campaign_manifest, f, indent=2)

        return campaign_manifest

    def _generate_programmatic_seo(self, dist_dir: Path, meta: Dict[str, Any], live_url: str) -> Dict[str, Any]:
        """Generates target keyword clusters and programmatic landing page configurations."""
        name = meta.get("name", "Developer Utility")
        category = meta.get("category", "Developer Tool")

        niches = [
            {"slug": f"free-online-{meta.get('niche_id', 'tool')}", "title": f"100% Free Online {name}", "volume": "High", "intent": "Transactional"},
            {"slug": f"best-{meta.get('niche_id', 'tool')}-2026", "title": f"Top Free {name} for Developers (2026)", "volume": "High", "intent": "Commercial"},
            {"slug": f"agency-{meta.get('niche_id', 'tool')}", "title": f"Agency & High-Volume {name} Solution", "volume": "Medium", "intent": "Transactional"},
            {"slug": f"how-to-use-{meta.get('niche_id', 'tool')}", "title": f"Complete Guide to {name}", "volume": "High", "intent": "Informational"}
        ]

        seo_data = {
            "primary_keywords": [
                f"free {name.lower()}",
                f"{name.lower()} online",
                f"best {category.lower()} 2026",
                f"zero cost {category.lower()}"
            ],
            "long_tail_clusters": niches,
            "robots_txt": f"User-agent: *\nAllow: /\nSitemap: {live_url}sitemap.xml",
            "pages": niches
        }

        with open(dist_dir / "seo_strategy.json", "w", encoding="utf-8") as f:
            json.dump(seo_data, f, indent=2)

        with open(dist_dir / "robots.txt", "w", encoding="utf-8") as f:
            f.write("User-agent: *\nAllow: /\n")

        return seo_data

    def _generate_social_campaigns(self, dist_dir: Path, meta: Dict[str, Any], live_url: str) -> Dict[str, Any]:
        """Generates high-converting, value-first launch content for social channels."""
        name = meta.get("name", "Developer Utility")
        problem = meta.get("core_problem", "Tedious manual workflows and expensive SaaS tools.")
        pro_price = meta.get("monetization", {}).get("pro_tier", "$19 one-time")

        social_campaigns = {
            "twitter_x_launch_thread": [
                f"🧵 Developers & Creators: Stop paying monthly subscriptions for basic {name}.\n\n{problem}\n\nI built a 100% free, client-side utility that solves this instantly in your browser.\n\nZero ads. Zero logins. Pure utility 👇",
                f"1/ Why this exists:\nMost alternatives force you into accounts, collect your data, or gate essential features behind $29/mo plans.\n\nThis runs entirely in your browser with zero server overhead — meaning sub-50ms speed and total data privacy.",
                f"2/ Try the free tool live right now:\n🔗 {live_url}\n\nFor power users and teams who need batch exports and agency commercial rights, the Pro Pack is available for just {pro_price} lifetime."
            ],
            "indie_hackers_post": {
                "title": f"I built {name} with $0 upfront infrastructure — Live on GitHub Pages",
                "body": f"Hey IH! I was tired of bloated, subscription-gated tools for {name}. I engineered a lightweight, zero-dependency browser tool hosted 100% free on GitHub Pages.\n\nLive tool: {live_url}\n\nWould love your feedback on the UX and conversion flow!"
            },
            "reddit_value_post": {
                "subreddit": "r/webdev",
                "title": f"Free Tool: {name} (No signups, client-side, zero tracking)",
                "content": f"Hey everyone, built a lightweight, privacy-first tool for {name}. Runs 100% client-side in the browser, no ads or tracking scripts.\n\nLink: {live_url}\n\nHope this saves you time in your projects! Any feature requests, drop them below."
            },
            "dev_to_article": {
                "title": f"How to Solve {name} Without Paying Monthly SaaS Fees",
                "tags": ["webdev", "javascript", "productivity", "opensource"],
                "markdown_body": f"""# Solving {name} Without Monthly Subscriptions

{problem}

Instead of paying recurring SaaS fees, you can use client-side browser capabilities to get this done in seconds.

## Live Free Tool
Check out the free tool here: [{name}]({live_url})

### Key Benefits:
- ⚡ Sub-50ms cold start
- 🔒 100% client-side privacy (no data leaves your machine)
- 💰 Zero upfront cost or subscription lock-in
"""
            }
        }

        with open(dist_dir / "social_campaigns.json", "w", encoding="utf-8") as f:
            json.dump(social_campaigns, f, indent=2)

        return social_campaigns

    def _generate_directory_submissions(self, dist_dir: Path, meta: Dict[str, Any], live_url: str) -> Dict[str, Any]:
        """Generates submission packages for free startup and tool directories."""
        name = meta.get("name", "Developer Utility")
        category = meta.get("category", "Developer Utilities")
        problem = meta.get("core_problem", "Solves developer workflows quickly.")

        submissions = {
            "directories": [
                {"name": "Toolify.ai", "category": category, "free_submission": True, "url": live_url},
                {"name": "ProductHunt", "pricing_model": "Free + Pro Upgrade", "free_submission": True, "url": live_url},
                {"name": "AlternativeTo.net", "target_alternative": "Commercial Alternatives", "free_submission": True, "url": live_url},
                {"name": "LaunchingNext", "category": category, "free_submission": True, "url": live_url},
                {"name": "BetaList", "category": "Early Access Tools", "free_submission": True, "url": live_url},
                {"name": "MicroLaunch", "category": "Indie Tools", "free_submission": True, "url": live_url},
                {"name": "SaaSHub", "category": category, "free_submission": True, "url": live_url},
                {"name": "DevHunt", "category": "Dev Tools", "free_submission": True, "url": live_url}
            ],
            "product_name": name,
            "live_url": live_url,
            "tagline": f"Instant, client-side {name} with zero subscription fees.",
            "description": f"{name} is a high-speed, zero-dependency browser utility designed to eliminate {problem}. Features instant export, clean responsive interface, and optional agency commercial pack."
        }

        with open(dist_dir / "directory_submissions.json", "w", encoding="utf-8") as f:
            json.dump(submissions, f, indent=2)

        return submissions

    def _generate_launch_kit_markdown(
        self,
        dist_dir: Path,
        meta: Dict[str, Any],
        live_url: str,
        social: Dict[str, Any],
        directory: Dict[str, Any]
    ) -> None:
        """Writes a unified, copy-paste ready LAUNCH_KIT.md document."""
        tw_thread = "\n\n---\n\n".join(social.get("twitter_x_launch_thread", []))
        reddit = social.get("reddit_value_post", {})
        ih = social.get("indie_hackers_post", {})
        devto = social.get("dev_to_article", {})

        content = f"""# 🚀 DISTRIBUTION & LAUNCH KIT: {meta.get('name', 'Digital Tool')}
**Live Production URL:** [{live_url}]({live_url})  
**Target Category:** {meta.get('category', 'Utility')}  
**Zero-Cost Policy:** $0 Upfront Spend  

---

## 1. 🧵 X / Twitter Launch Thread
Copy and publish as a scheduled or manual thread:

{tw_thread}

---

## 2. 💬 Reddit Value Post ({reddit.get('subreddit', 'r/webdev')})
**Title:** {reddit.get('title', '')}

**Body:**
```markdown
{reddit.get('content', '')}
```

---

## 3. 💡 Indie Hackers Show IH Post
**Title:** {ih.get('title', '')}

**Body:**
{ih.get('body', '')}

---

## 4. 📝 Dev.to / Hashnode Article
**Title:** {devto.get('title', '')}  
**Tags:** {', '.join(devto.get('tags', []))}

```markdown
{devto.get('markdown_body', '')}
```

---

## 5. 🌐 Free Directory Submission Metadata
- **Product Name:** {directory.get('product_name', '')}
- **Website:** {live_url}
- **Tagline:** {directory.get('tagline', '')}
- **Description:** {directory.get('description', '')}
- **Directories to Submit:**
"""
        for d in directory.get("directories", []):
            cat = d.get('category') or d.get('pricing_model') or 'Developer Tool'
            content += f"  - [ ] **{d['name']}** ({cat})\n"

        (dist_dir / "LAUNCH_KIT.md").write_text(content, encoding="utf-8")

    def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Executes Phase 3: Monetize & Drive Traffic."""
        node_path_str = context.get("workspace_path")
        if not node_path_str:
            raise ValueError("Growth Hacker requires workspace_path in context.")

        node_path = Path(node_path_str)
        manifest_file = node_path / "manifest.json"
        metadata = {}
        if manifest_file.exists():
            with open(manifest_file, "r", encoding="utf-8") as f:
                metadata = json.load(f).get("metadata", {})

        result = self.execute_with_self_correction(
            node_id=node_path.name,
            task_name="deploy_growth_campaign",
            task_fn=self.deploy_growth_campaign,
            node_path=node_path,
            node_metadata=metadata
        )
        return {
            "status": "TRAFFIC_DISTRIBUTION_READY",
            "campaign": result,
            "timestamp": get_utc_iso()
        }

