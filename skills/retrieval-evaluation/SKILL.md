---
name: retrieval-evaluation
description: Evaluate ranked retrieval output using supplied relevance judgments.
---
# Retrieval Evaluation

1. Confirm each query has a stable query ID, ranked retrieved IDs, and relevance grades.
2. Calculate metrics at the explicitly requested cutoff.
3. Exclude queries with no relevance judgments from aggregate relevance metrics and count them separately.
4. Include metric definitions and caveats in the report.
