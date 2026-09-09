# Math Research 2.0

[中文](README.md) | [Use and migration](docs/v2.0-guide.md) | [Implementation and validation](docs/v2.0-implementation-status.md)

Codex plugins for long-term collaborative mathematics. Turn papers, successful proofs and failed approaches into reusable tools and understanding that help with the next problem.

All four components use version `2.0.0`. Short guidance and concrete tools support the researcher's choice of proofs, counterexamples, literature, computation, collaboration and Lean.

## What the plugins support

| Research need | Support in 2.0 |
| --- | --- |
| Find and use previously read literature | Preserve source content, versions and locators; read bounded segments; rebuild tool pointers |
| Let agents record interpretations and questions | Searchable free-form annotations tied to card versions, with provenance and scope |
| Learn from successful and failed routes | Preserve transformations, constructions, programs, obstructions and reconsideration conditions; compare routes when useful |
| Keep the human involved | An editable understanding page distinguishing explanations, candidate ideas, intuition and open decisions |
| Continue after a session or quota interruption | Current progress, atomic snapshots, actual job identities and full logs, with stale-write and duplicate-dispatch protection |
| Use Lean during research | Compiler feedback, exact declarations and transitive axioms, separating execution, semantics, root closure and evidence identity |

The annotatable tool library and its pointer index are the core. Cards preserve mathematics and conditions; annotations carry interpretation and corrections; pointers lead back to evidence. More cards or graph nodes do not themselves constitute research progress.

## Choose a component

Components can be installed and used independently.

| Plugin / Skill | Use it for |
| --- | --- |
| `$math-research-workflow` | Research coordination and continuity across problems and sessions |
| `$rigorous-open-math-research` | Proofs, counterexamples, constructions and argument review |
| `$manage-math-research-program` | Literature, annotated tools, research experience and project understanding |
| `$lean-verify` | Lean feedback, precise target checks and reproducible verification |

Example:

> Use $manage-math-research-program to extract reusable tools from these proofs and failed approaches. Preserve their conditions and evidence pointers, and update our understanding of the problem.

## Install

The repository marketplace is named `math-research`. In a plugin-capable Codex CLI:

```bash
codex plugin marketplace add xsoc1/rigorous-open-math-research
codex plugin add math-research-workflow@math-research
codex plugin add rigorous-open-math-research@math-research
codex plugin add manage-math-research-program@math-research
codex plugin add lean-verify@math-research
```

Install only the components you need. For an existing installation, refresh the marketplace and reinstall the desired components. Start a new task after installation to load the updated skills and tools, as described in the [official plugin documentation](https://learn.chatgpt.com/docs/plugins). Tools use Python 3.10+; library indexing uses PyYAML; Lean operations use the project's pinned Lean/Lake environment.

Install the whole plugin rather than copying `SKILL.md` alone: executable helpers also live under the plugin's `scripts/` and `runtime/` directories. The [DSH adaptation](https://github.com/xsoc1/math-research-dsh) consumes this repository through a one-way synchronization process.

## Research outcome repository

[Sturm-Liouville theory research](https://github.com/Zhongshan-Big-Jun/Sturm-Liouville-theory-research) uses these plugins for long-term human-agent research. It contains spectral theory proofs, open problems, failed routes, tools, computational certificates and a partial Lean development.

The plugins assist organization, exploration and verification. Contributions, mathematical status and scope are documented by that repository's actual proofs and audits. Plugin use does not imply that all results have been formalized.

## Evidence and scope

The [implementation record](docs/v2.0-implementation-status.md) distinguishes features, executed tests, migration replays and experimental scope. The [migration guide](docs/v2.0-guide.md) covers existing cards, annotations, checkpoints and verification evidence.

The frozen [L1](benchmarks/codex-20260906-l1/CONCLUSIONS.md) and [Q9](benchmarks/codex-20260908-q9/CONCLUSIONS.md) comparisons are historical 1.x experiments, not evidence of 2.0 speedups or new discoveries. All Q9 arms passed proof review; the blank arm was fastest. Evaluate 2.0 through actual reuse, correct scope and progress over a long-running project.

The [Fuse / Prove2Me report](docs/lean-verification-platform-research-2026-09-09.md) informs the design. Local implementation does not imply production integration with either service or independent reproduction of the complete Kakeya or FLT formalizations.

## Development

```bash
python3 -X utf8 scripts/validate_all.py
python3 -X utf8 tests/test_research_state.py
```

[CI](.github/workflows/validate.yml) runs the other behavior checks. Tests should check actual behavior rather than the presence of prompt keywords. Historical protocol validation explicitly uses `validate_pipeline.py --legacy-v1`.

| Path | Contents |
| --- | --- |
| `plugins/` | Installable components, concise entries and on-demand helpers |
| `tests/`, `scripts/` | Behavior checks, maintenance tools and experiment harnesses |
| `docs/` | Guides, implementation evidence, research and historical designs |
| `benchmarks/` | Frozen tasks, runs, proofs, audits and cost evidence |
| `AGENTS.md` | Maintenance methods and current session summary |

[Design](docs/v2.0-refactor-plan.md) | [Cleanup record](docs/v2.0-cleanup.json) | [Maintenance history](AGENTS_HISTORY.md)

## License and attribution

Code and documentation use the [MIT license](LICENSE). Method attribution is preserved in component references and research reports. Third-party papers, software and names retain their own licenses and attribution; no endorsement is implied.
