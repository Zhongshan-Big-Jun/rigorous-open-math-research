# lean-verify

Develop Lean 4 proofs with local lemma discovery, actual interface experiments,
incremental candidate feedback and durable per-root jobs. Exact verification
continues to compare independently authored intended types and inspect
transitive axioms, current modules and semantic review separately.

## Structure

- `skills/lean-verify/SKILL.md` - the verification workflow skill.
- `scripts/lean_develop.py` - source search, actual type probes, candidate trial/save,
  nonempty independent root lists and the existing workflow's start/status jobs.
- `scripts/lean_feedback.py` - persistent LSP feedback and explicit CLI fallback.
- `scripts/verify_lean_project.py` - isolated exact declaration/type/axiom checking
  and optional explicit project builds, with retained v2 run manifests.
- `scripts/lean_evidence.py` and `scripts/lean_routes.py` - current evidence and
  AND/OR readiness; actual materialized roots remain required.
- `assets/verification_output.schema.json` - JSON Schema for the structured verdict.
- `assets/lean-audit-report.template.md` - audit report template.
- `assets/lean-obligation.template.md` - obligation-to-Lean-declaration mapping template.

## Usage

1. Install the plugin from the repo marketplace: `codex plugin marketplace add
   xsoc1/rigorous-open-math-research`, then `codex plugin add lean-verify@math-research`.
   (Alternative: install the skill directory directly via `$skill-installer`.)
2. Invoke `$lean-verify` with a Lean project directory and the informal theorem contract.
3. For development commands read
   [proof development](skills/lean-verify/references/v2-development.md); for
   exact contracts and result fields read
   [verification](skills/lean-verify/references/v2-verification.md).

Script (standalone):

```bash
python scripts/verify_lean_project.py --project <lean-project> --build --output <out>
```

## Requirements

- The skill itself is environment-agnostic. Machine verification needs a Lean 4 toolchain
  (`lean` and `lake` on PATH); without it the skill records that machine checks could not run
  and continues with static checks and the independent audit.

## Version

- 2.1.0 (local development): connected proof-development mode, with the existing
  exact verifier and v2 evidence format. A source version does not assert release
  or installation. [Release history](skills/lean-verify/references/changelog.md).
