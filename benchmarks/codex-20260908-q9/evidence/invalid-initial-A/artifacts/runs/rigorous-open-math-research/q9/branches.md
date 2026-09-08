NUMERICAL_EVIDENCE — branch-search work in progress; not a proof of Q9.

Input: TASK.md SHA-256 c7133b97e440e90095088927f105c9f88fcdc54f4a4772ee9f85ba5a139e6330.
Owner: branches worker. Scope O-branches: independent simultaneous-C1--C3
search for missed branches and certified counterexamples. No internet,
external projects, prior solutions, memory, or subagents used. Root maintains
the shared contract/ledger; this file is the worker's persistent ledger.

## Exact alternate coordinates

Put M=m^2, alpha=H_m(A), beta=H_m(B), delta=H_m(d), h=H_m(g).
Then C1 and C2 are exactly

    beta=(1-c)pi+c alpha,  h=c(pi/2-delta).

For 0<theta<pi/2, the inverse transformation is

    J_m(theta)=atan(tan(theta)/m),
    sin(J_m(theta))^2=sin(theta)^2/[M cos(theta)^2+sin(theta)^2].

Write a=sin(alpha)^2, b=sin(beta)^2, D=sin(delta)^2, H=sin(h)^2.
The equality sin(A)^2/sin(B)^2=sin(d)^2/sin(g)^2, for M>0,
is equivalent to

    C0+(1/M) C1=0,
    C0=a H(1-b)(1-D)-D b(1-H)(1-a),
    C1=a H(b+D)-D b(H+a).

The quadratic terms cancel exactly. If C1 is nonzero, t=1/M=-C0/C1;
admissibility requires 0<t<1. The exceptional C0=C1=0 case must be
checked separately before calling this a complete branch classification.
C3 becomes J_m(beta)-J_m(h)-c[J_m(alpha)+J_m(delta)]=0.

## Computational protocol (before execution)

Mathematical object returned: approximate admissible tuples solving the
single residual in alpha for sampled c,delta, with M eliminated as above.
Property checked exactly: none; all transcendentals and root tests use
Python binary64. Algebraic coordinate formulas above are exact identities.
Objective: find Q>0,R<=0, or find branch geometry absent from root's scan.
Invalidity: reject t outside (0,1), angle/domain violations, and r>=c^2.
Distribution: grids and seeded random c,delta; alpha intervals include
endpoint-biased subdivisions. Exact endpoint analysis is recorded separately.
Limits: bounded by worker deadline 2026-09-08 12:35 UTC; modest memory.
Seed: 20260908 for any random search.
Certificate: approximate root brackets and full tuple; no approximate
root is promoted without a separate exact isolation certificate.
Bridge: a successful candidate would be isolated with interval estimates
and IVT while establishing Q>0,R<=0 throughout the isolating interval.
Blind spots: tangential residual roots, alpha-grid holes, near-degenerate
coefficient cancellation, binary64 overflow or underflow, unsampled c,delta.

## Ledger

- 2026-09-08 12:11 UTC: read TASK.md, skill, computation/report phases, and
  root's m-grid code. Derived algebraic elimination above independently.
- 2026-09-08 12:14 UTC: branches_scan.py evaluated 5,330 (c,delta) pairs;
  returned 536 approximate roots, 120 with Q>0, none with Q>0,R<=0,
  no sampled multiple roots. Maximum m was 19,848.44 and maximum c among
  Q-positive roots was 0.71308256. This does not bound either quantity.

## Removal of the exceptional elimination case (exact)

Under the strict transformed angle ordering delta<alpha<beta and
delta<h<beta, the case C0=C1=0 is impossible. Indeed C0+C1=aH-Db,
so both vanishing imply aH=Db. Substitution in C0=0, with aH>0,
gives (1-b)(1-D)=(1-H)(1-a), hence b+D=H+a. Thus the unordered
pairs {a,H} and {D,b} have equal sums and products and are equal.
This would require a=D or a=b, each forbidden by D<a<b.
Consequently every admissible simultaneous solution has C1 nonzero and
is represented by the alternate coordinates. The finite scan still
does not exhaust those coordinates.

## Large-m branch probe protocol

The next independent probe fixes m,s=sqrt(r) and searches in c, reversing
the root's choice of dependent variable. It uses u=m tan(g), solves the
strictly increasing C2 residual

    atan(u)+c atan(s u/sqrt(1+(1-r)u^2/m^2))=c pi/2,

and solves C3 for b=m B, retaining scaled variables when m is large.
Since A(B)<=s B (differentiate), C3 implies

    m B <= [(1+c s)/(1-c s)] m g,

providing a bounded upper bracket even for enormous m. B<pi/2 is checked
separately. Search includes m through 10^150 and logarithmic endpoint
values of s and 1-s; no candidate is exact or certified by this scan.
At formal m=infinity, u solves atan(u)+c atan(su)=c pi/2,
w=u(1+cs)/(1-cs), and C1 becomes

    atan(w)-c atan(sw)-(1-c)pi=0.

These limiting equations are diagnostic only unless a limiting argument
and all hypotheses needed for a conclusion are separately proved.

## Exact remaining gap

No universal theorem or counterexample yet. Finite scans cannot exclude
all folds or endpoint regimes, and the exceptional elimination case remains
to be treated.
