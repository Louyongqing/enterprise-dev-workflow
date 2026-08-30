# Distribution Verification

Date: 2026-08-30

Version: `0.1.0+codex.20260828022715`

This report covers the distributable plugin package in this repository. It does not certify any target project's production readiness or regulatory compliance.

## Package checks

Run from `plugins/enterprise-dev-workflow`:

```powershell
python -B -m unittest discover -s tests -v
python -B scripts/validate_routing_contract.py .
python -B scripts/summarize_eval_runs.py evals/optimization-run-records.json
$codexRoot = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path ([Environment]::GetFolderPath('UserProfile')) '.codex' }
python -B (Join-Path $codexRoot 'skills/.system/plugin-creator/scripts/validate_plugin.py') .
Get-ChildItem skills -Directory | ForEach-Object {
  python -B (Join-Path $codexRoot 'skills/.system/skill-creator/scripts/quick_validate.py') $_.FullName
}
```

Results:

- 47 unit, contract, and distribution-hygiene tests passed.
- Package structure and the 20-case evaluation schema passed validation.
- Plugin manifest validation passed.
- All 12 bundled skills passed validation.
- `enterprise-delivery` remains the only implicitly invoked skill.

## Behavioral evidence

The maintained evaluation set covers L1/L2/L3 routing, composite security and migration risks, approval reuse, stale evidence, read-only requests, unavailable capabilities, and missing telemetry.

Two paired risk probes in `evals/optimization-run-records.json` retain the reviewed baseline/candidate outcomes: the baseline failed both risk requirements and the candidate passed both. Actual executing model IDs, token counts, latency, rework, and quota impact were unavailable and remain `null`. The summarizer therefore reports zero comparable passing pairs and no numeric savings.

Schema and package validation do not prove that every model will follow every workflow instruction. Representative behavior must be checked in a fresh task after installation.

## Distribution privacy

The shared package excludes the original local Git history and internal verification artifacts containing workstation paths or task identifiers. No credentials are required by the plugin, and no MCP server, app connection, or lifecycle hook is bundled.

The optional visual brainstorming companion starts only after user approval. It binds to loopback by default and creates a new key, port, and unpredictable owner-only OS runtime/temp directory for every launch; inherited environment variables cannot override that rotation. Visual content may be persisted under the consuming project's `.enterprise-dev-workflow/brainstorm/` directory; authenticated state remains outside the project. The stop path removes sensitive files without recursively deleting caller-supplied directories. The companion does not automatically load third-party brand images.

## NOT VERIFIED

- Installation from the remote GitHub marketplace: verify after the private repository is created and pushed.
- All 20 routing cases in fresh installed tasks: the full set was schema-validated, not rerun end to end for this packaging-only change.
- Token, latency, monetary, or subscription-quota savings: complete comparable host measurements are unavailable.
- Production application behavior, CI, deployment, migrations, rollback, performance, or security posture: no target application is part of this package verification.
