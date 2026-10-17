"""
The Engine - Red-Team Critique Council (Base Critic Interface)
Defines the specialized critique contract, scoring taxonomy, and inter-agent debate protocol.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
import logging

from the_engine.core.event_bus import EventBus
from the_engine.config import get_utc_iso

logger = logging.getLogger("TheEngine.Critics")


@dataclass
class CritiqueObjection:
    critic_name: str
    category: str
    severity: str  # "CRITICAL", "HIGH", "MEDIUM", "LOW"
    issue: str
    impact_on_goal: str
    recommended_remedy: str
    score_deduction: float


@dataclass
class CritiqueAssessment:
    critic_name: str
    domain: str
    score: float  # 0.0 to 10.0
    strengths: List[str] = field(default_factory=list)
    objections: List[CritiqueObjection] = field(default_factory=list)
    confidence: float = 1.0  # 0.0 to 1.0
    timestamp: str = field(default_factory=get_utc_iso)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "critic_name": self.critic_name,
            "domain": self.domain,
            "score": round(self.score, 1),
            "strengths": self.strengths,
            "objections": [
                {
                    "category": obj.category,
                    "severity": obj.severity,
                    "issue": obj.issue,
                    "impact": obj.impact_on_goal,
                    "remedy": obj.recommended_remedy,
                    "penalty": obj.score_deduction
                }
                for obj in self.objections
            ],
            "confidence": round(self.confidence, 2),
            "timestamp": self.timestamp
        }


class BaseSpecializedCritic(ABC):
    """Abstract base for specialized red-team critique agents."""

    def __init__(self, name: str, domain: str, event_bus: Optional[EventBus] = None):
        self.name = name
        self.domain = domain
        self.event_bus = event_bus

    def log(self, msg: str, level: str = "info") -> None:
        log_fn = getattr(logger, level.lower(), logger.info)
        log_fn(f"[{self.name} - {self.domain}]: {msg}")

    @abstractmethod
    def evaluate(self, node_path, opportunity: Dict[str, Any], engine_context: Dict[str, Any]) -> CritiqueAssessment:
        """Independently evaluates the node and engine from this critic's specialized lens."""
        pass

    def cross_examine(
        self,
        peer_assessments: Dict[str, CritiqueAssessment],
        node_path,
        engine_context: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Autonomous cross-agent debate round:
        Reviews findings by other critics and issues supporting or dissenting opinions.
        """
        rebuttals = []
        # Default cross-examination logic: derived critics can override with specialized counter-arguments
        return rebuttals
