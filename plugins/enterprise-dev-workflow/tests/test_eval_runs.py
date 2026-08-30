import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.summarize_eval_runs import summarize_runs


def record(variant, **changes):
    value = dict(case_id="calculation-1", variant=variant, fixture_id="fixture-a",
                 environment="isolated-python", requested_model="requested-model",
                 actual_model="reported-model", outcome="PASS", evidence=["reviewed-log"],
                 elapsed_seconds=2.0, input_tokens=80, output_tokens=20, rework_cycles=0)
    value.update(changes)
    return value


class EvalRunTests(unittest.TestCase):
    def test_measured_passing_pair(self):
        result = summarize_runs([record("baseline"), record("candidate", input_tokens=40, output_tokens=10)])
        self.assertEqual(1, result["comparable_pairs"])
        self.assertEqual(50.0, result["token_reduction_percent"])

    def test_unknown_tokens_are_not_zero(self):
        result = summarize_runs([record("baseline"), record("candidate", input_tokens=None)])
        self.assertIsNone(result["variants"]["candidate"]["total_tokens"])
        self.assertIsNone(result["token_reduction_percent"])

    def test_unknown_model_blocks_savings_claim(self):
        result = summarize_runs([record("baseline"), record("candidate", actual_model=None)])
        self.assertIsNone(result["token_reduction_percent"])

    def test_failed_quality_blocks_savings_claim(self):
        result = summarize_runs([record("baseline"), record("candidate", outcome="FAIL", input_tokens=1)])
        self.assertIsNone(result["token_reduction_percent"])

    def test_unverified_quality_blocks_savings_claim(self):
        result = summarize_runs([record("baseline"), record("candidate", outcome="NOT VERIFIED")])
        self.assertIsNone(result["token_reduction_percent"])

    def test_unmatched_environment_or_fixture_blocks_comparison(self):
        for field in ("environment", "fixture_id", "case_id"):
            with self.subTest(field=field):
                result = summarize_runs([record("baseline"), record("candidate", **{field: "different"})])
                self.assertIsNone(result["token_reduction_percent"])

    def test_missing_arm_is_not_a_comparison(self):
        self.assertIsNone(summarize_runs([record("candidate")])["token_reduction_percent"])

    def test_zero_baseline_is_not_divided(self):
        result = summarize_runs([record("baseline", input_tokens=0, output_tokens=0), record("candidate")])
        self.assertIsNone(result["token_reduction_percent"])

    def test_increased_tokens_are_reported_honestly(self):
        result = summarize_runs([record("baseline"), record("candidate", input_tokens=180)])
        self.assertEqual(-100.0, result["token_reduction_percent"])

    def test_bad_metrics_are_rejected(self):
        for value in (-1, True, "20", float("nan"), float("inf"), 0.5):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    summarize_runs([record("baseline", input_tokens=value)])

    def test_bad_shapes_are_rejected(self):
        for value in (None, {}, [], [None], [{"case_id": []}]):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    summarize_runs(value)

    def test_unknown_variant_or_empty_evidence_is_rejected(self):
        for changes in ({"variant": "other"}, {"evidence": []}, {"evidence": [False]}):
            with self.subTest(changes=changes):
                with self.assertRaises(ValueError):
                    summarize_runs([record("baseline", **changes)] if "variant" not in changes else [record("other")])

    def test_duplicate_trial_arm_is_rejected(self):
        with self.assertRaises(ValueError):
            summarize_runs([record("baseline"), record("baseline")])

    def test_partial_success_cannot_hide_failed_pairs(self):
        result = summarize_runs([record("baseline"), record("candidate"),
                                 record("baseline", case_id="second"),
                                 record("candidate", case_id="second", outcome="FAIL")])
        self.assertIsNone(result["token_reduction_percent"])

    def test_input_records_are_not_modified(self):
        records = [record("baseline"), record("candidate")]
        before = copy.deepcopy(records)
        summarize_runs(records)
        self.assertEqual(before, records)

    def test_cli_outputs_unknown_usage_without_inventing_savings(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "records.json"
            path.write_text(json.dumps([record("candidate", input_tokens=None, output_tokens=None)]), encoding="utf-8")
            script = Path(__file__).resolve().parents[1] / "scripts/summarize_eval_runs.py"
            result = subprocess.run([sys.executable, "-B", str(script), str(path)], text=True, capture_output=True)
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertIsNone(json.loads(result.stdout)["token_reduction_percent"])

    def test_cli_rejects_malformed_input(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "records.json"
            path.write_text("{invalid", encoding="utf-8")
            script = Path(__file__).resolve().parents[1] / "scripts/summarize_eval_runs.py"
            result = subprocess.run([sys.executable, "-B", str(script), str(path)], text=True, capture_output=True)
            self.assertEqual(1, result.returncode)
            self.assertNotIn("Traceback", result.stderr)

    def test_finite_values_cannot_overflow_aggregate(self):
        with self.assertRaises(ValueError):
            summarize_runs([record("baseline", case_id="one", elapsed_seconds=1e308),
                            record("baseline", case_id="two", elapsed_seconds=1e308)])

    def test_cli_handles_aggregate_overflow_without_traceback(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "records.json"
            path.write_text(json.dumps([record("baseline", case_id="one", elapsed_seconds=1e308),
                                        record("baseline", case_id="two", elapsed_seconds=1e308)]), encoding="utf-8")
            script = Path(__file__).resolve().parents[1] / "scripts/summarize_eval_runs.py"
            result = subprocess.run([sys.executable, "-B", str(script), str(path)], text=True, capture_output=True)
            self.assertEqual(1, result.returncode)
            self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
