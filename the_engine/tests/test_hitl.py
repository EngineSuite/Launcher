"""Tests for HITL Gatekeeper and Protocol Alerts"""
import unittest
from the_engine.core.hitl import HITLGatekeeper


class TestHITL(unittest.TestCase):
    def setUp(self):
        self.hitl = HITLGatekeeper(max_consecutive_failures=5)

    def test_stagnation_triggers_on_fifth_failure(self):
        node_id = "node_alpha"
        err_code = "ERR_API_TIMEOUT"

        for i in range(1, 5):
            alert = self.hitl.check_stagnation(node_id, err_code, "Timeout waiting for service")
            self.assertIsNone(alert)
            self.assertFalse(self.hitl.is_paused(node_id))

        # 5th failure triggers HITL
        alert = self.hitl.check_stagnation(node_id, err_code, "Timeout waiting for service")
        self.assertIsNotNone(alert)
        self.assertEqual(alert.trigger_type, "SYSTEM_STAGNATION")
        self.assertTrue(self.hitl.is_paused(node_id))
        self.assertIn("HUMAN-IN-THE-LOOP INTERVENTION REQUIRED", alert.format_alert())

    def test_financial_gate_trigger(self):
        node_id = "node_beta"
        alert = self.hitl.check_financial_gate(node_id, amount=10.00, current_balance=0.00, threshold=0.00)
        self.assertIsNotNone(alert)
        self.assertEqual(alert.trigger_type, "FINANCIAL_THRESHOLD")
        self.assertTrue(self.hitl.is_paused(node_id))

    def test_compliance_gate_trigger(self):
        node_id = "node_gamma"
        alert = self.hitl.check_compliance_gate(node_id, "KYC_VERIFICATION", "Bank account verification required")
        self.assertIsNotNone(alert)
        self.assertEqual(alert.trigger_type, "COMPLIANCE_LEGAL")
        self.assertTrue(self.hitl.is_paused(node_id))


if __name__ == "__main__":
    unittest.main()
