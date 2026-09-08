RIGOROUS_PARTIAL_RESULT

# Worker W1: the stronger sufficient-bound route

## Contract, status, and decision

The assigned claim is that, on the TASK.md domain and imposing C2 and C3,
`Q_quad > 0` implies `S = c^2-r-(m^2-1)(1-c^2)r sin(B)^2 >= 0`.
C1 is omitted only in this worker's stronger trial claim. The full assigned
claim remains open. The following partial theorem is proved:

**Theorem.** Assume the TASK.md domain, C3, and
`sqrt(r) <= 12/25`. Then `Q_quad > 0` implies `S > 0`.
Neither C1 nor C2 is needed for this theorem. In the smaller subdomain
`sqrt(r) <= 1/3`, the quantitative bound is
`S > (7/27)(c^2-r)`.

Consequently the original Q9 implication holds for every originally
admissible tuple with `r <= 144/625`, by the supplied strict bound
`T_quad < r sin(B)^2`. The exact remaining W1 gap is the region
`12/25 < sqrt(r) < c`, with C2 and C3 both imposed. No numerical scan is
being used to exclude that region.

**decision_delta:** W1 is reduced to the complementary region
`sqrt(r)>12/25`; this replaces the proposed complementary threshold `1/3`.
A C2-only version is rigorously false (exact witness below). The present
worker does not decide whether C1 is essential for the full Q9 result.

## Proof of the partial theorem

Write `s=sqrt(r)`, `e=1-c^2`, `k=m^2-1`,
`w=k sin(g)^2`, and `K=(1+cs)/(1-cs)`. All are positive.
Let `a(z)=asin(s sin z)`, so A=a(B) and d=a(g).

### 1. Two consequences of C3

Since

`a'(z)=s cos(z)/sqrt(1-s^2 sin(z)^2) <= s`,

we have `a(z)<=sz`. C3 therefore gives
`B-g=c(A+d)<=cs(B+g)`, whence `B/g<=K`.
The function `sin(z)/z` decreases on `(0,pi/2)` because its derivative
has numerator `z cos(z)-sin(z)<0` (differentiate that numerator).
Consequently

`sin(B)/sin(g) <= B/g <= K`.                                      (1)

For the second consequence, put `X=cot(B)` and `Y=cot(g)`.
Strict concavity of sine on `[0,pi]` and C3 give

`sin(B-g)=sin(c(A+d)) > c sin(A+d)`.

Here `0<A+d<pi` and `0<c<1`, so the strict concavity application is
within its domain. Expanding both sides and dividing by
`sin(B)sin(g)>0` yields

`Y-X > cs [sqrt(Y^2+1-r)+sqrt(X^2+1-r)]`.

Both square roots exceed the corresponding positive cotangent. Thus
`(1+cs)X < (1-cs)Y`, or `X/Y<1/K`. If

`f(B)=(c cos(B)-s cos(A))/sin(B)
     =cX-s sqrt(X^2+1-r)`,

then `f(B)<(c-s)X`, and hence

`f(B) tan(g) < L := (c-s)(1-cs)/(1+cs)`.                          (2)

### 2. An explicit upper bound for w from Q positivity

Set `rho=s cos(g)/cos(d)`, so `0<rho<s`. Dividing the denominator of
the second term of Q by `cos(d)` shows exactly that

`Q_quad tan(g)
 = f(B)tan(g) - c(1-r)^2 w/[1+w+c rho(1+r w)]`.

Therefore `Q_quad>0`, (2), and `rho<s` imply

`L > c(1-s^2)^2 w/[1+cs+(1+cs^3)w]`.

Define

`P(c,s)=1+2c^2-3cs-3c^2s^2+c(2+c^2)s^3`.

Direct expansion gives

`c(1-s^2)^2(1+cs)-(c-s)(1-cs)(1+cs^3)=s P(c,s)`.

We check the sign before dividing. For fixed `0<c<1`,

`P_s=3c[(2+c^2)s^2-2cs-1]`.

The bracket, being convex in s, is at most the larger of its endpoint
values `-1` and `c^4-1` on `[0,c]`; both are negative. Hence P decreases
on that interval, and

`P(c,s)>=P(c,c)=(1-c^2)(1-c^4)>0`.

Rearranging the preceding strict Q inequality now gives the global
C3-only necessary condition

`w < (c-s)(1-c^2s^2)/(s P(c,s))`.                                (3)

Combining (1) and (3),

`k e r sin(B)^2/(c^2-r)
 < e s(1+cs)^3/[(c+s)(1-cs)P(c,s)]`.                             (4)

Thus `S>0` follows whenever

`E(c,s):=(c+s)(1-cs)P(c,s)-(1-c^2)s(1+cs)^3 >= 0`.                (5)

This criterion is a newly proved sufficient condition obtained from Q
and C3, rather than an assumption of the supplied sufficient S bound.

### 3. Elementary quantitative bound when s<=1/3

For `2/3<c<1` and `0<s<=1/3`,

`P>=1+2c^2-c-c^2/3=1-c+(5/3)c^2>=1`.

Equation (3) implies `w<(c-s)/s`. Also `e<=5/9`,
`s/(c+s)<=1/3`, and `K<=2`. Using (1),

