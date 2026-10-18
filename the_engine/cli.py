"""
The Engine - Command-Line Interface & Dashboard
Provides full administrative control over the multi-agent system.
"""

import sys
import argparse
import json
from pathlib import Path

from the_engine.core.orchestrator import Orchestrator


def format_header(title: str) -> None:
    print("\n" + "=" * 70)
    print(f"  ⚡ THE ENGINE :: {title.upper()}")
    print("=" * 70)


def cmd_status(orchestrator: Orchestrator) -> None:
    format_header("System Status & Dashboard")
    status = orchestrator.get_status()
    fin = status["financial_summary"]

    print(f"Operational Mode    : {status['mode']}")
    print(f"Financial Policy    : {status['zero_cost_policy']}")
    print(f"Total Revenue       : ${fin['total_revenue']:.2f}")
    print(f"Total Expenses      : ${fin['total_expenses']:.2f}")
    print(f"Safe Reserve        : ${fin['safe_account_reserve']:.2f} (Untouchable Profit)")
    print(f"Reinvestable Pool   : ${fin['reinvestable_balance']:.2f}")
    print(f"Zero-Cost Integrity : {'✓ 100% COMPLIANT' if fin['zero_cost_integrity'] else '❌ BREACH DETECTED'}")
    
    milestone = status.get("incorporation_milestone", {})
    m_icon = "🎉" if milestone.get("milestone_reached") else "🛡️"
    print(f"Legal / Entity Mode : {m_icon} {milestone.get('status', 'DEFERRED_INCORPORATION_ACTIVE')}")
    print(f"Incorporation Goal  : ${milestone.get('total_revenue', 0):.2f} / ${milestone.get('threshold', 1500):.2f} (Chargebacks: {milestone.get('chargeback_count', 0)})")
    print(f"Entity Guidance     : {milestone.get('recommendation', '')}")
    print("-" * 70)
    live_cloud = status.get("live_cloud")
    if live_cloud:
        c_icon = "✓" if live_cloud["overall_healthy"] else "⚠"
        print(f"Live Cloud Host     : {c_icon} {live_cloud['provider']}")
        print(f"Base Production URL : {live_cloud['base_url']}")
        print("Live Cloud Probes   :")
        for name, p in live_cloud.get("probes", {}).items():
            st = f"✓ {p['status']} OK ({p.get('latency_ms', 0)}ms)" if p.get("healthy") else f"❌ {p.get('status', 'ERROR')}"
            print(f"  • {name:<16} : {p['url']} [{st}]")
        print("-" * 70)
    print(f"Active Nodes ({status['active_node_count']}):")
    if not status["active_nodes"]:
        print("  (No nodes deployed yet. Run 'python -m the_engine run' to launch one.)")
    for nid, details in status["active_nodes"].items():
        print(f"  • {nid:<28} | Status: {details['status']:<12} | Net: ${details['net_profit']:.2f} | Neg Cycles: {details['consecutive_neg']}")
    print("=" * 70 + "\n")


def cmd_run(orchestrator: Orchestrator) -> None:
    format_header("Executing Autonomous Operational Loop")
    summary = orchestrator.run_cycle()
    print("\n✓ Cycle Completed Successfully!")
    print(f"  • Deployed Node  : {summary['node_id']}")
    print(f"  • Selected Niche : {summary['opportunity']}")
    print(f"  • Workspace Path : {summary['workspace_path']}")
    print(f"  • Audit Status   : {summary['audit_compliance']}")
    print(f"  • Checkout State : {summary['checkout_status']}")
    print(f"  • Auditor Action : {summary['evaluation_action']}")
    print("\nNext step: Run 'python -m the_engine serve " + summary['node_id'] + "' to view the live product.\n")


def cmd_scout(orchestrator: Orchestrator) -> None:
    format_header("Scout Market Intelligence Scan")
    opps = orchestrator.scout.scan_opportunities()
    print(f"Found {len(opps)} zero-upfront-cost high-probability opportunities:\n")
    for i, opp in enumerate(opps, 1):
        print(f"[{i}] {opp['name']} (Viability Score: {opp['composite_score']}/10)")
        print(f"    Category : {opp['category']}")
        print(f"    Stack    : {opp['hosting_stack']}")
        print(f"    Pricing  : Free tier: {opp['monetization']['free_tier']}")
        print(f"               Pro tier: {opp['monetization']['pro_tier']}")
        print(f"    Channels : {', '.join(opp['monetization']['platforms'])}\n")


