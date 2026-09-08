# Accepted quadrature reduction partial package

## Status and bindings

`STRICT PARTIAL RESULT`.

This package contains only Route 10 identities accepted by independent audit
and narrow re-audit.

- Coordinator direct SHA-256:
  `e156f97b449daef0eac35ed7ae7ef30ceb2c6eac35983bc24534cf6f1b1a4634`.
- First audit SHA-256:
  `cc54e0dc73e2d8de402a669818f3145176f4d7e94e5f4f15fad869642998dd04`.
- E-binding repair SHA-256:
  `f5956bc3c6b00c28ed02237095fda7b0478bb5718f6c88098db588753172bf3c`.
- Re-audit SHA-256:
  `6a950bf3483585a6ddc526ece839fb931f0ff5accdce7abc01f02559f59a87c1`.

The re-audit verdict is `PASS`. The explicit quadrature sign implication
`(Q9)` is not included and remains `OPEN`.

## P20. Exact quadrature elimination

Let

```text
M=m^2,
k=M-1,
e=1-c^2,
r=sigma^(-2),
D=c^2-r,
F_m(z)=H_m(z)-m z.
```

For every tuple in the remaining acute chamber,

```text
c W=pi+F_m(g)-F_m(B),

c N=r[(pi-H_m(B))sin(B)^2+H_m(g)sin(g)^2],

F_m(g)-F_m(B)
=m k integral_[g,B] sin(z)^2/[1+k sin(z)^2] dz>0.
```

Define

```text
V=pi+F_m(g)-F_m(B),
U=(pi-H_m(B))sin(B)^2+H_m(g)sin(g)^2,
T_quad=r U/V.
```

Then

```text
c Psi=D V-k e r U,
Psi>0 iff D/(k e)>T_quad.
```

The quadrature threshold lies strictly below the previous coefficient
threshold. The exact positive gain is

```text
V sin(B)^2-U
=H_m(g)[sin(B)^2-sin(g)^2]
 +m(B-g)sin(B)^2
>0,

T_quad<r sin(B)^2=sin(A)^2.
```

## P21. Denominator-safe q-E reduction

The positive acute reconstructions are

```text
A=asin(sqrt(r)sin(B)),
d=asin(sqrt(r)sin(g)).
```

Define

```text
Q_quad=
 [c cos(B)-sqrt(r)cos(A)]/sin(B)
 -c k(1-r)^2 sin(g)cos(d)cos(g)
  /[cos(d)(1+k sin(g)^2)
    +c sqrt(r)cos(g)(1+k r sin(g)^2)].
```

Every displayed denominator is strictly positive, and the accepted Route 8
formulas give exactly

```text
Q_quad=m r(q-E),
q-E=Q_quad/(m r).
```

Thus strict signs are preserved. The remaining branch-local problem is the
explicit constrained implication

```text
Q_quad>0 implies (c^2-r)/(k e)>T_quad,              (Q9)
```

under the exact spectral, intrinsic, common-beta, and modal constraints.

## Exact remaining gap

Prove or refute `(Q9)` for `c>2/3`. Complete arbitrary finite-`c`
`PHI-SIGN`, KP-DET, KO-DET, simultaneous sector singularity, non-symmetric
roots, and global `G1'` remain open.
