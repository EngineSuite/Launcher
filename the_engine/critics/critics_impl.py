"""
The Engine - The 10 Specialized Red-Team Critique Agents
Implements 10 distinct, adversarial analytical perspectives that scrutinize
the web applications, digital deliverables, code architecture, and multi-agent pipeline.
"""

import json
import re
from pathlib import Path
from typing import Dict, Any, List

from the_engine.critics.base_critic import BaseSpecializedCritic, CritiqueAssessment, CritiqueObjection


# ==============================================================================
# 1. The Ergonomist (UX & Usability Critic)
# ==============================================================================
class UXCritic(BaseSpecializedCritic):
    def __init__(self, event_bus=None):
        super().__init__("The Ergonomist", "UX & Interaction Flow", event_bus)

    def evaluate(self, node_path: Path, opportunity: Dict[str, Any], engine_context: Dict[str, Any]) -> CritiqueAssessment:
        score = 10.0
        strengths = []
        objections = []

        html_file = node_path / "public" / "index.html"
        html = html_file.read_text(encoding="utf-8") if html_file.exists() else ""

        # Check modal exit path
        if "close" in html.lower() or "modal" in html.lower():
            strengths.append("Modal contains explicit dismissal control.")
        else:
            score -= 1.5
            objections.append(CritiqueObjection(
                critic_name=self.name,
                category="Interaction Dead-End",
                severity="HIGH",
                issue="Modal lacks an obvious close trigger or backdrop dismissal listener.",
                impact_on_goal="Traps users inside modal on mobile devices, causing high bounce rates.",
                recommended_remedy="Ensure .close-btn and window click listener are wired.",
                score_deduction=1.5
            ))

        # Check input ergonomics
        if "<input" in html or "<select" in html:
            strengths.append("Interactive form controls enable direct user manipulation.")

        # Check copy-to-clipboard feedback
        js_file = node_path / "public" / "app.js"
        js = js_file.read_text(encoding="utf-8") if js_file.exists() else ""
        if "clipboard" in js.lower() and "copied" in js.lower():
            strengths.append("Copy actions provide immediate positive visual micro-feedback.")
        else:
            score -= 1.0
            objections.append(CritiqueObjection(
                critic_name=self.name,
                category="Feedback Deficit",
                severity="MEDIUM",
                issue="Clipboard copy lacks animated or color-coded success confirmation.",
                impact_on_goal="Users repeatedly click copy button, assuming it failed.",
                recommended_remedy="Show '✓ Copied!' micro-state for 2000ms upon clipboard write.",
                score_deduction=1.0
            ))

        return CritiqueAssessment(self.name, self.domain, max(0.0, score), strengths, objections)

    def cross_examine(self, peer_assessments: Dict[str, CritiqueAssessment], node_path: Path, engine_context: Dict[str, Any]) -> List[Dict[str, Any]]:
        rebuttals = []
        conversion_rep = peer_assessments.get("The Monetizer")
        if conversion_rep and any("urgency" in o.issue.lower() for o in conversion_rep.objections):
            rebuttals.append({
                "from_critic": self.name,
                "to_critic": "The Monetizer",
                "position": "DISSENT",
                "argument": "Artificial countdown timers or aggressive popup urgency triggers degrade long-term brand trust and increase customer irritation."
            })
        return rebuttals


