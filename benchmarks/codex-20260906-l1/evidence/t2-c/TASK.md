# Frozen task: U2 total-variation asymptotics

Blind benchmark. Do not inspect any repository, git history, internet source, external memory,
prior benchmark output, or prior solution to this exact problem. Scratch exact or numerical
computation may be used only for falsification. Numerical evidence does not constitute proof.

Let `Z_2 wr Z` be the lamplighter group. Write each state as `(eta,z)`, where
`eta: Z -> Z_2` has finite support and `z in Z` is the base position. Let `0` denote the
all-zero lamp configuration.

Consider the discrete-time switch-walk-switch chain. From `(eta,z)`, independently resample the
lamp at `z` from `Bernoulli(1/2)`, move the base to `z+1` or `z-1` with probability `1/2` each,
then independently resample the lamp at the arrival site from `Bernoulli(1/2)`. Let `P_t^x`
denote the law at integer time `t>=0` started from `x`.

Set

```text
x=(0,0),
y=(0,2).
```

Thus both initial lamp configurations are all zero, and the two initial base positions are `0`
and `2`.

Prove that there are explicit constants `0<c<=C<infinity` and an explicit integer `t_0` such
that, for every integer `t>=t_0`,

```text
c/sqrt(t) <= ||P_t^x-P_t^y||_TV <= C/sqrt(t).
```

Here total variation is `sup_A |P_t^x(A)-P_t^y(A)|`, equivalently one half of the `l^1`
distance on the countable state space.

State every external theorem in the exact form used and verify all hypotheses. Audit parity,
small times, the effect of the two forced initial zero lamps, and every conditioning or
coupling step. Do not replace the chain by a different lamp convention or interpret `(0,2)` as
a lamp lit at site `2`.

A complete result requires both bounds with explicit constants. If incomplete, return the
strongest exact partial result and the first unresolved obligation without claiming completion.
