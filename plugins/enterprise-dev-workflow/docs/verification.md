# Distribution Verification

Date: 2026-09-16

Base version: `2.0.0` (local installs add one `+codex.<cachebuster>` suffix).

This report covers the distributable plugin package in this repository. It does not certify a consuming application's production readiness.

## Package checks

Run from `plugins/enterprise-dev-workflow`:

```powershell
python -B -m unittest discover -s tests -v
python -B scripts/validate_workflow_contract.py .
$codexInstallRoot = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path ([Environment]::GetFolderPath('UserProfile')) '.codex' }
python -B (Join-Path $codexInstallRoot 'skills/.system/plugin-creator/scripts/validate_plugin.py') .
Get-ChildItem skills -Directory | ForEach-Object {
  python -B (Join-Path $codexInstallRoot 'skills/.system/skill-creator/scripts/quick_validate.py') $_.FullName
}
```

Results:

- 20 workflow-contract and distribution-hygiene tests passed.
- Package structure and the 12-case workflow schema passed validation.
- Plugin manifest validation passed.
- All six bundled skills passed validation.
- `enterprise-delivery` is the only implicitly invoked skill.
- Shipped Markdown, JSON, and YAML contain no removed task-tier or host-model-choice contract.

## Scope evidence

The package contains six focused skills and four reusable standards references. The former task-tier, host-model-choice, visual brainstorming companion, agent orchestration, planning, review, duplicated verification, and optimization-metrics packages are no longer distributed.

The maintained workflow cases cover small changes, large requirements, bugs, UI, API, database, architecture, authorization, read-only diagnosis, dirty worktrees, missing test infrastructure, and out-of-scope discoveries.

## NOT VERIFIED

- Fresh-task behavior for all 12 workflow cases: the package and case schema are validated, but each prompt has not been exercised end to end in a newly installed task.
- Installation or upgrade from the remote GitHub marketplace for version 2.0.0: no remote publication or clean-profile installation was requested in this refactor.
- Consuming-application build, browser, API, database, deployment, performance, or security behavior: this repository contains a skills-only plugin, not a target application.
