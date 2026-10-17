"""
The Engine - Strict Human-in-the-Loop (HITL) Protocol Controller
Enforces hard gates for financial risk, legal/compliance barriers, and unresolvable stagnation.
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
from the_engine.config import get_utc_iso


@dataclass
class HITLAlert:
    node_id: str
    trigger_type: str  # "FINANCIAL_THRESHOLD" | "COMPLIANCE_LEGAL" | "SYSTEM_STAGNATION"
    error_code: Optional[str]
    description: str
    proposed_resolution: str
    action_required: str
    timestamp: str = ""

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = get_utc_iso()

    def format_alert(self) -> str:
        """
        Outputs the standardized Human-in-the-Loop notification template.
        """
        return f"""
================================================================================
🚨 [HUMAN-IN-THE-LOOP INTERVENTION REQUIRED] 🚨
--------------------------------------------------------------------------------
Node Identifier    : {self.node_id}
Trigger Category   : {self.trigger_type}
Timestamp (UTC)    : {self.timestamp}
Error Code         : {self.error_code or 'N/A'}

[DIAGNOSTIC CONTEXT]
{self.description}

[PROPOSED RESOLUTION PATH]
{self.proposed_resolution}

[ACTION REQUIRED FROM HUMAN]
{self.action_required}
--------------------------------------------------------------------------------
System execution for node '{self.node_id}' is PAUSED pending your explicit authorization.
================================================================================
""".strip()


class HITLGatekeeper:
    def __init__(self, max_consecutive_failures: int = 5):
        self.max_consecutive_failures = max_consecutive_failures
        self.failure_tracker: Dict[str, Dict[str, int]] = {}
        self.paused_nodes: Dict[str, HITLAlert] = {}

    def record_failure(self, node_id: str, error_code: str) -> int:
        """Tracks consecutive failures by error code for self-correction monitoring."""
        if node_id not in self.failure_tracker:
            self.failure_tracker[node_id] = {}
        current = self.failure_tracker[node_id].get(error_code, 0) + 1
        self.failure_tracker[node_id][error_code] = current
        return current

    def record_success(self, node_id: str, error_code: Optional[str] = None) -> None:
        """Resets failure counts upon successful self-correction."""
        if node_id in self.failure_tracker:
            if error_code and error_code in self.failure_tracker[node_id]:
                self.failure_tracker[node_id][error_code] = 0
            else:
                self.failure_tracker[node_id].clear()

    def check_stagnation(self, node_id: str, error_code: str, error_details: str) -> Optional[HITLAlert]:
        """Triggers HITL if the exact same error code has failed > 5 consecutive times."""
        count = self.record_failure(node_id, error_code)
        if count >= self.max_consecutive_failures:
            alert = HITLAlert(
                node_id=node_id,
                trigger_type="SYSTEM_STAGNATION",
                error_code=error_code,
                description=f"Self-correction loop failed {count} consecutive times on error '{error_code}'. Details: {error_details}",
                proposed_resolution="Manual review of code logic, external service status, or environment configuration.",
                action_required="Inspect the failure log, adjust the node configuration, or approve node retirement."
            )
            self.paused_nodes[node_id] = alert
            return alert
        return None

    def check_financial_gate(self, node_id: str, amount: float, current_balance: float, threshold: float = 0.0) -> Optional[HITLAlert]:
        """Triggers HITL if an expense exceeds allowable limits without earned capital."""
        if amount > current_balance or amount > threshold:
            alert = HITLAlert(
                node_id=node_id,
                trigger_type="FINANCIAL_THRESHOLD",
                error_code="FIN_THRESHOLD_EXCEEDED",
                description=(
                    f"Requested transaction amount of ${amount:.2f} exceeds allowable free limit (${threshold:.2f}). "
                    f"Current reinvestable earned balance: ${current_balance:.2f}."
                ),
                proposed_resolution="Reject paid transaction and utilize a free-tier alternative, or grant manual funding approval.",
                action_required="Provide budget override or instruct system to use 100% free fallback tools."
            )
            self.paused_nodes[node_id] = alert
            return alert
        return None

    def check_compliance_gate(self, node_id: str, compliance_type: str, details: str) -> HITLAlert:
        """Triggers HITL on hard external barriers: Captcha, KYC/MFA, ToS block."""
        alert = HITLAlert(
            node_id=node_id,
            trigger_type="COMPLIANCE_LEGAL",
            error_code=f"LEGAL_{compliance_type.upper()}",
            description=f"Encountered compliance or identity barrier: {details}",
            proposed_resolution="Complete one-time human credential verification or select an alternative API provider.",
            action_required=f"Perform manual verification for {compliance_type} or authorize an alternative path."
        )
        self.paused_nodes[node_id] = alert
        return alert

    def is_paused(self, node_id: str) -> bool:
        return node_id in self.paused_nodes

    def unpause(self, node_id: str) -> None:
        if node_id in self.paused_nodes:
            del self.paused_nodes[node_id]
        if node_id in self.failure_tracker:
            self.failure_tracker[node_id].clear()
