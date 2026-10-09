# Proof development with the pinned project

`scripts/lean_develop.py` connects source discovery, interface experiments,
candidate feedback, atomic saving and the existing exact-root verifier. The
host agent makes mathematical decisions and supplies proof candidates. The
tool runs installed local Lean; it has no model or automatic theorem generator.
Select this source tree or a separate development install explicitly. Editing
this repository does not change an already loaded skill or global installation.

## Discover and try interfaces

All global arguments precede the subcommand. Use the project's existing pinned
Lean/Lake, and add `--direct` to use prepared artifacts without package fetching.
For this development entrance, `--output` must be outside the project and cannot
be a project ancestor. The project itself and every project-internal directory
are rejected for all actions, including trial/save, verify, start and status.
Use a sibling evidence directory; do not place generated output over source
subtrees. The older standalone verifier/feedback entry points retain their
existing layout behavior. Source destinations cannot use directories excluded
from project snapshots, such as `.lake`, `.git` or `.lean-verify`.

```bash
python scripts/lean_develop.py --project PROJECT --output LOGS \
  --lean LEAN --lake LAKE --direct search --query hasDerivAt --limit 20
python scripts/lean_develop.py --project PROJECT --output LOGS \
  --lean LEAN --lake LAKE --direct probe --import MODULE --name Namespace.lemma
```

Search uses local `rg`, with a standard-library fallback, over current project
sources and the mathlib package named by `lake-manifest.json`. It returns actual
paths, source hashes, line numbers and modules. Names inferred from source
namespace structure are candidates. Comments, private declarations, macros
and unusual syntax can make inference incomplete. A search hit establishes
neither an installed API nor a proof. `--probe` checks inferred candidates;
explicit `probe` is preferable for a selected interface.

The probe compiles current local imports into disposable output directories,
then asks the actual Lean environment for the declaration's full type, universe
parameters and defining module. Failed or missing APIs retain real compiler
logs and return incomplete. Use these results to write a smaller experiment or
choose another route while retaining the mathematical target.

