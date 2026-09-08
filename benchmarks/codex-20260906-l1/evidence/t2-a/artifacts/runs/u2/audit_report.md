INDEPENDENTLY_AUDITED_PROOF

# Fresh independent completion audit — O4

**Verdict: PASS.** No load-bearing gap was found in the frozen, self-contained proof of

\[
\frac{1}{4\sqrt t}\leq\|P_t^{(0,0)}-P_t^{(0,2)}\|_{\mathrm{TV}}
\leq\frac{10^{10}}{\sqrt t}\qquad(t\in\mathbb Z,\ t\geq32).
\]

Reviewer: `/root/completion_audit`. Candidate author: `/root`.
The audit followed the installed rigorous-open-math-research skill and its
`references/phase-78-synthesis-audit.md` reference. It was conducted afresh from
`answer.md` and the frozen contract, without using previous audits or module proofs
to establish any mathematical step. No numerical verification, internet, history,
other project, session, or memory was used.

## Package binding

- Manifest SHA-256: `de22515202a3e3dab9ea0ee6b9cc053c608338ebd61e06b0ef22df32037d3f25`.
- Candidate SHA-256: `05884d2c49613f30d2c0bb0a6fd4d62ddefb25a2eead41504ce7e5a878a7c573`.
- Contract SHA-256: `6ad9b5e431af4324739f13f1204b49e9c530ee5bb84f6c957177f218988cc436`.
- Every file digest listed in the manifest was recomputed and matched.
- The obligation graph identifies O1–O3 as proved and O4 as the pending independent audit; this report discharges O4 without modifying the frozen graph or proof.

## Definition and semantic audit

The stated switch-walk-switch chain resamples independent fair bits at departure
and arrival, and both initial configurations are all-zero. Conditional on a fixed
base path of positive length, every visited site is resampled and its final lamp
is its last resampling bit. Different sites select different independent coins.
The walk visits every integer between its extreme positions. Consequently the
conditional product law on the visited interval is exactly the same for both
starts, including the initial zeros at 0 and 2. Conditioning further only on the
range and endpoint preserves that law. The common-kernel half-l1 contraction
therefore proves (1) with the prescribed convention for total variation.

The endpoint events in section 1 give exactly one parity-compatible binomial mass:
`p_t(0)` for even time and `p_t(1)` for odd time. The recurrence
`b_(n+1)/b_n=(2n+1)/(2n+2)` verifies the lower induction by the positive difference
`(2n+1)^2-4n(n+1)=1`. It verifies the upper induction by the positive cleared
numerator `3n+2`. These imply the claimed lower constant and (3), respectively.
The lamp kernel is used only at positive time; time zero is separately correct.

## Fourier and killed-kernel audit

The normalization in (4) is correct on the reachable parity class: the full
Fourier integrand is pi-periodic exactly when `j+t` is even. The exponential
expansion therefore gives `f_t(j)=p_t(j)` on that class.

The two external Fourier results are stated in exact standard forms. For
inversion, `g=2 B_t` is compactly supported and C2; the cutoff derivatives vanish,
and two integrations by parts give an integrable inverse transform. The
periodization is uniformly convergent on compact sets. Its j-th coefficient is
`(1/(2L)) integral f_t(v) exp(-i pi j v/L) dv = B_t(pi j/L)/L`.
Absolute integrability permits unfolding. Only finitely many coefficients are
nonzero, so continuous periodic Fourier uniqueness applies. Subtracting the two
cosine series gives the factor `4/L` and exactly (7).

At integer boundaries and reachable endpoints the image sum becomes the usual
finite sum of binomial probabilities. Independently checking the heat recurrence,
zero boundary values by symmetry and reindexing, and the delta initial condition
establishes the killed transition identity by induction. At an absorbing start
the image sums cancel. This argument does not apply an interval kernel to a start
outside its domain.

The compact cutoff is C3 and the spectral sum is locally finite in all parameters.
Alternatively, sixth-order decay of the transforms and their first three
x-derivatives dominates the differentiated image terms by a summable cubic
coefficient times sixth-order decay. These facts justify every parameter
derivative used later, including cutoff points.

## Derivative audit

For (9), differentiating the sine/cosine basis gives exactly the stated recurrence
for `b_(m,r)`. The majorant recurrence is valid because each factor `t-r+1`
that occurs in the second term is at most t. All exponents obey `t-r >= t/2`.
The four majorant rows through order six were independently regenerated.

