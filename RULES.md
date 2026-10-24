# Rules

1. Do not make up relevance judgments, query text, chunk IDs, or corpus facts.
2. A document is relevant only when the supplied qrels mark it relevant.
3. Report metric denominators and cutoffs clearly.
4. Queries with no relevance judgments are excluded from aggregate relevance metrics and counted separately.
5. Duplicate retrieved IDs are reported and counted only at their first rank for ranking metrics.
6. This is an offline evaluator; it does not connect to or modify a vector database.
