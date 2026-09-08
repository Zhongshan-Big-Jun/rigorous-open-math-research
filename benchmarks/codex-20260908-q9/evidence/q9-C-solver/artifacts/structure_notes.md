# Structural partial results

These notes use only the task statement. Write `rho=sqrt(r)`, `k=m^2-1`, `e=1-c^2`, and `delta=c^2-r`.

## An unconditional sign consequence of Q

On the entire stated domain, the term subtracted from the first term in `Q_quad` is strictly positive. Therefore `Q_quad>0` implies

\[
c\cos B>\rho\cos A.
\]

Both sides are positive. Squaring, substituting `sin^2 A=r sin^2 B`, and rearranging yields the strict inequality

\[
\boxed{\delta>(c^2-r^2)\sin^2 B.}\tag{S1}
\]

Consequently, **Q9 holds on the precisely specified subdomain**

\[
\boxed{k e r\le c^2-r^2.}\tag{S2}
\]

Indeed, (S1) and (S2) give `delta>k e r sin^2 B`; combining this with the supplied strict bound `T_quad<r sin^2 B` proves `delta/(k e)>T_quad`.

In particular, this proves Q9 for every admissible tuple with

\[
1<m\le\sqrt2,
\]

because

\[
c^2-r^2-e r=(c^2-r)(1+r)>0
\]

and `k<=1`. This is a new partial implication, rather than a restatement of the supplied sufficient condition: it deduces the required pointwise bound from `Q_quad>0` in a parameter subdomain that does not itself contain `B` or `g`.

## Constraint identities

Let `a=H_m(A)` and `t=H_m(d)`. Constraints (C1)--(C3) imply

\[
\pi-H_m(B)=c(\pi-a),\qquad H_m(g)=c(\pi/2-t),\qquad B-g=c(A+d).
\]

Since `V=pi-H_m(B)+H_m(g)+m(B-g)`, they give the exact identities

\[
\frac Vc=\frac{3\pi}2-a-t+m(A+d),
\]

\[
\frac{rU}c=(\pi-a)\sin^2 A+(\pi/2-t)\sin^2 d.
\]

Thus

\[
T_{\rm quad}=
\frac{(\pi-a)\sin^2 A+(\pi/2-t)\sin^2 d}
{(\pi-a)+(\pi/2-t)+m(A+d)}.
\]

All terms in the denominator and all displayed weights are positive.

## A stronger geometric consequence of the positive first term

Let

\[
L=\frac{c\cos B-\rho\cos A}{\sin B}.
\]

Assume the stated domain, (C3), and `L>0` (which follows from `Q_quad>0`). Since `sin A=rho sin B`, this condition is equivalent to

\[
\sin(2A)<c\sin(2B)<\sin(2B).
\]

The identity `sin(2B)-sin(2A)=2 sin(B-A) cos(A+B)` and `B>A` imply

\[
A+B<\pi/2.
\]

In particular `0<S=A+d<pi/2`. Strict concavity of sine on `(0,pi)` gives `sin(cS)>c sin S`. By (C3), `B-g=cS`, so expansion of both sides and substitution of `sin A=rho sin B`, `sin d=rho sin g` give

\[
\cot B+c r\cot A<\cot g-c r\cot d.
\]

Furthermore `r cot A=rho cos A/sin B>rho cot B`, since `A<B`. Consequently

\[
(1+c\rho)\cot B<\cot g-c r\cot d,
\]

and, using `c-rho>0`,

\[
\boxed{
L<\frac{(c-\rho)(\cos g-c\rho\cos d)}{(1+c\rho)\sin g}.
}\tag{S3}
\]

The numerator on the right is positive, as is already implied by the preceding displayed strict inequality. This reduces a necessary consequence of `Q_quad>0` to quantities involving `c,r,m,g,d` and removes `A,B`.

## Nonemptiness of the partial implication's antecedent

The following argument gives exact existence, without numerical residuals, of admissible tuples with `1<m<sqrt(2)` and `Q_quad>0`.

Fix `rho=1/10` (so `r=1/100`). More generally the construction below up to the positivity of Q works for every fixed `0<rho<2/3`.

Temporarily allow the boundary values `m=1` and `c=2/3`. Put

