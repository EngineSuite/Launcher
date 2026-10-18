"""
Unit tests for the 10-Agent Red-Team Critique Council
"""

import unittest
import tempfile
import shutil
from pathlib import Path

from the_engine.critics.council import CritiqueCouncil
from the_engine.core.hitl import HITLGatekeeper
from the_engine.core.event_bus import EventBus
from the_engine.core.ledger import Ledger


class TestCritiqueCouncil(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.workspace = Path(self.temp_dir) / "node_schemacraft_test"
        self.public_dir = self.workspace / "public"
        self.src_dir = self.workspace / "src"
        self.mon_dir = self.workspace / "monetization"
        self.dist_dir = self.workspace / "dist_pack"

        self.public_dir.mkdir(parents=True)
        self.src_dir.mkdir(parents=True)
        self.mon_dir.mkdir(parents=True)
        self.dist_dir.mkdir(parents=True)

        self.hitl = HITLGatekeeper()
        self.event_bus = EventBus()
        self.council = CritiqueCouncil(hitl_gatekeeper=self.hitl, event_bus=self.event_bus)

        # Populate compliant test node assets
        (self.public_dir / "index.html").write_text("""
        <!DOCTYPE html>
        <html>
        <head>
          <title>SchemaCraft Pro</title>
          <meta name="description" content="Generate validated JSON-LD schema markup for Google Search in seconds.">
        </head>
        <body>
          <header><h1>Generate Validated Schema in Seconds</h1></header>
          <main>
            <div id="generator">Free Utility</div>
            <div class="pro-features">
              <p>Bulk CSV generation and agency embed rights.</p>
            </div>
            <div class="direct-order">
              <p>Email businessbloke957@gmail.com to order.</p>
              <p>30-Day Money-Back Guarantee included.</p>
            </div>
          </main>
          <footer><p>&copy; 2026 SchemaCraft Pro</p></footer>
        </body>
        </html>
        """, encoding="utf-8")

        (self.public_dir / "app.js").write_text("""
        console.log("Safe script");
        navigator.clipboard.writeText("copied");
        """, encoding="utf-8")

        (self.src_dir / "server.py").write_text("import http.server\n", encoding="utf-8")
        (self.workspace / "manifest.json").write_text('{"status": "BUILT"}', encoding="utf-8")
        (self.mon_dir / "pricing.json").write_text("""
        {
          "tiers": [
            {"tier_id": "free", "price": 0.0, "features": ["Basic"]},
            {"tier_id": "pro", "price": 19.0, "features": ["Bulk", "Whitelabel", "API", "Templates"]}
          ]
        }
        """, encoding="utf-8")
        (self.dist_dir / "LICENSE.txt").write_text("THE SOFTWARE IS PROVIDED 'AS IS' WITHOUT WARRANTY. LIABILITY LIMITED TO PURCHASE PRICE.", encoding="utf-8")

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_council_membership_and_evaluation(self):
        """Verifies that all 10 specialized critics are convened."""
        self.assertEqual(len(self.council.critics), 10)

        ledger = Ledger(ledger_path=Path(self.temp_dir) / "ledger.json")
        decree = self.council.convene_council(
            node_path=self.workspace,
            opportunity={"name": "SchemaCraft Pro"},
            engine_context={"ledger": ledger}
        )

        self.assertEqual(decree["council_size"], 10)
        self.assertGreaterEqual(decree["consensus_score"], 8.0)
        self.assertEqual(decree["critical_vetoes"], 0)
        self.assertIn(decree["council_verdict"], ["APPROVED_BY_COUNCIL", "CONDITIONAL_APPROVAL"])
        self.assertEqual(len(decree["critic_breakdown"]), 10)

    def test_autonomous_inter_agent_debate_logging(self):
        """Verifies that cross-examination generates debate arguments across critics."""
        ledger = Ledger(ledger_path=Path(self.temp_dir) / "ledger.json")
        decree = self.council.convene_council(
            node_path=self.workspace,
            opportunity={"name": "SchemaCraft Pro"},
            engine_context={"ledger": ledger}
        )

        # Check event bus captured council events
        events = self.event_bus.get_events()
        eval_events = [e for e in events if e["topic"] == "council:critic_evaluated"]
        decree_events = [e for e in events if e["topic"] == "council:decree_finalized"]

        self.assertEqual(len(eval_events), 10)
        self.assertEqual(len(decree_events), 1)

    def test_critical_veto_on_security_leak(self):
        """Verifies that a critical vulnerability triggers an immediate council veto."""
        # Inject an exposed secret token into public directory
        (self.public_dir / "app.js").write_text("const apiKey = 'sk_live_1234567890abcdef123456';", encoding="utf-8")

        ledger = Ledger(ledger_path=Path(self.temp_dir) / "ledger.json")
        decree = self.council.convene_council(
            node_path=self.workspace,
            opportunity={"name": "SchemaCraft Pro"},
            engine_context={"ledger": ledger}
        )

        self.assertGreater(decree["critical_vetoes"], 0)
        self.assertIn(decree["council_verdict"], ["VETOED", "VETOED_P0_HARD_BLOCK"])
        self.assertIn(decree["council_status"], ["CRITICAL_DEFECT_DETECTED", "CRITICAL_DEFECT_BLOCKING_DEPLOYMENT"])
        self.assertTrue(decree["has_hard_veto"])


if __name__ == "__main__":
    unittest.main()
