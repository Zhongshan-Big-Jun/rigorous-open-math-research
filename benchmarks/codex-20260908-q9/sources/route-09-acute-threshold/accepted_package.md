# Accepted acute-threshold partial package

## Status and bindings

`STRICT PARTIAL RESULT`.

This package contains only statements accepted by the fresh independent audit
`AUDIT-W14-W15-ACUTE-RETRY-01`, verdict `PASS`.

- W14 SHA-256:
  `ef7ad48667026a5eb672c8d4bd48718903fd6dcf2102d9f16b8a6883ece948c2`.
- W15 SHA-256:
  `c961bcba5931957beb2e2e60baed90e9517d2af0d3015efa8605a86e985160a2`.
- Reconciliation SHA-256:
  `6b9973b8f56b06b1c254696976b9349f0bb5725745ac61e3dcadbd4901fbe959`.
- Retry audit JSON SHA-256:
  `672f7e3e762ff412450125ac4fecf634bf509f9a0535c94666f64bcc75b814ce`.
- Retry audit Markdown SHA-256:
  `009fcac07c3e2ceabc669e41fe6f7947146473b818a1dd1cefbf278baeb7ba27`.

Arbitrary finite-`c` `PHI-SIGN` and KP-DET remain `OPEN` for `c>2/3`.

## P16. Strict intrinsic compatibility monotonicity

On the unique remaining acute chamber, define

```text
c>1/2,
pi/(2c)<alpha<pi,
t=pi-alpha,
A=P_m(t),
B=P_m((1-c)pi+c t),
sigma=sin(B)/sin(A),
kappa=B-c A,
sin(kappa-c d)/sin(d)=sigma,
g=kappa-c d.
```

The root `d` exists and is unique, with

```text
0<d<A<B<pi/2,
0<d<g<B<pi/2.
```

Let

```text
J(A)=H_m(d(A))+H_m(g(A))/c-pi/2.
```

The full constrained derivative, including the implicit dependence of `d`,
satisfies

```text
J'(A)>0.
```

Moreover,

```text
lim_(A->0+) J(A)=pi(2-3c)/(2c).
```

Therefore a strict acute intrinsic root `J(A)=0` can exist only for

```text
c>2/3.
```

At `c=2/3`, the endpoint limit is zero but strict monotonicity gives
`J(A)>0` for every `A>0`, so no boundary equality enters the strict branch.

## P17. Closed KP-DET ratio range

The accepted common-beta chamber already proves KP-DET when
`c alpha<=pi/2`. Its complement is exactly the acute chamber of P16. Hence
every complete tuple with

```text
0<c<=2/3
```

satisfies

```text
Phi<0,
KP-DET.
```

This strictly extends the previously accepted range `0<c<=1/2`.

## P18. Exact scalar mass collapse

Let `M=m^2`, `k=M-1`, `e=1-c^2`, and use the accepted quantities
`D`, `A`, `d`, and the three mass coefficients. The transfer norms give

```text
X^2=P sin(A)^2,
C^2=P sin(d)^2,
C^2/X^2=sin(d)^2/sin(A)^2.
```

Substitution into the exact complete mass balance yields

```text
D(alpha+theta+m beta)
=k e[alpha sin(A)^2+theta sin(d)^2].
```

Consequently, every complete acute tuple satisfies

```text
0<D<k e max{sin(A)^2,sin(d)^2}.
```

At the unique intrinsic root, define

```text
W=alpha+theta+m beta,
N=alpha sin(A)^2+theta sin(d)^2,
Psi_(c,m)(A)=D W-k e N.
```

The exact mass equation is precisely `Psi_(c,m)(A)=0`. The remaining
branch-local obligation is the strictly weaker scalar implication

```text
q>E implies Psi_(c,m)(A)>0,
c>2/3,
J(A)=0.
```

This implication remains `OPEN`.

## P19. Uniform all-m boundary collar

Put

```text
t=pi-alpha,
h=pi/2-theta,
z=1/m in (0,1),
c0=2/3.
```

For every exact strict-modal, common-beta, positive-lock acute sequence with

```text
t->0,
h->0,
c->c0,
```

uniformly after compactifying by `z in [0,1]`, one has

```text
h/t=1+o(1),
c=c0+[2(1-z^2)/(3 pi)]t+o(t),
beta=2zt(1+o(1)),

t^2(q-E)=sqrt(3)/6+o(1),
TA=4/9+o(1),
Td=4/9+o(1),
t^2 Mmass=-2 pi/3+o(1).
```

Thus the strong threshold holds with a fixed positive margin in the collar,
but the exact normalized mass residual is strictly negative. No complete
tuple can approach this boundary. This is not a KP-DET counterexample.

## EVIDENCE boundary

W15's binary64 scans are non-exhaustive `EVIDENCE` only. They are not used in
P16-P19 and do not prove complete-system `q<=E` outside the collar.

## Exact remaining gap

For `c>2/3`, prove or refute

```text
q>E implies Psi_(c,m)(A)>0
```

at the unique intrinsic root `J(A)=0`. Complete arbitrary finite-`c`
`PHI-SIGN`, KP-DET, KO-DET, simultaneous sector singularity, non-symmetric
roots, and global `G1'` remain open.

