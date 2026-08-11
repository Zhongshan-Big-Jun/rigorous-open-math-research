# lean-verify

Strict verification workflow for Lean 4 formalizations: statement-fidelity audit, machine
checks (lake build, sorry/admit/axiom scan), per-obligation independent audit, structured
verdicts, and hash-bound run manifests.

## Structure

- `skills/lean-verify/SKILL.md` - the verification workflow skill.
- `scripts/verify_lean_project.py` - static and machine checks (stdlib only): records lean/lake
  versions and lean-toolchain, scans .lean files for sorry/admit/axiom, optionally runs
  `lake build`, and writes `run-manifest.json`.
- `assets/verification_output.schema.json` - JSON Schema for the structured verdict.
- `assets/lean-audit-report.template.md` - audit report template.
- `assets/lean-obligation.template.md` - obligation-to-Lean-declaration mapping template.

## Usage

1. Install the plugin from the repo marketplace: `codex plugin marketplace add
   xsoc1/rigorous-open-math-research`, then `codex plugin add lean-verify@math-research`.
   (Alternative: install the skill directory directly via `$skill-installer`.)
2. Invoke `$lean-verify` with a Lean project directory and the informal theorem contract.
3. The skill runs Phase 0-5 and emits `verification.json`, `audit_report.md`, and
   `run-manifest.json`.

Script (standalone):

```bash
python scripts/verify_lean_project.py --project <lean-project> --build --output <out>
```

## Requirements

- The skill itself is environment-agnostic. Machine verification needs a Lean 4 toolchain
  (`lean` and `lake` on PATH); without it the skill records that machine checks could not run
  and continues with static checks and the independent audit.

## Version

- 0.1.0 (2026-08-11): initial plugin with verification workflow skill, static/machine check
  script, structured verdict schema, and audit/obligation templates.
