PARTIAL

# Branch-safe common-beta orientation and a closed coefficient chamber

## Binding audit

The six packet inputs were checked before use. Their SHA-256 values are,
in packet order,

```text
67427fe00b6b7758552581cde19fdb449202b5e9ea7bf9013f6ba0a4135f3f9d
a96fde4cfaaf3cb83fcf416d3d7e627a5d63c4a48c2cd8a0c562e9dd8636e7d3
6c1bbbd871c9aef7c8c316d47d0b61c3ab34bfb806eb5ee715ed915df6103ee3
cd56d00daadad6315bc7fe267754c4516617e08832f6ffc5b3c77883c7e24192
a24a0fe82e19ef6a1aeb2e29c2379bb2f8793818940d43df9d87b9abd14ef1dc
11b3b68b8aa9b1dcfd593b1e919169f9057f3daa63ef1dfb6ccb09a46da7e1db
```

Every comparison returned equality.

## 1. Unsquared cosine audit

Retain all notation of the bound W1 and W10 packages, and put

```text
M=m^2,
k=M-1,
e=1-c^2,
x=cot(alpha),
y=cot(c alpha),
u=tan(theta),
v=tan(c theta).
```

Solving the two exact transfer systems, without dividing by a middle-layer
trigonometric factor, gives

```text
cos(beta)=X(C+M S x)/P,
sin(beta)=m X(C x-S)/P,                              (1)

cos(c beta)=s X(M Cc y-s)/(C Q),
sin(c beta)=-m s X(Cc+s y)/(C Q).                   (2)
```

For (1), the transfer determinant is `P/m>0`. For (2), it is `-Q/m<0`.
Thus (1)-(2) remain valid when any of `sin(beta)`, `cos(beta)`,
`sin(c beta)`, or `cos(c beta)` vanishes.

## 2. Exact common-beta orientation

Define four oriented phase angles by

```text
A=pi/2+atan2(m cos(alpha),sin(alpha)) in (0,pi),
B=pi/2+atan2(m cos(c alpha),sin(c alpha)) in (0,pi),
d=atan(1/(m tan(theta))) in (0,pi/2),
g=atan(tan(c theta)/m) in (0,pi/2).                  (3)
```

These definitions are single valued on the strict modal domain. They satisfy

```text
cot(A)=-m x,
cot(B)=-m y,
cot(d)=m u,
tan(g)=v/m.                                         (4)
```

The complex directions behind (1) factor as

```text
1+M u x+i m(x-u)=(1-i m u)(1+i m x).
```

Because `X<0`, the representative selected by
`d<beta<d+pi` is exactly

```text
beta=A+d.                                           (CB3)
```

Likewise, after extracting the positive factor `-s X Cc/(C Q)`, the
direction in (2) is

```text
v-M y+i m(1+v y)=(v+i m)(1+i m y).
```

The strict DD modal condition selects `B>g` and gives exactly

```text
c beta=B-g.                                         (CB2)
```

Therefore the branch-safe, unsquared common-beta identity is

```text
B-g=c(A+d).                                         (CB)
```

There is no hidden `pi` multiple in (CB): `A+d` lies in the unique DN
interval `(d,d+pi)`, while `B-g` lies in the unique DD interval
`(0,pi-g)`.

The accepted squared phase lock has a unique positive square root in these
angles:

```text
sin(B)/sin(A)=sin(g)/sin(d)=sigma>0.                 (PL+)
```

Indeed, `1+M x^2=csc(A)^2`, `1+M y^2=csc(B)^2`, and

```text
v^2(1+M u^2)/(M+v^2)=sin(g)^2/sin(d)^2.
```

Thus (CB) restores precisely the orientation discarded by the squared lock.

## 3. Coefficient and sign dictionary

Write the accepted mass coefficients as `(Acoef,Bcoef,Hcoef)` to distinguish
them from the phase angles `(A,B)`. Define

```text
JA=c^2 cot(A)^2-cot(B)^2,
Jd=c^2 cot(d)^2-cot(g)^2,
D=c^2-sigma^(-2).                                   (5)
```

Direct substitution into the accepted exact coefficient formulas gives

```text
Bcoef/(s^2 X^2)=(e-JA)/m,
Hcoef/(C^2 s^2)=e-Jd/M,
Lalpha=e-JA/M.                                      (6)
```

The accepted B-to-H identity also gives

```text
sign(Bcoef)=sign(e-Jd).                              (7)
```

Using (PL+),

```text
JA-e=D/sin(A)^2,
Jd-e=D/sin(d)^2.                                    (8)
```

Consequently all the following equivalences are exact:

```text
Bcoef<0 iff JA>e iff Jd>e iff sigma>1/c,             (9)

Acoef<0 iff JA>M e iff D>k e sin(A)^2,              (10)

Hcoef<0 iff Jd>M e iff D>k e sin(d)^2.              (11)
```

In the same variables, the accepted scalar `q` is

```text
q=[c sigma cos(B)-cos(A)]/[m sin(A)].                (12)
```

The accepted nonnegative correction has the denominator-safe form

```text
E=
 c k (sigma^2-1)^2 sin(d) cos(d) cos(g)
 --------------------------------------------------, (13)
 m[ sigma cos(d)(cos(g)^2+M sin(g)^2)
    +c cos(g)(cos(d)^2+M sin(d)^2) ]
```

where (13) follows from
`sin(g-d)sin(g+d)=(sigma^2-1)sin(d)^2`.
Under `Bcoef<0`, (9) gives `sigma>1/c>1`, so every factor in (13) is
strictly positive and `E>0`.

## 4. A complete closed chamber

### Theorem

Every spectral-band-modal tuple satisfying `Bcoef<0` and

```text
c alpha<=pi/2                                        (14)
```

