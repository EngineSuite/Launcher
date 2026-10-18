"""
The Engine - Deliberation Graph Schemas & Structured Handoff Payloads
Enforces strict machine-readable contracts across all chambers, debate rounds,
and the Evolution Synthesizer to eliminate conversational hallucination.
"""

from typing import Dict, Any, List, Optional, Literal
from dataclasses import dataclass, field, asdict
from the_engine.config import get_utc_iso


SeverityTier = Literal["P0", "P1", "P2", "P3"]
ResolutionStatus = Literal[
    "CONCEDED_WITH_OPTIMIZATION",
    "P0_HARD_VETO_UNRESOLVED",
    "CHALLENGE_WITHDRAWN",
    "DIRECTIVE_ISSUED"
]


@dataclass
class StructuredIssue:
    """Strict typed representation of a defect or optimization point."""
    issue_id: str                          # e.g. "SEC-XSS-001", "LEG-WARR-001"
    critic_name: str                       # Name of discovering lens
    chamber: str                           # "Commercial", "Technical", "Governance"
    category: str                          # Specific category (e.g. "XSS", "Passive Headline")
    severity_tier: SeverityTier            # P0 (Hard Veto), P1 (Critical), P2 (Weighted), P3 (Minor)
    is_hard_veto: bool                     # True only for P0 existential flaws (Security, Legal, Spend)
    issue: str                             # Precise problem description
    impact_metric: str                     # Measurable impact on system goal
    proposed_diff: str                     # Concrete remediation code/text patch
    score_deduction: float                 # Point deduction on 10.0 scale

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ConcessionRecord:
    """Represents a quantified Pareto trade-off between opposing chambers."""
    thread_name: str
    offering_critic: str
    benefiting_critic: str
    tolerated_penalty_metric: str          # e.g. "+15ms initial load latency"
    gained_benefit_metric: str             # e.g. "+25% conversion lift via interactive Canvas"
    concession_rationale: str
    is_p0_breach: bool = False             # Never allowed to be True

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class DebateRoundPayload:
    """Strict JSON payload emitted by an isolated 1v1 parallel debate thread."""
    thread_name: str                       # e.g. "Speed_vs_Conversion"
    round_number: int
    challenger: str
    defendant: str
    issue_in_debate: StructuredIssue
    rebuttal_argument: str
    concession: Optional[ConcessionRecord]
    resolution: ResolutionStatus
    binding_directive: str
    timestamp: str = field(default_factory=get_utc_iso)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "thread_name": self.thread_name,
            "round_number": self.round_number,
            "challenger": self.challenger,
            "defendant": self.defendant,
            "issue_in_debate": self.issue_in_debate.to_dict(),
            "rebuttal_argument": self.rebuttal_argument,
            "concession": self.concession.to_dict() if self.concession else None,
            "resolution": self.resolution,
            "binding_directive": self.binding_directive,
            "timestamp": self.timestamp
        }


@dataclass
class AntiObsolescenceAudit:
    """Measures technical, commercial, and legal freshness to ensure the product never rots."""
    modern_web_standards_score: float      # Native CSS/HTML5, View Transitions, no legacy libs
    commercial_relevance_score: float      # Problem-aware copy, freemium anchoring, 2026 value
    legal_governance_score: float          # Active AS-IS disclaimer, liability cap, refund guarantee
    composite_freshness_index: float       # 0.0 to 10.0
    detected_obsolete_patterns: List[str]
    modern_capabilities_detected: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class CouncilDecree:
    """The synthesized executive decision output by the Evolution Synthesizer."""
    node_id: str
    consensus_score: float
    council_verdict: str                   # "APPROVED_BY_COUNCIL", "VETOED_P0_HARD_BLOCK", "CONDITIONAL_APPROVAL"
    council_status: str
    has_hard_veto: bool
    hard_vetoes: List[Dict[str, Any]]
    total_objections: int
    negotiated_concessions: List[Dict[str, Any]]
    anti_obsolescence_audit: Dict[str, Any]
    parallel_debate_threads: List[Dict[str, Any]]
    prioritized_action_directives: List[str]
    chamber_breakdown: Dict[str, Any]
    fanout_execution_time_ms: float
    top_strengths: List[str] = field(default_factory=list)
    critic_breakdown: Dict[str, Any] = field(default_factory=dict)
    council_size: int = 10
    critical_vetoes: int = 0
    autonomous_debates: List[Dict[str, Any]] = field(default_factory=list)
    timestamp: str = field(default_factory=get_utc_iso)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
