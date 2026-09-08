**PASS — target PROVED; root closed. Score: 100/100.**

The candidate proves the stronger inequality
\(S=c^2-r-(m^2-1)(1-c^2)r\sin^2 B>0\) whenever \(Q_{\rm quad}>0\).
The supplied identity then yields the required strict \(R_{\rm quad}>0\).
No substantive gap or false mathematical claim was found, and no repair was
added to the submitted proof.

The load-bearing chain checks: C3 supplies the strict cotangent inequality
and the bound \(w<W\); the polynomial \(P\) used in division is positive.
The small-range Bernstein certificate proves \(S>0\) for
\(0<\sqrt r\le12/25\). In the complementary range, the positive inverse
branch and monotonicity arguments correctly bound both arctangent arguments.
The table then contradicts the exact C2 constraint. C1 remains an admissible
hypothesis; establishing the conclusion under C2-C3 alone includes every
tuple satisfying all three constraints.

The embedded verifier ran successfully. An independently written checker,
using exact rational interpolation and Bernstein coefficient recovery,
confirmed the certificate without importing the submitted implementation:

- All 30 small-range coefficients are strictly positive.
- All 1,890 complementary coefficients are nonnegative, with exactly 12
  zeros; every claimed bidegree and coefficient count agrees.
- The four angular contradictions have strict margins exceeding
  \(13/1600,13/1400,7/2400,3/80\), using only \(\pi>25/8\).

These are uniform polynomial certificates with justified degree bounds,
not numerical scans. The parameter ranges cover all required values,
including the internal seams. Singular endpoints are used only for
polynomial certification; division stays inside the original open domain.
The inverse-root uniqueness claim and both strict target inequalities were
checked explicitly.

Scores: correctness **40/40**, fidelity **20/20**, strict progress **15/15**,
calibration **10/10**, evidence **10/10**, reproducibility **5/5**. Full strict
progress is warranted because the argument proves the sufficient inequality
from the hypotheses and closes the entire target, beyond TASK.md's starting
facts. Both gap arrays are empty.

Detailed claim checks are in [audit.json](audit.json). Reproduce the exact
calculations with `python3 audit_scratch/verify_submitted.py` and
`python3 audit_scratch/independent_check.py`; the latter writes
[independent_results.json](audit_scratch/independent_results.json).
Only TASK.md, CANDIDATE.md and local scratch tools were used.
