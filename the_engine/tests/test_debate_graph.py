"""
Unit and Integration Tests for Parallel Debate Graph (Tri-Chamber DAG Deliberation Engine)
Validates:
1. Concurrent Fan-Out evaluation across 10 specialized Red-Team lenses.
2. Anti-Obsolescence Sentinel auditing technical, commercial, and legal rot.
3. P0 Hard-Veto Circuit Breakers for security exploits and compliance failures.
4. Pareto-Weighted Concession negotiation for soft performance/conversion trade-offs.
5. Dynamic telemetry grounding with real ledger balance and live measured cloud latency.
6. Full Council Decree synthesis and schema compliance.
"""

import unittest
import tempfile
import shutil
from pathlib import Path
import time

from the_engine.critics.debate_engine import ParallelDebateGraph
from the_engine.critics.schemas import (
    StructuredIssue,
    ConcessionRecord,
    DebateRoundPayload,
    AntiObsolescenceAudit,
    CouncilDecree
)
from the_engine.critics.critics_impl import (
    UXCritic,
    ConversionCritic,
    SecurityCritic,
    CopywritingCritic,
    SEOCritic,
    PerformanceCritic,
    LegalCritic,
    ArchitectureCritic,
    PipelineCritic,
    FinancialCritic
)
from the_engine.core.event_bus import EventBus
from the_engine.core.hitl import HITLGatekeeper
from the_engine.core.ledger import Ledger


