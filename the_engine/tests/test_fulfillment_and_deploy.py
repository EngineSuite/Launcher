"""
Unit tests for FulfillmentService and DeploymentManager
"""

import unittest
import tempfile
import shutil
from pathlib import Path

from the_engine.core.fulfiller import FulfillmentService
from the_engine.core.deployer import DeploymentManager
from the_engine.core.ledger import Ledger
from the_engine.core.isolation import NodeIsolationManager


class TestFulfillmentAndDeploy(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.nodes_dir = Path(self.temp_dir) / "nodes"
        self.ledger_file = Path(self.temp_dir) / "ledger.json"

        self.ledger = Ledger(ledger_path=self.ledger_file)
        self.isolation_mgr = NodeIsolationManager(nodes_dir=self.nodes_dir)

        # Create a mock node
        self.node_path = self.isolation_mgr.create_node_workspace("node_test_tool", {"name": "Test Tool"})
        public_dir = self.node_path / "public"
        public_dir.mkdir(parents=True, exist_ok=True)
        (public_dir / "index.html").write_text("<html><body>Test Tool</body></html>", encoding="utf-8")
        downloads = public_dir / "downloads"
        downloads.mkdir(exist_ok=True)
        (downloads / "test-pack.zip").write_text("PK000 mock zip content", encoding="utf-8")

        self.service = FulfillmentService(ledger=self.ledger, isolation_mgr=self.isolation_mgr)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_fulfill_order_and_reserve_split(self):
        """Verifies license generation, email dispatch template, and 50% Safe Reserve lock."""
        rec = self.service.fulfill_order(
            node_id="node_test_tool",
            buyer_email="buyer@example.com",
            amount=19.0,
            buyer_name="Alice Smith"
        )

        self.assertIn("-2026-", rec["license_key"])
        self.assertTrue(rec["license_key"].endswith("-PRO"))
        self.assertEqual(rec["amount_paid"], 19.0)
        self.assertEqual(rec["ledger_split"]["safe_reserve_locked"], 9.50)
        self.assertEqual(rec["ledger_split"]["reinvestment_pool"], 9.50)
        self.assertIn("Alice Smith", rec["email_dispatch"]["body"])
        self.assertIn("businessbloke957@gmail.com", rec["email_dispatch"]["body"])

        # Check ledger reflects 50% Safe Reserve
        summary = self.ledger.get_global_summary()
        self.assertEqual(summary["total_revenue"], 19.0)
        self.assertEqual(summary["safe_account_reserve"], 9.50)
        self.assertEqual(summary["reinvestable_balance"], 9.50)

    def test_deployment_manager_builds_dist(self):
        """Verifies multi-node distribution aggregation and platform configs."""
        deployer = DeploymentManager(root_dir=Path(self.temp_dir))
        res = deployer.build_distribution()

        self.assertEqual(res["status"], "DEPLOYMENT_PACKAGE_BUILT")
        dist_dir = Path(res["dist_dir"])

        # Check files generated
        self.assertTrue((dist_dir / "index.html").exists())
        self.assertTrue((dist_dir / ".nojekyll").exists())
        self.assertTrue((dist_dir / "_headers").exists())
        self.assertTrue((dist_dir / "_redirects").exists())
        self.assertTrue((dist_dir / "test_tool" / "index.html").exists())


if __name__ == "__main__":
    unittest.main()
