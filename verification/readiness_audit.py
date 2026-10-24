from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
required = [
 "agent.yaml","SOUL.md","AGENTS.md","RULES.md","DUTIES.md","EXPLAINABILITY.md","README.md",
 "requirements.txt","config/default.yaml","contracts/retrieval-evaluation.schema.json",
 "core/engine.py","core/cli.py","tools/retrieval_evaluation.yaml","tools/chunk_coverage_audit.yaml",
 "tools/ranking_diagnostics.yaml","skills/retrieval-evaluation/SKILL.md",
 "skills/chunk-coverage-audit/SKILL.md","skills/ranking-diagnostics/SKILL.md",
 "examples/evaluation.json","tests/test_engine.py"
]
missing = [x for x in required if not (ROOT / x).is_file()]
manifest_text = (ROOT / "agent.yaml").read_text(encoding="utf-8")
manifest_name = next((line.split(":", 1)[1].strip().strip('"') for line in manifest_text.splitlines() if line.startswith("name:")), "")
schema_ok = any(line.strip() == 'schema_version: "0.1.0"' for line in manifest_text.splitlines())
explain = (ROOT / "EXPLAINABILITY.md").read_text(encoding="utf-8")
headings = ["## Decision", "## Inputs", "## Limits"]
print(f"Required files: {len(required) - len(missing)}/{len(required)}")
print(f"Agent name: {manifest_name}")
print(f"Manifest schema version: {'PASS' if schema_ok else 'FAIL'}")
print(f"Explainability headings: {'PASS' if all(h in explain for h in headings) else 'FAIL'}")
if missing:
    print("Missing:", ", ".join(missing))
if missing or not schema_ok or not manifest_name or not all(h in explain for h in headings):
    sys.exit(1)
print("Readiness audit: PASS (local structural checks only; not OpenGAP/HiDevs validation)")
