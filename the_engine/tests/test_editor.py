"""
Unit tests for The Editor (Content & UX Brand Guardian Agent)
"""

import unittest
import tempfile
import shutil
from pathlib import Path

from the_engine.agents.editor import EditorAgent
from the_engine.core.hitl import HITLGatekeeper


class TestEditorAgent(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.workspace = Path(self.temp_dir) / "node_test_product"
        self.public_dir = self.workspace / "public"
        self.public_dir.mkdir(parents=True)
        self.hitl = HITLGatekeeper()
        self.editor = EditorAgent(hitl_gatekeeper=self.hitl)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_clean_content_scores_high(self):
        """Clean, customer-centric content passes without leaks."""
        clean_html = """
        <!DOCTYPE html>
        <html>
        <head><title>MetaCraft OG - Automated Social Cards</title></head>
        <body>
          <main>
            <h1>Generate Dynamic OpenGraph Cards in Seconds</h1>
            <div class="features">
              <p>High-converting social previews with zero latency.</p>
            </div>
            <div id="generator">Interactive Free Card Generator</div>
            <div class="order-box">
              <p>To order the Agency Bundle ($19), email businessbloke957@gmail.com.</p>
              <p>30-Day Money-Back Guarantee included.</p>
            </div>
          </main>
        </body>
        </html>
        """
        (self.public_dir / "index.html").write_text(clean_html, encoding="utf-8")

        report = self.editor.audit_content(self.workspace, auto_sanitize=False)

        self.assertEqual(report["leaks_found"], 0)
        self.assertEqual(report["verdict"], "APPROVED")
        self.assertGreaterEqual(report["content_quality_score"], 8.5)
        for key, audit in report["essential_information_audit"].items():
            self.assertTrue(audit["present"], f"Expected {key} to be present")

    def test_detects_and_sanitizes_internal_leaks(self):
        """Detects internal engine phrases and automatically sanitizes them."""
        leaky_html = """
        <!DOCTYPE html>
        <html>
        <body>
          <h1>SEO Tool</h1>
          <footer>
            <p>&copy; 2026 SchemaCraft Pro. Built on zero-cost infrastructure. All rights reserved.</p>
            <p>Maintained by The Engine. 100% Free Tier Compliant.</p>
          </footer>
        </body>
        </html>
        """
        (self.public_dir / "index.html").write_text(leaky_html, encoding="utf-8")

        # Run with auto_sanitize=True
        report = self.editor.audit_content(self.workspace, auto_sanitize=True)

        self.assertGreater(report["leaks_found"], 0)
        self.assertGreater(len(report["sanitization_modifications"]), 0)

        # Check sanitized file content
        sanitized_html = (self.public_dir / "index.html").read_text(encoding="utf-8")
        self.assertNotIn("Built on zero-cost infrastructure.", sanitized_html)
        self.assertNotIn("Maintained by The Engine. 100% Free Tier Compliant.", sanitized_html)
        self.assertIn("High-performance architecture", sanitized_html)

    def test_why_and_what_guidance_generation(self):
        """Generates clear explanations for what info must be displayed and why."""
        sparse_html = "<html><body><p>Just a basic paragraph.</p></body></html>"
        (self.public_dir / "index.html").write_text(sparse_html, encoding="utf-8")

        report = self.editor.audit_content(self.workspace, auto_sanitize=False)

        self.assertEqual(report["verdict"], "REQUIRES_SANITIZATION")
        self.assertLess(report["content_quality_score"], 6.0)

        # Verify recommendations explain both WHAT to display and WHY
        recs = report["recommendations"]
        self.assertGreater(len(recs), 0)
        for r in recs:
            if r["action"] == "DISPLAY":
                self.assertIn("what", r)
                self.assertIn("reason", r)
                self.assertTrue(len(r["what"]) > 10)
                self.assertTrue(len(r["reason"]) > 10)


if __name__ == "__main__":
    unittest.main()
