"""
The Engine - The Critique Council (Autonomous Adversarial Board)
Orchestrates 10 specialized Red-Team Critique Agents:
1. Conducts independent multi-dimensional scrutiny.
2. Coordinates autonomous inter-agent cross-examination and debate.
3. Synthesizes consensus voting into a binding Council Decision Decree.
"""

from pathlib import Path
from typing import Dict, Any, List, Optional
import logging

from the_engine.core.event_bus import EventBus
from the_engine.core.hitl import HITLGatekeeper
from the_engine.config import get_utc_iso
from the_engine.critics.critics_impl import (
    UXCritic,
    ConversionCritic,
    SecurityCritic,
    CopywritingCritic,
    SEOCritic,
    PerformanceCritic,
    LegalCritic,
    ArchitectureCritic,
    PipelineCritic,
    FinancialCritic
)

logger = logging.getLogger("TheEngine.CritiqueCouncil")


class CritiqueCouncil:
    """
    The 10-Agent Autonomous Critique Council:
    - 10 specialized agents review every asset from their own adversarial lens.
    - Agents cross-examine and debate each other's objections via EventBus.
    - Produces a unified Consensus Decree with prioritized actionable directives.
    """

    def __init__(self, hitl_gatekeeper: HITLGatekeeper, event_bus: Optional[EventBus] = None):
        self.hitl = hitl_gatekeeper
        self.event_bus = event_bus or EventBus()

        # Instantiate all 10 specialized critics
        self.critics = [
            UXCritic(event_bus=self.event_bus),
            ConversionCritic(event_bus=self.event_bus),
            SecurityCritic(event_bus=self.event_bus),
            CopywritingCritic(event_bus=self.event_bus),
            SEOCritic(event_bus=self.event_bus),
            PerformanceCritic(event_bus=self.event_bus),
            LegalCritic(event_bus=self.event_bus),
            ArchitectureCritic(event_bus=self.event_bus),
            PipelineCritic(event_bus=self.event_bus),
            FinancialCritic(event_bus=self.event_bus)
        ]

    def convene_council(
        self,
        node_path: Path,
        opportunity: Dict[str, Any],
        engine_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Executes the full 3-Stage Autonomous Deliberation Protocol:
        Stage 1: Independent Multi-Domain Scrutiny
        Stage 2: Inter-Agent Cross-Examination & Autonomous Debate
        Stage 3: Consensus Voting & Strategic Decree
        """
        node_id = node_path.name
        engine_ctx = engine_context or {}
        engine_ctx["hitl_gatekeeper"] = self.hitl
        engine_ctx["event_bus"] = self.event_bus

        logger.info(f"Convening 10-Agent Critique Council for '{node_id}'...")

        # ----------------------------------------------------------------------
        # Stage 1: Independent Multi-Domain Scrutiny
        # ----------------------------------------------------------------------
        assessments: Dict[str, Any] = {}
        all_objections = []
        all_strengths = []

        for critic in self.critics:
            assessment = critic.evaluate(node_path, opportunity, engine_ctx)
            assessments[critic.name] = assessment
            all_objections.extend(assessment.objections)
            all_strengths.extend(assessment.strengths)

            # Broadcast finding to event bus
            self.event_bus.publish(
                topic="council:critic_evaluated",
                sender=critic.name,
                payload={
                    "node_id": node_id,
                    "domain": critic.domain,
                    "score": assessment.score,
                    "objection_count": len(assessment.objections)
                }
            )

        # ----------------------------------------------------------------------
        # Stage 2: Autonomous Inter-Agent Cross-Examination & Debate
        # ----------------------------------------------------------------------
        debates: List[Dict[str, Any]] = []
        for critic in self.critics:
            rebuttals = critic.cross_examine(assessments, node_path, engine_ctx)
            for reb in rebuttals:
                debates.append(reb)
                self.event_bus.publish(
                    topic="council:debate_argument",
                    sender=critic.name,
                    payload=reb
                )

        # ----------------------------------------------------------------------
        # Stage 3: Consensus Voting & Final Strategic Decree
        # ----------------------------------------------------------------------
        scores = [a.score for a in assessments.values()]
        mean_score = sum(scores) / len(scores) if scores else 0.0

        # Check for critical vetoes
        critical_objections = [o for o in all_objections if o.severity == "CRITICAL"]
        high_objections = [o for o in all_objections if o.severity == "HIGH"]

        if critical_objections:
            council_verdict = "VETOED"
            council_status = "CRITICAL_DEFECT_DETECTED"
        elif mean_score >= 8.0 and len(high_objections) <= 1:
            council_verdict = "APPROVED_BY_COUNCIL"
            council_status = "READY_FOR_MONETIZATION"
        elif mean_score >= 7.0:
            council_verdict = "CONDITIONAL_APPROVAL"
            council_status = "MODIFICATIONS_RECOMMENDED"
        else:
            council_verdict = "REQUIRES_SUBSTANTIAL_REFINEMENT"
            council_status = "BELOW_COUNCIL_QUALITY_FLOOR"

        # Prioritize Action Directives (sorted by severity)
        severity_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
        sorted_objections = sorted(all_objections, key=lambda o: severity_order.get(o.severity, 4))

        prioritized_directives = [
            f"[{o.severity}] {o.critic_name} ({o.category}): {o.recommended_remedy} (Impact: {o.impact_on_goal})"
            for o in sorted_objections[:7]
        ]

        decree = {
            "node_id": node_id,
            "council_size": len(self.critics),
            "consensus_score": round(mean_score, 1),
            "council_verdict": council_verdict,
            "council_status": council_status,
            "critical_vetoes": len(critical_objections),
            "total_objections": len(all_objections),
            "top_strengths": all_strengths[:8],
            "autonomous_debates": debates,
            "prioritized_action_directives": prioritized_directives,
            "critic_breakdown": {
                name: asm.to_dict() for name, asm in assessments.items()
            },
            "timestamp": get_utc_iso()
        }

        self.event_bus.publish(
            topic="council:decree_finalized",
            sender="CritiqueCouncil",
            payload={
                "node_id": node_id,
                "score": decree["consensus_score"],
                "verdict": decree["council_verdict"]
            }
        )

        logger.info(f"Council Decree for '{node_id}': {council_verdict} (Score: {decree['consensus_score']}/10)")
        return decree
