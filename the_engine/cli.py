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
        format_header(f"The Critic & Strategist :: Executive Review for {args.node_id}")
        node_path = orchestrator.isolation_mgr.get_node_path(args.node_id)
        manifest = orchestrator.isolation_mgr.read_manifest(args.node_id) or {}
        opp = manifest.get("metadata", {})
        test_rep = orchestrator.tester.test_node(node_path)
        critique_rep = orchestrator.critic.review_node(node_path, opp)
        verdict = orchestrator.strategist.evaluate_and_decide(opp, test_rep, critique_rep)

        print(f"Critique Score     : {critique_rep['overall_quality_score']}/10 ({critique_rep['commercial_viability']})")
        print(f"QA Pass Rate       : {test_rep['pass_rate']}% (Grade: {test_rep['grade']})")
        print(f"Executive Decision : {verdict['executive_decision']} (Confidence: {verdict['market_confidence']})")
        print("-" * 70)
        print("Strengths Identified:")
        for s in critique_rep["strengths"]:
            print(f"  ✓ {s}")
        if critique_rep["vulnerabilities"]:
            print("\nVulnerabilities / Friction Points:")
            for v in critique_rep["vulnerabilities"]:
                print(f"  ⚠ {v}")
        if verdict["action_directives"]:
            print("\nStrategist Action Directives:")
            for a in verdict["action_directives"]:
                print(f"  • {a}")
        print("=" * 70 + "\n")
    elif args.command == "daemon":
        orchestrator.start_daemon(interval_seconds=args.interval, max_cycles=args.cycles)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