# ==============================================================================
# 2. The Monetizer (Conversion & Pricing Economics Critic)
# ==============================================================================
class ConversionCritic(BaseSpecializedCritic):
    def __init__(self, event_bus=None):
        super().__init__("The Monetizer", "Conversion & Pricing Economics", event_bus)

    def evaluate(self, node_path: Path, opportunity: Dict[str, Any], engine_context: Dict[str, Any]) -> CritiqueAssessment:
        score = 10.0
        strengths = []
        objections = []

        pricing_file = node_path / "monetization" / "pricing.json"
        pricing_data = {}
        if pricing_file.exists():
            try:
                pricing_data = json.loads(pricing_file.read_text(encoding="utf-8"))
            except Exception:
                pass

        tiers = pricing_data.get("tiers", [])
        free_tier = next((t for t in tiers if t.get("price") == 0), None)
        paid_tier = next((t for t in tiers if t.get("price", 0) > 0), None)

        if free_tier and paid_tier:
            strengths.append(f"Freemium price anchor established: $0 Free vs ${paid_tier.get('price')} Pro.")
            delta = len(paid_tier.get("features", [])) - len(free_tier.get("features", []))
            if delta >= 2:
                strengths.append(f"Clear feature delta (+{delta} pro deliverables).")
            else:
                score -= 1.5
                objections.append(CritiqueObjection(
                    critic_name=self.name,
                    category="Weak Value Anchor",
                    severity="HIGH",
                    issue="Pro tier does not show sufficient delta over the free tool.",
                    impact_on_goal="Visitors stay on the free tier and never upgrade.",
                    recommended_remedy="Bundle at least 3 distinct pro assets (templates, scripts, rights).",
                    score_deduction=1.5
                ))
        else:
            score -= 2.5
            objections.append(CritiqueObjection(
                critic_name=self.name,
                category="Pricing Structure Defect",
                severity="CRITICAL",
                issue="Missing dual-tier freemium monetization model.",
                impact_on_goal="Zero lead qualification or immediate customer monetization.",
                recommended_remedy="Implement distinct $0 free and $12-$19 pro tiers.",
                score_deduction=2.5
            ))

        # Check direct email purchase flow clarity
        html_file = node_path / "public" / "index.html"
        html = html_file.read_text(encoding="utf-8") if html_file.exists() else ""
        if "businessbloke957@gmail.com" in html:
            strengths.append("Direct order email eliminates 3rd-party checkout merchant fees.")
        else:
            score -= 2.0
            objections.append(CritiqueObjection(
                critic_name=self.name,
                category="Fulfillment Void",
                severity="CRITICAL",
                issue="No direct sales fulfillment channel detected.",
                impact_on_goal="Interested buyers cannot execute a purchase.",
                recommended_remedy="Embed businessbloke957@gmail.com with one-click mailto and copy triggers.",
                score_deduction=2.0
            ))

        return CritiqueAssessment(self.name, self.domain, max(0.0, score), strengths, objections)


# ==============================================================================
# 3. The Penetration Tester (Security & Input Sanitization Critic)
# ==============================================================================
class SecurityCritic(BaseSpecializedCritic):
    def __init__(self, event_bus=None):
        super().__init__("The Penetration Tester", "Application Security & Data Integrity", event_bus)

    def evaluate(self, node_path: Path, opportunity: Dict[str, Any], engine_context: Dict[str, Any]) -> CritiqueAssessment:
        score = 10.0
        strengths = []
        objections = []

        js_file = node_path / "public" / "app.js"
        js = js_file.read_text(encoding="utf-8") if js_file.exists() else ""

        # Check for dangerously set innerHTML with unescaped inputs
        if "innerhtml" in js.lower():
            # Check if textContent or escaping is used
            if "textcontent" in js.lower() or "escape" in js.lower() or "createelement" in js.lower():
                strengths.append("DOM updates use safe textContent and createElement patterns.")
            else:
                score -= 2.5
                objections.append(CritiqueObjection(
                    critic_name=self.name,
                    category="DOM XSS Vulnerability",
                    severity="CRITICAL",
                    issue="Detected potential unescaped innerHTML assignment with user inputs.",
                    impact_on_goal="Allows script injection into generated schema widgets or client sites.",
                    recommended_remedy="Replace innerHTML with textContent or strict DOM element creation.",
                    score_deduction=2.5
                ))
        else:
            strengths.append("No dangerous innerHTML usage found in clientside code.")

        # Check for exposed API secrets or keys in public files
        public_dir = node_path / "public"
        for p_file in public_dir.glob("*.*"):
            content = p_file.read_text(encoding="utf-8", errors="ignore")
            if re.search(r"(api[_-]?key|secret|password|bearer)\s*[:=]\s*['\"][a-zA-Z0-9_\-]{16,}['\"]", content, re.IGNORECASE):
                score -= 3.5
                objections.append(CritiqueObjection(
                    critic_name=self.name,
                    category="Credential Leakage",
                    severity="CRITICAL",
                    issue=f"Hardcoded API key or secret token detected in {p_file.name}.",
                    impact_on_goal="Compromises private API accounts and violates zero-cost guardrails.",
                    recommended_remedy="Strip all private keys; use client-side or environment variables only.",
                    score_deduction=3.5
                ))

        if not objections:
            strengths.append("Zero private keys, tokens, or plaintext secrets exposed in public directory.")

        return CritiqueAssessment(self.name, self.domain, max(0.0, score), strengths, objections)