def cmd_audit(orchestrator: Orchestrator) -> None:
    format_header("Financial & Health Audit")
    nodes = orchestrator.isolation_mgr.list_active_nodes()
    if not nodes:
        print("No active nodes to audit.")
        return
    for nid in nodes:
        audit = orchestrator.auditor.run({"node_id": nid})
        print(f"Node: {nid}")
        print(f"  • Zero-Cost Compliance : {audit['compliance']['status']}")
        print(f"  • Checkout Integrity   : {audit['checkout']['status']}")
        print(f"  • 48h Performance Eval : {audit['evaluation']['action']}")
        print(f"  • Consecutive Neg Days : {audit['evaluation']['consecutive_negative_cycles']}")
        print("-" * 50)


def cmd_record_sale(orchestrator: Orchestrator, node_id: str, amount: float, source: str) -> None:
    format_header(f"Recording Verified Sale: {node_id}")
    tx = orchestrator.ledger.record_revenue(
        node_id=node_id,
        amount=amount,
        source=source,
        description=f"Verified sale via {source}"
    )
    print(f"✓ Revenue of ${amount:.2f} logged from {source}.")
    print(f"  • 50% allocated to Safe Account Reserve: ${tx['reserve_allocation']:.2f}")
    print(f"  • 50% allocated to Reinvestable Balance: ${tx['reinvest_allocation']:.2f}")


def cmd_serve(orchestrator: Orchestrator, node_id: str, port: int = 8080) -> None:
    node_path = orchestrator.isolation_mgr.get_node_path(node_id)
    server_script = node_path / "src" / "server.py"
    if not server_script.exists():
        print(f"Error: Server script not found at {server_script}")
        sys.exit(1)

    print(f"\nStarting local zero-overhead micro-server for '{node_id}' on port {port}...")
    print(f"Visit: http://localhost:{port}\nPress Ctrl+C to terminate.\n")
    import subprocess
    subprocess.run([sys.executable, str(server_script), str(port)])


