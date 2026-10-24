# RAG Retrieval Quality Agent

Offline evaluation utilities for ranked retrieval results in Retrieval-Augmented Generation (RAG) pipelines.

## Metrics and diagnostics
- Precision@k
- Recall@k
- Reciprocal Rank (per query; aggregate MRR)
- nDCG@k
- Duplicate retrieved-ID warnings
- Missing relevance-judgment warnings
- Expected-evidence coverage checks

## Quick start
```bash
python -m unittest discover -s tests -v
python verification/readiness_audit.py
python -m core.cli evaluate examples/evaluation.json --k 3 --output retrieval-quality-report.json
```

## Input format
See `examples/evaluation.json`. Each query includes `query_id`, `retrieved` (ranked IDs), `relevance` (ID-to-grade mapping), and optional `expected_evidence_ids`.

## Metric definitions
- Precision@k: relevant unique retrieved IDs in the first k ranks divided by k, treating missing ranks as non-relevant.
- Recall@k: relevant unique retrieved IDs in the first k ranks divided by the total relevant unique IDs in the supplied judgments.
- Reciprocal Rank: 1 divided by the rank of the first relevant unique retrieved ID, or 0 if none is found.
- nDCG@k: discounted cumulative gain divided by ideal DCG, using gain `2^grade - 1` and discount `log2(rank + 1)`.
- Aggregate metrics are arithmetic means over queries that have at least one relevance judgment. Recall is omitted for a query with no relevant IDs.

## Scope
This agent evaluates retrieval rankings only. It does not evaluate answer generation, factuality, latency, cost, or the underlying corpus unless those are separately measured and supplied.
