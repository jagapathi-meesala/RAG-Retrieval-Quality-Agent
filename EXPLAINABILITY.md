# Explainability

## Decision
The agent compares ranked retrieval results with supplied relevance judgments. It computes Precision@k, Recall@k, Reciprocal Rank, and nDCG@k and emits rule-based diagnostics for duplicates, missing judgments, and absent expected evidence.

## Inputs
The agent accepts a JSON evaluation file containing queries, ranked retrieved IDs, relevance judgments, and an optional list of expected evidence IDs per query. Relevance judgments use integer grades, where values greater than zero count as relevant.

## Limits
The results depend on the completeness and correctness of the supplied judgments. The evaluator does not inspect document text, validate the corpus, measure generated answer faithfulness, or determine whether the relevance labels are unbiased. Metrics describe only the evaluated queries and retrieval cutoff.
