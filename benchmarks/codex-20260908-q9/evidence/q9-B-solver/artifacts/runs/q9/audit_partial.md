RIGOROUS_PARTIAL_RESULT

# Independent claim-local audit

**Verdict: PASS.** This verdict concerns the algebraic restricted-domain theorem and its exact nonempty admissible branch. It does not certify Q9 on the full domain.

## Inputs and scope

The only mathematical inputs read were:

- `TASK.md`, SHA-256 `c7133b97e440e90095088927f105c9f88fcdc54f4a4772ee9f85ba5a139e6330`.
- `runs/q9/partial_algebra.md`, initial SHA-256 `1414740994967772ede01684c3f365f264d81354d18804de452d48e6658c1ea6`; final reviewed SHA-256 `036931d3974fb6736691bc5a0990933e081e26462c8da7e33a9ade3555c1b353`.

The final revision only makes the smooth extension of H near zero explicit. That revision was read and agrees with the extension independently checked below. This PASS binds to the final reviewed hash.

The installed rigorous-open-math-research skill and its audit/reporting instructions were also read. No external mathematical sources, other projects, sessions, memory, or numerical branch data were used. All mathematical checks below were independently recomputed from the definitions. No claimed new lemma was accepted on the author's authority.

The audited statements are:

1. On the task's domain, even without C1--C3, positivity of Q implies
   `sin(B)^2 < (c^2-r)/(c^2-r^2)`.
2. Q9 holds, under C1--C3, on the additional subdomain
   `(m^2-1)(1-c^2)r <= c^2-r^2`.
3. This additional condition holds whenever `1<m<=sqrt(2)`.
4. For every fixed `m>1`, that subdomain contains exact admissible tuples with Q positive, obtained by a local implicit-function branch.

## Algebraic implication and strict signs

Write `k=m^2-1>0`, `e=1-c^2>0`, `s_B=sin(B)^2`, and `D=c^2-r^2`. Since `0<r<c^2<1`, both `c^2-r` and `D` are positive. Every factor in the second, subtracted term defining Q is positive: in particular `1-r>0`, `sin(g)>0`, `cos(g)>0`, and `cos(d)>0`. Its denominator is a sum of positive terms.

Thus `Q>0` implies `c cos(B)>sqrt(r) cos(A)`. Both sides are strictly positive, so squaring preserves this strict inequality. The identity `sin(A)^2=r sin(B)^2` gives

`c^2(1-s_B)>r(1-r s_B)`,

which is exactly

`D s_B<c^2-r`.

Division by `D>0` proves claim 1, without losing orientation.

Under condition (P), `k e r<=D`. Therefore

`k e r s_B <= D s_B < c^2-r`.

The supplied strict bound `T_quad<r s_B`, with `k e>0`, now gives

`k e T_quad < k e r s_B < c^2-r`.

This proves the strict conclusion Q9. In particular, equality in (P) causes no loss of strictness. No constraint has been replaced, approximately imposed, or supplemented by mass balance. The proof uses fewer than all three constraints, which is permissible for a theorem asserted on their simultaneous solution set.

When `1<m<=sqrt(2)`, `0<k<=1`. Direct expansion verifies

`c^2-r^2-e r = (c^2-r)(1+r)>0`.

Hence `k e r<=e r<c^2-r^2`, proving claim 3 with room to spare. The allowed endpoint `m=sqrt(2)` is included. The endpoint `m=1` is not claimed.

Relative to the supplied starting facts, the additional input is the proved angular restriction forced by Q positivity. It converts the supplied angle-dependent sufficient condition into the stated range depending only on `(m,c,r)`. This is a restricted-domain consequence and does not establish global Q9 or external-literature novelty.

## Exact branch and all first derivatives

Fix an arbitrary `m>1`; all neighborhoods below may depend on this fixed `m`. Put

`b=atan(sqrt(3)/m)`, `c0=2/3`, `h=(m^2+3)/(4m)`, `s=sin(b)>0`.

Use the residuals

`E1=H(B)-(1-c)pi-c H(asin(t sin(B)))`,

`E2=H(asin(t sin(g)))+H(g)/c-pi/2`,

`E3=B-g-c[asin(t sin(B))+asin(t sin(g))]`.

For the IFT, use the same elementary formula `H(z)=atan(m tan(z))` also for `z` in a small two-sided neighborhood of zero. This is a smooth extension of the originally specified H and is needed only to make an open neighborhood of `t=0`. For positive t the construction uses H solely in its original domain.

Because `b` lies strictly between zero and `pi/2`, all tangent evaluations are smooth near the base point; the arcsine arguments are near zero; and `c` stays away from zero. The residual map is therefore smooth on an open neighborhood of `(t,B,g,c)=(0,b,b,2/3)` in `R^4`. This neighborhood need not obey the final task inequalities, which will be imposed after constructing the positive-t branch.

Directly,

`H(b)=pi/3`, `H(0)=0`, and `E(0,b,b,2/3)=0`.

Differentiating H independently gives

`H'(z)=m/(cos(z)^2+m^2 sin(z)^2)=m/(1+k sin(z)^2)`.