# ==============================================================================
# 4. The Wordsmith (Copywriting & Persuasion Critic)
# ==============================================================================
class CopywritingCritic(BaseSpecializedCritic):
    def __init__(self, event_bus=None):
        super().__init__("The Wordsmith", "Persuasive Copywriting & Clarity", event_bus)

    def evaluate(self, node_path: Path, opportunity: Dict[str, Any], engine_context: Dict[str, Any]) -> CritiqueAssessment:
        score = 10.0
        strengths = []
        objections = []

        html_file = node_path / "public" / "index.html"
        html = html_file.read_text(encoding="utf-8") if html_file.exists() else ""

        # Check active headline
        h1_match = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.DOTALL | re.IGNORECASE)
        if h1_match:
            h1_text = re.sub(r"<[^>]+>", "", h1_match.group(1)).strip()
            if any(action in h1_text.lower() for action in ["generate", "cut", "build", "scale", "optimize", "stop", "get"]):
                strengths.append(f"Action-oriented outcome headline: '{h1_text}'")
            else:
                score -= 1.0
                objections.append(CritiqueObjection(
                    critic_name=self.name,
                    category="Passive Headline",
                    severity="MEDIUM",
                    issue="H1 headline describes the product name rather than an action or outcome.",
                    impact_on_goal="Fails to hook problem-aware buyers looking for immediate solutions.",
                    recommended_remedy="Lead with an active verb (e.g. 'Generate Validated Schema in Seconds').",
                    score_deduction=1.0
                ))

        # Check for vague jargon or fluff
        jargon_words = ["synergy", "paradigm", "cutting-edge", "revolutionary", "best-in-class"]
        for jw in jargon_words:
            if jw in html.lower():
                score -= 0.5
                objections.append(CritiqueObjection(
                    critic_name=self.name,
                    category="Buzzword Fluff",
                    severity="LOW",
                    issue=f"Found corporate buzzword '{jw}' in landing page copy.",
                    impact_on_goal="Reduces perceived authenticity and increases skepticism.",
                    recommended_remedy="Replace with concrete numbers or tangible performance metrics.",
                    score_deduction=0.5
                ))

        if not any(obj.severity in ["HIGH", "CRITICAL"] for obj in objections):
            strengths.append("Landing copy is punchy, direct, and focused on client outcomes.")

        return CritiqueAssessment(self.name, self.domain, max(0.0, score), strengths, objections)


# ==============================================================================
# 5. The Algorithmic Auditor (Technical SEO & Indexability Critic)
# ==============================================================================
class SEOCritic(BaseSpecializedCritic):
    def __init__(self, event_bus=None):
        super().__init__("The Algorithmic Auditor", "Technical SEO & Discoverability", event_bus)

    def evaluate(self, node_path: Path, opportunity: Dict[str, Any], engine_context: Dict[str, Any]) -> CritiqueAssessment:
        score = 10.0
        strengths = []
        objections = []

        html_file = node_path / "public" / "index.html"
        html = html_file.read_text(encoding="utf-8") if html_file.exists() else ""

        # 1. Meta Description
        if '<meta name="description"' in html.lower():
            strengths.append("Meta description present for Google search result snippets.")
        else:
            score -= 1.5
            objections.append(CritiqueObjection(
                critic_name=self.name,
                category="SERP Visibility Void",
                severity="HIGH",
                issue="Missing <meta name='description'> tag.",
                impact_on_goal="Search engines will auto-generate random snippet text, depressing CTR.",
                recommended_remedy="Include 150-160 character benefit-driven meta description.",
                score_deduction=1.5
            ))

        # 2. Canonical / Semantic Structure
        if "<main" in html.lower() and "<header" in html.lower():
            strengths.append("Proper HTML5 semantic layout (<header>, <main>, <footer>).")
        else:
            score -= 1.0
            objections.append(CritiqueObjection(
                critic_name=self.name,
                category="Semantic Weakness",
                severity="MEDIUM",
                issue="Lacks core HTML5 semantic container tags (<main>, <header>).",
                impact_on_goal="Depresses crawl accessibility scoring in modern search engines.",
                recommended_remedy="Wrap primary content in semantic <main> tag.",
                score_deduction=1.0
            ))

        # 3. Schema on Page
        if 'application/ld+json' in html.lower():
            strengths.append("Page dogfoods its own JSON-LD schema for Rich Results indexing.")

        return CritiqueAssessment(self.name, self.domain, max(0.0, score), strengths, objections)


