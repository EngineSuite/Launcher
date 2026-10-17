"""Tests for Individual Specialized Agents"""
import unittest
import tempfile
import shutil
from pathlib import Path

from the_engine.core.hitl import HITLGatekeeper
from the_engine.core.ledger import Ledger
from the_engine.core.isolation import NodeIsolationManager
from the_engine.agents.scout import ScoutAgent
from the_engine.agents.builder import BuilderAgent
from the_engine.agents.growth_hacker import GrowthHackerAgent
from the_engine.agents.auditor import AuditorAgent
from the_engine.agents.critic import CriticAgent


class TestAgents(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.nodes_dir = Path(self.temp_dir) / "nodes"
        self.ledger_file = Path(self.temp_dir) / "ledger.json"

        self.hitl = HITLGatekeeper()
        self.ledger = Ledger(ledger_path=self.ledger_file)
        self.isolation_mgr = NodeIsolationManager(nodes_dir=self.nodes_dir)

        self.scout = ScoutAgent(self.hitl)
        self.builder = BuilderAgent(self.hitl, self.isolation_mgr)
        self.growth_hacker = GrowthHackerAgent(self.hitl)
        self.auditor = AuditorAgent(self.hitl, self.ledger, self.isolation_mgr)
        self.critic = CriticAgent(self.hitl)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_scout_finds_viable_opportunities(self):
        opps = self.scout.scan_opportunities()
        self.assertGreater(len(opps), 0)
        best = self.scout.select_best_opportunity()
        self.assertIn("niche_id", best)
        self.assertEqual(best["zero_cost_feasibility"], 10.0)

    def test_builder_creates_isolated_node_workspace(self):
        best = self.scout.select_best_opportunity()
        node_path = self.builder.build_node(best)
        self.assertTrue(node_path.exists())
        self.assertTrue((node_path / "public" / "index.html").exists())
        self.assertTrue((node_path / "public" / "app.js").exists())
        self.assertTrue((node_path / "public" / "styles.css").exists())
        self.assertTrue((node_path / "src" / "server.py").exists())
        self.assertTrue((node_path / "src" / "schema_engine.py").exists())
        self.assertTrue((node_path / "monetization" / "pricing.json").exists())

    def test_growth_hacker_creates_distribution_assets(self):
        best = self.scout.select_best_opportunity()
        node_path = self.builder.build_node(best)
        res = self.growth_hacker.run({"workspace_path": str(node_path)})
        self.assertEqual(res["status"], "TRAFFIC_DISTRIBUTION_READY")
        self.assertTrue((node_path / "distribution" / "seo_strategy.json").exists())
        self.assertTrue((node_path / "distribution" / "social_campaigns.json").exists())
        self.assertTrue((node_path / "distribution" / "directory_submissions.json").exists())

    def test_auditor_enforces_zero_cost_and_fail_safe(self):
        best = self.scout.select_best_opportunity()
        node_path = self.builder.build_node(best)
        node_id = node_path.name

        # Cycle 1 audit
        audit1 = self.auditor.run({"node_id": node_id})
        self.assertEqual(audit1["compliance"]["status"], "COMPLIANT")
        self.assertEqual(audit1["evaluation"]["action"], "OPTIMIZE_COPY_AND_PRICING")

        # Cycle 2 audit
        audit2 = self.auditor.run({"node_id": node_id})
        self.assertEqual(audit2["evaluation"]["consecutive_negative_cycles"], 2)

        # Cycle 3 audit triggers fail-safe archive
        audit3 = self.auditor.run({"node_id": node_id})
        self.assertEqual(audit3["evaluation"]["action"], "FAIL_SAFE_ARCHIVE")
        self.assertNotIn(node_id, self.isolation_mgr.list_active_nodes())
        self.assertEqual(len(self.isolation_mgr.list_archived_nodes()), 1)

    def test_builder_injects_legal_armor_and_guarantee(self):
        best = self.scout.select_best_opportunity()
        node_path = self.builder.build_node(best)

        # 1. Standardized LICENSE.txt must exist with AS IS and liability cap
        license_path = node_path / "dist_pack" / "LICENSE.txt"
        self.assertTrue(license_path.exists())
        license_text = license_path.read_text(encoding="utf-8")
        self.assertIn('"AS IS"', license_text)
        self.assertIn("Limitation of Liability", license_text)
        self.assertIn("purchase price", license_text.lower())
        self.assertIn("30-Day", license_text)

        # 2. HTML must have 30-day money-back guarantee badge
        html_text = (node_path / "public" / "index.html").read_text(encoding="utf-8")
        self.assertIn("30-Day", html_text)
        self.assertIn("Money-Back Guarantee", html_text)

        # 3. Deliverable ZIP must be packaged in public/downloads
        downloads = list((node_path / "public" / "downloads").glob("*.zip"))
        self.assertGreater(len(downloads), 0)

    def test_critic_enforces_guarantee_and_license(self):
        best = self.scout.select_best_opportunity()
        node_path = self.builder.build_node(best)

        # Full compliance node should pass with high score
        review_pass = self.critic.review_node(node_path, best)
        self.assertGreaterEqual(review_pass["overall_quality_score"], 8.0)
        self.assertEqual(review_pass["commercial_viability"], "HIGH")

        # Strip LICENSE.txt and verify Critic penalizes and detects critical legal deficit
        license_path = node_path / "dist_pack" / "LICENSE.txt"
        if license_path.exists():
            license_path.unlink()
        review_fail = self.critic.review_node(node_path, best)
        self.assertLess(review_fail["overall_quality_score"], review_pass["overall_quality_score"])
        self.assertTrue(any("LEGAL DEFICIT" in v for v in review_fail["vulnerabilities"]))

    def test_auditor_incorporation_milestone(self):
        # 1. Under threshold ($19 revenue), incorporation is deferred
        milestone1 = self.auditor.check_incorporation_milestone(threshold=1500.0)
        self.assertFalse(milestone1["milestone_reached"])
        self.assertEqual(milestone1["status"], "DEFERRED_INCORPORATION_ACTIVE")

        # 2. Add revenue reaching $1,500 with zero chargebacks
        self.ledger.record_revenue("node_schemacraft_pro", 1500.0, "Gumroad", "Enterprise purchase")
        milestone2 = self.auditor.check_incorporation_milestone(threshold=1500.0)
        self.assertTrue(milestone2["milestone_reached"])
        self.assertEqual(milestone2["status"], "ENTITY_INCORPORATION_RECOMMENDED")
        self.assertGreaterEqual(milestone2["reinvestable_balance"], 750.0)


if __name__ == "__main__":
    unittest.main()

