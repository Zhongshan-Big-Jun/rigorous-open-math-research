# O-Qbound: analytic sufficient-bound implication

Owner: delegated `qbound` agent. Input: `TASK.md`, expected SHA-256
`c7133b97e440e90095088927f105c9f88fcdc54f4a4772ee9f85ba5a139e6330`.
Allowed provenance: task statement, current-run artifacts, installed skill.
No external literature, prior runs, network, or extra agents.

## Contract and closure gate

Try to prove, or exactly refute, under the task domain and C2,C3 (C1 may be
used if needed),
\[
 Q_{\rm quad}>0\implies c^2-r\ge (m^2-1)(1-c^2)r\sin^2 B.
\]
This is sufficient for Q9 by the supplied strict bound on T. It is a
stronger auxiliary statement, so refuting it alone does not refute Q9.

Parent preflight: 3000 random C2,C3 tuples gave 370 Q-positive tuples and
no numerical violation; this is evidence only. The first direct route
uses monotonicity of Q in k=m²−1 and evaluates it at
K=(c²−r)/[(1−c²)r sin² B].

## Route card

- Route key: `qbound_monotone_k_geometry`.
- Mechanism: Q is decreasing in k with c,r,B,g fixed; C3 determines g.
- Deliverable: show Q(K)≤0 under C3, or find an obstruction identifying the
  role of C2/C1.
- First test: sample c,r,B, solve C3 by bisection, evaluate Q(K).
- Cost tier: 1, standard-library binary64 exploratory computation only.
- Escalation criterion: an explicit geometric counterexample demands using
  C2; no broader scan without a new named inequality.
- Status: ACTIVE.

## First computation specification

Object: tuples c,r,B and g defined by C3.
Property: numerical sign of Q evaluated at K (not exact certification).
Score: largest Q(K), validity checked separately from score.
Domain/distribution: 10000 pseudorandom tuples, c uniform (2/3,1),
sqrt(r)/c uniform (0,1), B uniform (0,pi/2).
Arithmetic: binary64 and 60-step bisection, seed 290091.
Time/memory: short finite scan, no external numerical packages.
Certificate: replay script and maximal sampled tuple. Passing is only
evidence; a failure falsifies a route numerically until exact certification.
Blind spot: boundary limits and rounding can invalidate sign conclusions.

## Ledger

- 2026-09-08 12:07 UTC: skill and TASK read. The task hash will be checked
  before packaging. No accepted new theorem yet.
- 2026-09-08 12:10 UTC: first command `python` was unavailable; replay uses
  `python3`. The C3-only monotone-k route failed numerically in 898/10000
  samples. Largest sampled Q(K): c=0.8379228799778374,
  r=0.5058397731401507, B=0.0007748014330401752,
  g=0.00019615751957320675, K=2169812.605987971,
  Q(K)=112.43325502196052. This is an obstruction to dropping C2, not a
  certified counterexample to any task claim. Route status: BLOCKED.
- New mechanism: enforce C2 through x=m tan(g) and
  a=sqrt(r) cos(g)/cos(d), so atan(x)+c atan(a x)=c pi/2.
  Here 0<a<sqrt(r)<c<1. In particular x>tan[c pi/(2(1+c))]
  and a x²<c. These follow from monotonicity of arctan and convexity of tan,
  respectively; full proof will be packaged if either becomes load-bearing.

## Second computation specification

Prediction: Q>0 under C2,C3 excludes the large-r region in which the pure
C3 algebraic sufficient criterion fails. Return max r among Q-positive
tuples and max sufficient-bound ratio, not a theorem.
Sample 30000 tuples with c uniform (2/3,1), sqrt(r)/c uniform (0,1), and
log10(m-1) uniform (-3,4), seed 290092. C2,C3 roots use the current-run
`reproducibility/explore.py` bisection. Invalid-angle tuples are excluded.
Arithmetic: binary64 only; exact constraints are not certified. Preserve
the extremal tuples in a qbound-only file. Time budget under one minute.

