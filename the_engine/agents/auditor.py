"""
The Engine - The Auditor (Financial & Risk Controller Agent)
Monitors spend vs. revenue, calculates ROI daily, verifies zero-cost integrity,
executes 48h optimization reviews, and enforces the 72h fail-safe retirement protocol.
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime

from the_engine.agents.base import BaseAgent
from the_engine.core.hitl import HITLGatekeeper
from the_engine.core.ledger import Ledger
from the_engine.core.isolation import NodeIsolationManager
from the_engine.config import FAIL_SAFE_CONSECUTIVE_DAYS, BUDGET_SCALE_PERCENTAGE, get_utc_iso

logger = logging.getLogger("TheEngine.Auditor")


class AuditorAgent(BaseAgent):
    def __init__(self, hitl_gatekeeper: HITLGatekeeper, ledger: Ledger, isolation_mgr: NodeIsolationManager):
        super().__init__(
            name="The Auditor",
            role="Financial & Risk Controller",
            hitl_gatekeeper=hitl_gatekeeper
        )
        self.ledger = ledger
        self.isolation_mgr = isolation_mgr

    def verify_zero_cost_compliance(self, node_id: str) -> Dict[str, Any]:
        """
        Confirms the node has complied with the strict zero-upfront-cost rule.
        Throws a security exception if unauthorized spend occurred.
        """
        node_fin = self.ledger.get_node_summary(node_id)
        if node_fin["expenses"] > 0 and node_fin["revenue"] == 0:
            raise PermissionError(
                f"AUDIT BREACH: Node '{node_id}' incurred ${node_fin['expenses']} without prior earned revenue."
            )
        return {
            "status": "COMPLIANT",
            "expenses": node_fin["expenses"],
            "revenue": node_fin["revenue"],
            "zero_cost_rule_intact": True
        }

    def verify_checkout_integrity(self, node_id: str) -> Dict[str, Any]:
        """
        Validates that monetization channels and checkout tracking are configured.
        """
        node_path = self.isolation_mgr.get_node_path(node_id)
        pricing_file = node_path / "monetization" / "pricing.json"

        if not pricing_file.exists():
            return {"status": "FAILED", "reason": "Missing pricing.json"}

        with open(pricing_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        tiers = data.get("tiers", [])
        has_free = any(t.get("price") == 0 for t in tiers)
        has_pro = any(t.get("price") > 0 for t in tiers)

        return {
            "status": "CHECKOUT_VERIFIED" if (has_free and has_pro) else "WARNING",
            "tier_count": len(tiers),
            "free_tier_present": has_free,
            "pro_tier_present": has_pro
        }

    def evaluate_node_performance(self, node_id: str, simulated_hours: int = 48) -> Dict[str, Any]:
        """
        Executes the 48-hour optimization review:
        - If profitable: Scale budget by 20%
        - If losing money/no traction: Recommend copy rewrite, price adjustment, or trigger fail-safe
        """
        manifest = self.isolation_mgr.read_manifest(node_id) or {}
        node_summary = self.ledger.get_node_summary(node_id)
        consecutive_neg = manifest.get("consecutive_negative_cycles", 0)

        net_profit = node_summary["net_profit"]
        action = "HOLD"
        lessons = {}

        if net_profit > 0:
            action = "SCALE_BUDGET_20"
            scale_amount = round(self.ledger.data["reinvestable_balance"] * BUDGET_SCALE_PERCENTAGE, 2)
            consecutive_neg = 0
            self.log(f"Node '{node_id}' is PROFITABLE (Net: ${net_profit:.2f}). Scaling reinvestment budget by 20% (${scale_amount:.2f}).")
        else:
            consecutive_neg += 1
            if consecutive_neg >= FAIL_SAFE_CONSECUTIVE_DAYS:
                action = "FAIL_SAFE_ARCHIVE"
                lessons = {
                    "reason": f"Zero or negative traction for {consecutive_neg} consecutive review cycles.",
                    "node_id": node_id,
                    "final_net": net_profit,
                    "action_taken": "Archived node and triggered market pivot."
                }
                self.log(f"FAIL-SAFE TRIGGERED: Node '{node_id}' failing 3 consecutive cycles. Archiving immediately.", level="warning")
                self.isolation_mgr.archive_node(node_id, reason="3 Consecutive Negative Cycles", lessons_learned=lessons)
            else:
                action = "OPTIMIZE_COPY_AND_PRICING"
                self.log(f"Node '{node_id}' needs optimization (Cycle {consecutive_neg}/{FAIL_SAFE_CONSECUTIVE_DAYS}). Adjusting marketing copy.")

        # Update manifest
        if action != "FAIL_SAFE_ARCHIVE":
            self.isolation_mgr.update_manifest(node_id, {
                "consecutive_negative_cycles": consecutive_neg,
                "last_evaluated": get_utc_iso(),
                "last_action": action
            })

        return {
            "node_id": node_id,
            "net_profit": net_profit,
            "action": action,
            "consecutive_negative_cycles": consecutive_neg,
            "lessons": lessons
        }

    def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Executes Phase 4: Financial Audit & Optimization."""
        node_id = context.get("node_id")
        if not node_id:
            raise ValueError("Auditor requires node_id in context.")

        compliance = self.verify_zero_cost_compliance(node_id)
        checkout = self.verify_checkout_integrity(node_id)
        eval_result = self.evaluate_node_performance(node_id)

        return {
            "status": "AUDIT_COMPLETED",
            "compliance": compliance,
            "checkout": checkout,
            "evaluation": eval_result,
            "timestamp": get_utc_iso()
        }
