RIGOROUS_PARTIAL_RESULT

# Independent audit of the Jensen prerequisites

**Verdict: PASS within the specified claim-local scope.** The sharp consequence of C3, the explicit Jensen lower bound, the exact Q substitution, and the positive-denominator reduction to E are valid. The assertion `E>=0` remains open and was neither used as a proved fact nor investigated in this audit.

## Binding and scope

- Contract: `TASK.md`, SHA-256 `c7133b97e440e90095088927f105c9f88fcdc54f4a4772ee9f85ba5a139e6330`.
- Audited candidate: `runs/q9/jensen_prerequisites.md`, SHA-256 `62a08ff1f97a9a037c1790df10bc1a6df50f84d204ea475d75165421053e2c13`.

The audit independently recalculated the candidate's mathematical steps from the original definitions. It used the installed rigorous-open-math-research audit instructions. No external mathematical sources, numerical search, or unfinished-algebra files were consulted. All new prerequisite lemmas received explicit checks below.

## Domain and sharp C3 estimate

Under the candidate's hypotheses, `t=sqrt(r)` satisfies `0<t<c<1`. Therefore `u=ct` lies in `(0,1)`. The acute-angle domain implies `X=tan(B)>z=tan(g)>0`, hence `L>w>1`, where

`L^2=1+(1-t^2)X^2`, `w^2=1+(1-t^2)z^2`.

Also `h=mz>z>0`. The coefficients a and b are positive.

Set `x=A+d`. Since A and d are positive and each is less than `pi/2`, `0<x<pi`. Sine is strictly concave on `[0,x]`, so `sin(cx)>c sin(x)` for `0<c<1`. C3 is the exact identity `B-g=cx`; thus the direction of the claimed sine inequality is correct even if x exceeds `pi/2`.

With the common positive denominator `sqrt((1+X^2)(1+z^2))`, the two sine numerators are `X-z` and `t(Xw+zL)`. Consequently

`X-z>u(Xw+zL)`,

or `X(1-uw)>z(1+uL)>0`. This proves `1-uw>0` before division and gives

`X/z>(1+uL)/(1-uw)>0`.

Squaring these positive quantities and substituting the defining identities for L and w yields

`(L^2-1)(1-uw)^2-(w^2-1)(1+uL)^2>0`.

Independent expansion gives exactly

`(L+w)[(1+u^2)(L-w)-2u(Lw-1)]`.

Since `L+w>0`, this is equivalent to `LD>N`, with

`D=1+u^2-2uw`, `N=(1+u^2)w-2u`.

The estimate `N>(1+u^2)-2u=(1-u)^2>0` uses `w>1` and `u<1`. Hence `L>0` and `LD>N` force `D>0`, and division gives `L>N/D`. In particular, both arguments N/D and L used next are positive.

The first term of Q is exactly `P=(c-tL)/X`; its second term is strictly positive on the original domain. Thus Q positivity implies `P>0` and `c-tL>0`. Multiplying the earlier reciprocal ratio by this positive numerator gives

`0<Pz<(c-tL)(1-uw)/(1+uL)`.

For positive ell, direct differentiation gives

`d/dell [(c-t ell)/(1+u ell)]=-(t+uc)/(1+u ell)^2<0`.

Using `L>N/D` therefore increases this last upper bound when L is replaced by N/D. Direct expansion verifies all three simplifications

`D+uN=(1-u^2)(1-uw)>0`,

`cD-tN=a-bw`,

`a-b=(c-t)(1-ct)^2>0`.

Cancellation of the already positive factor `1-uw` gives

`0<Pz<(a-bw)/(1-u^2)=f`.

It follows that `a-bw>0`, hence `1<w<a/b` because `b>0`. There is no unsupported sign assumption in this part of the argument.

## Jensen estimate and the exact constant

From the definitions,

`tan(d)=tz/w`, `H(g)=atan(h)`, and `H(d)=atan(th/w)`.

C2 gives `c atan(th/w)+atan(h)=c pi/2`. Arctangent has second derivative `-2v/(1+v^2)^2<0` for `v>0`. The two inputs `th/w` and h are distinct and positive because `t/w<1`; the weights `c/(1+c)` and `1/(1+c)` are positive and sum to one. Strict Jensen concavity therefore has the candidate's stated direction:

`c pi/[2(1+c)]<atan(h(1+ct/w)/(1+c))`.

