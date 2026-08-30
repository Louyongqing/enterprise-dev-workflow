# Enterprise Dev Workflow Marketplace

Public marketplace for the `enterprise-dev-workflow` Codex plugin.

The plugin provides risk-aware software delivery workflows with L1/L2/L3 routing, systematic debugging, practical test-driven development, review, security checks, model routing, and evidence-based completion gates.

## Install

Install directly from this public GitHub marketplace.

```powershell
codex plugin marketplace add https://github.com/Louyongqing/enterprise-dev-workflow
codex plugin add enterprise-dev-workflow@enterprise-dev-workflow
```

Restart Codex or open a new task after installation so the bundled skills are discovered.

## Layout

```text
.agents/plugins/marketplace.json
plugins/enterprise-dev-workflow/
```

The package is skills-only: it does not install an MCP server, app connection, or lifecycle hook.

## Development

Run checks from `plugins/enterprise-dev-workflow`:

```powershell
python -B -m unittest discover -s tests -v
python -B scripts/validate_routing_contract.py .
```

See the plugin's own README and verification report for scope and limitations.

## License

MIT. Adapted third-party material is documented in `plugins/enterprise-dev-workflow/THIRD_PARTY_NOTICES.md`.
