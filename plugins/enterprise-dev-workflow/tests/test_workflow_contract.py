"""Test package and workflow-case invariants, never exact instruction prose."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.validate_workflow_contract import EXPECTED_SKILLS, validate_plugin_contract


class WorkflowContractTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for name in EXPECTED_SKILLS:
            self.write(f"skills/{name}/SKILL.md", f"---\nname: {name}\ndescription: Fixture.\n---\n# Workflow\n")
            value = "true" if name == "enterprise-delivery" else "false"
            self.write(f"skills/{name}/agents/openai.yaml", f"policy:\n  allow_implicit_invocation: {value}\n")
        self.cases = [{
            "id": "small-change",
            "prompt": "Update an isolated calculation.",
            "required_routes": ["enterprise-delivery", "verification"],
            "forbidden_routes": ["backend-architecture"],
            "required_outcomes": ["Verify the changed calculation."],
            "forbidden_outcomes": ["Refactor unrelated modules."],
        }]
        self.save()

    def write(self, relative, content):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def save(self):
        self.write("evals/workflow-cases.json", json.dumps(self.cases))

    def errors(self):
        return validate_plugin_contract(self.root)

    def test_valid_extensible_case_set(self):
        self.assertEqual([], self.errors())

    def test_rephrased_skill_is_still_valid(self):
        self.write("skills/code-quality/SKILL.md", "# Equivalent workflow with different prose\n")
        self.assertEqual([], self.errors())

    def test_missing_or_extra_skill(self):
        (self.root / "skills/code-quality/SKILL.md").unlink()
        self.assertTrue(self.errors())
        self.write("skills/unapproved/SKILL.md", "extra")
        self.assertTrue(self.errors())

    def test_only_enterprise_delivery_is_implicit(self):
        self.write("skills/enterprise-delivery/agents/openai.yaml", "policy:\n  allow_implicit_invocation: false\n")
        self.assertTrue(self.errors())
        self.write("skills/enterprise-delivery/agents/openai.yaml", "policy:\n  allow_implicit_invocation: true\n")
        self.write("skills/scope-control/agents/openai.yaml", "policy:\n  allow_implicit_invocation: true\n")
        self.assertTrue(self.errors())

    def test_duplicate_invalid_or_misplaced_policy(self):
        values = (
            "policy:\n  allow_implicit_invocation: false\n  allow_implicit_invocation: false\n",
            "policy:\n  allow_implicit_invocation: sometimes\n",
            "interface:\n  allow_implicit_invocation: false\npolicy:\n  other: true\n",
        )
        for value in values:
            with self.subTest(value=value):
                self.write("skills/code-quality/agents/openai.yaml", value)
                self.assertTrue(self.errors())

    def test_existing_internal_link(self):
        self.write("skills/enterprise-delivery/SKILL.md", "[Verify](../verification/SKILL.md)\n")
        self.assertEqual([], self.errors())

    def test_missing_or_escaping_link(self):
        for link in ("../not-here/SKILL.md", "../../../../outside.md"):
            with self.subTest(link=link):
                self.write("skills/enterprise-delivery/SKILL.md", f"[Target]({link})\n")
                self.assertTrue(self.errors())

    def test_malformed_or_empty_case_file(self):
        for value in ("{bad", "[]", "{}"):
            with self.subTest(value=value):
                self.write("evals/workflow-cases.json", value)
                self.assertTrue(self.errors())

    def test_bad_case_shapes_do_not_crash(self):
        for value in (None, 5, "text", {}, {"id": []}, {"id": {"nested": 1}}):
            with self.subTest(value=value):
                self.write("evals/workflow-cases.json", json.dumps([value]))
                self.assertTrue(self.errors())

    def test_duplicate_ids(self):
        self.cases.append(dict(self.cases[0]))
        self.save()
        self.assertTrue(self.errors())

    def test_unknown_conflicting_or_duplicate_routes(self):
        variants = (
            ("required_routes", ["missing"]),
            ("forbidden_routes", ["enterprise-delivery"]),
            ("required_routes", ["enterprise-delivery", "enterprise-delivery"]),
        )
        for field, value in variants:
            with self.subTest(field=field, value=value):
                old = self.cases[0][field]
                self.cases[0][field] = value
                self.save()
                self.assertTrue(self.errors())
                self.cases[0][field] = old

    def test_empty_or_invalid_outcomes(self):
        for field in ("required_outcomes", "forbidden_outcomes"):
            for value in ([], [""], "outcome", [False]):
                with self.subTest(field=field, value=value):
                    self.cases[0][field] = value
                    self.save()
                    self.assertTrue(self.errors())
            self.cases[0][field] = ["restored"]

    def test_removed_contract_language_is_rejected(self):
        self.write("README.md", "Classify this task as L2.")
        self.assertTrue(self.errors())

    def test_cli_errors_without_traceback(self):
        self.write("evals/workflow-cases.json", '[{"id": []}]')
        script = Path(__file__).resolve().parents[1] / "scripts/validate_workflow_contract.py"
        result = subprocess.run([sys.executable, "-B", str(script), str(self.root)], text=True, capture_output=True)
        self.assertEqual(1, result.returncode)
        self.assertNotIn("Traceback", result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