Both sides lie in the increasing interval for tangent. For `c>=2/3`, the left angle is at least `pi/5`. Thus

`h>((1+c)w/(w+ct)) tan(pi/5)`.

The lower bound `tan(pi/5)>7/10` is rigorous without decimal information about pi. Let `theta=atan(7/10)`, so `0<theta<pi/4` and `cos(theta)>0`. Expanding `(cos(theta)+i sin(theta))^5` gives

`sin(5theta)/cos(theta)^5=23807/100000>0`,

`cos(5theta)/cos(theta)^5=-5399/2000<0`.

Since `0<5theta<5pi/4`, these two signs force `pi/2<5theta<pi`. Consequently `theta<pi/5`, and monotonicity of tangent gives the claimed strict rational lower bound.

All factors in the resulting estimate for h are positive, so squaring preserves its strict direction and gives

`h^2>J w^2/(w+u)^2=j`,

where `J=(49/100)(1+c)^2`. This conclusion remains strict when using the weaker endpoint bound `c>=2/3`.

## Exact substitution in Q

Let `q_g=1+z^2`. Then

`sin(g)=z/sqrt(q_g)`, `cos(g)=1/sqrt(q_g)`, `cos(d)=w/sqrt(q_g)`.

The two expressions in the original denominator simplify as

`q_g+k z^2=1+h^2`,

`q_g+k t^2 z^2=w^2+t^2 h^2`.

Hence the original denominator, multiplied by `q_g^(3/2)`, is

`w(1+h^2)+u(w^2+t^2 h^2)`

`=w[1+uw+h^2(1+ut^2/w)]`.

Substituting the numerator as well and using `k z^2=h^2-z^2` yields precisely

`Q z=Pz-c(1-t^2)^2(h^2-z^2)/[1+uw+h^2(1+ut^2/w)]`.

Every cancelled factor is positive. This check starts from the task's exact Q expression and does not use an approximation or replace a constraint.

## Monotonicity and the exact E reduction

For the candidate's function K, write `A0=1+uw>0` and `B0=1+ut^2/w>0`. Its derivative is

`K'(x)=c(1-t^2)^2(A0+B0 z^2)/(A0+B0 x)^2>0`

for every `x>=0`. The denominator is positive throughout this domain. There is no need to assume `x>=z^2`, because the derivative remains positive when K itself is negative. Since `h^2>j>0`, this proves `K(h^2)>K(j)`.

Define the positive denominator

`M=(1+uw)(w+u)^2+Jw(w+ut^2)`.

Using `z^2=(w^2-1)/(1-t^2)` and the exact value of j, direct fraction simplification gives

`K(j)=c(1-t^2)[(1-t^2)Jw^2-(w^2-1)(w+u)^2]/M`.

Subtracting `f=(a-bw)/(1-u^2)` yields the exact identity

`K(j)-f=E/[(1-u^2)M]`,

where E is exactly the polynomial displayed in the candidate. On the entire proposed algebraic domain

`2/3<=c<1`, `c/2<=t<c`, `1<=w<=a/b`,

we have `u<1`, `w>0`, `w+u>0`, `J>0`, and `M>0`. Thus the denominator in this identity is strictly positive even on the included faces `c=2/3`, `t=c/2`, `w=1`, and `w=a/b`. The equivalence between `E>=0` and `K(j)>=f` is therefore valid there.

If E were proved nonnegative on that domain, every tuple under the analytic hypotheses would satisfy

`Q z=Pz-K(h^2)<f-K(h^2)<f-K(j)<=0`,

contradicting `Q>0` and `z>0`. The asserted conditional exclusion of all `t>=c/2` cases is consequently correct. Combining that conditional exclusion with the previously audited small-r theorem would settle Q9, but the antecedent polynomial theorem has not been established here.

## Verification and limits

There are no critical errors or gaps in the audited prerequisite lemmas or conditional reduction. The analytic derivations, strict signs, branch choices, divisions, Jensen weights, and included algebraic-domain boundaries were independently checked. A separate exact rational-coefficient Python calculation confirmed the C3 factorization, the three simplification identities, and both five-angle numerators. That calculation neither sampled nor asserted the sign of E.

Residual risks are explicit: `E>=0` is an open obligation outside this audit; no global Q9 verdict is issued; no complete classification or extra existence claim is proved; and no Lean/kernel verification or external-literature novelty audit was performed. This PASS must not be interpreted as certifying the polynomial inequality.