\[
\phi(z)=\arcsin(\rho\sin z).
\]

Here `phi'(z)=rho cos(z)/sqrt(1-rho^2 sin^2(z))`, and `0<phi'(z)<=rho<1` for `0<=z<pi/2`. The latter inequality follows by squaring `cos z<=sqrt(1-rho^2 sin^2 z)`.

There is a unique `B_0` in `(0,pi/2)` solving

\[
B_0-\tfrac23\phi(B_0)=\pi/3.
\]

The left side is strictly increasing, is zero at zero, and at `pi/2` is `pi/2-(2/3)arcsin rho>pi/3`, because `rho<2/3<sin(pi/4)`. There is likewise a unique `g_0` in `(0,pi/3)` solving

\[
g_0+\tfrac23\phi(g_0)=\pi/3.
\]

Set `A_0=phi(B_0)` and `d_0=phi(g_0)`. Then `B_0>pi/3>g_0>0`, and all three constraints hold exactly at `(m,c)=(1,2/3)`.

To continue these tuples, define

\[
E_1=H_m(B)-(1-c)\pi-cH_m(\phi(B)),
\]

\[
E_2=H_m(g)+cH_m(\phi(g))-c\pi/2.
\]

At `m=1,c=2/3`, their derivatives with respect to `B` and `g`, respectively, are

\[
1-c\phi'(B)>0,\qquad 1+c\phi'(g)>0.
\]

The ordinary smooth implicit function theorem therefore gives smooth `B(m,c)` and `g(m,c)` nearby satisfying `E_1=E_2=0`. Define

\[
E_3(m,c)=B(m,c)-g(m,c)-c[\phi(B(m,c))+\phi(g(m,c))].
\]

For `m=1`, the equations `E_1=E_2=0` show identically that

\[
E_3(1,c)=\pi(1-3c/2),
\]

so `partial_c E_3(1,2/3)=-3pi/2 != 0`. A second application of the smooth implicit function theorem gives a smooth function `c=c(m)` satisfying all three constraints exactly, with `c(1)=2/3`.

For the derivative, write `h(z)=sin z cos z`; this equals `partial_m H_m(z)` at `m=1`. Differentiating `E_1=E_2=0` at fixed `c=2/3` gives

\[
\partial_m E_3=-h(B_0)+h(g_0)+\tfrac23[h(A_0)+h(d_0)].
\]

Also

\[
B_0+g_0=2\pi/3+\tfrac23(A_0-d_0)>2\pi/3,
\]

and `B_0+g_0<pi` because both angles are acute. Hence

\[
h(g_0)-h(B_0)=-\sin(B_0-g_0)\cos(B_0+g_0)>0.
\]

Every summand in `partial_m E_3` as last written is positive. Therefore

\[
c'(1)=\frac{2}{3\pi}\left[h(g_0)-h(B_0)+\tfrac23(h(A_0)+h(d_0))\right]>0.
\]

Thus for all sufficiently small positive `m-1`, `2/3<c(m)<1`, `r<c(m)^2`, and all strict angle inequalities persist.

Finally take `rho=1/10`. Since `arcsin rho<2rho` for `0<rho<=1/2` (its derivative is at most `2/sqrt(3)<2` there),

\[
B_0=\pi/3+\tfrac23 A_0<\pi/3+\tfrac43\rho.
\]

The mean value theorem and `|cos'|<=1` give

\[
\tfrac23\cos B_0-\rho\cos A_0
>\tfrac13-\tfrac89\rho-\rho
=\tfrac13-\tfrac{17}{9}\rho>0.
\]

At `m=1` the second term of `Q_quad` vanishes, so `Q_quad>0` there. The formula is continuous at this boundary point, so `Q_quad>0` persists along the exact constraint branch for all sufficiently small positive `m-1`. Choosing these sufficiently small also makes `m<sqrt(2)`. This proves the claimed nonemptiness.

The external theorem used here is the standard finite-dimensional smooth implicit function theorem: a smooth system `F(x,y)=0` near a zero, whose Jacobian in the unknown vector `y` is invertible at that zero, has a unique smooth local solution `y=y(x)`. Smoothness holds here because all angles remain strictly below `pi/2`, the argument of each arcsine remains strictly within `(-1,1)`, and `m,c` remain positive; the required nonzero Jacobians were computed explicitly above.

