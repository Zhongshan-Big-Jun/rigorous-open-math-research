PARTIAL

# Acute compatibility monotonicity and exact mass collapse

## 1. Scope and notation

All six bound inputs were SHA-256 verified before use. Work only in

```text
c>1/2,  pi/(2c)<alpha<pi,  m>1.
```

Put

```text
M=m^2,  k=M-1,  e=1-c^2,
P_m(z)=atan(tan(z)/m),
H_m(z)=P_m^(-1)(z)=atan(m tan(z)).
```

Every argument of `P_m` and `H_m` below is in `(0,pi/2)`. Define

```text
t=pi-alpha,
A=P_m(t),
B=P_m((1-c)pi+c t),
sigma=sin(B)/sin(A),
kappa=B-c A.
```

Since `(1-c)pi+c t-t=(1-c)alpha>0`, one has

```text
0<A<B<pi/2,  sigma>1,  0<kappa<pi/2.
```

For fixed `(c,m,A)`, let `d=d(A)` be the root

```text
sin(kappa-c d)/sin(d)=sigma,
g=kappa-c d.
```

On the admissible interval, the logarithmic derivative in `d` is

```text
-c cot(g)-cot(d)<0.
```

The quotient tends to infinity at `d=0`. At the other endpoint it tends
either to zero, when `g` tends to zero, or to a number at most one, when
`d` tends to `pi/2`; this is strictly below `sigma`. Hence this root exists
and is unique for every `A` in the acute interval.

At the root, `sin(g)=sigma sin(d)`. Thus `g>d`. Also
`B-g=c(A+d)>0`; using the same positive sine ratio gives `A>d`. Therefore

```text
0<d<A,  0<g<B<pi/2.                                 (1)
```

## 2. Strict monotonicity of the intrinsic compatibility scalar

Define

```text
J(A)=H_m(d(A))+H_m(g(A))/c-pi/2.                    (2)
```

The intrinsic `P_m` compatibility is exactly `J(A)=0`. Indeed, if
`h=H_m(d)`, then (2) is equivalent to

```text
g=P_m(c(pi/2-h)),
d=P_m(h).
```

The following differentiation keeps the full implicit-root Jacobian. Set

```text
L=B' cot(B)-cot(A),
Lambda=c cot(g)+cot(d)>0.
```

Since

```text
H_m'(z)=m/(cos(z)^2+M sin(z)^2)>0,
B'=c H_m'(A)/H_m'(B),
kappa'=B'-c,
```

implicit differentiation of the logarithmic root equation gives

```text
d'=[kappa' cot(g)-L]/Lambda,
g'=kappa'-c d'.                                    (3)
```

Both signs needed in (3) are strict. First,

```text
B'=c[1+k sin(B)^2]/[1+k sin(A)^2]>c,
kappa'>0.
```

Next, writing `sin(B)=sigma sin(A)`, direct collection gives

```text
kappa' cot(g)-L
 =[cot(A)-c cot(B)+k sin(A)^2 T]/[1+k sin(A)^2],     (4)

T=(1-c)cot(A)
  +c[(cot(A)-cot(B))
     +(sigma^2-1)(cot(g)-cot(B))].                  (5)
```

Every term in (5) is positive by (1), `A<B`, and `sigma>1`.
Also `cot(A)-c cot(B)>0`. Hence (4) is positive and

```text
d'(A)>0.                                           (6)
```

The derivative `H_m'` is strictly decreasing on `(0,pi/2)`. Using (1),
(3), and (6), the constrained derivative of (2) is

```text
J'(A)
 =H_m'(d)d'+H_m'(g)g'/c
 =[H_m'(d)-H_m'(g)]d'+H_m'(g)kappa'/c
 >0.                                               (7)
```

Thus for each fixed `(c,m)`, the intrinsic acute compatibility has at most
one solution. This monotonicity uses the full chain rule; `d` was not held
fixed.

As `A` tends to zero, `B` tends to
`B_0=P_m((1-c)pi)` and `sigma` tends to infinity. The root equation forces
`d` to zero and hence `g` to `B_0`. Therefore

```text
lim_(A->0+) J(A)
 =(1-c)pi/c-pi/2
 =pi(2-3c)/(2c).                                   (8)
```

Equations (7)-(8) prove the exact exclusion

```text
J(A)=0 in the strict acute branch implies c>2/3.    (9)
```

For `c=2/3`, the limit in (8) is zero but strict monotonicity gives
`J(A)>0` for every `A>0`; no boundary equality enters the branch.

Combining (9) with the accepted closed chamber `c alpha<=pi/2` proves:

```text
Every complete tuple with 0<c<=2/3 satisfies PHI-SIGN and KP-DET.          (10)
```

This strictly extends the previously closed ratio range `0<c<=1/2`.

## 3. Exact collapse of the mass balance

