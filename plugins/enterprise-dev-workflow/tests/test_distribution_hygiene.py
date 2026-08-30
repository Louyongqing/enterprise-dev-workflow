"""Regression checks for the shareable package boundary."""

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class DistributionHygieneTests(unittest.TestCase):
    def test_removed_upstream_development_artifacts_stay_removed(self):
        debug_dir = ROOT / "skills" / "systematic-debugging"
        for name in (
            "CREATION-LOG.md",
            "test-academic.md",
            "test-pressure-1.md",
            "test-pressure-2.md",
            "test-pressure-3.md",
        ):
            with self.subTest(name=name):
                self.assertFalse((debug_dir / name).exists())

    def test_no_stale_upstream_paths_in_shipped_text(self):
        forbidden = (
            "docs/superpowers/specs",
            "skills/debugging/systematic-debugging",
            "skills/meta/testing-skills-with-subagents",
            "skills/testing/test-driven-development",
        )
        for path in ROOT.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in {".md", ".sh", ".cjs", ".js"}:
                continue
            text = path.read_text(encoding="utf-8")
            for marker in forbidden:
                with self.subTest(path=path.relative_to(ROOT), marker=marker):
                    self.assertNotIn(marker, text)

    def test_brainstorm_runtime_is_ephemeral_and_separate_from_content(self):
        launcher = (ROOT / "skills" / "brainstorming" / "scripts" / "start-server.sh").read_text(encoding="utf-8")
        server = (ROOT / "skills" / "brainstorming" / "scripts" / "server.cjs").read_text(encoding="utf-8")
        self.assertIn('BRAINSTORM_RUNTIME_DIR=', launcher)
        self.assertIn('mktemp -d', launcher)
        self.assertIn('SESSION_DIR="$BRAINSTORM_RUNTIME_DIR"', launcher)
        self.assertIn('BRAINSTORM_PROJECT_BASE="${PROJECT_DIR}/.enterprise-dev-workflow/brainstorm"', launcher)
        self.assertIn('BRAINSTORM_CONTENT_SESSION=', launcher)
        self.assertIn('CONTENT_DIR="${BRAINSTORM_CONTENT_SESSION}/content"', launcher)
        self.assertIn('BRAINSTORM_IGNORE_FILE="${BRAINSTORM_CONTENT_SESSION}/.gitignore"', launcher)
        self.assertIn('BRAINSTORM_CONTENT_DIR="$CONTENT_DIR"', launcher)
        self.assertIn("process.env.BRAINSTORM_CONTENT_DIR", server)
        self.assertIn("session_dir: SESSION_DIR", server)
        self.assertNotIn("BRAINSTORM_TOKEN_FILE", launcher + server)
        self.assertNotIn("BRAINSTORM_PORT_FILE", launcher + server)
        self.assertNotIn("process.env.BRAINSTORM_TOKEN", server)
        self.assertNotIn("process.env.BRAINSTORM_PORT", server)
        stop = (ROOT / "skills" / "brainstorming" / "scripts" / "stop-server.sh").read_text(encoding="utf-8")
        self.assertNotIn("rm -rf", stop)

    def test_visual_companion_does_not_auto_load_remote_brand_image(self):
        server = (ROOT / "skills" / "brainstorming" / "scripts" / "server.cjs").read_text(encoding="utf-8")
        self.assertNotIn("SUPERPOWERS_BRAND_IMAGE_URL", server)
        self.assertNotIn("primeradiant.com/brand/", server)

    def test_verification_commands_have_no_unresolved_placeholders(self):
        report = (ROOT / "docs" / "verification.md").read_text(encoding="utf-8")
        self.assertNotIn("<plugin-creator>", report)
        self.assertNotIn("<skill-creator>", report)


if __name__ == "__main__":
    unittest.main()
