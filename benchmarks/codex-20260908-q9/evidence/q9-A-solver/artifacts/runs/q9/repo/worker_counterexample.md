RIGOROUS_PARTIAL_RESULT

# W2: branch and singular-parameter audit

## Contract and provenance

This worker attacked original Q9 literally, allowing either polarity. The sole mathematical input was `TASK.md`.

Verified authoritative SHA-256: `c7133b97e440e90095088927f105c9f88fcdc54f4a4772ee9f85ba5a139e6330`.

Restrictions: no internet, previous solutions, other projects, other workers' artifacts, session history, or remembered project materials; no subagents. Python 3.14.4 standard library only. The installed rigorous-open-math-research skill and its contract, computation, orchestration, and reporting references were read. The attempted `git status --short` failed because the environment denied opening `/dev/null`; this worker made no git commits and only wrote `worker_counterexample*` files.

Parent's supplied preflight: a prior 11-by-11 parameter scan found 79 approximate full roots, 28 Q-positive, no counterexample. This worker did not inspect or reuse its code. Acceptance for this bounded task was a rigorously isolatable negative witness, a independently derived useful partial lemma, or a reproducible negative search with exact limitations.

## Proved result

**Theorem.** Every tuple in the original domain satisfying C2 and C3 with

\[
0<\sqrt r\le \frac27
\]

satisfies \(R_{\rm quad}>0\), whether or not \(Q_{\rm quad}>0\). In particular Q9 is true on this subdomain. The subdomain contains tuples satisfying all of C1--C3.

This goes beyond the supplied starting facts: it derives a parameter condition independent of \(m,B,g\) that guarantees the supplied sufficient inequality, and proves that the resulting domain contains full admissible solutions.

### General bound from C2 and C3

Put \(s=\sqrt r\) and \(L=(1+cs)/(1-cs)\). Then

\[
k(1-c^2)r\sin^2 B < (1-c^2)s L^2. \tag{1}
\]

Indeed C2 gives

\[
H_m(g)+H_m(d)=c\frac\pi2+(1-c)H_m(d)<\frac\pi2.
\]

The two angles are positive, so their tangent product is less than 1:

\[
m^2\tan g\tan d<1.
\]

Since \(\sin d=s\sin g\), it follows that

\[
m^2s\sin^2g<\cos g\cos d<1,
\qquad k\sin^2 g<\frac1s. \tag{2}
\]

Strict concavity of sine on \([0,\pi/2]\) gives
\(\sin(sz)>s\sin z\) for \(0<s<1\), \(0<z<\pi/2\). Since both sides are in the principal increasing sine range,

\[
\arcsin(s\sin z)<sz.
\]

Consequently C3 implies

\[
B-g=c(A+d)<cs(B+g),
\quad \frac Bg<L.
\]

The function \(\sin z/z\) is strictly decreasing on \((0,\pi/2)\): its derivative has numerator \(z\cos z-\sin z<0\), because \(\sin z-z\cos z\) has positive derivative \(z\sin z\) and vanishes at zero. Therefore

\[
\frac{\sin B}{\sin g}<\frac Bg<L.
\]

Multiplying this squared bound by (2) proves (1).

### Uniform estimate for s at most 2/7

For fixed \(0<s\le2/7\), define

\[
f_s(c)=(1-c^2)\left(\frac{1+cs}{1-cs}\right)^2.
\]

Its logarithmic derivative is

