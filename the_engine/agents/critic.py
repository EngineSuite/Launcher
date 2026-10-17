"""
The Engine - The Critic (Adversarial Quality & Red Team Agent)
Powered by the 10-Agent Critique Council.
Scrutinizes revenue nodes and the engine framework across 10 specialized dimensions,
conducting autonomous inter-agent cross-examination and debate.
"""

from pathlib import Path
from typing import Dict, Any, Optional

from the_engine.agents.base import BaseAgent
from the_engine.core.hitl import HITLGatekeeper
from the_engine.core.event_bus import EventBus
from the_engine.critics.council import CritiqueCouncil


class CriticAgent(BaseAgent):
    """
    CriticAgent coordinates the 10-Agent Critique Council:
    1. The Ergonomist (UX & Usability)
    2. The Monetizer (Conversion & Pricing Economics)
    3. The Penetration Tester (Security & Data Integrity)
    4. The Wordsmith (Persuasive Copywriting & Clarity)
    5. The Algorithmic Auditor (Technical SEO & Discoverability)
    6. The Latency Hunter (Performance & Web Vitals)
    7. The Legal Counsel (Compliance & Risk Armor)
    8. The Systems Architect (Code Quality & Modular Architecture)
    9. The Meta-Critic (Agent Orchestration & Pipeline Inspector)
    10. The Chief Risk Officer (Financial Governance & Safe Reserve Risk)
    """

    def __init__(self, hitl_gatekeeper: HITLGatekeeper, event_bus: Optional[EventBus] = None):
        super().__init__(
            name="The Critic",
            role="10-Agent Red-Team Critique Council",
            hitl_gatekeeper=hitl_gatekeeper
        )
        self.council = CritiqueCouncil(hitl_gatekeeper=hitl_gatekeeper, event_bus=event_bus)

    def review_node(
        self,
        node_path: Path,
        opportunity: Dict[str, Any],
        engine_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Convenes the 10-Agent Critique Council to adversarially evaluate the node and engine.
        """
        node_id = node_path.name
        self.log(f"Convening 10-Agent Critique Council for '{node_id}'...")

        decree = self.council.convene_council(
            node_path=node_path,
            opportunity=opportunity,
            engine_context=engine_context
        )

        final_score = decree["consensus_score"]
        viability = "HIGH" if final_score >= 8.0 else ("MODERATE" if final_score >= 7.0 else "LOW")

        # Map high-priority objections to vulnerabilities
        vulnerabilities = []
        for critic_name, asm in decree["critic_breakdown"].items():
            for obj in asm.get("objections", []):
                if obj["severity"] in ["CRITICAL", "HIGH"]:
                    vulnerabilities.append(f"[{obj['severity']}] {critic_name}: {obj['issue']}")

        review_result = {
            "node_id": node_id,
            "overall_quality_score": final_score,
            "commercial_viability": viability,
            "council_verdict": decree["council_verdict"],
            "council_status": decree["council_status"],
            "strengths": decree["top_strengths"],
            "vulnerabilities": vulnerabilities,
            "actionable_upgrades": decree["prioritized_action_directives"],
            "autonomous_debates": decree["autonomous_debates"],
            "council_decree": decree
        }

        self.log(f"Council deliberation complete. Consensus Score: {final_score}/10 ({decree['council_verdict']})")
        return review_result

    def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        node_path_str = context.get("workspace_path")
        opp = context.get("opportunity", {})
        engine_ctx = context.get("engine_context", {})
        if not node_path_str:
            raise ValueError("Critic requires workspace_path in context.")

        node_path = Path(node_path_str)
        report = self.execute_with_self_correction(
            node_id=node_path.name,
            task_name="review_node",
            task_fn=self.review_node,
            node_path=node_path,
            opportunity=opp,
            engine_context=engine_ctx
        )
        return {
            "status": "CRITIQUE_COUNCIL_DELIBERATION_COMPLETED",
            "report": report
        }
