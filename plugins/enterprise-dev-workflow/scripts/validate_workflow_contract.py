"""Validate package and workflow-case invariants, not agent behavior."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


EXPECTED_SKILLS = {
    "code-quality",
    "enterprise-delivery",
    "scope-control",
    "systematic-debugging",
    "task-decomposition",
    "verification",
}
EXTERNAL_ROUTES = {
    "api-design",
    "backend-architecture",
    "codebase-recon",
    "database-engineering",
    "frontend-design",
    "project-verification",
    "security-review",
    "webapp-testing",
}
ALLOWED_ROUTES = EXPECTED_SKILLS | EXTERNAL_ROUTES
POLICY = re.compile(r"(?m)^[ \t]+allow_implicit_invocation:[ \t]*(true|false)[ \t]*(?:#.*)?$")
POLICY_KEY = re.compile(r"(?m)^[ \t]+allow_implicit_invocation:")
LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
REMOVED_PATTERNS = {
    "task tier": re.compile(r"\bL[123]\b"),
    "removed routing skill": re.compile("model" + "-routing", re.IGNORECASE),
    "execution model selection": re.compile("model" + r"[ -]selection", re.IGNORECASE),
    "strong execution model": re.compile("strong" + r"[ -]model", re.IGNORECASE),
    "fast execution model": re.compile("fast" + r"[ -]model", re.IGNORECASE),
    "premium execution model": re.compile("premium" + r"[ -]model", re.IGNORECASE),
    "fallback execution model": re.compile("fallback" + r"[ -]model", re.IGNORECASE),
}
TEXT_SUFFIXES = {".json", ".md", ".yaml", ".yml"}


def read_text(path: Path, errors: list[str]) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        errors.append(f"{path}: cannot read UTF-8 file: {exc}")
        return None


def valid_policy(metadata: str, expected: str) -> bool:
    lines = metadata.splitlines()
    headers = [index for index, line in enumerate(lines) if re.fullmatch(r"policy:[ \t]*(?:#.*)?", line)]
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


def validate_links(path: Path, root: Path, content: str, errors: list[str]) -> None:
    for raw in LINK.findall(content):
        target = raw.strip().strip("<>").split("#", 1)[0]
        if not target or target.startswith(("https://", "http://", "mailto:")):
            continue
        resolved = (path.parent / target).resolve()
        if not resolved.is_relative_to(root):
            errors.append(f"{path}: link escapes plugin: {target}")
        elif not resolved.exists():
            errors.append(f"{path}: missing link target: {target}")


def string_list(value: object, label: str, errors: list[str], *, nonempty: bool = False) -> list[str]:
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
    path = root / "evals" / "workflow-cases.json"
    raw = read_text(path, errors)
    if raw is None:
        return
    try:
        cases = json.loads(raw)
    except json.JSONDecodeError as exc:
        errors.append(f"workflow-cases.json: invalid JSON: {exc}")
        return
    if not isinstance(cases, list) or not cases:
        errors.append("workflow-cases.json: expected nonempty case array")
        return

    expected_fields = {
        "id", "prompt", "required_routes", "forbidden_routes",
        "required_outcomes", "forbidden_outcomes",
    }
    seen: set[str] = set()
    for index, case in enumerate(cases):
        label = f"workflow-cases.json case[{index}]"
        if not isinstance(case, dict):
            errors.append(f"{label}: expected object")
            continue
        if set(case) != expected_fields:
            errors.append(f"{label}: fields must be exactly {sorted(expected_fields)}")
        case_id = case.get("id")
        if not isinstance(case_id, str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]*", case_id):
            errors.append(f"{label}: invalid id")
        else:
            label = f"workflow-cases.json {case_id}"
            if case_id in seen:
                errors.append(f"{label}: duplicate id")
            seen.add(case_id)
        if not isinstance(case.get("prompt"), str) or not case["prompt"].strip():
            errors.append(f"{label}: prompt must be nonempty string")
        required = string_list(case.get("required_routes"), f"{label} required_routes", errors, nonempty=True)
        forbidden = string_list(case.get("forbidden_routes"), f"{label} forbidden_routes", errors)
        string_list(case.get("required_outcomes"), f"{label} required_outcomes", errors, nonempty=True)
        string_list(case.get("forbidden_outcomes"), f"{label} forbidden_outcomes", errors, nonempty=True)
        for route in required + forbidden:
            if route not in ALLOWED_ROUTES:
                errors.append(f"{label}: unknown route {route}")
        if set(required) & set(forbidden):
            errors.append(f"{label}: a route cannot be both required and forbidden")


def validate_removed_contracts(root: Path, errors: list[str]) -> None:
    scan_roots = [root / "README.md", root / ".codex-plugin" / "plugin.json",
                  root / "docs", root / "evals", root / "references", root / "skills"]
    paths: list[Path] = []
    for candidate in scan_roots:
        if candidate.is_file():
            paths.append(candidate)
        elif candidate.is_dir():
            paths.extend(path for path in candidate.rglob("*") if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES)
    for path in paths:
        content = read_text(path, errors)
        if content is None:
            continue
        for label, pattern in REMOVED_PATTERNS.items():
            if pattern.search(content):
                errors.append(f"{path}: contains {label}")


def validate_plugin_contract(plugin_root: Path) -> list[str]:
    root = Path(plugin_root).resolve()
    errors: list[str] = []
    skills = root / "skills"
    if not skills.is_dir():
        return [f"missing skills directory: {skills}"]
    actual = {
        path.name for path in skills.iterdir()
        if path.is_dir() and (path / "SKILL.md").is_file()
    }
    if actual != EXPECTED_SKILLS:
        errors.append(f"skill set mismatch: missing={sorted(EXPECTED_SKILLS - actual)}, extra={sorted(actual - EXPECTED_SKILLS)}")
    for name in sorted(EXPECTED_SKILLS):
        skill_path = skills / name / "SKILL.md"
        content = read_text(skill_path, errors)
        if content is not None:
            validate_links(skill_path, root, content, errors)
        metadata = read_text(skills / name / "agents" / "openai.yaml", errors)
        if metadata is not None:
            expected = "true" if name == "enterprise-delivery" else "false"
            if not valid_policy(metadata, expected):
                errors.append(f"{name}: exactly one policy allow_implicit_invocation: {expected} is required")
    validate_cases(root, errors)
    validate_removed_contracts(root, errors)
    return sorted(set(errors))


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if len(args) > 1:
        print("Usage: validate_workflow_contract.py [plugin-root]", file=sys.stderr)
        return 2
    root = Path(args[0]) if args else Path(__file__).resolve().parents[1]
    errors = validate_plugin_contract(root)
    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        return 1
    print("PASS: package structure and workflow-case schema (not runtime behavior)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
