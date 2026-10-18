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
from the_engine.critics.debate_engine import ParallelDebateGraph
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
    - Executes Tri-Chamber Deliberation DAG with concurrent Fan-Out evaluation.
    - Anti-Obsolescence Sentinel guards against technical, commercial, and legal rot.
    - Isolated 1v1 parallel debate threads ground trade-offs in live system telemetry.
    - Enforces P0 Hard-Veto Circuit Breakers while calculating Pareto-weighted consensus.
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

        # High-performance DAG Deliberation Engine
        self.debate_graph = ParallelDebateGraph(critics=self.critics, event_bus=self.event_bus)

    def convene_council(
        self,
        node_path: Path,
        opportunity: Dict[str, Any],
        engine_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Executes the high-performance parallel Tri-Chamber Deliberation DAG:
        Phase 1: Concurrent Fan-Out evaluation across all 10 specialized lenses.
        Phase 2: Anti-Obsolescence Sentinel auditing technical, commercial, and legal freshness.
        Phase 3: Isolated 1v1 cross-chamber debate threads grounded in real system telemetry.
        Phase 4: P0 Hard-Veto Circuit Breakers vs. Pareto-Weighted Concession Synthesis.
        """
        node_id = node_path.name
        engine_ctx = engine_context or {}
        engine_ctx["hitl_gatekeeper"] = self.hitl
        engine_ctx["event_bus"] = self.event_bus

        logger.info(f"Convening Tri-Chamber Deliberation DAG for '{node_id}' across 10 lenses...")
        decree = self.debate_graph.run_dag_deliberation(
            node_path=node_path,
            opportunity=opportunity,
            engine_context=engine_ctx
        )

        logger.info(f"Council Decree for '{node_id}': {decree.council_verdict} (Score: {decree.consensus_score}/10, Hard Veto: {decree.has_hard_veto})")
        return decree.to_dict()

