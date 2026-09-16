"""Regression checks for the shareable package boundary."""
import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parents[1]
EXPECTED_SKILLS = {
    "code-quality", "enterprise-delivery", "scope-control",
    "systematic-debugging", "task-decomposition", "verification",
}


class DistributionHygieneTests(unittest.TestCase):
    def test_package_contains_only_the_six_v2_skills(self):
        actual = {
            path.name for path in (ROOT / "skills").iterdir()
            if path.is_dir() and (path / "SKILL.md").is_file()
        }
        self.assertEqual(EXPECTED_SKILLS, actual)

    def test_required_references_exist(self):
        for name in ("coding-standards.md", "comments.md", "testing.md", "task-template.md"):
            with self.subTest(name=name):
                self.assertTrue((ROOT / "references" / name).is_file())

    def test_manifest_describes_v2_scope_control(self):
        manifest = json.loads((ROOT / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
        self.assertRegex(manifest["version"], r"^2\.0\.0(?:\+codex\.[A-Za-z0-9._-]+)?$")
        rendered = json.dumps(manifest).lower()
        self.assertIn("scope", rendered)
        self.assertNotIn("model-routing", rendered)
        self.assertIsInstance(manifest["interface"]["defaultPrompt"], list)

    def test_removed_contracts_are_absent_from_shipped_text(self):
        patterns = (
            re.compile(r"\bL[123]\b"),
            re.compile("model" + "-routing", re.IGNORECASE),
            re.compile("model" + r"[ -]selection", re.IGNORECASE),
        )
        roots = (ROOT, REPO_ROOT / "README.md")
        paths = []
        for candidate in roots:
            if candidate.is_file():
                paths.append(candidate)
            else:
                paths.extend(path for path in candidate.rglob("*") if path.is_file() and path.suffix.lower() in {".md", ".json", ".yaml", ".yml"})
        for path in paths:
            text = path.read_text(encoding="utf-8")
            for pattern in patterns:
                with self.subTest(path=path.relative_to(REPO_ROOT), pattern=pattern.pattern):
                    self.assertIsNone(pattern.search(text))

    def test_no_generated_or_secret_artifacts(self):
        forbidden_names = {"__pycache__", ".pytest_cache", ".env", "node_modules"}
        for path in ROOT.rglob("*"):
            with self.subTest(path=path.relative_to(ROOT)):
                self.assertNotIn(path.name, forbidden_names)
                self.assertNotEqual(".pyc", path.suffix.lower())

    def test_verification_commands_have_no_unresolved_placeholders(self):
        report = (ROOT / "docs" / "verification.md").read_text(encoding="utf-8")
        self.assertNotIn("<plugin-creator>", report)
        self.assertNotIn("<skill-creator>", report)


if __name__ == "__main__":
    unittest.main()