\[
\frac{f_s'(c)}{f_s(c)}
=-\frac{2c}{1-c^2}+\frac{4s}{1-c^2s^2}.
\]

It is negative whenever \(2s<c\): indeed
\(2s(1-c^2)<c(1-c^2)<c(1-c^2s^2)\). The condition holds throughout \(c>2/3\), \(s\le2/7\). Hence

\[
(1-c^2)sL^2
\le \frac59\cdot\frac27\left(\frac{1+4/21}{1-4/21}\right)^2
=\frac{6250}{18207}.
\]

Here monotonicity of \(s((1+(2/3)s)/(1-(2/3)s))^2\) in \(s>0\) is immediate from its positive factors, each increasing. On the other hand,

\[
c^2-s^2>\frac49-\frac4{49}=\frac{160}{441}.
\]

The exact difference is

\[
\frac{160}{441}-\frac{6250}{18207}=\frac{830}{42483}>0.
\]

Together with (1), this proves

\[
c^2-r>k(1-c^2)r\sin^2B.
\]

The supplied strict inequality \(U<V\sin^2B\), and positivity of all factors, now give \(R_{\rm quad}>0\).

### Nonemptiness under all three constraints

Fix \(m=2\), and temporarily extend parameters to a neighborhood of \((c,s)=(2/3,0)\). Define \(g(c,s)\) and \(B(c,s)\) as the local roots of C2 and C3, with
\(d=\arcsin(s\sin g)\), \(A=\arcsin(s\sin B)\). At \(s=0\), these are

\[
g(c,0)=B(c,0)=\arctan\left(\frac{\tan(c\pi/2)}m\right).
\]

These roots depend continuously and differentiably on \((c,s)\) near the base point. To check the implicit-function hypotheses directly, the derivative of
\(H_m(g)+cH_m(d)-c\pi/2\) with respect to \(g\) at \(s=0\) is \(H_m'(g)>0\); after solving this equation, the derivative with respect to \(B\) of \(B-g-c(A+d)\) at \(s=0\) is 1. All functions involved are continuously differentiable near the base point, which lies away from inverse-trigonometric endpoints.

Set

\[
\Phi(c,s)=H_m(B(c,s))-cH_m(A(c,s))-(1-c)\pi.
\]

Then \(\Phi(c,0)=\pi(3c/2-1)\). Differentiation at \(s=0\), writing \(x=\sin^2g(c,0)\), gives

\[
g_s=-c\sin g(1+kx),\qquad
B_s=c\sin g(1-kx),
\]

and hence

\[
\Phi_s(c,0)=-\frac{2cmk\sin^3g}{1+k\sin^2g}<0. \tag{3}
\]

At \(c=2/3\), choose a sufficiently small fixed \(s_0\in(0,2/7)\), so that \(\Phi(2/3,s_0)<0\). By continuity the same negative sign holds for all \(c>2/3\) sufficiently close to \(2/3\); their value \(\Phi(c,0)\) is positive. The intermediate value theorem yields \(s\in(0,s_0)\) with \(\Phi(c,s)=0\). C1--C3 hold simultaneously. By choosing the neighborhood sufficiently small, \(g>0\), \(B<\pi/2\), and \(s<c\); C3 at positive \(s\) gives \(B>g\). Thus these are genuine full admissible tuples in the asserted subdomain.

At the base point \(s=0,m=2,c=2/3\), the continuous extension of Q equals
\(c\cot g/(1+k\sin^2g)>0\). Shrinking the same neighborhood therefore even yields full admissible examples with Q-positive antecedent. This last statement uses continuity only and is not needed for the theorem.

## Numerical work, coverage, and limitations

All scripts use binary64 `math` trigonometric functions and bisection. They are discovery instruments, not exact certificates. C2 is solved in the stable coordinate \(y=H_m(g)\), and then C3 is solved for B using its strictly positive B derivative; infeasible points are omitted. Sign changes of the reduced C1 residual in s are isolated numerically. Mathematical objects returned are approximate tuples; objectives are Q>0 with R<=0, additional roots, and failure of the stronger sufficient condition. Invalidity is never incorporated into an objective score: points without feasible C3 are discarded.

1. `worker_counterexample_search.py` used 340 structured (m,c) pairs, including m-1 down to 1e-8, m up to 1e8, c-2/3 and 1-c down to 1e-8. It returned 199 approximate C1--C3 roots, 109 Q-positive, zero Q-positive/R-nonpositive candidates, and zero multiple sign-changing roots. The scan data retain the full parameter grid. Every Q-positive root had positive `sufficient = c²-r-k e r sin²B` (minimum approximately 0.428649).
2. `worker_counterexample_explore.py`, seed 906081729, scanned 2,500 random/adversarial (m,c) pairs, m-1 log-uniform from 1e-6 to 1e6 and mixed uniform/log distributions in c. It returned 1,364 approximate full roots, 565 Q-positive, zero counterexample candidates, and maximum one sign-changing root per pair. Every Q-positive root again had positive `sufficient` (minimum approximately 0.386199). It additionally generated 10,000 random C2/C3 cases; after feasibility filtering, none met Q>0 and `sufficient`<=0.
3. `worker_counterexample_qboundary.py`, seed 926001, scanned 5,000 further (m,c) pairs under only C2/C3, including m-1 from 1e-5 to 1e7. It sought Q=0 boundaries and monitored \(S=k e r\sin^2B/(c^2-r)\). The largest approximate S among its Q-positive candidates was about 0.168166. These cases generally do not satisfy C1 and are explicitly not original-target witnesses.

Blind spots: sign-change searches can miss tangent roots or narrow intervals between sampled s values. Binary64 bisection with a fixed absolute B interval becomes relatively inaccurate for m near 1e8; two nonmonotone residual flags occurred at that scale and are not accepted as genuine branches. Some reported near-Q-boundary values at very large m remain appreciably positive because angular rounding is amplified; no such value is a certificate. No interval arithmetic or exact root isolation was performed because no negative candidate was found. The scans neither prove branch uniqueness nor Q9 outside the proved subdomain.

## Reproducibility

Replay from the workspace:

```
python3 runs/q9/repo/worker_counterexample_search.py
python3 runs/q9/repo/worker_counterexample_explore.py
python3 runs/q9/repo/worker_counterexample_qboundary.py
```

Each script writes its same-prefix JSON data file. Recorded runtime on this environment was approximately 0.64, 4.94, and 6.65 seconds, respectively. Those timings exclude reasoning and tool interaction. Code and JSON hashes are recorded in `worker_counterexample_hashes.json`.

## Remaining gap and decision delta

Original Q9 for \(\sqrt r>2/7\) is unresolved by this worker. No certified counterexample or candidate requiring isolation was found. Branch uniqueness and global nonexistence of negative tuples remain unproved.

Decision delta: deprioritize blind full-constraint scanning; the large numerical gap to the stronger sufficient boundary favors proving Q+C2+C3 imply that boundary. The proved C2/C3 small-s theorem is an independent fallback with an exact nonempty domain. Parent informed this worker that a separate possible full route is under development; none of that route's artifacts was read or used here.

Novelty is not assessed, as all external searches were forbidden. Confidence: high in statement fidelity and the elementary proofs after self-check; incomplete for original Q9; numerical reproducibility bounded by ordinary platform binary64 behavior. This report is not independently audited and does not claim global completion.
