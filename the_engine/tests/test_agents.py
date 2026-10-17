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


if __name__ == "__main__":
    unittest.main()
