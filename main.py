#!/usr/bin/env python3
"""
CLI entry point for the multi-agent financial advisor system.

Usage:
    python main.py --company "Tata Motors" --budget 100000 --duration "5 years" --risk moderate
"""
import argparse
import json
import sys
from datetime import datetime

from orchestrator import Orchestrator, UserRequest, PipelineResult


def parse_args():
    parser = argparse.ArgumentParser(
        description="Multi-agent AI financial advisor (Market/News/Risk/Portfolio/"
        "Verifier/Explainability agents orchestrated in Python)."
    )
    parser.add_argument("--company", required=True, help='e.g. "Tata Motors"')
    parser.add_argument("--budget", required=True, type=float, help="e.g. 100000")
    parser.add_argument("--duration", required=True, help='e.g. "5 years"')
    parser.add_argument(
        "--risk",
        default="moderate",
        choices=["conservative", "moderate", "aggressive"],
        help="User risk profile (default: moderate)",
    )
    parser.add_argument(
        "--save-json",
        default=None,
        help="Optional path to save the full pipeline result as JSON",
    )
    return parser.parse_args()


def render_report(result: PipelineResult) -> str:
    m, n, r, p, v, e = (
        result.market_analysis,
        result.news_analysis,
        result.risk_assessment,
        result.portfolio_recommendation,
        result.verification,
        result.explainability,
    )
    lines = []
    lines.append("=" * 70)
    lines.append(
        f"  INVESTMENT ANALYSIS: {result.request.company}"
    )
    lines.append("=" * 70)
    lines.append(
        f"Budget: {result.request.budget:,.0f} | "
        f"Duration: {result.request.duration} | "
        f"Risk Profile: {result.request.risk_profile}"
    )

    lines.append("\n--- Market Analysis " + "-" * 45)
    lines.append(m.get("market_summary", ""))
    for s in m.get("strengths", []):
        lines.append(f"  + {s}")
    for w in m.get("weaknesses", []):
        lines.append(f"  - {w}")

    lines.append("\n--- News Analysis " + "-" * 48)
    lines.append(f"Overall sentiment: {n.get('overall_sentiment', 'N/A')}")
    for pn in n.get("positive_news", []):
        lines.append(f"  + {pn}")
    for nn in n.get("negative_news", []):
        lines.append(f"  ! {nn}")

    lines.append("\n--- Risk Analysis " + "-" * 48)
    lines.append(f"Overall Risk: {r.get('overall_risk', 'N/A')}")
    lines.append(f"Risk Score: {r.get('risk_score', 'N/A')}")
    lines.append(r.get("risk_reasoning", ""))

    lines.append("\n--- Portfolio Suggestion " + "-" * 41)
    for item in p.get("allocation", []):
        lines.append(f"  {item.get('asset', ''):<25} {item.get('percentage', 0)}%")
    lines.append(f"Strategy: {p.get('expected_strategy', '')}")
    for w in p.get("warnings", []):
        lines.append(f"  ⚠ {w}")

    lines.append("\n--- Verification " + "-" * 49)
    status = "No unsupported claims detected." if v.get("verified") else "Issues detected:"
    lines.append(status)
    for issue in v.get("issues", []):
        lines.append(f"  - {issue}")
    lines.append(f"Confidence adjustment: {v.get('confidence_adjustment', 0)}")

    lines.append("\n--- Explainability " + "-" * 47)
    lines.append(e.get("summary", ""))
    lines.append("Reasoning:")
    for reason in e.get("reasoning", []):
        lines.append(f"  - {reason}")
    lines.append("Key assumptions:")
    for a in e.get("assumptions", []):
        lines.append(f"  - {a}")
    lines.append("Could change with:")
    for u in e.get("uncertainties", []):
        lines.append(f"  - {u}")

    lines.append("\n" + "=" * 70)
    lines.append(f"  FINAL CONFIDENCE: {result.final_confidence}%")
    lines.append("=" * 70)

    return "\n".join(lines)


def main():
    args = parse_args()
    request = UserRequest(
        company=args.company,
        budget=args.budget,
        duration=args.duration,
        risk_profile=args.risk,
    )

    orchestrator = Orchestrator()
    try:
        result = orchestrator.run(request)
    except Exception as exc:
        print(f"\nPipeline failed: {exc}", file=sys.stderr)
        sys.exit(1)

    print(render_report(result))

    save_path = args.save_json
    if save_path:
        payload = {
            "request": {
                "company": result.request.company,
                "budget": result.request.budget,
                "duration": result.request.duration,
                "risk_profile": result.request.risk_profile,
            },
            "market_analysis": result.market_analysis,
            "news_analysis": result.news_analysis,
            "risk_assessment": result.risk_assessment,
            "portfolio_recommendation": result.portfolio_recommendation,
            "verification": result.verification,
            "explainability": result.explainability,
            "final_confidence": result.final_confidence,
            "generated_at": datetime.utcnow().isoformat() + "Z",
        }
        with open(save_path, "w") as f:
            json.dump(payload, f, indent=2)
        print(f"\nFull JSON report saved to: {save_path}")


if __name__ == "__main__":
    main()
