"""
The Engine - The Orchestrator (Main Loop Controller)
Coordinates The Scout, The Builder, The Growth Hacker, and The Auditor.
Enforces the 4-Phase Autonomous Operational Loop and acts as the gatekeeper to the HITL protocol.
"""

import logging
import time
from typing import Dict, Any, Optional
from datetime import datetime
from pathlib import Path

from the_engine.config import get_utc_iso, get_utc_now
from the_engine.core.hitl import HITLGatekeeper, HITLAlert
from the_engine.core.ledger import Ledger
from the_engine.core.isolation import NodeIsolationManager
from the_engine.core.event_bus import EventBus
from the_engine.agents.scout import ScoutAgent
from the_engine.agents.builder import BuilderAgent
from the_engine.agents.growth_hacker import GrowthHackerAgent
from the_engine.agents.auditor import AuditorAgent
from the_engine.agents.tester import TesterAgent
from the_engine.agents.critic import CriticAgent
from the_engine.agents.strategist import StrategistAgent

logger = logging.getLogger("TheEngine.Orchestrator")


class Orchestrator:
    def __init__(self):
        self.hitl = HITLGatekeeper()
        self.ledger = Ledger()
        self.isolation_mgr = NodeIsolationManager()
        self.event_bus = EventBus()

        # Initialize specialized agents
        self.scout = ScoutAgent(hitl_gatekeeper=self.hitl)
        self.builder = BuilderAgent(hitl_gatekeeper=self.hitl, isolation_mgr=self.isolation_mgr)
        self.tester = TesterAgent(hitl_gatekeeper=self.hitl)
        self.critic = CriticAgent(hitl_gatekeeper=self.hitl)
        self.strategist = StrategistAgent(hitl_gatekeeper=self.hitl)
        self.growth_hacker = GrowthHackerAgent(hitl_gatekeeper=self.hitl)
        self.auditor = AuditorAgent(hitl_gatekeeper=self.hitl, ledger=self.ledger, isolation_mgr=self.isolation_mgr)

        logger.info("The Engine 7-Agent Orchestration Layer initialized. Autopilot by Default.")

    def run_cycle(self) -> Dict[str, Any]:
        """
        Executes the full 4-Phase Autonomous Operational Loop:
        1. Analyze (Scout)
        2. Build (Builder)
        3. Monetize (Growth Hacker)
        4. Optimize (Auditor)
        """
        cycle_id = f"cycle_{get_utc_now().strftime('%Y%m%d_%H%M%S')}"
        logger.info(f"=== Starting Autonomous Cycle: {cycle_id} ===")
        self.event_bus.publish("cycle:started", "Orchestrator", {"cycle_id": cycle_id})

        # Phase 1: Analyze
        logger.info("[Phase 1: Analyze] Launching Scout market intelligence scan...")
        active_nodes = self.isolation_mgr.list_active_nodes()
        scout_res = self.scout.run({"existing_node_ids": active_nodes})
        opportunity = scout_res["opportunity"]
        node_id = f"node_{opportunity['niche_id']}"
        self.event_bus.publish("scout:completed", "Scout", {"opportunity": opportunity})

        # Phase 2: Build
        logger.info(f"[Phase 2: Build] Handing off opportunity '{opportunity['name']}' to Builder...")
        builder_res = self.builder.run({"opportunity": opportunity})
        workspace_path = builder_res["workspace_path"]
        self.event_bus.publish("builder:completed", "Builder", {"node_id": node_id, "path": workspace_path})

        # Phase 3: Verify (The Tester)
        logger.info(f"[Phase 3: Verify] Handing off '{node_id}' to Tester for empirical QA checks...")
        tester_res = self.tester.run({"workspace_path": workspace_path})
        test_report = tester_res["report"]
        self.event_bus.publish("tester:completed", "Tester", {"node_id": node_id, "report": test_report})

        # Phase 4: Critique (The Critic)
        logger.info(f"[Phase 4: Critique] Handing off '{node_id}' to Critic for adversarial evaluation...")
        critic_res = self.critic.run({"workspace_path": workspace_path, "opportunity": opportunity})
        critique_report = critic_res["report"]
        self.event_bus.publish("critic:completed", "Critic", {"node_id": node_id, "report": critique_report})

        # Phase 5: Decide (The Strategist / Deep Thinker)
        logger.info(f"[Phase 5: Decide] Handing off findings to Strategist for executive launch verdict...")
        strategist_res = self.strategist.run({
            "opportunity": opportunity,
            "test_report": test_report,
            "critique_report": critique_report
        })
        verdict = strategist_res["verdict"]
        self.event_bus.publish("strategist:completed", "Strategist", {"node_id": node_id, "verdict": verdict})

        # Phase 6: Monetize (The Growth Hacker) - Proceeds once approved
        logger.info(f"[Phase 6: Monetize] Launching distribution campaigns via Growth Hacker...")
        growth_res = self.growth_hacker.run({"workspace_path": workspace_path})
        self.event_bus.publish("growth:completed", "GrowthHacker", {"node_id": node_id, "campaign": growth_res})

        # Phase 7: Optimize & Audit (The Auditor)
        logger.info(f"[Phase 7: Optimize] Conducting financial & health audit via Auditor...")
        audit_res = self.auditor.run({"node_id": node_id})
        self.event_bus.publish("auditor:completed", "Auditor", {"node_id": node_id, "audit": audit_res})

        summary = {
            "cycle_id": cycle_id,
            "status": "COMPLETED",
            "node_id": node_id,
            "opportunity": opportunity["name"],
            "workspace_path": workspace_path,
            "qa_grade": test_report.get("grade", "N/A"),
            "qa_pass_rate": f"{test_report.get('pass_rate', 0)}%",
            "critique_score": f"{critique_report.get('overall_quality_score', 0)}/10",
            "executive_decision": verdict.get("executive_decision", "APPROVED"),
            "audit_compliance": audit_res["compliance"]["status"],
            "checkout_status": audit_res["checkout"]["status"],
            "evaluation_action": audit_res["evaluation"]["action"],
            "global_financials": self.ledger.get_global_summary(),
            "completed_at": get_utc_iso()
        }

        self.event_bus.publish("cycle:finished", "Orchestrator", summary)
        logger.info(f"=== Autonomous Cycle {cycle_id} Successfully Completed ===")
        return summary

    def get_status(self) -> Dict[str, Any]:
        """Returns the real-time operational status of the entire engine."""
        active_nodes = self.isolation_mgr.list_active_nodes()
        archived_nodes = self.isolation_mgr.list_archived_nodes()
        financials = self.ledger.get_global_summary()

        node_details = {}
        for nid in active_nodes:
            manifest = self.isolation_mgr.read_manifest(nid) or {}
            fin = self.ledger.get_node_summary(nid)
            node_details[nid] = {
                "status": manifest.get("status"),
                "revenue": fin["revenue"],
                "expenses": fin["expenses"],
                "net_profit": fin["net_profit"],
                "consecutive_neg": manifest.get("consecutive_negative_cycles", 0)
            }

        return {
            "engine_state": "ACTIVE",
            "mode": "Autopilot by Default (95%+ Autonomy)",
            "zero_cost_policy": "Strict $0 Upfront - Earn It First",
            "active_node_count": len(active_nodes),
            "archived_node_count": len(archived_nodes),
            "active_nodes": node_details,
            "financial_summary": financials,
            "incorporation_milestone": self.auditor.check_incorporation_milestone(),
            "paused_hitl_nodes": list(self.hitl.paused_nodes.keys())
        }

    def start_daemon(self, interval_seconds: int = 3600, max_cycles: Optional[int] = None) -> None:
        """
        Runs the engine continuously as a background daemon.
        Periodically runs health audits, reviews node performance, and triggers Scout if needed.
        """
        cycle_count = 0
        logger.info(f"The Engine Daemon started. Interval: {interval_seconds}s. Autopilot active.")
        print(f"\n⚡ The Engine Daemon started. Interval: {interval_seconds}s. Press Ctrl+C to stop.\n")

        try:
            while max_cycles is None or cycle_count < max_cycles:
                cycle_count += 1
                now_str = get_utc_iso()
                print(f"[{now_str}] Daemon Cycle #{cycle_count}: Running active node audit...")

                active_nodes = self.isolation_mgr.list_active_nodes()
                for nid in active_nodes:
                    audit_res = self.auditor.run({"node_id": nid})
                    print(f"  • Node '{nid}': {audit_res['compliance']['status']} | Action: {audit_res['evaluation']['action']}")

                # If no active nodes exist, autonomously scout and build one
                if not active_nodes:
                    print(f"[{now_str}] No active nodes found. Autonomously launching new revenue cycle...")
                    self.run_cycle()

                if max_cycles is not None and cycle_count >= max_cycles:
                    break

                time.sleep(interval_seconds)
        except KeyboardInterrupt:
            print("\n⚡ The Engine Daemon stopped gracefully by user.")