Let `(Acoef,Bcoef,Hcoef)` be the accepted mass coefficients. The audited
transfer formulas give, after squaring and adding the common-beta sine and
cosine equations,

```text
X^2=P sin(A)^2.
```

The definition `cot(d)=m tan(theta)` similarly gives

```text
C^2=P sin(d)^2,
C^2/X^2=sin(d)^2/sin(A)^2.                          (11)
```

Use the accepted identities

```text
Acoef/(s^2 X^2)=e-JA/M,
Bcoef/(s^2 X^2)=(e-JA)/m,
Hcoef/(C^2 s^2)=e-Jd/M,

JA=e+D/sin(A)^2,
Jd=e+D/sin(d)^2,
D=c^2-sigma^(-2).
```

Substituting these and (11) into

```text
alpha Acoef+beta Bcoef+theta Hcoef=0
```

and multiplying by the strictly positive factor `M sin(A)^2` yields the
exact scalar mass identity

```text
D(alpha+theta+m beta)
 =k e[alpha sin(A)^2+theta sin(d)^2].               (12)
```

There is no inequality or numerical input in (12). Since all weights are
positive, every complete tuple satisfies

```text
0<D
 <k e max{sin(A)^2,sin(d)^2}.                      (13)
```

Thus the requested threshold conclusion is strictly incompatible with the
exact mass balance. This confirms that proving the threshold implication
would close the branch, but (12) also identifies a strictly weaker direct
target.

## 4. One-scalar remaining sign problem for c>2/3

For the unique phase-lock root `d(A)`, set

```text
alpha(A)=pi-H_m(A),
theta(A)=pi/2-H_m(d(A)),
beta(A)=A+d(A),

W=alpha+theta+m beta,
N=alpha sin(A)^2+theta sin(d)^2,
Psi_(c,m)(A)=D W-k e N.                             (14)
```

By (7), the intrinsic equation `J(A)=0` has at most one root; call it
`A_(c,m)` when it exists. At that root, the exact mass balance is precisely

```text
Psi_(c,m)(A_(c,m))=0.                               (15)
```

Consequently, after the new chamber (10), the direct acute obstruction is
reduced to the single explicit sign implication

```text
q>E implies Psi_(c,m)(A_(c,m))>0,  c>2/3.           (16)
```

Implication (16) is strictly weaker than the requested max threshold,
because

```text
N/W<max{sin(A)^2,sin(d)^2}.
```

The left endpoint is audited exactly:

```text
lim_(A->0+) Psi_(c,m)(A)=3 pi c^2/2>0.              (17)
```

For future differentiation, no partial derivative of the implicit root may
replace the following full formula. From (3),

```text
D'=2 sigma^(-2)L,
W'=-H_m'(A)-H_m'(d)d'+m(1+d'),

N'=-H_m'(A)sin(A)^2+alpha sin(2A)
   +d'[-H_m'(d)sin(d)^2+theta sin(2d)],

Psi'=2 sigma^(-2)L W+D W'-k e N'.                  (18)
```

Formula (18) differentiates only along the unique phase-lock root. The
intrinsic equation `J=0` is an isolated scalar condition at fixed `(c,m)`;
it is not legitimate to set `J'=0`. A variation of `c` or `m` would require
the corresponding additional Jacobian columns.

The first unresolved inequality is the sign implication (16), equivalently

```text
q>E implies
D>k e[alpha sin(A)^2+theta sin(d)^2]
       /(alpha+theta+m(A+d))                        (19)
```

at the unique intrinsic root. No sign for the right side of (18) has been
proved here. Hence arbitrary finite-`c` `PHI-SIGN` and KP-DET remain open
only for `c>2/3`. No numerical evidence is used.

## 5. Denominator and boundary audit

- `m`, `M`, `k`, `e`, `sin(A)`, `sin(B)`, `sin(d)`, and `sin(g)` are
  strictly positive.
- `Lambda=c cot(g)+cot(d)` is strictly positive, so the implicit derivative
  (3) has no singular denominator.
- `cos(z)^2+M sin(z)^2` is strictly positive for every occurrence of
  `H_m'(z)`.
- The proof does not divide by `D`, `q-E`, a cotangent, or a middle-layer
  sine or cosine.
- The endpoint `A=0` is used only as a one-sided limit and is not admitted as
  a strict modal tuple.
- At `c=2/3`, the endpoint equality in (8) cannot enter because `J'>0` and
  `A>0`.
- Switch collision and all modal boundary faces excluded by the frozen
  contract remain excluded.

decision_delta: Proved strict monotonicity of the fully constrained intrinsic compatibility scalar, excluded the entire acute branch for c<=2/3 and thereby extended complete PHI-SIGN and KP-DET to 0<c<=2/3; collapsed exact mass to (12) and reduced the remaining c>2/3 gap to the weaker one-scalar implication q>E => Psi>0 at the unique intrinsic root.
