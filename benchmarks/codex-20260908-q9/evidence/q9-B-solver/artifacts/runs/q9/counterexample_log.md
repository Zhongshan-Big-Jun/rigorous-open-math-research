# Counterexample search record

All scans are NUMERICAL_EVIDENCE only and carry no proof weight.

- Initial constrained scan: 116 numerical roots, 46 with Q>0, no violating tuple.
- Seeded 35-second random scan: 7,855 (m,c) choices, 5,563 numerical roots, 2,958 with Q>0, no violation of the supplied sufficient condition.
- Relaxed C2+C3 probe: 373,920 sampled tuples, 55,331 with Q>0; no stronger-bound failure found.
- Omitting C3 yielded numerical violations of Q9 (relax_c3_R.json); these are not admissible Q9 counterexamples.
- Jensen polynomial exploratory probe: 200,000 points survived. Superseded as evidence by the exact integer Bernstein certificate.

Reproducibility scripts and outputs are in reproducibility/. These are historical route-selection aids, not load-bearing dependencies of answer.md.