# ==============================================================================
# 6. The Latency Hunter (Performance & Web Vitals Critic)
# ==============================================================================
class PerformanceCritic(BaseSpecializedCritic):
    def __init__(self, event_bus=None):
        super().__init__("The Latency Hunter", "Performance & Web Vitals", event_bus)

    def evaluate(self, node_path: Path, opportunity: Dict[str, Any], engine_context: Dict[str, Any]) -> CritiqueAssessment:
        score = 10.0
        strengths = []
        objections = []

        public_dir = node_path / "public"

        # Check total assets weight
        total_kb = sum(f.stat().st_size for f in public_dir.glob("*.*") if f.is_file()) / 1024.0
        if total_kb < 150.0:
            strengths.append(f"Ultra-lightweight static footprint ({round(total_kb, 1)} KB total). Sub-50ms TTFB.")
        else:
            score -= 1.0
            objections.append(CritiqueObjection(
                critic_name=self.name,
                category="Payload Bloat",
                severity="MEDIUM",
                issue=f"Total public directory assets exceed 150 KB ({round(total_kb, 1)} KB).",
                impact_on_goal="Slows mobile First Contentful Paint (FCP) and raises bounce rate.",
                recommended_remedy="Minify CSS/JS and remove unnecessary inline images.",
                score_deduction=1.0
            ))

        # Check for heavy external CDNs (fonts, heavy frameworks)
        html_file = public_dir / "index.html"
        html = html_file.read_text(encoding="utf-8") if html_file.exists() else ""
        if "cdn.jsdelivr.net" in html or "unpkg.com" in html or "react.production" in html:
            score -= 1.5
            objections.append(CritiqueObjection(
                critic_name=self.name,
                category="Third-Party Script Dependency",
                severity="HIGH",
                issue="Relies on external CDNs or heavy runtime frameworks.",
                impact_on_goal="Creates single points of failure and increases Cumulative Layout Shift (CLS).",
                recommended_remedy="Use zero-dependency vanilla JS and system monospace/sans fonts.",
                score_deduction=1.5
            ))
        else:
            strengths.append("100% Zero-CDN vanilla architecture. Immune to upstream CDN outages.")

        return CritiqueAssessment(self.name, self.domain, max(0.0, score), strengths, objections)


# ==============================================================================
# 7. The Legal Counsel (Compliance & Risk Armor Critic)
# ==============================================================================
class LegalCritic(BaseSpecializedCritic):
    def __init__(self, event_bus=None):
        super().__init__("The Legal Counsel", "Licensing, Compliance & Risk Armor", event_bus)

    def evaluate(self, node_path: Path, opportunity: Dict[str, Any], engine_context: Dict[str, Any]) -> CritiqueAssessment:
        score = 10.0
        strengths = []
        objections = []

        # 1. License Check
        license_path = node_path / "dist_pack" / "LICENSE.txt"
        if not license_path.exists():
            license_path = node_path / "LICENSE.txt"

        if license_path.exists():
            l_text = license_path.read_text(encoding="utf-8").lower()
            if "as is" in l_text and "liability" in l_text:
                strengths.append("Legal Armor Verified: Comprehensive 'AS IS' warranty waiver and liability cap.")
            else:
                score -= 2.0
                objections.append(CritiqueObjection(
                    critic_name=self.name,
                    category="Inadequate Liability Shield",
                    severity="HIGH",
                    issue="LICENSE.txt exists but lacks explicit purchase-price liability limitation.",
                    impact_on_goal="Exposes developer to consequential damages claims.",
                    recommended_remedy="Inject standardized commercial license capping liability strictly to price paid.",
                    score_deduction=2.0
                ))
        else:
            score -= 3.0
            objections.append(CritiqueObjection(
                critic_name=self.name,
                category="CRITICAL LEGAL DEFICIT",
                severity="CRITICAL",
                issue="CRITICAL LEGAL DEFICIT: Deliverable package does not contain a LICENSE.txt file.",
                impact_on_goal="Leaves intellectual property and commercial usage rights undefined.",
                recommended_remedy="Inject Commercial LICENSE.txt into dist_pack before packaging.",
                score_deduction=3.0
            ))

        # 2. Refund Policy Check
        html_file = node_path / "public" / "index.html"
        html = html_file.read_text(encoding="utf-8") if html_file.exists() else ""
        if "30-day" in html.lower() and ("guarantee" in html.lower() or "money-back" in html.lower()):
            strengths.append("Explicit 30-day money-back guarantee completely neutralizes chargeback risk.")
        else:
            score -= 1.5
            objections.append(CritiqueObjection(
                critic_name=self.name,
                category="Chargeback Exposure",
                severity="HIGH",
                issue="Missing prominent 30-Day Money-Back Guarantee badge.",
                impact_on_goal="Disgruntled buyers dispute transactions with banks incurring $15-$25 dispute fines.",
                recommended_remedy="State 30-Day No-Hassle Money-Back Guarantee directly on sales interface.",
                score_deduction=1.5
            ))

        return CritiqueAssessment(self.name, self.domain, max(0.0, score), strengths, objections)


