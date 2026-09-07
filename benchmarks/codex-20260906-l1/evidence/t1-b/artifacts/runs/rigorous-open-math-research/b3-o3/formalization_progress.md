# Formalization progress

Decision: scaffold. Verification tier: 0 statement scaffold, UNCHECKED.
Artifact: lean-proof/B3O3.lean (workspace-relative).

Observed environment: `command -v python3 lean lake` returned /usr/bin/python3
and no Lean or Lake path. No build was run. No dependencies were downloaded.
Formal verification is not requested by the user and is not claimed.

| Informal obligation | Scaffold declaration |
| --- | --- |
| O0 interior root count and derivative simplicity | B3O3.root_count |
| O1 determinant and trace | B3O3.matrix_invariants |
| O2 quotient identity, degree and leading coefficient | B3O3.polynomial_representation |
| O3 scalar root count and simplicity | B3O3.scalar_roots |
| O4 all polynomial roots and strict location | B3O3.polynomial_roots |
| O5 n=1; endpoints/midpoint; R=1 | B3O3.n_one, B3O3.special_y, B3O3.constant_density_boundary |

Exact formalization gap: all eight proof bodies contain `sorry`; compilation,
formal statement fidelity, and proof completion are unverified. This gap is
separate from the complete elementary mathematical argument.
