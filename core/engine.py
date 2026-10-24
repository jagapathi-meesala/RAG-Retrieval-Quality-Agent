"""Deterministic offline metrics for ranked retrieval results."""
from __future__ import annotations
import math

LIMITATIONS = [
    "Metrics depend on the supplied relevance judgments and their completeness.",
    "This evaluator does not inspect document text or generated answers.",
    "Results apply only to the supplied query set and cutoff.",
]

def _unique_in_rank_order(ids):
    seen, result, duplicates = set(), [], []
    for item in ids:
        if item in seen:
            duplicates.append(item)
        else:
            seen.add(item)
            result.append(item)
    return result, duplicates

def evaluate_query(query, k=5, relevance_threshold=1):
    findings = []
    if not isinstance(query, dict):
        return {"query_id": None, "status": "invalid_input", "metrics": {}, "findings": [{"rule_id":"IN-000","severity":"error","message":"Query entry must be an object."}]}
    qid = query.get("query_id")
    retrieved = query.get("retrieved")
    relevance = query.get("relevance")
    if not isinstance(qid, str) or not qid.strip():
        findings.append({"rule_id":"IN-001","severity":"error","message":"query_id must be a non-empty string."})
    if not isinstance(retrieved, list) or any(not isinstance(x, str) or not x.strip() for x in (retrieved if isinstance(retrieved, list) else [])):
        findings.append({"rule_id":"IN-002","severity":"error","message":"retrieved must be a list of non-empty string IDs."})
        retrieved = []
    if not isinstance(relevance, dict) or any(not isinstance(v, int) or isinstance(v, bool) or v < 0 for v in (relevance.values() if isinstance(relevance, dict) else [])):
        findings.append({"rule_id":"IN-003","severity":"error","message":"relevance must map IDs to non-negative integer grades."})
        relevance = {}
    if any(f["severity"] == "error" for f in findings):
        return {"query_id": qid if isinstance(qid, str) else None, "status":"invalid_input", "metrics":{}, "findings":findings}
    ranked, duplicates = _unique_in_rank_order(retrieved)
    if duplicates:
        findings.append({"rule_id":"RET-001","severity":"warning","message":"Duplicate retrieved IDs found; only first occurrence counts in ranking metrics.","evidence":{"duplicate_ids":duplicates}})
    if not relevance:
        findings.append({"rule_id":"JUD-001","severity":"warning","message":"No relevance judgments supplied; query excluded from aggregate relevance metrics."})
        return {"query_id":qid,"status":"issues_found","metrics":{},"findings":findings,"judged":False}
    relevant = {doc_id for doc_id, grade in relevance.items() if grade >= relevance_threshold}
    top = ranked[:k]
    hits = sum(1 for doc_id in top if relevance.get(doc_id, 0) >= relevance_threshold)
    precision = hits / k
    recall = (hits / len(relevant)) if relevant else None
    rr = 0.0
    for rank, doc_id in enumerate(ranked, start=1):
        if relevance.get(doc_id, 0) >= relevance_threshold:
            rr = 1.0 / rank
            break
    dcg = sum((2 ** relevance.get(doc_id, 0) - 1) / math.log2(rank + 1) for rank, doc_id in enumerate(top, start=1))
    ideal_grades = sorted(relevance.values(), reverse=True)[:k]
    idcg = sum((2 ** grade - 1) / math.log2(rank + 1) for rank, grade in enumerate(ideal_grades, start=1))
    ndcg = dcg / idcg if idcg else None
    expected = query.get("expected_evidence_ids", [])
    coverage = None
    if not isinstance(expected, list) or any(not isinstance(x, str) for x in expected):
        findings.append({"rule_id":"IN-004","severity":"error","message":"expected_evidence_ids must be a list of string IDs when provided."})
    elif expected:
        found = [x for x in expected if x in top]
        coverage = len(set(found)) / len(set(expected)) if set(expected) else 1.0
        missing = [x for x in expected if x not in top]
        if missing:
            findings.append({"rule_id":"EVD-001","severity":"warning","message":"Some expected evidence IDs are absent from the top-k results.","evidence":{"missing_ids":missing,"k":k}})
    metrics = {"precision_at_k":precision,"recall_at_k":recall,"reciprocal_rank":rr,"ndcg_at_k":ndcg}
    if coverage is not None:
        metrics["expected_evidence_coverage_at_k"] = coverage
    return {"query_id":qid,"status":"error" if any(f["severity"]=="error" for f in findings) else ("issues_found" if findings else "passed"),"metrics":metrics,"findings":findings,"judged":True,"relevant_count":len(relevant)}

def evaluate_dataset(data, k=5, relevance_threshold=1):
    if not isinstance(data, dict) or not isinstance(data.get("queries"), list):
        return {"agent":"RAG Retrieval Quality Agent","status":"error","k":k,"summary":{"query_count":0,"judged_query_count":0,"unjudged_query_count":0},"per_query":[],"aggregate_metrics":{},"findings":[{"rule_id":"IN-100","severity":"error","message":"Input must be an object containing a queries list."}],"limitations":LIMITATIONS}
    per_query = [evaluate_query(q, k, relevance_threshold) for q in data["queries"]]
    judged = [q for q in per_query if q.get("judged") and q.get("metrics")]
    metric_names = ("precision_at_k","recall_at_k","reciprocal_rank","ndcg_at_k","expected_evidence_coverage_at_k")
    aggregate = {}
    for name in metric_names:
        vals = [q["metrics"][name] for q in judged if name in q["metrics"] and q["metrics"][name] is not None]
        if vals:
            aggregate[name] = sum(vals) / len(vals)
    findings = []
    for q in per_query:
        findings.extend([dict(f, query_id=q.get("query_id")) for f in q.get("findings", [])])
    errors = sum(1 for f in findings if f["severity"] == "error")
    warnings = sum(1 for f in findings if f["severity"] == "warning")
    status = "error" if errors else ("issues_found" if warnings else "passed")
    return {"agent":"RAG Retrieval Quality Agent","status":status,"k":k,"relevance_threshold":relevance_threshold,
        "summary":{"query_count":len(per_query),"judged_query_count":len(judged),"unjudged_query_count":sum(1 for q in per_query if q.get("judged") is False),"error_count":errors,"warning_count":warnings},
        "aggregate_metrics":aggregate,"per_query":per_query,"findings":findings,
        "metric_definitions":{"precision_at_k":"relevant unique IDs in top-k divided by k; missing ranks count as non-relevant","recall_at_k":"relevant unique IDs in top-k divided by all relevant IDs in supplied judgments","reciprocal_rank":"1/rank of first relevant unique retrieved ID, or 0","ndcg_at_k":"DCG/ideal DCG using gain 2^grade - 1 and discount log2(rank + 1)"},
        "limitations":LIMITATIONS}
