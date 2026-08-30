"""Validate package/evaluation invariants, not agent behavior or prose."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

EXPECTED_SKILLS = {
    "brainstorming", "dispatching-parallel-agents", "enterprise-delivery",
    "model-routing", "project-verification", "requesting-code-review",
    "security-review", "subagent-driven-development", "systematic-debugging",
    "test-driven-development", "verification-before-completion", "writing-plans",
}
LEVELS = {"NONE": 0, "L1": 1, "L2": 2, "L3": 3}
POLICY = re.compile(r"(?m)^[ \t]+allow_implicit_invocation:[ \t]*(true|false)[ \t]*(?:#.*)?$")
POLICY_KEY = re.compile(r"(?m)^[ \t]+allow_implicit_invocation:")
LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")


def read_text(path: Path, errors: list[str]) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        errors.append(f"{path}: cannot read UTF-8 file: {exc}")
        return None


def valid_policy(metadata: str, expected: str) -> bool:
    """Validate the supported block-style policy without accepting misplaced keys."""
    lines = metadata.splitlines()
    headers = [i for i, line in enumerate(lines) if re.fullmatch(r"policy:[ \t]*(?:#.*)?", line)]
    if len(headers) != 1 or len(POLICY_KEY.findall(metadata)) != 1:
        return False
    block = []
    for line in lines[headers[0] + 1:]:
        if line and not line[0].isspace() and not line.startswith("#"):
            break
        block.append(line)
    content = [line for line in block if line.strip() and not line.lstrip().startswith("#")]
    if not content or any("\t" in line[:len(line) - len(line.lstrip())] for line in content):
        return False
    direct_indent = min(len(line) - len(line.lstrip(" ")) for line in content)
    direct_children = [line for line in content if len(line) - len(line.lstrip(" ")) == direct_indent]
    return POLICY.findall("\n".join(direct_children)) == [expected]


def validate_links(path: Path, root: Path, text: str, errors: list[str]) -> None:
    for raw in LINK.findall(text):
        target = raw.strip().strip("<>").split("#", 1)[0]
        if not target or target.startswith(("https://", "http://", "mailto:")):
            continue
        resolved = (path.parent / target).resolve()
        if not resolved.is_relative_to(root):
            errors.append(f"{path}: link escapes plugin: {target}")
        elif not resolved.exists():
            errors.append(f"{path}: missing link target: {target}")


def string_list(value: object, label: str, errors: list[str], nonempty=False) -> list[str]:
    if not isinstance(value, list) or (nonempty and not value):
        errors.append(f"{label}: expected {'nonempty ' if nonempty else ''}array")
        return []
    if any(not isinstance(item, str) or not item.strip() for item in value):
        errors.append(f"{label}: entries must be nonempty strings")
        return []
    if len(value) != len(set(value)):
        errors.append(f"{label}: duplicate entries")
    return value


def validate_cases(root: Path, errors: list[str]) -> None:
    raw = read_text(root / "evals/routing-cases.json", errors)
    if raw is None:
        return
    try:
        cases = json.loads(raw)
    except json.JSONDecodeError as exc:
        errors.append(f"routing-cases.json: invalid JSON: {exc}")
        return
    if not isinstance(cases, list) or not cases:
        errors.append("routing-cases.json: expected nonempty case array")
        return
    seen = set()
    for index, case in enumerate(cases):
        label = f"routing-cases.json case[{index}]"
        if not isinstance(case, dict):
            errors.append(f"{label}: expected object")
            continue
        case_id = case.get("id")
        if not isinstance(case_id, str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]*", case_id):
            errors.append(f"{label}: invalid id")
        else:
            label = f"routing-cases.json {case_id}"
            if case_id in seen:
                errors.append(f"{label}: duplicate id")
            seen.add(case_id)
        if not isinstance(case.get("prompt"), str) or not case["prompt"].strip():
            errors.append(f"{label}: prompt must be nonempty string")
        level = case.get("expected_level")
        floor = case.get("minimum_level", level)
        if not isinstance(level, str) or level not in LEVELS:
            errors.append(f"{label}: invalid expected_level")
        if not isinstance(floor, str) or floor not in LEVELS:
            errors.append(f"{label}: invalid minimum_level")
        elif isinstance(level, str) and level in LEVELS and LEVELS[level] < LEVELS[floor]:
            errors.append(f"{label}: expected level cannot lower minimum risk")
        required = string_list(case.get("required_skills"), f"{label} required_skills", errors)
        forbidden = string_list(case.get("forbidden_default_skills"), f"{label} forbidden_default_skills", errors)
        string_list(case.get("required_outcomes"), f"{label} required_outcomes", errors, nonempty=True)
        for skill in required + forbidden:
            if skill not in EXPECTED_SKILLS:
                errors.append(f"{label}: unknown skill {skill}")
        if set(required) & set(forbidden):
            errors.append(f"{label}: a skill cannot be required and forbidden")
        if level == "NONE" and required:
            errors.append(f"{label}: NONE cannot require implementation workflows")


def validate_plugin_contract(plugin_root: Path) -> list[str]:
    root = Path(plugin_root).resolve()
    errors: list[str] = []
    skills = root / "skills"
    if not skills.is_dir():
        return [f"missing skills directory: {skills}"]
    actual = {path.name for path in skills.iterdir() if path.is_dir()}
    if actual != EXPECTED_SKILLS:
        errors.append(f"skill set mismatch: missing={sorted(EXPECTED_SKILLS - actual)}, extra={sorted(actual - EXPECTED_SKILLS)}")
    for name in sorted(EXPECTED_SKILLS):
        path = skills / name / "SKILL.md"
        text = read_text(path, errors)
        if text is not None:
            validate_links(path, root, text, errors)
        metadata = read_text(skills / name / "agents/openai.yaml", errors)
        if metadata is not None:
            expected = "true" if name == "enterprise-delivery" else "false"
            if not valid_policy(metadata, expected):
                errors.append(f"{name}: exactly one policy allow_implicit_invocation: {expected} is required")
    validate_cases(root, errors)
    return sorted(set(errors))


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if len(args) > 1:
        print("Usage: validate_routing_contract.py [plugin-root]", file=sys.stderr)
        return 2
    root = Path(args[0]) if args else Path(__file__).resolve().parents[1]
    errors = validate_plugin_contract(root)
    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        return 1
    print("PASS: package structure and evaluation schema (not runtime behavior)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
