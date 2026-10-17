"""
The Engine - The Strategist (Deep Thinker & Executive Decision Agent)
Synthesizes market intelligence (Scout), functional test proof (Tester),
and adversarial critique (Critic) to make authoritative GO / NO-GO decisions.
"""

import logging
from typing import Dict, Any, List

from the_engine.agents.base import BaseAgent
from the_engine.core.hitl import HITLGatekeeper

logger = logging.getLogger("TheEngine.Strategist")


class StrategistAgent(BaseAgent):
    def __init__(self, hitl_gatekeeper: HITLGatekeeper):
        super().__init__(
            name="The Strategist",
            role="Deep Reasoning & Executive Launch Authority",
            hitl_gatekeeper=hitl_gatekeeper
        )

    def evaluate_and_decide(
        self,
        opportunity: Dict[str, Any],
        test_report: Dict[str, Any],
        critique_report: Dict[str, Any],
        editor_report: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Synthesizes technical, commercial, content, and strategic dimensions:
        - Must achieve >= 90% functional test pass rate.
        - Must achieve >= 7.5/10 commercial critique score.
        - Must achieve >= 8.0/10 content hygiene score with zero leaks (The Editor).
        - Must enforce strict zero-upfront-cost architecture.
        """
        node_id = test_report.get("node_id", "unknown")
        pass_rate = test_report.get("pass_rate", 0.0)
        grade = test_report.get("grade", "F")
        critique_score = critique_report.get("overall_quality_score", 0.0)
        viability = critique_report.get("commercial_viability", "LOW")

        self.log(f"Synthesizing launch readiness for '{node_id}'...")
        self.log(f"  • Tester Pass Rate   : {pass_rate}% (Grade {grade})")
        self.log(f"  • Critic Score       : {critique_score}/10 ({viability})")
        if editor_report:
            self.log(f"  • Editor Quality     : {editor_report.get('content_quality_score', 0)}/10 (Leaks: {editor_report.get('leaks_found', 0)})")

        decision = "APPROVED_FOR_LAUNCH"
        rationale = []
        action_directives = []

        # Gate 1: Strict Functional Reliability
        if pass_rate < 90.0:
            decision = "REQUIRES_REFINEMENT"
            rationale.append(f"Functional reliability ({pass_rate}%) is below minimum standard (90.0%).")
            for defect in test_report.get("defects", []):
                action_directives.append(f"Fix QA defect: {defect['check']} - {defect['error']}")

        # Gate 2: Commercial Quality & Value Delta
        if critique_score < 7.5:
            if decision == "APPROVED_FOR_LAUNCH":
                decision = "REQUIRES_REFINEMENT"
            rationale.append(f"Commercial critique score ({critique_score}/10) indicates weak buyer incentive.")
            for upgrade in critique_report.get("actionable_upgrades", []):
                action_directives.append(f"Apply commercial upgrade: {upgrade}")

        # Gate 3: Content Hygiene & Brand Presentation (The Editor)
        if editor_report:
            editor_score = editor_report.get("content_quality_score", 10.0)
            leaks = editor_report.get("leaks_found", 0)
            if editor_score < 8.0 or leaks > 0:
                if decision == "APPROVED_FOR_LAUNCH":
                    decision = "REQUIRES_REFINEMENT"
                rationale.append(f"Content quality score ({editor_score}/10) with {leaks} detected leak(s).")
                for rec in editor_report.get("recommendations", []):
                    action_directives.append(f"Content Edit: {rec.get('action')} {rec.get('item')} - {rec.get('reason')}")
            else:
                rationale.append(f"Content hygiene verified by The Editor ({editor_score}/10). Zero leaks detected.")

        # Gate 4: High-Confidence Approval
        if decision == "APPROVED_FOR_LAUNCH":
            rationale.append("All technical, deliverable, content, and commercial requirements fully satisfied.")
            rationale.append(f"Pass rate ({pass_rate}%) and critique score ({critique_score}/10) meet launch criteria.")

        verdict = {
            "node_id": node_id,
            "executive_decision": decision,
            "status": "APPROVED" if decision == "APPROVED_FOR_LAUNCH" else "REJECTED_FOR_REFINEMENT",
            "qa_grade": grade,
            "qa_pass_rate": pass_rate,
            "critique_score": critique_score,
            "editor_score": editor_report.get("content_quality_score") if editor_report else None,
            "rationale": rationale,
            "action_directives": action_directives,
            "market_confidence": "HIGH" if (pass_rate >= 95 and critique_score >= 8.5) else "MODERATE"
        }

        self.log(f"EXECUTIVE VERDICT for '{node_id}': {decision} (Confidence: {verdict['market_confidence']})")
        return verdict

    def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        opp = context.get("opportunity", {})
        test_report = context.get("test_report", {})
        critique_report = context.get("critique_report", {})
        editor_report = context.get("editor_report")

        verdict = self.execute_with_self_correction(
            node_id=test_report.get("node_id", "unknown"),
            task_name="evaluate_and_decide",
            task_fn=self.evaluate_and_decide,
            opportunity=opp,
            test_report=test_report,
            critique_report=critique_report,
            editor_report=editor_report
        )
        return {
            "status": "STRATEGIC_DECISION_FINALIZED",
            "verdict": verdict
        }