Development and strict probes keep `pp.all`, `pp.universes` and `pp.explicit`,
enable `pp.deepTerms` and `pp.proofs`, and use `pp.maxSteps=10000000` with
`maxRecDepth=8192` during readable type printing. These options were checked
against native Lean 4.31.0 and its
[pinned option definitions](https://github.com/leanprover/lean4/blob/v4.31.0/src/Lean/PrettyPrinter/Delaborator/Options.lean)
and [delaborator implementation](https://github.com/leanprover/lean4/blob/v4.31.0/src/Lean/PrettyPrinter/Delaborator/Basic.lean).
`pp.maxDepth` is unavailable there, and `pp.maxSteps=0` immediately omits terms.
The limits remain finite. Any compiler failure or remaining `⋯` keeps the probe
incomplete, and strict derivation/evidence recheck also rejects omitted readable
types. The complete encoded `type_expression` and transitive bindings are
retained separately; the readable string does not replace their hashes.

## Construct, inspect, revise and save

Write a complete candidate file outside the source destination, then:

```bash
python scripts/lean_develop.py --project PROJECT --output LOGS \
  --lean LEAN --lake LAKE --direct --timeout 120 trial \
  --file Topic/Result.lean --candidate CANDIDATE --backend cli
python scripts/lean_develop.py --project PROJECT --output LOGS \
  --lean LEAN --lake LAKE --direct save --receipt TRIAL_JSON
```

`trial` accepts new destinations and prepares project-local imports using the
existing isolated compiler. It delegates to `FeedbackSession`: `auto` prefers
LSP and falls back to CLI; `cli` gives real diagnostics; `lsp` keeps unavailable
or stale feedback incomplete. For persistent goals, hover and unsaved-buffer
experiments, use the existing JSON-lines `lean_feedback.py` session. Python
callers may retain `DevelopSession` to keep that same feedback engine warm.

To keep discovery, trials and saving in one live process, run the same global
arguments followed by `serve --backend auto` (or `cli`). Send one JSON object
per line; each response is one JSON line, including explicit incomplete results.

```json
{"action":"probe","names":["Namespace.lemma"],"imports":["Module"]}
{"action":"trial","file":"Topic/Result.lean","candidate":"CANDIDATE"}
{"action":"save","receipt":"TRIAL_JSON_FROM_PREVIOUS_RESPONSE"}
{"action":"feedback","request":{"action":"goals","file":"Topic/Result.lean","line":10,"character":2}}
{"action":"restart"}
{"action":"close"}
```

Successive unsaved candidates can reuse current local import preparation after
checking source, environment, artifact hashes and current module resolution.
The feedback engine retains its existing LSP version/dependency checks. Restart
discards the development cache and LSP session. `close` releases the live
session; final `verify` remains a separate exact-root operation. CLI responses
use ASCII-safe JSON so native Windows GBK stdout can carry Unicode types.
The process captures its loaded Python-tool hashes. A later source-code change
keeps further requests incomplete until a new Python process is started;
restarting only LSP cannot reload Python or relabel old code with new hashes.
That identity includes every existing `lean_evidence.TOOL_NAMES` entry, including
`lake_build_guard.py` and `run_manifest.schema.json`, as well as the development,
feedback and route tools. Final verify/status snapshots bind the same full set.
Native Windows Lean/Lake/LSP/search commands use hidden background processes;
the workflow retains its detached supervisor and hides child console windows.
POSIX process-group behavior is retained.

Each trial freezes candidate bytes and records disk/source/configuration,
runtime, loaded-artifact and tool identities. `save` rechecks all of them,
including current import resolution, and uses the workflow's atomic writer.
It repeats the source and destination checks after the runtime/import queries,
immediately before the atomic compare-and-write, so an edit during those
queries cannot authorize saving the older trial.
Source edits by another collaborator make the old trial stale; rerun it against
the current state before saving. Error, unavailable, timeout and stale feedback
cannot authorize saving. Successfully saving a file leaves exact-root closure
pending; warnings and imported unproved assumptions are checked at final roots.

## Independently authored target list

Keep one nonempty list of intended formal roots with the project's existing
results mapping. Each entry requires `id`, `file`, `declaration` and a full
`expected_type` written from the source contract before checking the candidate.

```json
{
  "targets": [
    {
      "id": "natural-addition",
      "file": "Main.lean",
      "declaration": "Example.result",
      "expected_type": "∀ n : Nat, n + 0 = n",
      "universes": []
    }
  ]
}
```

Optional existing identity fields pass through to the exact verifier. Optional
`input_file_hashes` binds actual informal sources or other non-Lean input paths
to SHA-256 values; relative paths are resolved in the project. The adapter also
binds the original target-list file, so changing the intended roots invalidates
old receipts without rewriting them. Optional `semantic_audit` points to an
existing review, subject to the verifier's separate current binding checks.

```bash
python scripts/lean_develop.py --project PROJECT --output EVIDENCE \
  --lean LEAN --lake LAKE --direct --timeout 300 verify --targets TARGETS_JSON
```

`--target-id` selects one declared root. Missing IDs, empty lists and absent
expected types are rejected. Every selected root invokes `verify_lean_project`
and then `lean_evidence`; the combined exit is nonzero for any incomplete root.
The adapter never derives an intended type from the candidate or sets success
on its own. It writes `development-result.json` with paths to the unchanged v2
verification manifests, exact closure, actual machine state and separate
semantic-review state. A successful implication proves its recorded conditional
scope. Automatic checks cannot establish every informal semantic match,
nonempty carrier or satisfiable hypothesis; review those explicitly.

For multiple roots, all final manifest rechecks form one terminal pass. The
adapter binds common project sources/configuration, the original target-list
bytes, declared non-Lean inputs, runtime/tool identities and listed evidence
bytes before and after that pass. Changes anywhere in those bindings keep every
row and the combined result incomplete, even when a previously observed root
check passed. `batch-inputs.json` retains the observed snapshots. Target-list
identity hashes the bytes actually parsed, not a later reread. These checks
observe declared bindings; they do not create an OS-wide filesystem transaction
or prevent an uncooperative writer from editing after the last observation.
Recheck saved evidence when consuming it.

## Decompose, compose and continue

For complex goals, `routes --graph GRAPH --root ID [--root-manifest MANIFEST]`
delegates to `lean_routes.py`. Record typed leaves, reusable checked lemmas and
AND/OR alternatives, then write a Lean application of the selected route as an
ordinary candidate. Trial/save/verify the actual root declaration. Route
readiness, closed leaves and cycles have the existing meanings; a missing root
remains incomplete. There is no parallel workflow language or graph-based proof
acceptance.

For checks that must survive an interrupted client:

```bash
python scripts/lean_develop.py --project PROJECT --output EVIDENCE \
  --lean LEAN --lake LAKE --direct --timeout 300 start \
  --targets TARGETS_JSON --target-id natural-addition --job-id root-check-01
python scripts/lean_develop.py --project PROJECT --output EVIDENCE \
  status --job-id root-check-01
```

`start` uses the existing `research_state.py` local supervisor, binds current
sources and a project-local target list and retains its real job ID. Repeating
the same request returns the existing job rather than dispatching it again.
Use a new ID for a changed request. `status` reopens recorded state and logs;
only a finished successful job with matching current inputs, bound output and
fresh exact-root manifests can report a checked root. Unknown or interrupted
jobs remain incomplete and keep their original process identity and logs for
inspection. Exit code 0 or process completion alone establishes no theorem.
The terminal status rechecks also require common declared bindings to remain
stable across the complete manifest pass.
All manifest, contract, stdout and job reads finish before the final evidence
and input snapshots. Summary, job record and stdout/stderr bytes also participate
in the evidence stability check. These are observed boundaries, with the same
post-observation filesystem limitation described above.

## Tests and limits

From the marketplace root, run `test_lean_develop.py` with standard unittest
discovery. Opt-in `test_lean_develop_real.py` uses `LEAN_VERIFY_REAL_LEAN` and
`LEAN_VERIFY_REAL_LAKE`, and preserves generic fixture evidence under
`LEAN_VERIFY_TEST_TMPDIR` with `LEAN_VERIFY_KEEP_TEST_ARTIFACTS=1` and
`LEAN_DEVELOP_TEST_REPORT`. This fixture covers actual interface/diagnostic
feedback, revision, save, exact verification, target extension and job recovery;
it contains no research-specific constants or objects.

Run the retained `test_v2_verifier.py`, `test_v2_lean_real.py` and repository
`scripts/validate_all.py` too. Local platform runs apply only to the tested
platform. CI configuration is not evidence that CI ran. Neither generic fixtures
nor a single research integration establish universal speedup. Compare the same
task and environment using retained failed trials and real compiler operations.
Rich analysis targets can produce very large complete expression/dependency
records and manifests. The joint research run observed roughly 218 MB of
declaration extraction, 1.4 GB of manifest data and 4.8 GB of Python memory for
one root. Generic fixture timings do not predict those evidence costs.
