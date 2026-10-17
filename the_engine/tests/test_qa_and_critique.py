"""Tests for QA Tester, Critic, and Strategist Agents"""
import unittest
from pathlib import Path

from the_engine.core.hitl import HITLGatekeeper
from the_engine.agents.tester import TesterAgent
from the_engine.agents.critic import CriticAgent
from the_engine.agents.strategist import StrategistAgent


class TestQAAndCritiqueAgents(unittest.TestCase):
    def setUp(self):
        self.hitl = HITLGatekeeper()
        self.tester = TesterAgent(self.hitl)
        self.critic = CriticAgent(self.hitl)
        self.strategist = StrategistAgent(self.hitl)
        self.schemacraft_path = Path(__file__).resolve().parent.parent.parent / "nodes" / "node_schemacraft_pro"

    def test_tester_verifies_schemacraft_node(self):
        res = self.tester.test_node(self.schemacraft_path)
        self.assertEqual(res["status"], "PASSED")
        self.assertGreaterEqual(res["pass_rate"], 90.0)
        self.assertEqual(res["grade"], "A+")
        self.assertEqual(res["details"]["deliverable_zip_exists"], "PASSED")
        self.assertEqual(res["details"]["zip_file_integrity"], "PASSED")

    def test_critic_scores_schemacraft_node(self):
        opp = {"name": "SchemaCraft Pro", "niche_id": "schemacraft_pro"}
        res = self.critic.review_node(self.schemacraft_path, opp)
        self.assertGreaterEqual(res["overall_quality_score"], 7.5)
        self.assertIn("strengths", res)
        self.assertGreater(len(res["strengths"]), 0)

    def test_strategist_approves_healthy_node(self):
        opp = {"name": "SchemaCraft Pro", "niche_id": "schemacraft_pro"}
        test_rep = {"node_id": "node_schemacraft_pro", "pass_rate": 100.0, "grade": "A+", "defects": []}
        critique_rep = {"overall_quality_score": 8.8, "commercial_viability": "HIGH", "actionable_upgrades": []}

        verdict = self.strategist.evaluate_and_decide(opp, test_rep, critique_rep)
        self.assertEqual(verdict["executive_decision"], "APPROVED_FOR_LAUNCH")
        self.assertEqual(verdict["status"], "APPROVED")

    def test_strategist_rejects_flawed_node(self):
        opp = {"name": "Flawed Node", "niche_id": "flawed"}
        test_rep = {"node_id": "node_flawed", "pass_rate": 60.0, "grade": "F", "defects": [{"check": "zip", "error": "corrupt"}]}
        critique_rep = {"overall_quality_score": 5.0, "commercial_viability": "LOW", "actionable_upgrades": ["Fix all"]}

        verdict = self.strategist.evaluate_and_decide(opp, test_rep, critique_rep)
        self.assertEqual(verdict["executive_decision"], "REQUIRES_REFINEMENT")
        self.assertEqual(verdict["status"], "REJECTED_FOR_REFINEMENT")


if __name__ == "__main__":
    unittest.main()
