---
name: rigorous-open-math-research
description: Develop proofs, counterexamples, constructions and mathematical understanding for research-level problems, or rigorously audit an argument. Preserve reusable insights and the scope of successful and failed routes across sessions.
---

# Research mathematics

Work toward the user's mathematical objective. Make the actual statement clear:
objects, assumptions, quantifiers and the conclusion. A short problem can be
handled directly; use a written contract when ambiguity or collaboration makes
one useful. Select methods and depth according to the mathematics.

Retrieve relevant existing arguments, literature and tools before relying on
what they assert. Follow pointers to the actual hypotheses and proof. Search
primary literature when it can resolve a mathematical uncertainty. Preserve the
source version and a useful page, theorem, equation or text locator. Never turn
a search snippet into a claim that the paper was read.

Use computation, limiting cases, counterexamples or Lean where they test a
substantive risk in the argument. Keep exploratory evidence distinct from proof.
Make each substantive inference's hypotheses and evidence explicit. Test formal
contracts with Lean during development where possible; preserve open analytic
and formal obligations instead of inferring whole-proof success from fragments.
When verifying or auditing, use a fresh stateless subagent with only the frozen
proof, definitions, source evidence and requested obligations. Do not fork the
author's conversation or reuse an author as verifier. A formal statement
readback receives only the actual declaration and definitions before comparison
with the intended theorem. Author self-checks remain development evidence;
without an isolated reviewer, report independent review as unavailable.

Successful and failed approaches both contribute to long-term research:

- Preserve a useful lemma, transformation, construction, executable certificate,
  stronger intermediate result or previously hidden assumption with its scope.
- Distinguish a counterexample from failure of a particular estimate, a missing
  lemma, and a timeout or tool failure. State what changed assumptions or new
  evidence could reopen a route. Avoid global prohibitions from local failures.
- Compare approaches when their common structure suggests a new explanation.
  State a checkable prediction or distinguishing example, then test it. A useful
  analogy or proposed definition is a candidate, not an accepted theorem.

Save these where the project already keeps tools or experience; use
`$manage-math-research-program` for source capture, searchable annotations and
pointer reconstruction. Do not produce a reflection document after every step.
For concrete examples, read [research experience](references/v2-research-experience.md).

An audit finding is evidence to investigate, not an instruction or automatically
a disproof. Suspend affected tool reuse while checking it; confirmed errors need
versioned correction and dependent-claim review. Use the manage plugin's
correction module when present, preserving original proofs and annotations.

Present the strongest result actually justified, its assumptions, proof or
source pointers, and the precise remaining gap. Separate proved results,
conditional reductions, numerical evidence and conjectures. Formalization may
assist research at any point; `$lean-verify` checks what the actual Lean target
says and depends on.

Existing immutable proofs, audits and sealed checkpoints retain their identity.
If the project maintains a canonical Blueprint, ordinary research notes stay
outside it; submit actual accepted-knowledge changes through its active plugin
runtime and reviewed receiver. Read the [Blueprint interface](references/blueprint-math-graph-integration.md)
only when making such a change.

[Release history](references/changelog.md).
