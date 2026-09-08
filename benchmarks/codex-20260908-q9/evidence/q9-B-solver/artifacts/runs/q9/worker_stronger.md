# Worker O4: stronger pointwise sufficient condition

Status: RIGOROUS_PARTIAL_RESULT; started 2026-09-08 15:04 UTC, bounded deadline 15:18:30 UTC.

## Contract and scope

Authoritative input: TASK.md, read in full. All its strict domain conditions and simultaneous exact C1, C2, C3 remain hypotheses. Assigned claim O4 is

`Q_quad > 0 => c^2-r >= (m^2-1)(1-c^2) r sin(B)^2`.

This would imply Q9 using the supplied strict `T_quad < r sin(B)^2`, but a reduction to O4 alone is not progress. Parent owns global artifacts and numerical/counterexample branches. This worker edits only this file and explicitly worker-prefixed reproducibility files. No internet, prior projects, sessions, memory, or prior solutions are used. No Lean project has been provided to this worker. Novelty is not assessed.

The parent closure gate already records a direct attempt and numerical falsification probe, with decision ESCALATE. This worker is the resulting bounded analytic route. No further delegation is opened.

## Route registry

O4-A, direct trigonometric/derivative inequalities: ACTIVE. First deliverable is a bound retaining m dependence and using the exact constraints. The elementary bound obtained by ignoring the negative term of Q is already known and is not a new result.

## Research ledger

- 15:04 UTC: read TASK.md, closure_gate.md, skill and relevant phase references. Contract checked against exact parent assignment. Repository initial status recorded in tool output; all work is shared with parent, so no global commit is made by this worker.

## New lemma O4-L1: an exact upper bound supplied by C2

Let `0<c<1`, `m>0`, `0<d,g<pi/2`, and suppose `H_m(g)+c H_m(d)=c pi/2`. Then

`m^2 tan(g) tan(d) < c`.

Proof. Put `theta=pi/2-H_m(d)`, so `0<theta<pi/2` and `H_m(g)=c theta`. Strict convexity of `tan` on `(0,pi/2)` together with `tan(0)=0` gives `tan(c theta)<c tan(theta)`. Taking tangents and using the prescribed acute branches gives `m tan(g)<c/(m tan(d))`. All factors are positive, proving the claim. Under `sin(d)=sqrt(r) sin(g)`, multiplication by positive cosines gives

`m^2 sqrt(r) sin(g)^2 < c cos(g) cos(d)`.

In particular `(m^2-1) sin(g)^2 < c/sqrt(r)` for `m>1`.

## New lemma O4-L2: explicit small-root region

