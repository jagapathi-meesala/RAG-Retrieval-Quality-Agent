import unittest
from core.engine import evaluate_query, evaluate_dataset

class TestRetrievalMetrics(unittest.TestCase):
    def test_perfect_precision_recall(self):
        q = {"query_id":"q1","retrieved":["a","b"],"relevance":{"a":1,"b":1}}
        metrics = evaluate_query(q, k=2)["metrics"]
        self.assertEqual(metrics["precision_at_k"], 1.0)
        self.assertEqual(metrics["recall_at_k"], 1.0)
        self.assertEqual(metrics["reciprocal_rank"], 1.0)
        self.assertAlmostEqual(metrics["ndcg_at_k"], 1.0)
    def test_reciprocal_rank(self):
        q = {"query_id":"q1","retrieved":["x","b"],"relevance":{"b":1}}
        self.assertEqual(evaluate_query(q, k=2)["metrics"]["reciprocal_rank"], 0.5)
    def test_duplicates_only_count_once(self):
        q = {"query_id":"q1","retrieved":["a","a","b"],"relevance":{"a":1,"b":1}}
        result = evaluate_query(q, k=2)
        self.assertEqual(result["metrics"]["precision_at_k"], 1.0)
        self.assertTrue(any(f["rule_id"] == "RET-001" for f in result["findings"]))
    def test_unjudged_query_excluded(self):
        report = evaluate_dataset({"queries":[{"query_id":"q1","retrieved":["a"],"relevance":{}}]}, k=1)
        self.assertEqual(report["summary"]["unjudged_query_count"], 1)
        self.assertEqual(report["aggregate_metrics"], {})
    def test_expected_evidence_coverage(self):
        q = {"query_id":"q1","retrieved":["a","b"],"relevance":{"a":1},"expected_evidence_ids":["a","c"]}
        result = evaluate_query(q, k=2)
        self.assertEqual(result["metrics"]["expected_evidence_coverage_at_k"], 0.5)
        self.assertTrue(any(f["rule_id"] == "EVD-001" for f in result["findings"]))

if __name__ == "__main__":
    unittest.main()