Second probe result: valid tuples 23650; Q-positive tuples 3679. Largest
sampled r among Q-positive tuples was 0.0597935723271213 at
(m,c)=(1.00133475085486,0.6698497394805489). Largest sufficient-bound ratio
was 0.15809659297223444, at r=0.04423362992712607,
m=171.17409236458786, c=0.6701124087067245. The extremal records are in
`qbound_c2probe.json`. Numerical evidence only.

## Proved geometric reduction (candidate, awaiting independent audit)

Write q=sqrt(r), y=sin²g, w=k y and
\[
N=q[1+2c^2-3cq-3c^2q^2+c(2+c^2)q^3].
\]
Under the task domain and C3, Q>0 implies
\[
w<Z:=\frac{(c-q)(1-c^2q^2)}{N}.
\]
Indeed sin is concave on [0,pi], and B-g=c(A+d), so
sin(B-g)≥c sin(A+d). Hence
\[
\frac{\sin B}{\sin g}\ge
\frac{\cos B+cq\cos A}{\cos g-cq\cos d},
\]
where the denominator is positive because the numerator and sin B are
positive. Q>0 also gives c cosB−q cosA>0. Since
z=cosB/cosA<1 and (cz−q)/(z+cq) is increasing in z,
\[
\sin g\,\frac{c\cos B-q\cos A}{\sin B}
 \le\frac{c-q}{1+cq}(\cos g-cq\cos d).
\]
Divide the positive Q inequality by cosg and set beta=cosd/cosg>1.
Its right summand is
c w(1−q²)²/[1+cq/beta+w(1+cq³/beta)]. Replacing beta by 1 increases
the upper bound on the first term and the denominator of the right term.
Consequently
\[
\frac{(c-q)(1-cq)}{1+cq}>
\frac{c w(1-q^2)^2}{1+cq+w(1+cq^3)}.
\]
Cross multiplication gives wN<(c−q)(1−c²q²). N>0: the bracket P(q)
has derivative 3c[(q−c)((2+c²)q+c³)+(c⁴−1)]<0 on 0<q<c;
therefore P(q)>P(c)=(1−c²)²(1+c²)>0.

Also A≤qB and d≤qg, since z↦asin(q sin z) has derivative at most q.
C3 then gives B/g≤(1+cq)/(1−cq), and decreasing sin(z)/z gives
\[
\frac{\sin B}{\sin g}\le L:=\frac{1+cq}{1-cq}.
\]
Thus Q>0 yields k sin²B<L² Z. The desired sufficient inequality follows
on the explicit algebraic subdomain
\[
G:=(c+q)N(1-cq)-(1-c²)q²(1+cq)^3\ge0.
\]
This is narrower and independently checkable; it uses Q to obtain a bound
not supplied in TASK, but it does not yet establish the entire target.

## Explicit partial theorem: r≤c²/4

The algebraic criterion G>0 holds for 2/3<c<1 and 0<q≤c/2. Indeed direct
expansion gives
\[
\frac{G}{cq}=(1-cq)(1+2c²)(1-q²)^2
 -(1-c²)q²[(5-q²)+cq(3+q²)].
\]
Here 1−cq≥1/2, 1+2c²≥17/9, and 1−q²≥3/4, so the first term is
at least 17/32. Also (1−c²)q²≤c²(1−c²)/4≤1/16, and the bracket
is at most 5+(1/2)(3+1/4)=53/8. Therefore
G/(cq)≥17/32−53/128=15/128>0.
The previous lemma now gives k(1−c²)r sin²B<c²−r whenever Q>0.
No C1 or C2 was used in this partial theorem.

Next named gap: can C2 plus C3 plus Q>0 imply q≤c/2? A relaxed probe will
retain beta=cosd/cosg in the geometric Q bound, parameterizing
a=q/beta and x=m tan g from atan(x)+c atan(a x)=c pi/2. Its domain is
c in (2/3,1), q in [c/2,c), a in (0,q), with m>1 checked after reconstructing
sin²g=(q²−a²)/(q²(1−a²)). Test 10000 tuples with seed 290093; binary64 only.
Output any failure of the relaxed algebraic exclusion. This checks whether
the missing B dependence must be retained before investing in a proof.
