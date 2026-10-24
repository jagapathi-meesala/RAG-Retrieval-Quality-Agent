"""CLI for offline RAG retrieval evaluation."""
import argparse, json
from pathlib import Path
from core.engine import evaluate_dataset

def main():
    parser = argparse.ArgumentParser(description="Evaluate ranked RAG retrieval results against relevance judgments.")
    parser.add_argument("input", help="Path to evaluation JSON")
    parser.add_argument("--k", type=int, default=5)
    parser.add_argument("--relevance-threshold", type=int, default=1)
    parser.add_argument("--output", default="retrieval-quality-report.json")
    args = parser.parse_args()
    if args.k < 1:
        parser.error("--k must be at least 1")
    if args.relevance_threshold < 0:
        parser.error("--relevance-threshold must be non-negative")
    data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    report = evaluate_dataset(data, args.k, args.relevance_threshold)
    Path(args.output).write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status":report["status"],"summary":report["summary"],"aggregate_metrics":report["aggregate_metrics"],"output":args.output}, indent=2))
    return 1 if report["status"] == "error" else 0

if __name__ == "__main__":
    raise SystemExit(main())