Under the TASK domain and C2,C3 (C1 and Q's sign are not needed), write `t=sqrt(r)`. If

`(1-c^2)c t ((1+ct)/(1-ct))^2 <= c^2-t^2`,

then strictly `k e r sin(B)^2 < c^2-r`, and hence Q9's conclusion holds.

Proof. For fixed `0<t<1`, the function `z -> asin(t sin(z))` has derivative `t cos(z)/sqrt(1-t^2 sin(z)^2) <= t` on `[0,pi/2)`. Thus `A<=tB` and `d<=tg`. By C3,

`B-g=c(A+d)<=ct(B+g)`,

so `B/g <= (1+ct)/(1-ct)`. The function `sin(z)/z` strictly decreases on `(0,pi/2)`: its derivative has numerator `z cos(z)-sin(z)<0`, since the negative of this numerator has derivative `z sin(z)>0` and vanishes at zero. Therefore `sin(B)/sin(g)<B/g`, using `B>g`. By O4-L1,

`k e r sin(B)^2 = e t^2 [k sin(g)^2] [sin(B)/sin(g)]^2 < e c t ((1+ct)/(1-ct))^2`.

The assumed elementary inequality gives the claimed strict conclusion. The existing supplied bound `T_quad<r sin(B)^2` then gives Q9. This is a proved partial region, not a proof of O4 on the full domain. It is stronger than a conditional restatement of the supplied sufficient condition because its extra hypothesis depends only on c,r and is independently shown to imply that sufficient condition from C2,C3.

## Research ledger additions

- C2+C3 relaxation probe: 20,000 standard-library floating tests found no O4 violation. Parent independently had a larger equivalent probe, so this computational branch was stopped to avoid duplication. This is numerical evidence only.
- C3 alone fails the boundary inequality `Q(k0)<=0`, where `k0=(c^2-r)/(e r sin(B)^2)`: a numerical witness is `c=.9673830277544953, r=.6735459579415752, B=.22744569237095022, g=.026414394817423095, k0=119.34888684779791`, giving `Q(k0)=.4338332640894627`. It is an obstruction to dropping C2, not a certified counterexample to O4.
- Repository-status command failed because the sandbox denied opening `/dev/null`; no repository history was read and no git mutation was attempted.
- O4-L1 and O4-L2 recorded and sent to parent immediately. No broad numerical scan is continued.

## New lemma O4-L3: tangent separation from C3

Assume `0<c<1`, `0<t<1`, `0<g<B<pi/2`, `A=asin(t sin B)`, `d=asin(t sin g)`, and C3. Then

`tan(g)/tan(B) < (1-ct)/(1+ct)`.

Proof. Set `x=A+d`, so `0<x<pi`. Strict concavity of sine on `[0,pi]` gives `sin(cx)>c sin(x)`. Further,

`sin(A+d)=t[sin(B)cos(d)+sin(g)cos(A)] > t[sin(B)cos(g)+sin(g)cos(B)] = t sin(B+g)`,

because `d<g`, `A<B`, and all factors are positive. As `B-g=c(A+d)`, these give `sin(B-g)>ct sin(B+g)`. Division by the positive `cos(B)cos(g)` yields `(tan B-tan g)>ct(tan B+tan g)`. Rearranging gives the claim, since `1+ct>0`.

- Approximately 15:12 UTC: discovered and sent O4-L3 to parent. This controls the cotangent ratio in Q more directly than the previous angle ratio; no inference from this lemma to full O4 is claimed.

## New lemma O4-L4: a sharper local consequence of C3 and Q positivity

Under the TASK domain and C3, define `u=t cos(g)/cos(d)` and `v=t cos(B)/cos(A)`, where `t=sqrt(r)`. Then `0<v<u<t`. If the first term of Q is positive, then

`[c cos(B)-t cos(A)] tan(g)/sin(B) < (c u-r)(u-c r)/[u(u+c r)]`.

Proof. The same strict sine-concavity step as O4-L3, without weakening the cosine factors, gives

`sin(B-g)>c sin(A+d)=ct[sin(B)cos(d)+sin(g)cos(A)]`.

Divide by `cos(B)cos(g)>0` and use `cos(d)/cos(g)=t/u`, `cos(A)/cos(B)=t/v`. Thus

`tan(B)-tan(g)>cr[tan(B)/u+tan(g)/v]`.

It follows that

`tan(g)/tan(B)<(1-cr/u)/(1+cr/v)`.

The left side is positive, so `u>cr`. Positivity of Q's first term is `c-r/v>0`. Multiplication and the strictly decreasing function `x -> (c-x)/(1+cx)` give

`[c-r/v] tan(g)/tan(B) < (c-r/v)(1-cr/u)/(1+cr/v) < (c-r/u)(1-cr/u)/(1+cr/u)`.

This is the displayed conclusion. Strict monotonicity `v<u` follows by differentiating `t cos(z)/sqrt(1-r sin(z)^2)`: the derivative is negative for `0<z<pi/2`.

For `J=k sin(g)^2`, Q positivity therefore implies the necessary inequality

`(c u-r)(u-c r)/[u(u+c r)] > c(1-r)^2 J/[1+c u+J(1+c r u)]`.

This is only a necessary consequence, not the missing theorem. A numerical relaxation of this inequality combined with C2 permits values with `t>=c/2`; therefore this coarse local bound by itself does not prove the desired exclusion. In that relaxation the loss occurs at large g, where replacing v by u discards too much of C3.

## New theorem O4-L5: full stronger inequality on `r<=c^2/4`

Assume `0<c<1`, `m>1`, `0<r<c^2`, `0<g<B<pi/2`, the exact TASK definitions of A,d, and C2,C3. If `r<=c^2/4`, then

`k(1-c^2) r sin(B)^2 < c^2-r`.

In particular, on this nontrivial parameter region the conclusion of Q9 holds without assuming C1 or Q positivity. The parent supplies exact nonemptiness under all original constraints via its separate small-root implicit-function branch; that existence proof is not reproduced or claimed by this worker.

Proof. Put `t=sqrt(r)` and `x=c^2`. The function `t -> (1-c^2)c t[(1+ct)/(1-ct)]^2` strictly increases for `0<t<c`, since it is a product of positive strictly increasing factors, while `c^2-t^2` strictly decreases. Therefore it suffices for O4-L2 to check `t=c/2`. At that endpoint the requisite inequality is

`2(1-x)(2+x)^2 <=3(2-x)^2`.

Its right side minus left side is

`4-12x+9x^2+2x^3=(3x-2)^2+2x^3>0`.

All reductions divide only by positive quantities (`c^2`, `(2-x)^2`) since `0<c<1`. O4-L2 now proves the strict conclusion.

## Current exact gap and decision delta

O4 remains open for `c^2/4<r<c^2`. The newly proved region requires no condition involving k, B, g beyond C2,C3, and no Q sign. A proof that all admissible Q-positive tuples have `r<c^2/4` would finish O4, but this exclusion is currently only a candidate lemma, with numerical evidence and no proof. It is not treated as a proved reduction solving the assignment. O4-L4 gives a rigorous local necessary inequality but its relaxation does not exclude the remaining region; do not repeat it without a sharper mechanism retaining the dependence of v on B.

Decision delta: add an exact `r<=c^2/4` theorem to the parent partial result, and focus any remaining full-proof effort on the named region `r>c^2/4`; do not invest in another broad scan of the already sampled C2+C3 relaxation.

## Audit and bounded handoff

The worker has rechecked O4-L1 through O4-L5 for sign and branch fidelity. All inverse trigonometric uses stay on the original acute branches; all divisions in those proofs are by explicitly positive factors. This is a local self-audit, not an independent proof certification. No Lean verification or literature audit was run. Parent is independently auditing its integrated small-root theorem. Numerical records are separated from the proved lemmas.

The direct universal O4 attempt remains BLOCKED at the explicitly named region `r>c^2/4`. The latest local relaxation was a zero-gain round: it yielded a necessary inequality but still allowed high-r parameter values, so it cannot establish the conjectured `Q>0 => r<c^2/4` without a new estimate retaining B. No certified refutation of O4 was found.

Final worker status: RIGOROUS_PARTIAL_RESULT. No global completion claimed. New independent payload is the sharpened C2 tangent bound O4-L1, the C3 tangent separation O4-L3, the local inequality O4-L4 with its stated limitation, and the resulting exact small-root stronger theorem O4-L5. Parent's own small-root artifact supersedes the duplicate exposition here for final assembly.

## New lemma O4-L6: unique algebraic Q threshold under C3

Fix `0<t<c<1` and acute geometry satisfying C3, write `r=t^2`, `u=t cos(g)/cos(d)`, and `P=[c cos(B)-t cos(A)]/sin(B)`. Regard Q as a function of an independent parameter `k>=0` with this geometry fixed. If `P>0`, then Q strictly decreases from P to a negative limit and has a unique positive zero

`k_Q=P(1+cu)/[c(1-r)^2 sin(g)cos(g)-P sin(g)^2(1+cru)]`.

In particular the displayed denominator is positive, and `Q>0` is equivalent to `0<=k<k_Q` in this fixed geometry.

Proof. The exact formula is `Q=P-a k/(b+d k)` where

`a=c(1-r)^2 sin(g)cos(g)>0`, `b=1+cu>0`, `d=sin(g)^2(1+cru)>0`.

Thus `dQ/dk=-ab/(b+dk)^2<0`. O4-L3 and `cos(A)>cos(B)` show `P<(c-t)(1-ct)/(1+ct) cot(g)`. Also `u<t`, so `a/d>c(1-t^2)^2 cot(g)/(1+ct^3)`. These imply `P<a/d` provided

`D=c(1-t^2)^2(1+ct)-(c-t)(1-ct)(1+ct^3)>0`.

Expansion gives `D=t f(t)` with

`f(t)=1+2c^2-3ct-3c^2t^2+c(2+c^2)t^3`.

Here `f'(t)=3c[(2+c^2)t^2-2ct-1]`. The bracket is a convex quadratic; at t=0 it is -1, and at t=c it is `c^4-1<0`. Convexity places it below the chord joining those values, hence it is negative throughout `[0,c]`. Thus `f(t)>f(c)=(1-c^2)(1-c^4)>0`. Consequently `P-a/d<0`, as required. Solving `P(b+dk)=ak` now gives the positive threshold and its equivalence without losing orientation.

This closes an algebraic threshold side-obligation only. It does not prove that C2 lies beyond k_Q for `r>=c^2/4`; that remains an open geometric inequality.