## Remaining gap

These results do not decide the implication for tuples with `k e r>c^2-r^2` (necessarily `m>sqrt(2)`). No claim is made that such tuples do or do not violate Q9.

## Independent audit of the later cubic certificate

The root agent subsequently obtained a complete-proof route. The following is an independent check of the algebraic certificate in `root_polynomial_cert.py`; it supersedes the research status in the preceding paragraph insofar as that route is incorporated and proved in the final submission.

Set `t=sqrt(r)`, `h=1-t^2`, and define

\[
\Delta=1-c^2t^2,\quad w=1+6t+3t^2,\quad z=3+2t,
\]
\[
C=c(1+2t^2+c^2t^2),\quad D=t(1+2c^2+c^2t^2),
\quad P=C/\Delta,\quad J=D/\Delta,\quad L=z/w.
\]

For the cubic

\[
N(v)=c h v(1+Lh-v^2)-(P-Jv)[v(1+L)+ct(v^2+t^2L)],
\]

write `Delta*w*N(v)=n3 v^3+n2 v^2+n1 v+n0`. Direct expansion gives

\[
n_3=w(Dct-ch\Delta),\quad n_2=D(w+z)-Cctw,
\]
\[
n_1=ch(w+zh)\Delta-C(w+z)+Dct^3z,\quad
n_0=-Cct^3z.
\]

The polynomial `D^2 [n1+2n2(C/D)+3n3(C/D)^2]` is exactly

\[
H=n_1D^2+2n_2CD+3n_3C^2.
\]

The independent standard-library code in `exact_structure_poly.py` constructed these polynomials separately and found exact coefficient-by-coefficient equality with the root script for `H`, `n2`, and `n1+2n2+3n3`.

Under the rectangle substitution `c=(2+x)/3`, `t=(1+2y)/3`, the tensor Bernstein coefficients have these independently reproduced properties:

| Polynomial | Degrees in x,y | Exact minimum Bernstein coefficient |
|---|---:|---:|
| `n0+n1+n2+n3` | `(4,6)` | `0` |
| `n1+2n2+3n3` | `(4,6)` | `9382/6561` |
| `n2` | `(4,5)` | `25553/6561` |
| `H` | `(9,12)` | `134561396/387420489` |

For the first polynomial, its `(0,0)` Bernstein coefficient is `15169/59049>0`. Its associated basis function is `(1-x)^4(1-y)^6`, which is strictly positive when `c<1` and `t<1`. Thus the first polynomial is also strictly positive throughout the domain relevant to the task, including `t=1/3`.

The tensor Bernstein conversion formula used by both scripts is correct: for a polynomial `p(x,y)=sum a_kl x^k y^l` of separate degrees `(n,m)`, its coefficient at `B_i^n(x) B_j^m(y)` is

\[
b_{ij}=\sum_{k\le i,\ell\le j}a_{k\ell}
\frac{\binom{i}{k}}{\binom{n}{k}}
\frac{\binom{j}{\ell}}{\binom{m}{\ell}}.
\]

Every operation in the scripts uses exact rational arithmetic.

Finally, the inference from these polynomial signs is sound. Since `P-J=(c-t)(1-ct)/(1+ct)>0`, one has `v_star=P/J=C/D>1`. The signs certify `N(1)>0`, `N'(1)>0`, `N'(v_star)>0`, and `n2>0`. If `n3>=0`, then `N''(v)>0` for `v>=1`, hence `N'(v)>0`. If `n3<0`, then `N'` is a concave quadratic; positivity at both endpoints makes it positive on the whole interval `[1,v_star]`. Thus `N(v)>0` there.

At `v=v_star`, the second summand in the definition of `N` vanishes, so

\[
N(v_{\rm star})=chv_{\rm star}(1+Lh-v_{\rm star}^2)>0.
\]

Therefore `1+Lh>v_star^2`, which also verifies that the proposed lower comparison value `k_0=L cot^2(g)-1` is positive whenever `1<v<v_star` and `v^2=1+h tan^2(g)`. A separate assertion of this positivity is unnecessary.