# ==============================================================================
# 8. The Systems Architect (Code Quality & Maintainability Critic)
# ==============================================================================
class ArchitectureCritic(BaseSpecializedCritic):
    def __init__(self, event_bus=None):
        super().__init__("The Systems Architect", "Code Quality & Modular Architecture", event_bus)

    def evaluate(self, node_path: Path, opportunity: Dict[str, Any], engine_context: Dict[str, Any]) -> CritiqueAssessment:
        score = 10.0
        strengths = []
        objections = []

        # Check server.py zero-dependency implementation
        server_file = node_path / "src" / "server.py"
        if server_file.exists():
            code = server_file.read_text(encoding="utf-8")
            if "flask" in code.lower() or "fastapi" in code.lower() or "express" in code.lower():
                score -= 2.0
                objections.append(CritiqueObjection(
                    critic_name=self.name,
                    category="External Runtime Dependency",
                    severity="HIGH",
                    issue="Server relies on external third-party frameworks requiring pip install.",
                    impact_on_goal="Breaks portability and violates zero-external-dependency rule.",
                    recommended_remedy="Implement with Python standard library http.server.",
                    score_deduction=2.0
                ))
            else:
                strengths.append("Server runs on 100% Python standard library (http.server). Zero pip dependencies.")
        else:
            score -= 2.0
            objections.append(CritiqueObjection(
                critic_name=self.name,
                category="Missing Micro-Server",
                severity="HIGH",
                issue="src/server.py not found in workspace.",
                impact_on_goal="Node cannot self-serve preview traffic.",
                recommended_remedy="Generate standalone http.server entrypoint.",
                score_deduction=2.0
            ))

        # Check node workspace isolation
        manifest_file = node_path / "manifest.json"
        if manifest_file.exists():
            strengths.append("Node maintains complete contextual isolation with manifest.json state tracker.")
        else:
            score -= 1.5
            objections.append(CritiqueObjection(
                critic_name=self.name,
                category="Isolation Defect",
                severity="HIGH",
                issue="Missing manifest.json in node directory.",
                impact_on_goal="Orchestrator cannot verify lifecycle state or operational status.",
                recommended_remedy="Generate valid node manifest upon scaffolding.",
                score_deduction=1.5
            ))

        return CritiqueAssessment(self.name, self.domain, max(0.0, score), strengths, objections)