class TestParallelDebateGraph(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.workspace = Path(self.temp_dir) / "node_schemacraft_pro"
        self.public_dir = self.workspace / "public"
        self.src_dir = self.workspace / "src"
        self.mon_dir = self.workspace / "monetization"
        self.dist_dir = self.workspace / "dist_pack"

        self.public_dir.mkdir(parents=True)
        self.src_dir.mkdir(parents=True)
        self.mon_dir.mkdir(parents=True)
        self.dist_dir.mkdir(parents=True)

        self.event_bus = EventBus()
        self.hitl = HITLGatekeeper()

        # Instantiate 10 specialized critics
        self.critics = [
            UXCritic(event_bus=self.event_bus),
            ConversionCritic(event_bus=self.event_bus),
            SecurityCritic(event_bus=self.event_bus),
            CopywritingCritic(event_bus=self.event_bus),
            SEOCritic(event_bus=self.event_bus),
            PerformanceCritic(event_bus=self.event_bus),
            LegalCritic(event_bus=self.event_bus),
            ArchitectureCritic(event_bus=self.event_bus),
            PipelineCritic(event_bus=self.event_bus),
            FinancialCritic(event_bus=self.event_bus)
        ]

        self.debate_graph = ParallelDebateGraph(critics=self.critics, event_bus=self.event_bus)

        # Build clean, modern, compliant node assets
        (self.public_dir / "index.html").write_text("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
          <meta charset="UTF-8">
          <meta name="viewport" content="width=device-width, initial-scale=1.0">
          <title>SchemaCraft Pro - High-Converting Schema Generator</title>
          <meta name="description" content="Generate validated JSON-LD schema markup for Google Search in seconds.">
          <link rel="stylesheet" href="styles.css">
        </head>
        <body>
          <header><h1>Generate Validated Schema Markup in Seconds</h1></header>
          <main>
            <canvas id="preview-canvas" width="400" height="200"></canvas>
            <div id="generator">Interactive Free Utility</div>
            <div class="pro-features">
              <p>Bulk CSV generation and agency embed rights.</p>
            </div>
            <div class="direct-order">
              <p>Email businessbloke957@gmail.com to order.</p>
              <p>30-Day Money-Back Guarantee included.</p>
            </div>
          </main>
          <footer><p>&copy; 2026 SchemaCraft Pro</p></footer>
          <script src="app.js"></script>
        </body>
        </html>
        """, encoding="utf-8")

        (self.public_dir / "styles.css").write_text("""
        body { display: flex; flex-direction: column; font-family: sans-serif; }
        main { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
        """, encoding="utf-8")

        (self.public_dir / "app.js").write_text("""
        const canvas = document.getElementById('preview-canvas');
        if (canvas) {
            const ctx = canvas.getContext('2d');
            ctx.fillStyle = '#0070f3';
            ctx.fillRect(10, 10, 100, 100);
        }
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
        (self.dist_dir / "LICENSE.txt").write_text("THE SOFTWARE IS PROVIDED 'AS IS' WITHOUT WARRANTY. LIMITATION OF LIABILITY TO PURCHASE PRICE.", encoding="utf-8")

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_fanout_concurrency_and_performance(self):
        """Verifies concurrent Fan-Out evaluation across all 10 lenses completes in parallel."""
        ledger = Ledger(ledger_path=Path(self.temp_dir) / "ledger.json")
        ctx = {"ledger": ledger, "live_cloud_latency": {"schemacraft": 130.0}}

        t0 = time.time()
        assessments = self.debate_graph.execute_fanout_evaluation(
            node_path=self.workspace,
            opportunity={"name": "SchemaCraft Pro"},
            engine_context=ctx
        )
        elapsed = (time.time() - t0) * 1000

        self.assertEqual(len(assessments), 10)
        self.assertIn("The Penetration Tester", assessments)
        self.assertIn("The Latency Hunter", assessments)
        self.assertIn("The Legal Counsel", assessments)
        self.assertIn("The Chief Risk Officer", assessments)
        self.assertLess(elapsed, 2000.0, f"Fanout took too long: {elapsed}ms")

    def test_anti_obsolescence_sentinel_modern(self):
        """Audits modern capabilities against decay and validates freshness index."""
        audit = self.debate_graph.run_anti_obsolescence_audit(self.workspace)

        self.assertIsInstance(audit, AntiObsolescenceAudit)
        self.assertGreaterEqual(audit.composite_freshness_index, 8.5)
        self.assertEqual(audit.legal_governance_score, 10.0)
        self.assertIn("Modern CSS Grid/Flexbox Layout", audit.modern_capabilities_detected)
        self.assertIn("Mobile-First Viewport Standard", audit.modern_capabilities_detected)
        self.assertIn("Native Client-Side HTML5 Canvas Engine", audit.modern_capabilities_detected)
        self.assertIn("Active Outcome Headline (High-Converting)", audit.modern_capabilities_detected)
        self.assertIn("Strict AS-IS Warranty Disclaimer", audit.modern_capabilities_detected)

    def test_anti_obsolescence_sentinel_rot_detection(self):
        """Validates detection of obsolete 2010-era patterns (jQuery, passive titles, missing AS-IS)."""
        rot_dir = Path(self.temp_dir) / "rot_node"
        (rot_dir / "public").mkdir(parents=True)
        (rot_dir / "dist_pack").mkdir(parents=True)

        (rot_dir / "public" / "index.html").write_text("""
        <html>
        <head><title>Tool</title></head>
        <body>
          <h1>Schema Generator</h1>
          <p>Synergy and paradigm shift in tech.</p>
          <script src="http://code.jquery.com/jquery-1.9.1.js"></script>
        </body>
        </html>
        """, encoding="utf-8")
        (rot_dir / "public" / "styles.css").write_text("body { margin: 0; }", encoding="utf-8")
        (rot_dir / "dist_pack" / "LICENSE.txt").write_text("Standard MIT License without liability disclaimer.", encoding="utf-8")

        audit = self.debate_graph.run_anti_obsolescence_audit(rot_dir)

        self.assertLess(audit.composite_freshness_index, 7.0)
        self.assertTrue(any("Legacy Render-Blocking" in obs for obs in audit.detected_obsolete_patterns))
        self.assertTrue(any("Passive Product Name H1" in obs for obs in audit.detected_obsolete_patterns))
        self.assertTrue(any("Dated Buzzword" in obs for obs in audit.detected_obsolete_patterns))
        self.assertTrue(any("Missing AS-IS Warranty" in obs for obs in audit.detected_obsolete_patterns))

    def test_p0_hard_veto_security_circuit_breaker(self):
        """Verifies that an arbitrary script injection / innerHTML triggers a non-negotiable P0 hard veto."""
        # Inject dangerous innerHTML exploit into app.js
        (self.public_dir / "app.js").write_text("""
        const userCode = location.search.substring(1);
        document.getElementById('output').innerHTML = userCode;
        """, encoding="utf-8")

        ledger = Ledger(ledger_path=Path(self.temp_dir) / "ledger.json")
        ctx = {"ledger": ledger}

        decree = self.debate_graph.run_dag_deliberation(
            node_path=self.workspace,
            opportunity={"name": "SchemaCraft Pro"},
            engine_context=ctx
        )

        self.assertTrue(decree.has_hard_veto)
        self.assertEqual(decree.consensus_score, 0.0)
        self.assertEqual(decree.council_verdict, "VETOED_P0_HARD_BLOCK")
        self.assertEqual(decree.council_status, "CRITICAL_DEFECT_BLOCKING_DEPLOYMENT")
        self.assertGreater(len(decree.hard_vetoes), 0)
        self.assertEqual(decree.hard_vetoes[0]["severity_tier"], "P0")
        self.assertEqual(decree.hard_vetoes[0]["critic_name"], "The Penetration Tester")

    def test_p0_hard_veto_legal_circuit_breaker(self):
        """Verifies missing AS-IS warranty disclaimer triggers an immediate compliance veto."""
        # Wipe the LICENSE.txt file
        (self.dist_dir / "LICENSE.txt").write_text("Use freely.", encoding="utf-8")

        ledger = Ledger(ledger_path=Path(self.temp_dir) / "ledger.json")
        ctx = {"ledger": ledger}

        decree = self.debate_graph.run_dag_deliberation(
            node_path=self.workspace,
            opportunity={"name": "SchemaCraft Pro"},
            engine_context=ctx
        )

        self.assertTrue(decree.has_hard_veto)
        self.assertEqual(decree.consensus_score, 0.0)
        self.assertEqual(decree.council_verdict, "VETOED_P0_HARD_BLOCK")
        self.assertEqual(decree.hard_vetoes[0]["critic_name"], "The Legal Counsel")

    def test_pareto_weighted_concession_negotiation(self):
        """Verifies soft trade-off negotiation between Latency Hunter and Monetizer."""
        # Inject substantial CSS payload to trigger performance critique (> 150 KB)
        large_css = "/* bloat */\n" + (".cls { margin: 0; }\n" * 10000)
        (self.public_dir / "styles.css").write_text(large_css, encoding="utf-8")

        assessments = self.debate_graph.execute_fanout_evaluation(
            node_path=self.workspace,
            opportunity={"name": "SchemaCraft Pro"},
            engine_context={}
        )

        telemetry = {
            "real_ledger": {"reinvestable_balance": 150.0},
            "measured_cloud_latency_ms": {"schemacraft": 185.0}
        }

        debate_payload = self.debate_graph._run_speed_vs_conversion_debate(assessments, telemetry)

        self.assertEqual(debate_payload.thread_name, "Speed_vs_Conversion")
        self.assertEqual(debate_payload.resolution, "CONCEDED_WITH_OPTIMIZATION")
        self.assertIsNotNone(debate_payload.concession)
        self.assertEqual(debate_payload.concession.offering_critic, "The Latency Hunter")
        self.assertEqual(debate_payload.concession.benefiting_critic, "The Monetizer")
        self.assertFalse(debate_payload.concession.is_p0_breach)
        self.assertIn("185.0ms", debate_payload.concession.tolerated_penalty_metric)

    def test_dynamic_telemetry_grounding(self):
        """Verifies the CRO and Auditor inspect real telemetry rather than hallucinating numbers."""
        ledger = Ledger(ledger_path=Path(self.temp_dir) / "ledger.json")
        ledger.record_revenue(
            node_id="node_schemacraft_pro",
            amount=50.0,
            source="Gumroad",
            description="Verified sale"
        )

        telemetry = {
            "real_ledger": ledger.get_global_summary(),
            "measured_cloud_latency_ms": {"schemacraft": 129.5}
        }

        # Safe reserve should be 50% ($25.00)
        self.assertEqual(telemetry["real_ledger"]["safe_account_reserve"], 25.0)

        assessments = self.debate_graph.execute_fanout_evaluation(
            node_path=self.workspace,
            opportunity={"name": "SchemaCraft Pro"},
            engine_context={"ledger": ledger}
        )

        spend_debate = self.debate_graph._run_spend_vs_growth_debate(assessments, telemetry)
        self.assertEqual(spend_debate.resolution, "CHALLENGE_WITHDRAWN")
        self.assertIn("$25.00", spend_debate.binding_directive)

    def test_full_decree_synthesis_and_serialization(self):
        """Verifies complete Council Decree conforms to dataclass contract and serializes to dict."""
        ledger = Ledger(ledger_path=Path(self.temp_dir) / "ledger.json")
        decree = self.debate_graph.run_dag_deliberation(
            node_path=self.workspace,
            opportunity={"name": "SchemaCraft Pro"},
            engine_context={"ledger": ledger, "live_cloud_latency": {"schemacraft": 130.0}}
        )

        self.assertIsInstance(decree, CouncilDecree)
        self.assertFalse(decree.has_hard_veto)
        self.assertGreaterEqual(decree.consensus_score, 8.5)
        self.assertEqual(decree.council_verdict, "APPROVED_BY_COUNCIL")
        self.assertIn("Commercial_Chamber", decree.chamber_breakdown)
        self.assertIn("Technical_Chamber", decree.chamber_breakdown)
        self.assertIn("Governance_Chamber", decree.chamber_breakdown)

        as_dict = decree.to_dict()
        self.assertEqual(as_dict["node_id"], "node_schemacraft_pro")
        self.assertEqual(as_dict["council_size"], 10)
        self.assertIn("anti_obsolescence_audit", as_dict)
        self.assertIn("parallel_debate_threads", as_dict)


if __name__ == "__main__":
    unittest.main()
