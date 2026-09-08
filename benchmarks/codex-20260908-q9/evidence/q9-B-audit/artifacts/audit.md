**PASS. Q9 is proved, and the target is closed. Score: 100/100.**

The submission proves a stronger result using C2 and C3: \(Q_{\rm quad}>0\) forces \(r<c^2/4\), and throughout \(0<r\le c^2/4\) it proves
\[
c^2-r>k(1-c^2)r\sin^2 B.
\]
Together with the supplied strict bound \(T_{\rm quad}<r\sin^2 B\), this gives the exact requested strict conclusion, including \(R_{\rm quad}>0\). Proving this on the larger domain requiring C2 and C3 suffices for every tuple satisfying C1-C3.

I checked the trigonometric branches, inequality directions, positivity before squaring or dividing, strict Jensen step, rational five-angle bound, transformed expression for Q, and the common-denominator identity. The case \(r=c^2/4\) is covered explicitly. No substantive gap or unresolved remainder was found; no repair was supplied.

The embedded certificate executes successfully. An independent reconstruction of equation (11), its substitutions, and a separate rational Bernstein conversion confirm degrees (26,18,4), 637 terms in F, 2,103 in G, and exactly 2,535 positive and 30 zero Bernstein coefficients. All coefficients with first index zero are positive, proving the stated uniform strict positivity for c<1. These are exact coefficient identities, not a finite numerical scan.

Scores: correctness 40/40; fidelity 20/20; strict_progress 15/15; calibration 10/10; evidence 10/10; reproducibility 5/5. Strict progress receives 15 because the two parameter ranges close the full implication, beyond the supplied starting facts.

Reproduce with `python3 candidate_certificate.py` and `python3 audit_check.py`. Exact outputs and input hashes are in `audit_check_results.json`; claim-level findings are in `audit.json`. Only TASK.md, CANDIDATE.md, and local scratch computation were used.