has

```text
q<0<E,
G>0,
Xi>0,
Phi<0.                                               (15)
```

Hence KP-DET holds on this chamber. In particular, because every complete
mass tuple has `Bcoef<0`, KP-DET holds for every complete tuple with

```text
0<c<=1/2.                                            (16)
```

### Proof

The alpha-side form of (6) is

```text
m Bcoef/(s^2 X^2)=e+M(y^2-c^2 x^2).                 (17)
```

If `alpha<=pi/2`, then `0<c alpha<alpha<=pi/2` and the strict decrease of
`cot` gives `y>x>=0`. The right side of (17) is then positive. Therefore
`Bcoef<0` forces `alpha>pi/2`, hence `x<0`.

Under (14), `y>=0`. Since the phase-lock factor `rho` is strictly positive,

```text
q=x-c rho y<0.
```

This remains strict on the boundary `c alpha=pi/2`, where `y=0` and `x<0`.
Equation (9) and (13) give `E>0`, proving `q<E`. The accepted factorization

```text
G=X [M Dtheta/P](q-E)
```

then gives `G>0`, because `X<0`, `Dtheta>0`, and `P>0`. The accepted split

```text
Xi=X^2 G-r K Dtheta
```

has `r>0` and `K<0`, so `Xi>0`. The accepted W3 implication gives
`Phi<0`, and the lossless W1 Schur reduction gives KP-DET.

If `c<=1/2`, then `c alpha<c pi<=pi/2` for every `alpha<pi`, so (14) is
automatic. This proves (16).

## 5. The only remaining common-beta chamber

After Section 4, a tuple with `Bcoef<0` and possible `q>E` must satisfy

```text
c>1/2,
pi/(2c)<alpha<pi.                                   (18)
```

Thus all four angles `A,B,d,g` lie in `(0,pi/2)`. Put

```text
kappa=B-c A.
```

Equations (CB) and (PL+) reduce the simultaneous orientation and phase lock
to the one-variable equation

```text
R(d)=sin(kappa-c d)/sin(d)=sigma,                    (19)
g=kappa-c d.
```

On the full admissible interval where `0<d<pi/2` and `0<g<pi/2`,

```text
d/dd log(R(d))=-c cot(g)-cot(d)<0.                  (20)
```

Hence (19) has at most one admissible solution. Since an admissible tuple
supplies one, its `d`, `g`, and therefore its common `beta`, are unique.
This is a strict reduction: neither a squared phase choice nor a second
modal branch remains.

For an alternative scalar convexity form, define

```text
P_m(t)=atan(tan(t)/m),  0<t<pi/2.
```

Then

```text
P_m''(t)=
 2m(M-1)sin(t)cos(t)/(M cos(t)^2+sin(t)^2)^2>0.      (21)
```

Writing `t=pi-alpha` and `h=pi/2-theta`, the remaining chamber (18) has

```text
A=P_m(t),
B=P_m((1-c)pi+c t),
d=P_m(h),
g=P_m(c(pi/2-h)).                                   (22)
```

The common-beta condition is the scalar equation

```text
C_m,c,t(h)=
 P_m((1-c)pi+c t)-P_m(c(pi/2-h))
 -c P_m(t)-c P_m(h)=0.                              (23)
```

Its derivative is

```text
C_m,c,t'(h)=c[P_m'(c(pi/2-h))-P_m'(h)].             (24)
```

Because `P_m'` is strictly increasing, (23) is strictly increasing before
`h=c pi/[2(1+c)]` and strictly decreasing after it. Equations (19)-(24)
give a branch-safe one-scalar monotonicity or convexity formulation of the
remaining common-beta decision.

## 6. First unresolved step and exact effect

The exact remaining SC-rem obligation is confined to (18). By (10)-(11),
`q>E` would force the forbidden negative same-sign coefficient chamber
precisely if one proves

```text
q>E implies
D>k e max{sin(A)^2,sin(d)^2}                         (25)
```

at the unique root (19), subject also to the exact intrinsic compatibility
(22). If (25) holds, then `Acoef<0`, `Bcoef<0`, and `Hcoef<0`, contradicting
the exact mass balance

```text
alpha Acoef+beta Bcoef+theta Hcoef=0.
```

Neither the strict convexity (21) nor the unimodality (24) alone proves
(25). Establishing the needed scalar derivative or endpoint comparison in
the remaining acute chamber is the first unresolved load-bearing step.
Therefore complete-system `q<=E`, global SC-rem, complete `G>=0`, complete
`Phi<0`, and global KP-DET remain open. The chamber (14), including all
`c<=1/2`, is closed strictly with `G>0`, `Phi<0`, and KP-DET.

## Denominator and boundary audit

- `P,Q,C,s,M,k` are strictly positive on the packet domain.
- `X<0`, so no division by `X` crosses an equality face.
- `sin(A),sin(B),sin(d),sin(g)` are strictly positive. The square root in
  (PL+) therefore introduces no sign choice.
- No division by `x`, `y`, or a middle-layer sine or cosine was used.
- The face `c alpha=pi/2` is included in the closed chamber and has `q<0`.
- The face `alpha=pi/2` is incompatible with `Bcoef<0` by (17).
- For `c=1/2`, strict `alpha<pi` gives strict `c alpha<pi/2`.
- The modal and switch-collision faces excluded by the frozen contract were
  not reintroduced.
- No numerical evidence is used in any theorem above.

decision_delta: Restored the exact unsquared identity `B-g=c(A+d)`, proved its positive square-root lock and unique acute-branch reconstruction, and closed KP-DET strictly for every complete tuple with `c alpha<=pi/2`, in particular for all `0<c<=1/2`; the only remaining common-beta sign gap is the scalar acute-chamber implication (25).
