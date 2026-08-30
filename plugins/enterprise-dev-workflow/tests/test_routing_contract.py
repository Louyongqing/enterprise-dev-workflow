"""Test package and evaluation invariants, never exact instruction prose."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from scripts.validate_routing_contract import validate_plugin_contract

SKILLS = ("brainstorming", "dispatching-parallel-agents", "enterprise-delivery",
          "model-routing", "project-verification", "requesting-code-review",
          "security-review", "subagent-driven-development", "systematic-debugging",
          "test-driven-development", "verification-before-completion", "writing-plans")


class RoutingContractTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for name in SKILLS:
            self.write(f"skills/{name}/SKILL.md", f"---\nname: {name}\ndescription: Fixture.\n---\n# Workflow\n")
            value = "true" if name == "enterprise-delivery" else "false"
            self.write(f"skills/{name}/agents/openai.yaml", f"policy:\n  allow_implicit_invocation: {value}\n")
        self.cases = [{
            "id": "routine-example", "prompt": "Update an isolated calculation.",
            "expected_level": "L1", "minimum_level": "L1",
            "required_skills": ["enterprise-delivery", "project-verification"],
            "forbidden_default_skills": ["brainstorming"],
            "required_outcomes": ["Verify the changed calculation."],
        }]
        self.save()

    def write(self, relative, content):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def save(self):
        self.write("evals/routing-cases.json", json.dumps(self.cases))

    def errors(self):
        return validate_plugin_contract(self.root)

    def test_valid_extensible_case_set(self):
        self.assertEqual([], self.errors())

    def test_rephrased_skill_is_still_valid(self):
        self.write("skills/model-routing/SKILL.md", "# Equivalent workflow with different prose\n")
        self.assertEqual([], self.errors())

    def test_missing_skill_file(self):
        (self.root / "skills/security-review/SKILL.md").unlink()
        self.assertTrue(self.errors())

    def test_extra_skill(self):
        self.write("skills/unapproved/SKILL.md", "extra")
        self.assertTrue(self.errors())

    def test_router_must_be_implicit(self):
        self.write("skills/enterprise-delivery/agents/openai.yaml", "policy:\n  allow_implicit_invocation: false\n")
        self.assertTrue(self.errors())

    def test_other_skill_cannot_be_implicit(self):
        self.write("skills/brainstorming/agents/openai.yaml", "policy:\n  allow_implicit_invocation: true\n")
        self.assertTrue(self.errors())

    def test_duplicate_or_invalid_policy(self):
        for value in ("false\n  allow_implicit_invocation: false", "sometimes", '"false"'):
            with self.subTest(value=value):
                self.write("skills/brainstorming/agents/openai.yaml", f"policy:\n  allow_implicit_invocation: {value}\n")
                self.assertTrue(self.errors())

    def test_existing_internal_link(self):
        self.write("skills/enterprise-delivery/SKILL.md", "[Verify](../project-verification/SKILL.md)\n")
        self.assertEqual([], self.errors())

    def test_policy_value_in_wrong_section_is_rejected(self):
        self.write("skills/brainstorming/agents/openai.yaml", "interface:\n  allow_implicit_invocation: false\npolicy:\n  other: true\n")
        self.assertTrue(self.errors())

    def test_second_invalid_policy_value_cannot_be_ignored(self):
        self.write("skills/brainstorming/agents/openai.yaml", "policy:\n  allow_implicit_invocation: false\n  allow_implicit_invocation: invalid\n")
        self.assertTrue(self.errors())

    def test_nested_or_block_scalar_policy_key_is_rejected(self):
        for field in ("other:", "description: |"):
            with self.subTest(field=field):
                self.write("skills/brainstorming/agents/openai.yaml", f"policy:\n  {field}\n    allow_implicit_invocation: false\n")
                self.assertTrue(self.errors())

    def test_missing_or_escaping_links(self):
        for link in ("../not-here/SKILL.md", "../../../../outside.md"):
            with self.subTest(link=link):
                self.write("skills/enterprise-delivery/SKILL.md", f"[Target]({link})\n")
                self.assertTrue(self.errors())

    def test_malformed_json(self):
        self.write("evals/routing-cases.json", "{bad")
        self.assertTrue(self.errors())

    def test_bad_shapes_do_not_crash(self):
        for value in (None, 5, "text", {}, {"id": []}, {"id": {"nested": 1}}):
            with self.subTest(value=value):
                self.write("evals/routing-cases.json", json.dumps([value]))
                self.assertTrue(self.errors())

    def test_duplicate_ids(self):
        self.cases.append(dict(self.cases[0]))
        self.save()
        self.assertTrue(self.errors())

    def test_empty_cases(self):
        self.cases = []
        self.save()
        self.assertTrue(self.errors())

    def test_unknown_conflicting_or_duplicate_skills(self):
        for field, value in (
            ("required_skills", ["missing"]),
            ("forbidden_default_skills", ["enterprise-delivery"]),
            ("required_skills", ["enterprise-delivery", "enterprise-delivery"]),
        ):
            with self.subTest(field=field, value=value):
                old = self.cases[0][field]
                self.cases[0][field] = value
                self.save()
                self.assertTrue(self.errors())
                self.cases[0][field] = old

    def test_empty_or_invalid_outcomes(self):
        for value in ([], [""], "outcome", [False]):
            with self.subTest(value=value):
                self.cases[0]["required_outcomes"] = value
                self.save()
                self.assertTrue(self.errors())

    def test_risk_floor_cannot_be_lowered(self):
        self.cases[0].update(minimum_level="L3", expected_level="L2")
        self.save()
        self.assertTrue(self.errors())

    def test_high_risk_composite_case(self):
        self.cases[0].update(id="overlap-auth", minimum_level="L3", expected_level="L3")
        self.save()
        self.assertEqual([], self.errors())

    def test_read_only_case(self):
        self.cases[0].update(expected_level="NONE", minimum_level="NONE",
                             required_skills=[], forbidden_default_skills=["brainstorming"])
        self.save()
        self.assertEqual([], self.errors())

    def test_invalid_level(self):
        self.cases[0]["expected_level"] = "L0"
        self.save()
        self.assertTrue(self.errors())

    def test_cli_errors_without_traceback(self):
        self.write("evals/routing-cases.json", '[{"id": []}]')
        script = Path(__file__).resolve().parents[1] / "scripts/validate_routing_contract.py"
        result = subprocess.run([sys.executable, "-B", str(script), str(self.root)],
                                text=True, capture_output=True)
        self.assertEqual(1, result.returncode)
        self.assertNotIn("Traceback", result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
