REPAIR

# Immutable E-definition binding and Q7-Q8 substitution

## Action and immutable provenance

- Action ID: `REPAIR-DIRECT-E-BINDING-01`.
- Repair scope: only the dependency gap in `(Q7)-(Q8)`.
- Route 8 prover source:
  `route-08-common-beta-orientation/prover_result.md`.
- Route 8 prover SHA-256:
  `6ecc0ae44f6841414a8a8be8077ed919f1d66d285dc66abbdc79f85660c44d6d`.
- Route 8 independent audit SHA-256:
  `bb1207baf181f37459345ed3cff4deb560b5c0acc18fdc3952b8410ffb6bd820`.
- Route 10 candidate SHA-256:
  `e156f97b449daef0eac35ed7ae7ef30ceb2c6eac35983bc24534cf6f1b1a4634`.
- Route 10 audit SHA-256:
  `cc54e0dc73e2d8de402a669818f3145176f4d7e94e5f4f15fad869642998dd04`.

The immutable Route 8 prover source states the exact accepted formula

```text
E=
 c k (sigma^2-1)^2 sin(d)cos(d)cos(g)
 ------------------------------------------------------------------. (E0)
 m[sigma cos(d)(cos(g)^2+M sin(g)^2)
   +c cos(g)(cos(d)^2+M sin(d)^2)]
```

This repair does not edit that source or the original Route 10 candidate.

## Line-by-line substitution

Use the Route 10 variables

```text
r=sigma^(-2),
M=m^2,
k=M-1,
sin(d)=sqrt(r)sin(g).
```

All square roots are positive on the acute branch. First,

```text
sigma=r^(-1/2),
(sigma^2-1)^2=(1-r)^2/r^2,

cos(g)^2+M sin(g)^2=1+k sin(g)^2,
cos(d)^2+M sin(d)^2=1+k r sin(g)^2.                (E1)
```

The numerator of `(E0)` becomes

```text
c k(1-r)^2 sin(g)cos(d)cos(g)/r^(3/2).             (E2)
```

The denominator of `(E0)` becomes

```text
m r^(-1/2)
 [cos(d)(1+k sin(g)^2)
  +c sqrt(r)cos(g)(1+k r sin(g)^2)].               (E3)
```

Dividing `(E2)` by `(E3)` gives

```text
m r E=
 c k(1-r)^2 sin(g)cos(d)cos(g)
 -------------------------------------------------. (E4)
 cos(d)(1+k sin(g)^2)
 +c sqrt(r)cos(g)(1+k r sin(g)^2)
```

Every factor in the denominator of `(E4)` is strictly positive.

For the q term, the positive lock gives

```text
sin(A)=sqrt(r)sin(B),
sigma=r^(-1/2).
```

Substitution in the accepted formula

```text
q=[c sigma cos(B)-cos(A)]/[m sin(A)]
```

yields

```text
m r q=[c cos(B)-sqrt(r)cos(A)]/sin(B).              (E5)
```

The first term of Route 10 `(Q7)` is exactly `(E5)`, and its second term is
exactly `(E4)`. Therefore

```text
Q_quad=m r(q-E),
q-E=Q_quad/(m r).                                  (E6)
```

Since `m r>0`, `(E6)` preserves the strict sign.

## Repair boundary

- No statement in `(Q1)-(Q6)` is changed.
- The open implication `(Q9)` is not attempted and is not claimed proved.
- No numerical evidence is used.
- The repair supplies only the missing immutable dependency and its exact
  algebraic substitution.

decision_delta: Bound the exact immutable Route 8 definition of E and proved line by line that the second Q7 term is mrE, repairing the sole dependency gap in Q7-Q8 while leaving Q9 and c>2/3 KP-DET open.
