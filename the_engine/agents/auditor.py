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

    def probe_live_cloud_deployment(self, base_url: str = "https://neerajkukreti.github.io/Launcher/") -> Dict[str, Any]:
        """
        Probes the live public cloud deployment (GitHub Pages / Cloudflare Pages)
        to verify uptime, HTTP response codes, latency, and SSL integrity from local machine.
        """
        import urllib.request
        import time

        endpoints = {
            "portal": base_url,
            "schemacraft": f"{base_url.rstrip('/')}/schemacraft/",
            "dev_cheatsheet": f"{base_url.rstrip('/')}/dev_cheatsheet/",
            "meta_craft_og": f"{base_url.rstrip('/')}/meta_craft_og/"
        }

        results = {}
        all_healthy = True

        for name, url in endpoints.items():
            start_time = time.time()
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "TheEngine-Auditor-Sentinel/1.0"})
                with urllib.request.urlopen(req, timeout=5) as resp:
                    latency_ms = round((time.time() - start_time) * 1000, 1)
                    status_code = resp.status
                    healthy = status_code == 200
                    results[name] = {
                        "url": url,
                        "status": status_code,
                        "healthy": healthy,
                        "latency_ms": latency_ms
                    }
            except Exception as e:
                all_healthy = False
                results[name] = {
                    "url": url,
                    "status": "OFFLINE_OR_UNREACHABLE",
                    "healthy": False,
                    "error": str(e),
                    "latency_ms": None
                }

        return {
            "provider": "GitHub Pages (Global Edge CDN)",
            "base_url": base_url,
            "overall_healthy": all_healthy,
            "probes": results,
            "probed_at": get_utc_iso()
        }

    def evaluate_node_performance(
        self,
        node_id: str,
        simulated_hours: int = 48,
        force_tick: bool = True,
        min_hours_between_cycles: float = 24.0
    ) -> Dict[str, Any]:
        """
        Executes the 48-hour optimization review:
        - If profitable: Scale budget by 20%
        - If losing money/no traction: Recommend copy rewrite, price adjustment, or trigger fail-safe
        - In continuous daemon mode, enforces real-time 24-hour cycle spacing so brand-new nodes aren't prematurely archived.
        """
        manifest = self.isolation_mgr.read_manifest(node_id) or {}
        node_summary = self.ledger.get_node_summary(node_id)
        consecutive_neg = manifest.get("consecutive_negative_cycles", 0)

        net_profit = node_summary["net_profit"]
        action = "HOLD"
        lessons = {}

        # If running in daemon mode without force_tick, ensure at least min_hours_between_cycles have elapsed
        if not force_tick:
            last_eval = manifest.get("last_evaluated") or manifest.get("created_at")
            if last_eval:
                try:
                    from datetime import datetime, timezone
                    last_time = datetime.fromisoformat(last_eval.replace("Z", "+00:00"))
                    now = datetime.now(timezone.utc)
                    elapsed_hours = (now - last_time).total_seconds() / 3600.0
                    if elapsed_hours < min_hours_between_cycles:
                        # 24-hour review cycle still active in the market
                        return {
                            "node_id": node_id,
                            "net_profit": net_profit,
                            "action": f"MONITORING_ACTIVE (Cycle {consecutive_neg + 1}/3, {elapsed_hours:.1f}h/{min_hours_between_cycles:.0f}h)",
                            "consecutive_negative_cycles": consecutive_neg,
                            "lessons": {}
                        }
                except Exception:
                    pass

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

    def check_incorporation_milestone(self, threshold: float = 1500.0) -> Dict[str, Any]:
        """
        Evaluates the Deferred Incorporation ("Earned Entity") milestone.
        - While revenue < threshold: Operate safely as an Individual via Merchant of Record (Gumroad / Lemon Squeezy)
          with $0 upfront overhead and automated global tax/VAT shielding.
        - When total revenue >= threshold ($1,500) and zero chargebacks:
          Flags milestone recommendation to deploy earned profits from Reinvestment Pool
          to formalize an LLC / legal entity for full personal asset insulation with $0 out-of-pocket cost.
        """
        summary = self.ledger.get_global_summary()
        tot_rev = summary.get("total_revenue", 0.0)
        reinvest_bal = summary.get("reinvestable_balance", 0.0)
        safe_reserve = summary.get("safe_account_reserve", 0.0)

        chargebacks = [
            t for t in self.ledger.data.get("transactions", [])
            if t.get("type") in ("CHARGEBACK", "DISPUTE")
        ]

        if tot_rev >= threshold and len(chargebacks) == 0:
            status = "ENTITY_INCORPORATION_RECOMMENDED"
            reached = True
            msg = (
                f"Milestone Reached! Total revenue (${tot_rev:.2f}) meets or exceeds ${threshold:.2f} "
                f"with 0 chargebacks. Reinvestment pool has ${reinvest_bal:.2f} available. "
                "Recommend deploying earned profits to formalize an LLC / corporate entity to insulate personal assets "
                "with 100% earned profit and zero out-of-pocket risk."
            )
        else:
            status = "DEFERRED_INCORPORATION_ACTIVE"
            reached = False
            msg = (
                f"Deferred Incorporation Active: Operating safely as Individual via Merchant of Record "
                f"(Gumroad / Lemon Squeezy) to preserve $0 overhead and automated global VAT shield. "
                f"Incorporation milestone progress: ${tot_rev:.2f} / ${threshold:.2f}."
            )

        return {
            "status": status,
            "milestone_reached": reached,
            "threshold": threshold,
            "total_revenue": tot_rev,
            "reinvestable_balance": reinvest_bal,
            "safe_account_reserve": safe_reserve,
            "chargeback_count": len(chargebacks),
            "recommendation": msg
        }

    def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Executes Phase 4: Financial Audit & Optimization."""
        node_id = context.get("node_id")
        if not node_id:
            raise ValueError("Auditor requires node_id in context.")

        force_tick = context.get("force_tick", not context.get("daemon_mode", False))
        min_hours = context.get("min_hours_between_cycles", 24.0)

        compliance = self.verify_zero_cost_compliance(node_id)
        checkout = self.verify_checkout_integrity(node_id)
        eval_result = self.evaluate_node_performance(
            node_id,
            force_tick=force_tick,
            min_hours_between_cycles=min_hours
        )
        milestone = self.check_incorporation_milestone()

        return {
            "status": "AUDIT_COMPLETED",
            "compliance": compliance,
            "checkout": checkout,
            "evaluation": eval_result,
            "incorporation_milestone": milestone,
            "timestamp": get_utc_iso()
        }
