---
name: chunk-coverage-audit
description: Assess whether expected evidence identifiers occur in top-k retrieval results.
---
# Chunk Coverage Audit

1. Use only supplied expected evidence IDs.
2. Check presence in the first k unique retrieved IDs.
3. Report missing IDs and the cutoff.
4. Do not infer document content from IDs.
