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

        seo_assets = self._generate_programmatic_seo(dist_dir, node_metadata)
        social_assets = self._generate_social_campaigns(dist_dir, node_metadata)
        directory_assets = self._generate_directory_submissions(dist_dir, node_metadata)

        campaign_manifest = {
            "node_id": node_metadata.get("niche_id", "unknown"),
            "status": "CAMPAIGN_READY",
            "generated_at": get_utc_iso(),
            "seo_pages_count": len(seo_assets.get("pages", [])),
            "distribution_channels": ["Google Organic (Programmatic SEO)", "X / Twitter", "Indie Hackers", "Reddit r/SEO", "Dev Directories"],
            "total_spend": 0.00  # Strictly $0 upfront
        }

        with open(dist_dir / "campaign_manifest.json", "w", encoding="utf-8") as f:
            json.dump(campaign_manifest, f, indent=2)

        return campaign_manifest

    def _generate_programmatic_seo(self, dist_dir: Path, meta: Dict[str, Any]) -> Dict[str, Any]:
        """Generates target keyword clusters and programmatic landing page configurations."""
        niches = [
            {"slug": "schema-generator-for-dentists", "title": "JSON-LD Schema Generator for Dentists & Dental Clinics", "volume": "High", "intent": "Transactional"},
            {"slug": "schema-generator-for-lawyers", "title": "Legal Service & Attorney Schema Markup Generator", "volume": "High", "intent": "Transactional"},
            {"slug": "local-business-schema-multiple-locations", "title": "Multi-Location Local SEO Schema Generator for Agencies", "volume": "Very High", "intent": "Commercial"},
            {"slug": "faq-schema-generator-google-rich-snippets", "title": "Instant FAQPage JSON-LD Schema Generator", "volume": "High", "intent": "Informational"},
            {"slug": "shopify-product-schema-generator", "title": "Shopify E-Commerce JSON-LD Product & Review Generator", "volume": "High", "intent": "Transactional"},
            {"slug": "saas-organization-schema-generator", "title": "Software & SaaS Organization Schema Builder", "volume": "Medium", "intent": "Commercial"}
        ]

        seo_data = {
            "primary_keywords": [
                "free json ld schema generator",
                "google rich snippets generator 2026",
                "local business structured data generator",
                "schema org bulk generator"
            ],
            "long_tail_clusters": niches,
            "robots_txt": "User-agent: *\\nAllow: /\\nSitemap: https://schemacraft.pages.dev/sitemap.xml",
            "pages": niches
        }

        with open(dist_dir / "seo_strategy.json", "w", encoding="utf-8") as f:
            json.dump(seo_data, f, indent=2)

        # Generate robots.txt
        with open(dist_dir / "robots.txt", "w", encoding="utf-8") as f:
            f.write("User-agent: *\nAllow: /\n")

        return seo_data

    def _generate_social_campaigns(self, dist_dir: Path, meta: Dict[str, Any]) -> Dict[str, Any]:
        """Generates high-converting, value-first launch content for social channels."""
        social_campaigns = {
            "twitter_x_launch_thread": [
                "🧵 Stop paying $49/mo just to generate Google JSON-LD schema for client websites.\n\nI built a 100% free, instant Schema generator that validates rich snippets in real-time.\n\nNo sign-up. No credit card. Zero ads.\n\nHere's how to use it to boost your Google CTR by 30% 👇",
                "1/ Google search rankings prioritize structured data. If you don't have JSON-LD on your site, you are leaving click-through rates on the table.\n\nSchemaCraft Pro supports LocalBusiness, Organization, FAQ, Products, and How-To schemas instantly.",
                "2/ Try the free generator right now: https://schemacraft.pages.dev\n\nFor digital agencies managing 50+ locations, the Agency Pro pack lets you bulk export via CSV for just $19 lifetime."
            ],
            "indie_hackers_post": {
                "title": "I built an agency-grade JSON-LD Schema Generator with $0 upfront infrastructure",
                "body": "Hey IH! SEO tools have gotten bloated and overpriced. I wanted a lightning-fast utility to generate bulletproof Schema.org markup with zero friction. Built this on a modern zero-cost static stack. Would love your feedback!"
            },
            "reddit_value_post": {
                "subreddit": "r/SEO",
                "title": "Free Tool: Instant JSON-LD Schema Generator with Real-Time Rich Results Validation",
                "content": "Hey r/SEO, created a clean, fast schema generator that outputs 100% valid schema for Google rich results. Free for everyone, hope it helps your workflows!"
            }
        }

        with open(dist_dir / "social_campaigns.json", "w", encoding="utf-8") as f:
            json.dump(social_campaigns, f, indent=2)

        return social_campaigns

    def _generate_directory_submissions(self, dist_dir: Path, meta: Dict[str, Any]) -> Dict[str, Any]:
        """Generates submission packages for free startup and tool directories."""
        submissions = {
            "directories": [
                {"name": "Toolify.ai", "category": "SEO & Marketing", "free_submission": True},
                {"name": "AlternativeTo.net", "target_alternative": "Merkle Schema Generator", "free_submission": True},
                {"name": "ProductHunt", "pricing_model": "Free + Paid Pro Upgrade", "free_submission": True},
                {"name": "SaaSHub", "category": "Developer Utilities", "free_submission": True},
                {"name": "DevHunt", "category": "Dev Tools", "free_submission": True}
            ],
            "tagline": "The fastest JSON-LD schema builder for rich snippets and local SEO.",
            "description": "Generate, test, and export 100% Google-compliant Schema.org markup in seconds. Features 8+ core schemas, real-time live preview, and bulk CSV export."
        }

        with open(dist_dir / "directory_submissions.json", "w", encoding="utf-8") as f:
            json.dump(submissions, f, indent=2)

        return submissions

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
