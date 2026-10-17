"""
The Engine - The Editor (Content & UX Brand Guardian Agent)
Audits, filters, and sanitizes public HTML and marketing copy.
Removes internal engine jargon, technical leaks, and unwanted operational data.
Ensures customer-facing pages exclusively display high-converting, value-focused information.
"""

import re
import logging
from pathlib import Path
from typing import Dict, Any, List, Tuple

from the_engine.agents.base import BaseAgent
from the_engine.core.hitl import HITLGatekeeper

logger = logging.getLogger("TheEngine.Editor")


class EditorAgent(BaseAgent):
    """
    The Editor inspects customer-facing web surfaces to:
    1. Filter out internal jargon, engine scaffolding, technical leaks, and redundant text.
    2. Enforce the presence of high-converting, essential customer-centric information.
    3. Provide clear explanations of WHAT information should be shown and WHY.
    """

    # Unwanted information and internal leaks that must NOT appear on user-facing pages
    LEAK_PATTERNS = [
        (
            r"the engine",
            "Internal Engine Branding",
            "CRITICAL",
            "Buyers do not need to know about the internal orchestration framework. It creates confusion and dilutes product branding."
        ),
        (
            r"zero-cost infrastructure",
            "Internal Operational Strategy",
            "HIGH",
            "Highlighting '$0 cost infrastructure' makes the software appear amateur or cheap rather than professional and reliable."
        ),
        (
            r"node_[a-z0-9_]+",
            "Internal Node Directory Identifier",
            "CRITICAL",
            "Internal filesystem IDs should never leak into client-facing HTML or UI components."
        ),
        (
            r"100% free tier compliant",
            "Internal Framework Constraint",
            "HIGH",
            "Emphasizing free-tier compliance shifts buyer attention to infrastructure limits rather than enterprise reliability."
        ),
        (
            r"downloads/[a-z0-9_\-]+\.zip",
            "Exposed Public Download Link",
            "CRITICAL",
            "Direct links to the paid bundle allow visitors to bypass payment and download deliverables for free."
        ),
        (
            r"gumroad\.com|stripe\.com|payhip\.com",
            "Third-Party Checkout Redirect",
            "HIGH",
            "Redirecting to third-party processors conflicts with the direct email fulfillment model and incurs unnecessary platform fees."
        ),
        (
            r"lorem ipsum|todo:|\[placeholder\]",
            "Unfinished / Mock Content",
            "CRITICAL",
            "Placeholder copy signals incomplete or broken work, destroying buyer confidence immediately."
        ),
        (
            r"hitl|gatekeeper|scout agent|builder agent",
            "Autonomous Multi-Agent Jargon",
            "HIGH",
            "Internal agent terminology should never leak into external product copy."
        )
    ]

    # Required buyer information and the strategic rationale for WHY it must be displayed
    ESSENTIAL_INFO_RULES = {
        "headline_outcome": {
            "title": "Primary Outcome Headline",
            "what_to_display": "A clear, active headline stating the exact outcome (e.g. 'Rank Higher on Google with Validated Schema in Seconds').",
            "why_display": "Visitors decide whether to stay within 5 seconds. If the headline explains technical specs instead of the outcome, bounce rate skyrockets."
        },
        "feature_benefit_mapping": {
            "title": "Feature-to-Benefit Value Proposition",
            "what_to_display": "Distinct bullet points translating technical assets into business value (e.g. 'Bulk CSV generation saves 10+ agency hours per client').",
            "why_display": "Features tell, but benefits sell. Buyers need rational justification for why the paid package is worth their money."
        },
        "order_instructions": {
            "title": "Direct Fulfillment & Ordering Clarity",
            "what_to_display": "Exact email address (businessbloke957@gmail.com), accepted payment options (PayPal, Wire, Wise, Crypto), and dispatch turnaround (under 1 hour).",
            "why_display": "Without an automated cart, customers need 100% clarity on how their payment is handled and how quickly they receive their files."
        },
        "risk_reversal": {
            "title": "Risk Reversal (Guarantee & License)",
            "what_to_display": "Explicit 30-Day No-Hassle Money-Back Guarantee and commercial usage rights.",
            "why_display": "Eliminates buyer hesitation and fear of buyer's remorse, dramatically increasing conversion rates."
        },
        "instant_free_utility": {
            "title": "Interactive Proof / Instant Utility",
            "what_to_display": "A free interactive tool or calculator accessible immediately without signup.",
            "why_display": "Proves product competence immediately and establishes goodwill before asking for a transaction."
        }
    }

    def __init__(self, hitl_gatekeeper: HITLGatekeeper):
        super().__init__(
            name="The Editor",
            role="Content & UX Brand Guardian",
            hitl_gatekeeper=hitl_gatekeeper
        )

    def audit_content(self, workspace_path: Path, auto_sanitize: bool = True) -> Dict[str, Any]:
        """
        Audits public HTML files in the node workspace.
        Detects leakages, checks essential buyer information, and sanitizes content.
        """
        node_id = workspace_path.name
        index_file = workspace_path / "public" / "index.html"

        if not index_file.exists():
            return {
                "node_id": node_id,
                "status": "FAILED",
                "error": "public/index.html not found"
            }

        html_content = index_file.read_text(encoding="utf-8")
        original_html = html_content

        # 1. Leakage & Unwanted Information Scan
        leaks_detected: List[Dict[str, str]] = []
        for pattern, label, severity, why_remove in self.LEAK_PATTERNS:
            matches = re.findall(pattern, html_content, re.IGNORECASE)
            if matches:
                leaks_detected.append({
                    "pattern": pattern,
                    "label": label,
                    "severity": severity,
                    "occurrences": len(matches),
                    "matched_sample": matches[0],
                    "why_remove": why_remove
                })

        # 2. Essential Information Evaluation
        html_lower = html_content.lower()
        essential_audit: Dict[str, Any] = {}

        # Outcome headline check
        has_h1 = "<h1" in html_lower
        essential_audit["headline_outcome"] = {
            "present": has_h1,
            "details": self.ESSENTIAL_INFO_RULES["headline_outcome"]
        }

        # Feature benefit mapping check
        has_benefits = "benefit" in html_lower or "pro-features" in html_lower or "features" in html_lower
        essential_audit["feature_benefit_mapping"] = {
            "present": has_benefits,
            "details": self.ESSENTIAL_INFO_RULES["feature_benefit_mapping"]
        }

        # Order instructions check
        has_order_email = "businessbloke957@gmail.com" in html_lower and ("email" in html_lower or "order" in html_lower)
        essential_audit["order_instructions"] = {
            "present": has_order_email,
            "details": self.ESSENTIAL_INFO_RULES["order_instructions"]
        }

        # Risk reversal check
        has_guarantee = ("30-day" in html_lower or "30 day" in html_lower) and ("guarantee" in html_lower or "money-back" in html_lower)
        essential_audit["risk_reversal"] = {
            "present": has_guarantee,
            "details": self.ESSENTIAL_INFO_RULES["risk_reversal"]
        }

        # Instant utility check
        has_utility = "generator" in html_lower or "calculator" in html_lower or "matrix" in html_lower
        essential_audit["instant_free_utility"] = {
            "present": has_utility,
            "details": self.ESSENTIAL_INFO_RULES["instant_free_utility"]
        }

        # 3. Auto-Sanitization (if requested or enabled)
        modifications_made: List[str] = []
        if auto_sanitize and leaks_detected:
            # Clean known internal engine phrases
            replacements = [
                (
                    r"Built on zero-cost infrastructure\.",
                    "High-performance architecture built for Google Search compliance."
                ),
                (
                    r"Maintained by The Engine\. 100% Free Tier Compliant\.",
                    "Engineered by CloudZero • Verified Production Architecture."
                ),
                (
                    r"Built on zero-cost infrastructure",
                    "Enterprise-grade reliability"
                )
            ]
            for target_pattern, replacement in replacements:
                if re.search(target_pattern, html_content, re.IGNORECASE):
                    html_content = re.sub(target_pattern, replacement, html_content, flags=re.IGNORECASE)
                    modifications_made.append(f"Sanitized '{target_pattern}' -> '{replacement}'")

            if html_content != original_html:
                index_file.write_text(html_content, encoding="utf-8")
                self.log(f"Auto-sanitized {len(modifications_made)} internal leak(s) in {index_file.name}")

        # Compute Scoring
        leak_penalty = sum(2.0 if l["severity"] == "CRITICAL" else 1.0 for l in leaks_detected)
        missing_essential_penalty = sum(1.5 for k, v in essential_audit.items() if not v["present"])

        content_quality_score = max(0.0, min(10.0, 10.0 - leak_penalty - missing_essential_penalty))
        verdict = "APPROVED" if (content_quality_score >= 8.0 and not any(l["severity"] == "CRITICAL" for l in leaks_detected)) else "REQUIRES_SANITIZATION"

        report = {
            "node_id": node_id,
            "agent": self.name,
            "content_quality_score": round(content_quality_score, 1),
            "verdict": verdict,
            "leaks_found": len(leaks_detected),
            "leaks_details": leaks_detected,
            "essential_information_audit": essential_audit,
            "sanitization_modifications": modifications_made,
            "recommendations": self._generate_recommendations(leaks_detected, essential_audit)
        }

        return report

    def _generate_recommendations(self, leaks: List[Dict[str, str]], essential: Dict[str, Any]) -> List[Dict[str, str]]:
        recs = []
        for leak in leaks:
            recs.append({
                "action": "REMOVE",
                "item": leak["label"],
                "reason": leak["why_remove"]
            })

        for key, audit in essential.items():
            if not audit["present"]:
                recs.append({
                    "action": "DISPLAY",
                    "item": audit["details"]["title"],
                    "what": audit["details"]["what_to_display"],
                    "reason": audit["details"]["why_display"]
                })

        return recs

    def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Runs content audit on the provided node workspace."""
        workspace_path_str = context.get("workspace_path")
        if not workspace_path_str:
            raise ValueError("Editor requires 'workspace_path' in context.")

        workspace_path = Path(workspace_path_str)
        auto_sanitize = context.get("auto_sanitize", True)

        report = self.execute_with_self_correction(
            node_id=workspace_path.name,
            task_name="content_audit",
            task_fn=self.audit_content,
            workspace_path=workspace_path,
            auto_sanitize=auto_sanitize
        )

        return {
            "status": "CONTENT_AUDIT_COMPLETED",
            "report": report
        }