The Gaussian moments for powers 1, 3, 5, 7, and 9 are respectively
`4, 16, 128, 1536, 24576` with the stated powers of t. Applying the product rule
to `theta^3 cos^t(theta)` independently yields integral bounds
`53616 t`, `55008 t`, `21240 t`, and `3360 t`; their sum is `133224 t`.
All six integrations by parts have zero endpoint terms. The direct bound is
`4/(pi t^2)`. Combining the direct and sixth-order bounds with
`min(1,y^-6) <= 64(1+y)^-6` proves (8) with the displayed A.

The affine argument derivatives of the two image terms give respectively
`4 k^2` and `4 k(k+1)` in (11), including the signs. Their zero coefficients
remove exactly the potentially short image distances. The remaining two tails
have combined coefficient at most `24 j^2`, so summing `j^-4 <= 4/3` gives
`32 A t L^-6`.

For the spectral estimate, `B_L` is bounded by `s E/L`; the two chain-rule terms
in `B_LL` give `(3s+s^2)E/L^2`. The trigonometric derivatives in the candidate
follow from `U=u/L`, `V=v/L`, with both ratios in [0,1]. Reapplying the product
rule gives, after combining all three mixed parameter terms, the bracket
`6+18q+8q^2+(7+6q)s+s^2`. This is bounded by
`q^2(32+13s+s^2)` since q>1, and hence by the right side of (14).

The spectral summation uses `pi^2/8>1` and
`alpha j^2 >= (alpha+j^2)/2`. The termwise integral comparison is in the correct
direction: on `[j-1,j]`, `(x+1)^3 exp(-x^2/2)` is at least
`j^3 exp(-j^2/2)`. The total comparison integral is `5+4I`, where
`I=integral_0^infinity exp(-x^2/2) dx<2`. Thus the spectral prefactor is less
than `1568*64*13 = 1304576`, safely below the final proof's D=1500000.
No narrower-interval estimate is used outside its stipulated width condition.

## Range assembly, boundary, and adversarial audit

Inclusion-exclusion (15) is exactly the restriction to paths attaining both range
endpoints. All four killed kernels have start and terminal points inside or on
their absorbing boundaries. The order of corner differences gives the minus sign
in (16). The integration rectangle keeps `l <= a,z <= r`, and L is positive.
Interpolation in real a is analytic only; no unproved probabilistic conditioning
identity is asserted at noninteger starts.

For width N, common ranges have `m` from `2-N` through 0, giving N-1 ranges and
at most N+1 endpoints. The a-integral has length two and cancels the TV factor
one half. Hence N-squared times the derivative bound is valid. For narrow widths,
`N <= L <= N+2 <= 2N <= sqrt(t)`, and the resulting sum is at most
`4D/sqrt(t)`. For wide widths, the decreasing integral comparison starts at
`floor(sqrt(t)/2)`; bounding this floor below by `sqrt(t)/4` gives exactly
`2048A/(3sqrt(t))`. No parity factor has been incorrectly gained in these counts.

The exceptional supports are disjoint: the start-0 paths have maximum below 2,
whereas the start-2 paths have minimum above 0. The map `S -> 2-S` equates their
masses. Reflection after the first hit of 2 bijects hitting paths ending at
`z<=1` with all paths ending at `4-z>=3`, preserving individual path probability.
Symmetry leaves the four masses with indices -2,-1,0,1. Exactly two are reachable,
which gives `4/sqrt(t)`. The common and exceptional cases exhaust both supports.

Adding the established estimates gives `6150000004/sqrt(t)`, strictly below the
claimed upper constant. All integer times at least 32 are covered. The lower
bound covers every positive time, and the separate time-zero observation is
correct. The argument has no circular dependency or target-equivalent unproved
lemma; its infinite upper sums are convergent estimates of originally finite
probability sums.

## Covered scope and residual risk

Covered: the original chain and TV definitions, both all-zero starts, every
load-bearing claim in `answer.md`, explicit constants, parity, small times,
absorbing boundaries, smooth cutoff points, both width regimes, exceptional
reflection, conditioning marginals, analytic interchanges, and manifest integrity.

No mathematical obligation required for the stated theorem remains open.
This is an independent informal proof audit, not Lean or other kernel-based
formal verification. The auxiliary module files were hash-checked, but this
verdict uses the self-contained final proof rather than their earlier derivations
or constants. Novelty and literature priority were not investigated or claimed.
The standard Fourier inversion and uniqueness theorems remain explicit accepted
analytic prerequisites; their exact formulations and all application hypotheses
were checked. No additional research is requested after this PASS.
