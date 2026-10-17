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
        format_header(f"10-Agent Red-Team Critique Council :: Deliberation for {args.node_id}")
        node_path = orchestrator.isolation_mgr.get_node_path(args.node_id)
        manifest = orchestrator.isolation_mgr.read_manifest(args.node_id) or {}
        opp = manifest.get("metadata", {})
        decree = orchestrator.critic.council.convene_council(
            node_path=node_path,
            opportunity=opp,
            engine_context={"ledger": orchestrator.ledger}
        )

        print(f"Council Size     : {decree['council_size']} Specialized Red-Team Agents")
        print(f"Consensus Score  : {decree['consensus_score']}/10")
        print(f"Council Verdict  : {decree['council_verdict']} ({decree['council_status']})")
        print(f"Total Objections : {decree['total_objections']} (Critical Vetoes: {decree['critical_vetoes']})")
        print("-" * 70)

        print("🏛️ Individual Critic Assessments:")
        for name, data in decree["critic_breakdown"].items():
            status_icon = "✓" if data["score"] >= 8.0 else ("⚠" if data["score"] >= 6.5 else "❌")
            print(f"  {status_icon} {name:<24} | Score: {data['score']:>4.1f}/10 | Domain: {data['domain']}")
            for obj in data["objections"]:
                print(f"     ↳ [{obj['severity']}] {obj['category']}: {obj['issue']}")

        if decree["autonomous_debates"]:
            print("\n⚔️ Autonomous Inter-Agent Debates & Cross-Examinations:")
            for d in decree["autonomous_debates"]:
                print(f"  • [{d['position']}] {d['from_critic']} ➔ {d['to_critic']}:")
                print(f"    \"{d['argument']}\"")

        print("\n🎯 Prioritized Action Directives for System Betterment:")
        for directive in decree["prioritized_action_directives"]:
            print(f"  • {directive}")

        print("=" * 70 + "\n")
    elif args.command == "daemon":
        orchestrator.start_daemon(interval_seconds=args.interval, max_cycles=args.cycles)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
