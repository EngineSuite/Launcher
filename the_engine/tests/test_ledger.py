"""Tests for Financial Ledger and Zero-Cost Guardrails"""
import unittest
import tempfile
import shutil
from pathlib import Path

from the_engine.core.ledger import Ledger


class TestLedger(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.ledger_file = Path(self.temp_dir) / "test_ledger.json"
        self.ledger = Ledger(ledger_path=self.ledger_file)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_initial_state_zero_capital(self):
        self.assertEqual(self.ledger.data["initial_capital"], 0.0)
        self.assertEqual(self.ledger.data["earned_balance"], 0.0)
        self.assertEqual(self.ledger.data["total_revenue"], 0.0)
        self.assertEqual(self.ledger.data["total_expenses"], 0.0)
        self.assertEqual(self.ledger.data["reinvestable_balance"], 0.0)
        self.assertEqual(self.ledger.data["safe_account_reserve"], 0.0)

    def test_zero_cost_blocks_unearned_spending(self):
        """Must forbid spending when no revenue has been earned."""
        self.assertFalse(self.ledger.can_spend(5.00))
        with self.assertRaises(PermissionError):
            self.ledger.record_expense(
                node_id="node_test",
                amount=5.00,
                category="API_COST",
                description="Unauthorized spend"
            )

    def test_revenue_allocation_and_reinvestment(self):
        """Revenue should split 50% to reserve and 50% to reinvestable balance."""
        tx = self.ledger.record_revenue(
            node_id="node_test",
            amount=20.00,
            source="Gumroad",
            description="Test sale"
        )
        self.assertEqual(tx["reserve_allocation"], 10.00)
        self.assertEqual(tx["reinvest_allocation"], 10.00)
        self.assertEqual(self.ledger.data["total_revenue"], 20.00)
        self.assertEqual(self.ledger.data["safe_account_reserve"], 10.00)
        self.assertEqual(self.ledger.data["reinvestable_balance"], 10.00)

        # Now spending within the 50% reinvestable pool is permitted
        self.assertTrue(self.ledger.can_spend(5.00))
        exp = self.ledger.record_expense(
            node_id="node_test",
            amount=5.00,
            category="INFRA",
            description="Permitted reinvestment"
        )
        self.assertEqual(exp["amount"], 5.00)
        self.assertEqual(self.ledger.data["total_expenses"], 5.00)
        self.assertEqual(self.ledger.data["reinvestable_balance"], 5.00)
        # Safe reserve must remain completely untouched!
        self.assertEqual(self.ledger.data["safe_account_reserve"], 10.00)


if __name__ == "__main__":
    unittest.main()