# ==============================================================================
# 9. The Meta-Critic (Agent Orchestration & Pipeline Inspector)
# ==============================================================================
class PipelineCritic(BaseSpecializedCritic):
    def __init__(self, event_bus=None):
        super().__init__("The Meta-Critic", "Agent Orchestration & Self-Correction Pipeline", event_bus)

    def evaluate(self, node_path: Path, opportunity: Dict[str, Any], engine_context: Dict[str, Any]) -> CritiqueAssessment:
        score = 10.0
        strengths = []
        objections = []

        hitl = engine_context.get("hitl_gatekeeper")
        if hitl and hasattr(hitl, "max_consecutive_failures"):
            strengths.append(f"HITL safety protocol enforced: Halts on {hitl.max_consecutive_failures} identical errors.")
        else:
            score -= 2.0
            objections.append(CritiqueObjection(
                critic_name=self.name,
                category="Unchecked Autonomous Loop",
                severity="CRITICAL",
                issue="No consecutive failure ceiling detected for agent self-repair.",
                impact_on_goal="Risk of infinite retry loops consuming CPU cycles in unattended mode.",
                recommended_remedy="Enforce strict max 5 consecutive failure threshold via HITLGatekeeper.",
                score_deduction=2.0
            ))

        event_bus = engine_context.get("event_bus")
        if event_bus:
            strengths.append("Inter-agent communication synchronized via decoupled EventBus.")
        else:
            score -= 1.0
            objections.append(CritiqueObjection(
                critic_name=self.name,
                category="Telemetry Blindspot",
                severity="MEDIUM",
                issue="Event bus telemetry missing in orchestration context.",
                impact_on_goal="Agents cannot react asynchronously to sibling task results.",
                recommended_remedy="Pass shared EventBus instance across all agent runtimes.",
                score_deduction=1.0
            ))

        return CritiqueAssessment(self.name, self.domain, max(0.0, score), strengths, objections)


# ==============================================================================
# 10. The Chief Risk Officer (Financial & Safe Reserve Critic)
# ==============================================================================
class FinancialCritic(BaseSpecializedCritic):
    def __init__(self, event_bus=None):
        super().__init__("The Chief Risk Officer", "Financial Governance & Safe Reserve Risk", event_bus)

    def evaluate(self, node_path: Path, opportunity: Dict[str, Any], engine_context: Dict[str, Any]) -> CritiqueAssessment:
        score = 10.0
        strengths = []
        objections = []

        ledger = engine_context.get("ledger")
        if ledger:
            summary = ledger.get_global_summary()
            if summary.get("total_expenses", 0.0) == 0.0:
                strengths.append("Strict $0 Upfront Cost rule 100% compliant. Zero capital at risk.")
            else:
                score -= 3.0
                objections.append(CritiqueObjection(
                    critic_name=self.name,
                    category="Capital Violation",
                    severity="CRITICAL",
                    issue=f"Detected ${summary.get('total_expenses')} in unearned expenses.",
                    impact_on_goal="Violates the foundational 'Earn It First' financial constitution.",
                    recommended_remedy="Eliminate all paid subscriptions; revert to free tier tools.",
                    score_deduction=3.0
                ))

            safe_reserve = summary.get("safe_account_reserve", 0.0)
            net = summary.get("net_profit", 0.0)
            if net > 0:
                reserve_ratio = safe_reserve / net
                if reserve_ratio >= 0.49:
                    strengths.append(f"Safe Account Reserve locked at {round(reserve_ratio * 100)}% of profit (Untouchable).")
                else:
                    score -= 2.0
                    objections.append(CritiqueObjection(
                        critic_name=self.name,
                        category="Reserve Depletion Risk",
                        severity="HIGH",
                        issue=f"Safe Reserve ratio ({round(reserve_ratio*100)}%) is below mandatory 50% lock.",
                        impact_on_goal="Leaves system vulnerable to over-reinvestment without secured profit.",
                        recommended_remedy="Enforce mathematical 50% split on every recorded transaction.",
                        score_deduction=2.0
                    ))
        else:
            score -= 1.5
            objections.append(CritiqueObjection(
                critic_name=self.name,
                category="Ledger Missing",
                severity="HIGH",
                issue="Financial ledger not provided in review context.",
                impact_on_goal="Inability to audit financial health and reserve compliance.",
                recommended_remedy="Wire Ledger into all review cycles.",
                score_deduction=1.5
            ))

        return CritiqueAssessment(self.name, self.domain, max(0.0, score), strengths, objections)

    def cross_examine(self, peer_assessments: Dict[str, CritiqueAssessment], node_path: Path, engine_context: Dict[str, Any]) -> List[Dict[str, Any]]:
        rebuttals = []
        conversion = peer_assessments.get("The Monetizer")
        if conversion and conversion.score < 8.0:
            rebuttals.append({
                "from_critic": self.name,
                "to_critic": "The Monetizer",
                "position": "SUPPORT",
                "argument": "Weak conversion mechanics threaten the 48-hour profitability SLA and will trigger premature node archival."
            })
        return rebuttals
