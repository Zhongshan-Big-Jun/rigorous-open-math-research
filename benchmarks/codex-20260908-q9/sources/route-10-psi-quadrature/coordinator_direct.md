PARTIAL

# Direct quadrature reduction of the remaining acute sign problem

## Action and scope

- Action ID: `DIRECT-PSI-CGT2D3-01`.
- Target: `PHI-SIGN-CGT2D3`.
- Model-response budget: one coordinator response.
- Worker dispatches: zero.
- Restart, duplicate dispatch, and transcript replay counts: `0`, `0`, and
  `0`.

This direct action starts from the accepted common-beta and acute-threshold
packages. It does not reopen the proved `0<c<=2/3` chamber. The identities
below are candidate strict mathematics pending independent audit. The global
sign implication is not claimed as proved.

## Input bindings

- `problem_contract.md`:
  `67427fe00b6b7758552581cde19fdb449202b5e9ea7bf9013f6ba0a4135f3f9d`.
- `route-08-common-beta-orientation/accepted_package.md`:
  `2257a61c95cdcfa58b12cae577c5097ea4f124cd5d6077b6ebe550eb0779f8ed`.
- `route-09-acute-threshold/accepted_package.md`:
  `c76ed655d854bb327fc3755cbd0c2438cddd6eaf37f64111944dcf13db7be45d`.
- `route-09-acute-threshold/audit/retry_independent_audit.json`:
  `672f7e3e762ff412450125ac4fecf634bf509f9a0535c94666f64bcc75b814ce`.

## 1. Exact elimination of the physical layer weights

Retain the accepted acute variables. Put

```text
M=m^2,
k=M-1,
e=1-c^2,
r=sigma^(-2),
D=c^2-r,
F_m(z)=H_m(z)-m z.
```

On the remaining chamber, `Bcoef<0` gives

```text
0<r<c^2<1.
```

The exact spectral and intrinsic identities give

```text
H_m(B)=pi-c alpha,
H_m(g)=c theta,
B-g=c beta.
```

Therefore the accepted weights

```text
W=alpha+theta+m beta,
N=alpha sin(A)^2+theta sin(d)^2
```

satisfy the exact formulas

```text
c W=pi+F_m(g)-F_m(B),                               (Q1)

c N=r[(pi-H_m(B))sin(B)^2+H_m(g)sin(g)^2].         (Q2)
```

Indeed, the positive phase lock gives

```text
sin(A)^2=r sin(B)^2,
sin(d)^2=r sin(g)^2.
```

Also

```text
F_m'(z)=-m k sin(z)^2/[1+k sin(z)^2],
```

so

```text
F_m(g)-F_m(B)
=m k integral_[g,B] sin(z)^2/[1+k sin(z)^2] dz>0. (Q3)
```

No mass equation is used in (Q1)-(Q3).

## 2. Exact quadrature threshold

Define

```text
V=pi+F_m(g)-F_m(B),
U=(pi-H_m(B))sin(B)^2+H_m(g)sin(g)^2,
T_quad=r U/V.
```

The accepted mass residual becomes

```text
c Psi=D V-k e r U,

Psi>0 iff D/(k e)>T_quad.                           (Q4)
```

The new threshold is strictly weaker than the old coefficient threshold.
In fact,

```text
V sin(B)^2-U
=H_m(g)[sin(B)^2-sin(g)^2]
 +m(B-g)sin(B)^2
>0.                                                 (Q5)
```

Consequently,

```text
T_quad<r sin(B)^2=sin(A)^2.                        (Q6)
```

Equation (Q5) gives the exact positive amount by which the quadrature target
improves the previous sufficient condition
`D>k e sin(A)^2`. This gain contains both the middle-layer length `B-g` and
the strict phase separation `B>g`.

## 3. Denominator-safe endpoint form of q-E

The positive phase lock allows the acute reconstructions

```text
A=asin(sqrt(r)sin(B)),
d=asin(sqrt(r)sin(g)),

cos(A)=sqrt(1-r sin(B)^2),
cos(d)=sqrt(1-r sin(g)^2).
```

After substitution in the accepted formulas for `q` and `E`, define

```text
Q_quad=
 [c cos(B)-sqrt(r)cos(A)]/sin(B)
 -c k(1-r)^2 sin(g)cos(d)cos(g)
  /[cos(d)(1+k sin(g)^2)
    +c sqrt(r)cos(g)(1+k r sin(g)^2)].              (Q7)
```

Every denominator in (Q7) is strictly positive, and direct cancellation
gives

```text
q-E=Q_quad/(m r).                                   (Q8)
```

Thus the remaining implication is exactly the explicit quadrature
inequality

```text
Q_quad>0 implies (c^2-r)/(k e)>T_quad.              (Q9)
```

It is imposed only on triples `(B,g,r)` satisfying the exact branch
constraints

```text
0<g<B<pi/2,
0<d<A<B<pi/2,
H_m(B)=(1-c)pi+c H_m(A),
H_m(d)+H_m(g)/c=pi/2,
B-g=c(A+d).
```

This formulation removes `alpha`, `theta`, `beta`, `W`, `N`, and the
implicit root derivative from the sign comparison. It retains the full
unsquared orientation and does not enlarge the branch by treating the listed
constraints as optional.

## 4. Boundary and sign audit

- `m>1`, so `k>0`.
- `0<c<1`, so `e>0`.
- `0<r<c^2`, so `D>0`.
- `0<g<B<pi/2`, hence every sine, cosine, and denominator in (Q1)-(Q9) is
  positive.
- `B-g=c beta>0`, so the strict gain in (Q5) cannot vanish.
- No squaring is used to infer the sign of `Q_quad`.
- No numerical scan is used as proof.

## Decision

`RIGOROUS_PARTIAL_RESULT`, pending independent audit of the new identities.

The direct action did not prove or refute (Q9). It replaced the original
mass-weighted implication by a denominator-safe three-variable quadrature
inequality and exhibited the exact positive gap (Q5) below the old maximum
coefficient threshold. The first remaining step is an independent audit of
(Q1)-(Q8), followed, only if accepted, by a bounded prover and falsifier wave
focused exclusively on (Q9).

decision_delta: Eliminated all physical layer weights from the remaining acute mass residual, derived an exact positive quadrature gain below the old coefficient threshold, and reduced q>E implies Psi>0 to the explicit denominator-safe inequality (Q9); global c>2/3 PHI-SIGN and KP-DET remain open.
