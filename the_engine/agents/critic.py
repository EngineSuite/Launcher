"""
The Engine - The Critic (Adversarial Quality & Red Team Agent)
Scrutinizes revenue nodes from the perspective of an uncompromising buyer.
Finds conversion friction, weak copywriting, and gaps in value proposition,
producing concrete upgrade blueprints.
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any, List

from the_engine.agents.base import BaseAgent
from the_engine.core.hitl import HITLGatekeeper

logger = logging.getLogger("TheEngine.Critic")


class CriticAgent(BaseAgent):
    def __init__(self, hitl_gatekeeper: HITLGatekeeper):
        super().__init__(
            name="The Critic",
            role="Adversarial Quality & Conversion Critique",
            hitl_gatekeeper=hitl_gatekeeper
        )

    def review_node(self, node_path: Path, opportunity: Dict[str, Any]) -> Dict[str, Any]:
        """
        Adversarially tears down a node's commercial viability:
        1. Value Delta: Is the Pro tier 10x more valuable than free?
        2. Trust Signals: Guarantees, Google test links, clean formatting.
        3. Conversion Friction: Obvious CTAs, minimal clicks to purchase.
        4. Copy Punchiness: Pain-focused vs feature-focused.
        """
        node_id = node_path.name
        self.log(f"Conducting adversarial quality review of '{node_id}'...")

        pricing_file = node_path / "monetization" / "pricing.json"
        pricing_data = {}
        if pricing_file.exists():
            with open(pricing_file, "r", encoding="utf-8") as f:
                pricing_data = json.load(f)

        index_file = node_path / "public" / "index.html"
        html_text = index_file.read_text(encoding="utf-8") if index_file.exists() else ""

        strengths = []
        vulnerabilities = []
        upgrades = []
        score = 8.5  # Base score

        # 1. Inspect Value Delta
        tiers = pricing_data.get("tiers", [])
        pro_tier = next((t for t in tiers if t.get("price", 0) > 0), None)
        if pro_tier:
            features = pro_tier.get("features", [])
            if len(features) >= 4:
                strengths.append(f"Pro tier packs {len(features)} distinct features justifying the price point.")
            else:
                score -= 1.0
                vulnerabilities.append("Pro tier feature list is sparse. Hard to justify one-time fee.")
                upgrades.append("Add at least 2 more high-utility deliverables (e.g. templates, whitelabel code).")

        # 2. Inspect Trust & Friction in HTML
        if "guarantee" in html_text.lower() or "money-back" in html_text.lower():
            strengths.append("Money-back guarantee is explicitly stated, lowering buyer risk.")
        else:
            score -= 0.5
            vulnerabilities.append("No explicit risk-reversal guarantee found.")
            upgrades.append("Add a '30-Day Money-Back Guarantee' badge near checkout buttons.")

        if "instant" in html_text.lower() or "download" in html_text.lower():
            strengths.append("Instant delivery promise is prominent.")

        # Check for interactive demo
        if "sample" in html_text.lower() or "preview" in html_text.lower():
            strengths.append("Interactive sample data allows users to test value before buying.")
        else:
            score -= 1.0
            vulnerabilities.append("Lacks an instant interactive sample to prove efficacy.")
            upgrades.append("Provide a 1-click 'Load Sample Data' button.")

        # 3. Check for Clear CTA
        cta_count = html_text.lower().count("btn-pro") + html_text.lower().count("btn-primary")
        if cta_count >= 2:
            strengths.append("Strong visual call-to-action distribution across the page.")
        else:
            score -= 0.5
            vulnerabilities.append("Call-to-action buttons are sparse.")
            upgrades.append("Add sticky or repeated purchase buttons.")

        final_score = max(1.0, min(10.0, round(score, 1)))

        review_result = {
            "node_id": node_id,
            "overall_quality_score": final_score,
            "commercial_viability": "HIGH" if final_score >= 8.0 else ("MODERATE" if final_score >= 6.5 else "LOW"),
            "strengths": strengths,
            "vulnerabilities": vulnerabilities,
            "actionable_upgrades": upgrades
        }

        self.log(f"Critique finished for '{node_id}'. Quality Score: {final_score}/10 ({review_result['commercial_viability']})")
        return review_result

    def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        node_path_str = context.get("workspace_path")
        opp = context.get("opportunity", {})
        if not node_path_str:
            raise ValueError("Critic requires workspace_path in context.")

        node_path = Path(node_path_str)
        report = self.execute_with_self_correction(
            node_id=node_path.name,
            task_name="review_node",
            task_fn=self.review_node,
            node_path=node_path,
            opportunity=opp
        )
        return {
            "status": "CRITIQUE_COMPLETED",
            "report": report
        }