def main():
    parser = argparse.ArgumentParser(description="The Engine: Autonomous Revenue Multi-Agent System")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("status", help="Display system status and dashboard")
    subparsers.add_parser("run", help="Execute the 4-phase autonomous operational loop")
    subparsers.add_parser("scout", help="Run Scout market intelligence scan")
    subparsers.add_parser("audit", help="Run Auditor financial and health audit")

    sale_p = subparsers.add_parser("record-sale", help="Record a verified incoming sale")
    sale_p.add_argument("node_id", type=str, help="Node ID")
    sale_p.add_argument("amount", type=float, help="Sale amount in USD")
    sale_p.add_argument("--source", type=str, default="Gumroad", help="Payment source")

    serve_p = subparsers.add_parser("serve", help="Serve a node web application locally")
    serve_p.add_argument("node_id", type=str, help="Node ID to serve")
    serve_p.add_argument("--port", type=int, default=8080, help="Port (default: 8080)")

    test_p = subparsers.add_parser("test", help="Run QA verification tests on a node")
    test_p.add_argument("node_id", type=str, help="Node ID to test")

    review_p = subparsers.add_parser("review", help="Run Critic & Strategist review on a node")
    review_p.add_argument("node_id", type=str, help="Node ID to review")

    edit_p = subparsers.add_parser("audit-content", help="Run The Editor to audit, sanitize, and verify HTML content")
    edit_p.add_argument("node_id", type=str, help="Node ID to audit")
    edit_p.add_argument("--no-sanitize", action="store_true", help="Audit only without auto-modifying HTML")

    council_p = subparsers.add_parser("council", help="Convene the 10-Agent Red-Team Critique Council to scrutinize and debate a node")
    council_p.add_argument("node_id", type=str, help="Node ID to scrutinize")

    fulfill_p = subparsers.add_parser("fulfill", help="Generate license key, invoice, and dispatch email to fulfill an order")
    fulfill_p.add_argument("node_id", type=str, help="Node ID (e.g. node_schemacraft_pro)")
    fulfill_p.add_argument("buyer_email", type=str, help="Customer email address")
    fulfill_p.add_argument("--amount", type=float, default=None, help="Amount paid in USD")
    fulfill_p.add_argument("--client-name", type=str, default=None, help="Customer name")

    deploy_p = subparsers.add_parser("deploy-prep", help="Compile and optimize all active nodes into /dist for GitHub Pages / Cloudflare Pages")

    live_p = subparsers.add_parser("audit-live", help="Probe real-time health, latency, and uptime of the live cloud deployment")
    live_p.add_argument("--url", type=str, default="https://enginesuite.github.io/Launcher/", help="Base URL of production deployment")

    daemon_p = subparsers.add_parser("daemon", help="Run The Engine continuously in the background")
    daemon_p.add_argument("--interval", type=int, default=3600, help="Check interval in seconds (default: 3600)")
    daemon_p.add_argument("--cycles", type=int, default=None, help="Max cycles (default: infinite)")

    args = parser.parse_args()
    orchestrator = Orchestrator()

    if args.command == "status" or not args.command:
        cmd_status(orchestrator)
    elif args.command == "run":
        cmd_run(orchestrator)
    elif args.command == "scout":
        cmd_scout(orchestrator)
    elif args.command == "audit":
        cmd_audit(orchestrator)
    elif args.command == "record-sale":
        cmd_record_sale(orchestrator, args.node_id, args.amount, args.source)
    elif args.command == "serve":
        cmd_serve(orchestrator, args.node_id, args.port)
    elif args.command == "test":
        format_header(f"The Tester :: QA Verification for {args.node_id}")
        node_path = orchestrator.isolation_mgr.get_node_path(args.node_id)
        res = orchestrator.tester.test_node(node_path)
        print(f"Status    : {res['status']}")
        print(f"Grade     : {res['grade']} (Pass Rate: {res['pass_rate']}%)")
        print(f"Checks    : {res['checks_passed']}/{res['checks_run']} passed")
        if res["defects"]:
            print("\nDefects Found:")
            for d in res["defects"]:
                print(f"  ❌ {d['check']}: {d['error']}")
        else:
            print("\n✓ 100% of functional checks passed without defect.")
        print("=" * 70 + "\n")
    elif args.command == "review":
        format_header(f"The Critic, Editor & Strategist :: Executive Review for {args.node_id}")
        node_path = orchestrator.isolation_mgr.get_node_path(args.node_id)
        manifest = orchestrator.isolation_mgr.read_manifest(args.node_id) or {}
        opp = manifest.get("metadata", {})
        test_rep = orchestrator.tester.test_node(node_path)
        editor_rep = orchestrator.editor.audit_content(node_path, auto_sanitize=False)
        critique_rep = orchestrator.critic.review_node(
            node_path=node_path,
            opportunity=opp,
            engine_context={"ledger": orchestrator.ledger}
        )
        verdict = orchestrator.strategist.evaluate_and_decide(opp, test_rep, critique_rep, editor_report=editor_rep)

        print(f"Content Hygiene    : {editor_rep['content_quality_score']}/10 (Verdict: {editor_rep['verdict']})")
        print(f"Critique Score     : {critique_rep['overall_quality_score']}/10 ({critique_rep['commercial_viability']})")
        print(f"QA Pass Rate       : {test_rep['pass_rate']}% (Grade: {test_rep['grade']})")
        print(f"Executive Decision : {verdict['executive_decision']} (Confidence: {verdict['market_confidence']})")
        print("-" * 70)
        print("Strengths Identified:")
        for s in critique_rep["strengths"]:
            print(f"  ✓ {s}")
        if editor_rep["leaks_found"] > 0:
            print("\nContent Leaks Detected:")
            for leak in editor_rep["leaks_details"]:
                print(f"  ❌ [{leak['severity']}] {leak['label']}: '{leak['matched_sample']}'")
                print(f"     Why remove: {leak['why_remove']}")
        if critique_rep["vulnerabilities"]:
            print("\nVulnerabilities / Friction Points:")
            for v in critique_rep["vulnerabilities"]:
                print(f"  ⚠ {v}")
        if verdict["action_directives"]:
            print("\nStrategist Action Directives:")
            for a in verdict["action_directives"]:
                print(f"  • {a}")
        print("=" * 70 + "\n")
    elif args.command == "audit-content":
        format_header(f"The Editor :: Content & UX Brand Audit for {args.node_id}")
        node_path = orchestrator.isolation_mgr.get_node_path(args.node_id)
        auto_sanitize = not args.no_sanitize
        rep = orchestrator.editor.audit_content(node_path, auto_sanitize=auto_sanitize)

        print(f"Content Score : {rep['content_quality_score']}/10")
        print(f"Audit Verdict : {rep['verdict']}")
        print(f"Leaks Found   : {rep['leaks_found']}")
        print("-" * 70)

        if rep["leaks_details"]:
            print("🚫 Unwanted Information & Leaks Detected (What to Remove & Why):")
            for leak in rep["leaks_details"]:
                print(f"  • [{leak['severity']}] {leak['label']} (Count: {leak['occurrences']})")
                print(f"    Matched text : '{leak['matched_sample']}'")
                print(f"    Why hide it  : {leak['why_remove']}")
            print()
        else:
            print("✓ Zero unwanted technical leaks or internal jargon detected.\n")

        print("📋 Essential Customer Information Audit (What Should Be Shown & Why):")
        for key, item in rep["essential_information_audit"].items():
            status = "✓ PRESENT" if item["present"] else "❌ MISSING"
            print(f"  [{status}] {item['details']['title']}")
            print(f"    What to show : {item['details']['what_to_display']}")
            print(f"    Why show it  : {item['details']['why_display']}")

        if rep["sanitization_modifications"]:
            print("\n🛠️ Auto-Sanitization Actions Applied:")
            for mod in rep["sanitization_modifications"]:
                print(f"  • {mod}")

        print("=" * 70 + "\n")
    elif args.command == "council":
        format_header(f"10-Agent Red-Team Critique Council :: Tri-Chamber Deliberation for {args.node_id}")
        node_path = orchestrator.isolation_mgr.get_node_path(args.node_id)
        manifest = orchestrator.isolation_mgr.read_manifest(args.node_id) or {}
        opp = manifest.get("metadata", {})
        decree = orchestrator.critic.council.convene_council(
            node_path=node_path,
            opportunity=opp,
            engine_context={"ledger": orchestrator.ledger}
        )

        v_icon = "❌" if decree.get("has_hard_veto") else ("✓" if decree['consensus_score'] >= 8.0 else "⚠")
        print(f"Council Size     : {decree['council_size']} Specialized Red-Team Agents (Tri-Chamber Architecture)")
        print(f"DAG Fan-Out Time : {decree.get('fanout_execution_time_ms', 0)}ms (10 Concurrent Evaluation Threads)")
        print(f"Consensus Score  : {decree['consensus_score']}/10")
        print(f"Council Verdict  : {v_icon} {decree['council_verdict']} ({decree['council_status']})")
        print(f"Defect Matrix    : {decree['total_objections']} Objections (Hard P0 Vetoes: {decree.get('critical_vetoes', 0)})")
        print("-" * 70)

        # Anti-Obsolescence Sentinel Section
        audit = decree.get("anti_obsolescence_audit", {})
        if audit:
            f_idx = audit.get("composite_freshness_index", 0.0)
            f_icon = "✓" if f_idx >= 8.5 else ("⚠" if f_idx >= 7.0 else "❌")
            print(f"🛡️ Anti-Obsolescence Sentinel (Freshness Index: {f_icon} {f_idx}/10):")
            print(f"  • Modern Web Standards : {audit.get('modern_web_standards_score', 0)}/10")
            print(f"  • Commercial Relevance : {audit.get('commercial_relevance_score', 0)}/10 (2026 Standards)")
            print(f"  • Legal Governance     : {audit.get('legal_governance_score', 0)}/10 (AS-IS Armor & Caps)")
            if audit.get("modern_capabilities_detected"):
                print("  ✓ Detected Modern Capabilities:")
                for cap in audit["modern_capabilities_detected"]:
                    print(f"    • {cap}")
            if audit.get("detected_obsolete_patterns"):
                print("  ⚠ Flagged Obsolete Patterns (Must Be Modernized):")
                for obs in audit["detected_obsolete_patterns"]:
                    print(f"    • {obs}")
            print("-" * 70)

        # Tri-Chamber Breakdown
        chambers = decree.get("chamber_breakdown", {})
        if chambers:
            print("🏛️ Tri-Chamber Deliberation Scores:")
            for c_name, c_data in chambers.items():
                c_clean = c_name.replace("_", " ")
                print(f"  • {c_clean:<22} : {c_data['score']:>4.1f}/10 (Lenses: {', '.join(c_data['lenses'])})")
            print("-" * 70)

        # 1v1 Parallel Debate Threads & Pareto Concessions
        debates = decree.get("parallel_debate_threads", [])
        if debates:
            print("⚔️ Parallel 1v1 Debate Threads & Pareto-Weighted Concessions:")
            for d in debates:
                res = d.get("resolution", "")
                r_icon = "⛔" if "P0" in res else ("⚖️" if "CONCEDED" in res else "✓")
                print(f"  {r_icon} [{d['thread_name']}] {d['challenger']} ➔ {d['defendant']} ({res}):")
                print(f"    Argument : \"{d.get('rebuttal_argument', '')}\"")
                conc = d.get("concession")
                if conc:
                    print(f"    Concession: {conc.get('offering_critic')} tolerated {conc.get('tolerated_penalty_metric')} for {conc.get('gained_benefit_metric')}")
                    print(f"    Rationale : {conc.get('concession_rationale')}")
                if d.get("binding_directive"):
                    print(f"    Directive : {d.get('binding_directive')}")
            print("-" * 70)

        # P0 Hard Vetoes Banner (if triggered)
        if decree.get("has_hard_veto") and decree.get("hard_vetoes"):
            print("⛔ [CIRCUIT BREAKER ACTIVATED] P0 HARD VETOES BLOCKING DEPLOYMENT:")
            for hv in decree["hard_vetoes"]:
                print(f"  ❌ [{hv.get('severity_tier', 'P0')}] {hv.get('critic_name')} ({hv.get('category')}): {hv.get('issue')}")
                print(f"     Required Remediation: {hv.get('proposed_diff')}")
            print("-" * 70)

        print("🎯 Prioritized Action Directives for System Evolution:")
        for directive in decree["prioritized_action_directives"]:
            print(f"  • {directive}")

        print("=" * 70 + "\n")
    elif args.command == "fulfill":
        from the_engine.core.fulfiller import FulfillmentService
        format_header(f"Order Fulfillment & License Dispatch :: {args.node_id}")
        service = FulfillmentService(ledger=orchestrator.ledger, isolation_mgr=orchestrator.isolation_mgr)
        rec = service.fulfill_order(
            node_id=args.node_id,
            buyer_email=args.buyer_email,
            amount=args.amount,
            buyer_name=args.client_name
        )
        print(f"Order Reference: {rec['order_id']}")
        print(f"Product        : {rec['product_name']}")
        print(f"Delivered To   : {rec['buyer_email']}")
        print(f"License Key    : {rec['license_key']}")
        print(f"Amount Paid    : ${rec['amount_paid']:.2f} USD")
        print(f"Safe Reserve   : +${rec['ledger_split']['safe_reserve_locked']:.2f} (50% Locked Untouchable Profit)")
        print(f"Reinvestment   : +${rec['ledger_split']['reinvestment_pool']:.2f}")
        print(f"Deliverable    : {rec['deliverable_file']}")
        print("-" * 70)
        print("✉️ Ready-to-Send Email Dispatch Template (Copy & Paste to Customer):")
        print(f"Subject: {rec['email_dispatch']['subject']}\n")
        print(rec['email_dispatch']['body'])
        print("=" * 70 + "\n")
    elif args.command == "deploy-prep":
        from the_engine.core.deployer import DeploymentManager
        format_header("Static Cloud Distribution Packaging (/dist)")
        mgr = DeploymentManager()
        res = mgr.build_distribution()
        print(f"Distribution Directory : {res['dist_dir']}")
        print(f"Total Compiled Assets  : {res['total_assets_kb']} KB")
        print(f"Free Hosting Target    : {', '.join(res['free_hosting_platforms'])}")
        print("-" * 70)
        print("Active Packaged Nodes:")
        for n in res["deployed_nodes"]:
            print(f"  • {n['name']} ➔ Path: {n['path']}")
        print("\n✓ /dist is ready for instant deployment to GitHub Pages or Cloudflare Pages.")
        print("=" * 70 + "\n")
    elif args.command == "audit-live":
        format_header("The Auditor :: Live Cloud Deployment & Uptime Sentinel")
        cloud = orchestrator.auditor.probe_live_cloud_deployment(args.url)
        c_icon = "✓" if cloud["overall_healthy"] else "⚠"
        print(f"Provider       : {cloud['provider']}")
        print(f"Base URL       : {cloud['base_url']}")
        print(f"Overall Health : {c_icon} {'ALL SYSTEMS OPERATIONAL (200 OK)' if cloud['overall_healthy'] else 'INCIDENT DETECTED'}")
        print(f"Timestamp      : {cloud['probed_at']}")
        print("-" * 70)
        print("Real-Time Endpoint Probes:")
        for name, p in cloud["probes"].items():
            if p.get("healthy"):
                st = f"✓ {p['status']} OK (Latency: {p.get('latency_ms', 0)}ms)"
            else:
                st = f"❌ {p.get('status')} ({p.get('error', 'Unreachable')})"
            print(f"  • {name:<16} : {p['url']}")
            print(f"    ↳ Live Status: {st}")
        print("=" * 70 + "\n")
    elif args.command == "daemon":
        orchestrator.start_daemon(interval_seconds=args.interval, max_cycles=args.cycles)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