Since `sin(b)^2=3/(m^2+3)`, it follows that `H'(b)=h>0`, and `H'(0)=m`.

For `A(t,B)=asin(t sin(B))` and `d(t,g)=asin(t sin(g))`, their relevant partial derivatives are

`A_t=sin(B)/sqrt(1-t^2 sin(B)^2)`,

`A_B=t cos(B)/sqrt(1-t^2 sin(B)^2)`,

`d_t=sin(g)/sqrt(1-t^2 sin(g)^2)`,

`d_g=t cos(g)/sqrt(1-t^2 sin(g)^2)`.

At the base point these become `A_t=d_t=s` and `A_B=d_g=0`. The remaining cross derivatives with respect to `(B,g,c)` are zero. The chain rule then gives

```text
D_(B,g,c)E = [ h     0       pi     ]
              [ 0     3h/2   -3pi/4 ]
              [ 1    -1       0     ],

D_t E = (-(2/3)m s, m s, -(4/3)s).
```

Expanding the determinant along the first row gives

`det J = h(-3pi/4)+pi(-3h/2)=-9pi h/4`,

which is nonzero for every fixed `m>1`.

The finite-dimensional smooth implicit function theorem therefore applies in its stated local form: an open-neighborhood smooth map, a zero residual, and an invertible derivative in `(B,g,c)` give a unique local smooth branch `(B(t),g(t),c(t))` through the base point. This use entails no global uniqueness assertion.

Differentiating `E(t,B(t),g(t),c(t))=0`, and multiplying the second row by `2/3`, yields

`h B'+pi c'=(2/3)m s`,

`h g'-(pi/2)c'=-(2/3)m s`,

`B'-g'=(4/3)s`.

Subtracting the second equation from the first, and using the third, gives

`(3pi/2)c'=(4/3)(m-h)s`.

Consequently

`c'(0)=8(m-h)s/(9pi)>0`,

because `m-h=3(m^2-1)/(4m)>0`. This verifies both the value and its strict sign. No unproved derivative assertion remains.

## Entry into the complete task domain

Since `c'(0)>0`, differentiability implies `c(t)>2/3` for all sufficiently small positive t. Continuity simultaneously gives `c(t)<1`, `0<B(t)<pi/2`, and `0<g(t)<pi/2`. Shrink the neighborhood further to ensure `0<t<c(t)` and `t<1`; then `r=t^2` obeys `0<r<c(t)^2` and `sqrt(r)=t` with the principal positive root.

For such t, A and d are positive. Since `t<1` and B and g are acute, monotonicity of sine and the principal arcsine gives `A<B` and `d<g`. The exact residual identity E3=0 gives

`B-g=c(A+d)>0`.

This also yields `d<A`, by monotonicity in the corresponding acute angles. Thus all required strict inequalities `0<d<A<B<pi/2`, `0<g<B<pi/2`, and `d<g` hold simultaneously. E1=E2=E3=0 are precisely C1--C3 with their original orientation and principal branches. The endpoint itself is used solely for construction and is not falsely asserted to be admissible.

## Q positivity and condition (P) on the exact branch

At t=0, the Q denominator extends to `1+k sin(b)^2>0`. Replacing `sqrt(r)` by t and `r` by `t^2` gives a continuous local expression agreeing with the task's Q for positive t. Direct substitution and combination of its two terms gives

`Q0=c0 cot(b)-c0 k sin(b)cos(b)/(1+k sin(b)^2)`

`   =c0 cos(b)/[sin(b)(1+k sin(b)^2)]>0`.

All signs are strict because b is acute and `k>0`. Continuity therefore gives Q positive for every sufficiently small positive t. This is an exact existence argument; floating-point residuals play no role.

Finally the continuous gap in (P) is

`G(t)=c(t)^2-t^4-k(1-c(t)^2)t^2`,

and `G(0)=4/9>0`. Hence (P) is strict throughout a sufficiently small positive interval. The finitely many neighborhood restrictions above can be met simultaneously by taking their minimum. The construction works for every fixed `m>1`, including every m in the claimed interval, and proves nonemptiness of the exact constrained Q-positive subdomain.

## Audit conclusion and remaining limits

No critical errors or mathematical gaps were found in these four claims. The strict inequalities, equality case of (P), boundary start at `c=2/3` and `r=0`, local quantifiers, all constraint residuals, Jacobian, branch derivatives, and exact branch admissibility were checked.

The global implication remains unproved on Q-positive constrained tuples outside (P); the supplied sufficient condition may still settle individual tuples there. This audit did not investigate those tuples, classify the entire solution set, establish external novelty, or perform Lean/kernel verification. The standard finite-dimensional implicit function theorem is the sole general existence theorem used, and all its hypotheses were checked explicitly.

An optional symbolic-CAS check was attempted, but the installed Python environment lacks SymPy (`ModuleNotFoundError`). No successful CAS result is claimed; the derivative and determinant checks above are direct analytic and algebraic computations. The initial input hashes were checked with `sha256sum` and matched the supplied candidate binding; the final reviewed revision was also independently hashed.
