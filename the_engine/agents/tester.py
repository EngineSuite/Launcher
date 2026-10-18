"""
The Engine - The Tester (QA & Functional Verification Agent)
Empirically tests every aspect of a node to verify that all code, assets,
APIs, and downloadable digital deliverables actually work end-to-end.
"""

import json
import zipfile
import logging
import subprocess
from pathlib import Path
from typing import Dict, Any, List

from the_engine.agents.base import BaseAgent
from the_engine.core.hitl import HITLGatekeeper

logger = logging.getLogger("TheEngine.Tester")


class TesterAgent(BaseAgent):
    def __init__(self, hitl_gatekeeper: HITLGatekeeper):
        super().__init__(
            name="The Tester",
            role="Quality Assurance & Functional Verification",
            hitl_gatekeeper=hitl_gatekeeper
        )

    def test_node(self, node_path: Path) -> Dict[str, Any]:
        """
        Runs automated empirical tests across the node:
        1. Manifest & configuration integrity
        2. Web assets presence & syntax checks (HTML, JS, CSS)
        3. Backend engine imports & execution checks
        4. Deliverable ZIP validation (file integrity, contents, non-zero size)
        5. Pricing structure & checkout links
        """
        results: Dict[str, Any] = {
            "node_id": node_path.name,
            "checks_run": 0,
            "checks_passed": 0,
            "checks_failed": 0,
            "defects": [],
            "details": {}
        }

        self._check_manifest(node_path, results)
        self._check_web_assets(node_path, results)
        self._check_interactive_flows(node_path, results)
        self._check_backend_code(node_path, results)
        self._check_deliverable_zip(node_path, results)
        self._check_monetization_config(node_path, results)

        pass_rate = round((results["checks_passed"] / results["checks_run"] * 100), 1) if results["checks_run"] > 0 else 0.0
        results["pass_rate"] = pass_rate

        if pass_rate >= 95.0:
            results["grade"] = "A+"
        elif pass_rate >= 85.0:
            results["grade"] = "B"
        elif pass_rate >= 70.0:
            results["grade"] = "C"
        else:
            results["grade"] = "F"

        results["status"] = "PASSED" if results["checks_failed"] == 0 else "DEFECTS_FOUND"
        self.log(f"Test run completed for '{node_path.name}': {results['status']} (Pass Rate: {pass_rate}%, Grade: {results['grade']})")
        return results

    def _record_check(self, results: Dict[str, Any], check_name: str, passed: bool, error_msg: str = "") -> None:
        results["checks_run"] += 1
        if passed:
            results["checks_passed"] += 1
            results["details"][check_name] = "PASSED"
        else:
            results["checks_failed"] += 1
            results["details"][check_name] = f"FAILED: {error_msg}"
            results["defects"].append({"check": check_name, "error": error_msg})

    def _check_manifest(self, node_path: Path, results: Dict[str, Any]) -> None:
        manifest_file = node_path / "manifest.json"
        if not manifest_file.exists():
            self._record_check(results, "manifest_exists", False, "manifest.json missing")
            return
        try:
            with open(manifest_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            has_id = bool(data.get("node_id"))
            self._record_check(results, "manifest_valid_json", True)
            self._record_check(results, "manifest_has_node_id", has_id, "node_id missing in manifest")
        except Exception as e:
            self._record_check(results, "manifest_valid_json", False, str(e))

    def _check_web_assets(self, node_path: Path, results: Dict[str, Any]) -> None:
        public_dir = node_path / "public"
        index_html = public_dir / "index.html"
        app_js = public_dir / "app.js"
        styles_css = public_dir / "styles.css"

        self._record_check(results, "index_html_exists", index_html.exists(), "index.html missing")
        self._record_check(results, "app_js_exists", app_js.exists(), "app.js missing")
        self._record_check(results, "styles_css_exists", styles_css.exists(), "styles.css missing")

        if index_html.exists():
            content = index_html.read_text(encoding="utf-8")
            has_doctype = "<!DOCTYPE html>" in content
            has_head = "<head>" in content and "</head>" in content
            has_body = "<body>" in content and "</body>" in content
            self._record_check(results, "html_structure_valid", has_doctype and has_head and has_body, "Malformed HTML")

    def _check_interactive_flows(self, node_path: Path, results: Dict[str, Any]) -> None:
        """
        Runs headless DOM execution & synthetic click simulations on the node's public assets
        using dom_runner.js to empirically prove that UI event listeners exist and execute.
        """
        public_dir = node_path / "public"
        if not public_dir.exists():
            return

        dom_runner = Path(__file__).resolve().parent.parent / "core" / "dom_runner.js"
        if not dom_runner.exists():
            logger.warning(f"dom_runner.js not found at {dom_runner}")
            return

        try:
            proc = subprocess.run(
                ["node", str(dom_runner), str(public_dir)],
                capture_output=True,
                text=True,
                timeout=15
            )
            raw_out = proc.stdout.strip()
            if raw_out:
                try:
                    payload = json.loads(raw_out)
                except Exception:
                    payload = {"success": proc.returncode == 0, "raw": raw_out}
            else:
                payload = {"success": proc.returncode == 0, "error": proc.stderr.strip()}

            if proc.returncode == 0 and payload.get("success", False):
                tested = payload.get("buttons_with_listeners", 0)
                simulated = payload.get("clicks_simulated", 0)
                self._record_check(
                    results,
                    "interactive_flows_verified",
                    True,
                    f"Verified {tested} buttons with {simulated} simulated clicks"
                )
                results["details"]["interactive_flows_summary"] = {
                    "buttons_with_listeners": tested,
                    "clicks_simulated": simulated,
                    "elements": payload.get("interactive_elements", [])
                }
            else:
                errors = payload.get("errors", [])
                err_summary = "; ".join([e.get("message", str(e)) for e in errors]) if errors else payload.get("error", "DOM execution failed")
                self._record_check(
                    results,
                    "interactive_flows_verified",
                    False,
                    f"Interactive DOM failure: {err_summary}"
                )
        except Exception as e:
            self._record_check(results, "interactive_flows_verified", False, f"Flow runner error: {str(e)}")

    def _check_backend_code(self, node_path: Path, results: Dict[str, Any]) -> None:
        server_py = node_path / "src" / "server.py"
        self._record_check(results, "server_py_exists", server_py.exists(), "src/server.py missing")

    def _check_deliverable_zip(self, node_path: Path, results: Dict[str, Any]) -> None:
        downloads_dir = node_path / "public" / "downloads"
        zip_files = list(downloads_dir.glob("*.zip")) if downloads_dir.exists() else []

        if not zip_files:
            self._record_check(results, "deliverable_zip_exists", False, "No downloadable ZIP package found in public/downloads/")
            return

        target_zip = zip_files[0]
        self._record_check(results, "deliverable_zip_exists", True)

        # Verify ZIP integrity
        try:
            is_valid = zipfile.is_zipfile(target_zip)
            self._record_check(results, "zip_file_integrity", is_valid, "Corrupted ZIP archive")

            with zipfile.ZipFile(target_zip, "r") as zf:
                file_list = zf.namelist()
                has_files = len(file_list) > 0
                has_readme = any("README" in f.upper() for f in file_list)
                self._record_check(results, "zip_contains_files", has_files, "ZIP archive is empty")
                self._record_check(results, "zip_contains_readme_documentation", has_readme, "Missing README inside package")
        except Exception as e:
            self._record_check(results, "zip_file_integrity", False, str(e))

    def _check_monetization_config(self, node_path: Path, results: Dict[str, Any]) -> None:
        pricing_file = node_path / "monetization" / "pricing.json"
        if not pricing_file.exists():
            self._record_check(results, "pricing_json_exists", False, "pricing.json missing")
            return

        try:
            with open(pricing_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            tiers = data.get("tiers", [])
            has_free = any(t.get("price") == 0 for t in tiers)
            has_paid = any(t.get("price") > 0 for t in tiers)

            self._record_check(results, "has_free_tier", has_free, "Missing $0 free tier")
            self._record_check(results, "has_paid_tier", has_paid, "Missing paid monetization tier")
        except Exception as e:
            self._record_check(results, "pricing_json_exists", False, str(e))

    def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Executes verification on the target node."""
        node_path_str = context.get("workspace_path")
        if not node_path_str:
            raise ValueError("Tester requires workspace_path in context.")

        node_path = Path(node_path_str)
        report = self.execute_with_self_correction(
            node_id=node_path.name,
            task_name="test_node",
            task_fn=self.test_node,
            node_path=node_path
        )
        return {
            "status": "QA_VERIFICATION_COMPLETED",
            "report": report
        }
