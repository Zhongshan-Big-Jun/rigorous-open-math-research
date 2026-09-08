# Completed route registry

| Route | Owner | Outcome | Artifact |
|---|---|---|---|
| Monotone elimination of C2/C3, numerical remaining C1 | root | Structural reduction; floating searches only evidence | repo/constraint_elimination.md, reproducibility/probe.py |
| Stronger bound using Q and C3 | stronger_bound | Proved for sqrt(r)<=12/25 | repo/worker_stronger_bound.md |
| Independent original-constraint disproof search | counterexample | No witness found; small-r theorem proved independently | repo/worker_counterexample.md |
| Exact exclusion of larger sqrt(r) via C2 | root | Candidate complete proof, audit pending | answer.md |

No routes remain active. C2-only and C3-only trial strengthenings failed;
C2 and C3 together suffice. C1 is still assumed for application to Q9.
