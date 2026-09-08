# Research ledger

Start: 2026-09-08 13:19:07 UTC. Hard deadline 14:19:07 UTC; consolidation by 14:09:07 UTC.
Read installed workflow, manager and rigorous research skills. No prior research artifacts in workspace. Git status failed because /dev/null access is restricted; .git is read-only. Lean/lake and scipy/numpy/sympy/mpmath are unavailable on PATH/current Python. Python 3.14.4 is available.
Workflow validate_pipeline initial check passed (0 packets, 1 warning for absent Lean manifest). doctor.py was inspected but not run: its default config/plugin inspection would exceed the user restriction; required skill files are directly available. No plugin installation or network action permitted.

13:21 UTC. O1 direct elimination: for fixed m>1,c in (2/3,1), s in [0,c), a_s(z)=asin(s sin z), C2 has one g in (0,pi/2), since H(a_s(g))+H(g)/c is continuous strictly increasing from 0 to a value >pi/2. The function B-c a_s(B) has derivative 1-c s cos(B)/cos(a_s(B)) >=1-cs>0. C3 therefore has at most one B, existing exactly when g+c a_s(g)<pi/2-c asin(s), and then B>g for s>0. For s=0, B=g and C1 residual equals (3c/2-1)pi>0. This boundary is a probe only, not admissible.

Cheap probe completed: 79 approximate simultaneous roots on 11 by 11 structured (c,m) grid, 28 with Q>0, no counterexamples. Every positive-Q sample also satisfies the supplied sufficient condition. Numerics are evidence only; coarse r scanning could miss roots. This motivates a strictly stronger candidate lemma Q>0 => c²-r >= k(1-c²)r sin²B under C2,C3; falsifying or proving it determines whether C1 is needed.

Worker W1 reports 14,722 C2,C3 reduced numerical tuples, 1,547 Q-positive, no S<0 (evidence only). Stronger C2-alone lemma fails numerically; C3-alone lemma fails in a small-angle limiting test. These are route obstructions, not Q9 counterexamples. Root derived exact transformed S identity in repo/transformed_sufficient_bound.md. A separate disproof route will focus on original simultaneous constraints and possible missed branches/singular regimes; all numerical returns need certification.

2026-09-08T13:44:03.162789+00:00: Full candidate obtained and frozen in answer.md. Exact polynomial certificate checks 30 positive small-s coefficients and 1890 nonnegative complementary coefficients, 12 zero, plus all angle comparisons. No floating point used in final proof. Begin final consolidation immediately (well before active second 3000). No further research authorized after certification.

2026-09-08T13:53:38.229031+00:00: Independent fresh package audit PASS, zero gaps, full original-domain fidelity and every certificate coefficient checked. Independent exact interpolation agrees with the candidate coefficient computation. Fast-close STOP. Final proof bytes unchanged. No further research.

Final deterministic gate found that completion bindings must use paths relative to the closure-gate directory, whereas v1 used project-relative paths. This is an artifact-coordinate error; proof and verifier bytes are unchanged. Preserved v1 manifest/audit/graph under audit_v1, corrected only binding paths and graph proof anchor, and requested the independent reviewer to rebind the existing mathematical PASS to the corrected manifest. No research or new theorem change.

2026-09-08T13:56:34.336050+00:00: Independent reviewer checked only corrected manifest-coordinate bindings and rebound the existing PASS to manifest 04a7643f3e546e359bb35a1d0663e4e025318ee83229f76795dd58b857283567. Proof and coefficient checks were not repeated; mathematical bytes unchanged. STOP remains in force.
