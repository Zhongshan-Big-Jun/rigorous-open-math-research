# Problem contract

Authoritative statement: TASK.md and the user message, 2026-09-08.

# Constrained acute quadrature implication

Decide the universal implication below. An affirmative proof or a rigorously
certified counterexample is a complete answer. If it remains unresolved,
deliver the strongest proved partial result and the exact remaining gap.

## Definitions and domain

All variables are real. Let

```text
m>1,  2/3<c<1,  0<r<c^2,  0<g<B<pi/2,
k=m^2-1,  e=1-c^2,
H_m(z)=arctan(m tan(z))  for 0<=z<pi/2,
F_m(z)=H_m(z)-m z,
A=arcsin(sqrt(r) sin(B)),
d=arcsin(sqrt(r) sin(g)).
```

Use the principal positive square root and principal inverse trigonometric
branches. Thus `0<d<A<B<pi/2` and `d<g`. Impose all three exact constraints:

```text
H_m(B)=(1-c)pi+c H_m(A),                             (C1)
H_m(d)+H_m(g)/c=pi/2,                               (C2)
B-g=c(A+d).                                        (C3)
```

The constraints are simultaneous. They cannot be dropped, replaced by an
approximately satisfied equation, or squared with the orientation discarded.
No mass-balance equation is an additional hypothesis of this problem.

Define

```text
V=pi+F_m(g)-F_m(B),
U=(pi-H_m(B))sin(B)^2+H_m(g)sin(g)^2,
T_quad=r U/V,

Q_quad=
 [c cos(B)-sqrt(r)cos(A)]/sin(B)
 -c k(1-r)^2 sin(g)cos(d)cos(g)
  /[cos(d)(1+k sin(g)^2)
    +c sqrt(r)cos(g)(1+k r sin(g)^2)].
```

All denominators here are positive on the stated domain.

## Target Q9

For every tuple `(m,c,r,B,g)` satisfying the domain and (C1)-(C3), prove or
refute

```text
Q_quad>0  implies  (c^2-r)/(k e)>T_quad.             (Q9)
```

Equivalently, with `R_quad=(c^2-r)V-k e r U`, decide whether
`Q_quad>0 implies R_quad>0`. Both inequalities are strict. A refutation must
certify an admissible tuple with `Q_quad>0` and `R_quad<=0`, including the
three exact constraints. An existence proof isolating such a tuple with
rigorous error bounds is acceptable; floating-point residuals alone are not.

## Common starting facts

The following elementary identities and sufficient condition are supplied
equally to every solver. They may be used, but deriving them again is not
new progress on Q9:

```text
F_m'(z)=-m k sin(z)^2/[1+k sin(z)^2],
V=pi+m k integral_[g,B] sin(z)^2/[1+k sin(z)^2] dz>pi,

V sin(B)^2-U
 =H_m(g)[sin(B)^2-sin(g)^2]+m(B-g)sin(B)^2>0,

0<T_quad<r sin(B)^2=sin(A)^2.
```

Consequently `c^2-r>=k e r sin(B)^2` is already a sufficient condition for
`R_quad>0`. A proof that only restates this sufficient condition does not
settle Q9. The interval `c<=2/3` is outside the task; solving that easier
interval does not address the target.

## Delivery and evidence

Write `answer.md` as a self-contained mathematical submission. It must state
the result, prove each claimed new lemma with its exact domain, and separate
the unproved remainder from proved statements. Keep all load-bearing proof
arguments and any exact certificate needed to check the result in this file;
supporting scripts can also be retained for reproducibility.

Finite scans, asymptotic heuristics, an equivalent reformulation with the
same unproved implication, and a conditional result assuming the missing
inequality do not count as full resolution. A partial theorem on a precisely
specified nonempty subdomain can count as partial progress. Explain how it
goes beyond the supplied starting facts. Existence of a full solution in the
allowed time, polarity, and novelty in the external literature are unknown.


## Contract audit
All three constraints are simultaneous, branches are principal, r<c^2, and c>2/3. No mass balance may be added. Completion is a self-contained proof or an exact admissible counterexample. Partial results must specify a nonempty domain and exact gap. No literature, internet, memory, sessions, or other projects may be consulted.

## Novelty preflight
Openness unknown. skip: search_forbidden; blind benchmark. Post-discovery search is also forbidden. No novelty claim. Snapshot: TASK.md SHA256 c7133b97e440e90095088927f105c9f88fcdc54f4a4772ee9f85ba5a139e6330