`k e r sin(B)^2/(c^2-r)
 <= e s^2 K^2 w/[(c-s)(c+s)]
 < e s K^2/(c+s) <= (5/9)(1/3)4=20/27`.

This proves the stated strict quantitative bound.

### 4. Exact polynomial certificate for s<=12/25

Expansion of (5) gives

`E=c+2c^3-(c^2+2c^4)s+(-7c+c^3)s^2
      +(-c^2+7c^4)s^3+(2c+c^3)s^4+(-2c^2-c^4)s^5`.

Put `u=3c-2` and `v=25s/12`. In the claimed rectangle both lie in
`[0,1]`. With `b_i^n(t)=binom(n,i)t^i(1-t)^(n-i)`, the following exact
identity is a certificate:

`E((2+u)/3,12v/25)
  = (1/1054687500) sum_{i=0}^4 sum_{j=0}^5 N_ij b_i^4(u)b_j^5(v)`.

The rows `i=0,...,4`, with columns `j=0,...,5`, of N are

```text
1328125000 1243125000 1051925000  765469000  412948680  12607112
1650390625 1534140625 1300215625  966327625  571546705 138478561
2050781250 1891406250 1603781250 1216202250  781848450 330011178
2548828125 2329453125 1972378125 1522315125 1052902845 604001061
3164062500 2860312500 2410762500 1885396500 1387790820 974492532
```

The identity is verified by expansion; a short exact-arithmetic checker
is included in `worker_stronger_bound_check.py`. Every listed integer is
positive. The Bernstein basis functions are nonnegative and their
double sum is 1. Therefore

`E>=12607112/1054687500=3151778/263671875>0`

throughout the closed rectangle. Applying (4) proves `S>0`.

## Exact obstruction to dropping C3

The C2-only strengthening is false. Set

`m=10`, `c=3/4`, `r=101/301`,
`g=atan(1/10)`, `d=atan(1/(10 sqrt(3)))`,
`sin(B)^2=1093/69993`, and `A=asin(sqrt(r)sin(B))`.

Then `sin(d)^2=r sin(g)^2`, so d has exactly the required definition.
Also `H_m(g)=pi/4` and `H_m(d)=pi/6`, which prove C2 exactly.
The given value of `sin(B)^2` is
`(c^2-r)/(k e r)`, so `S=0` exactly. The original domain holds:
`r<c^2`, `sin(B)^2>sin(g)^2=1/101`, and both are below 1.
The expression for Q reduces to

`Q=(3/4)sqrt(68900/1093)-sqrt(2116707500/99026893)
   -(29700000/9150701)/(200/101+100 sqrt(3)/301)`.

Use the exact rational bounds

`sqrt(68900/1093)>7939/1000`,
`sqrt(2116707500/99026893)<4624/1000`,
`sqrt(3)>1732/1000`.

Each follows by squaring positive rationals. Substitution in the
displayed Q expression gives a rational lower bound greater than
`3/50`. The checker verifies these four rational comparisons. Thus
`Q>0` and `S=0` with C2 exactly. This witness is not claimed to satisfy
C1 or C3 and does not refute the actual task.

## Numerical ledger (evidence only)

A seeded floating-point scan, solving C2 and C3 by monotone bisection,
sampled 15,000 tuples with c uniform on `(2/3,1)`, s uniform on `(0,c)`,
and log(m) uniform on `(0,log(10^6))`, seed 9029. It obtained 14,722
admissible reduced tuples and 1,547 Q-positive ones, with no S-negative
Q-positive tuple. The smallest observed S was about 0.341731.

A second scan of 80,000 similarly sampled tuples with `m<10^4`,
seed 99229, found maximum Q-positive s about 0.2345660885 at
`m=1.0042509427`, `c=0.6827390722`, `B=1.2216138687`,
`g=0.9397906250`. This numerical result does not prove a bound on s.
These exploratory scans were run directly in the shell and are not
part of the exact certificate.

## Verification, provenance, and remaining gaps

The proof was checked in a separate local pass for signs, strictness,
the domains of sine concavity and the square roots, positivity before
division, and all endpoint cases in the certificate rectangle.
The supporting checker uses Python standard-library Fraction arithmetic
only. Lean and an independent worker audit were not run by this worker;
the root owns acceptance and final package audit.

The C2/C3-only Q-positive small-r region is nonempty: at the extended
value s=0, C2 gives `g=atan(tan(c pi/2)/m)` and C3 gives `B=g`.
At that limit `Q=c cot(g)/(1+k sin(g)^2)>0`. The supplied monotone
elimination and continuity then give admissible C2/C3 solutions with
`s>0` sufficiently small and Q positive. This assertion does not claim
C1 for those solutions.

Only TASK.md, the supplied current-run elimination artifact, and the
installed skill instructions were read. No internet, prior projects,
memory, session files, or external mathematics libraries were used.
The input hashes checked at the start were:

* TASK.md: `c7133b97e440e90095088927f105c9f88fcdc54f4a4772ee9f85ba5a139e6330`.
* constraint_elimination.md:
  `16f56af4a2284927fa65ca28eca8dc1f37a23bcd4e54eba3721f291bd986614a`.

No novelty claim is made. No shared ledgers, git state, or parent-owned
files were modified. Full W1 and full Q9 remain unresolved in this
worker artifact; the frontier is exactly the complementary region
`sqrt(r)>12/25`, with both C2 and C3 retained.
