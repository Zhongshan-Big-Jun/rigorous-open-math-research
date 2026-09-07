# Closed obligations

- O1: PROVED and independent audit PASS. Full-chain upper bound10^12/sqrt(t) for every integer t>=1024. Dependencies: exact lamp kernel and joint interval/endpoint estimate. Proof: ../../answer.md, parts1 and3–6.
- O2: PROVED and independent audit PASS. Lower bound1/(2sqrt(t)) for every integer t>=1, by the endpoint event z<=0 and elementary binomial recurrence. Proof: ../../answer.md, part2.
- L1: exact independent last-reset kernel, including initially unvisited zeros. CLOSED.
- L2: spectral estimate for intervals of size<=sqrt(t), image estimate for larger intervals, and one-sided support bounds. CLOSED.
- H: explicit Gaussian estimate for the third binomial difference, derived from an exact exchangeability identity. CLOSED.

Remaining mathematical gap: none. Formalization: not requested; no Lean verification claim. Fast-close STOP.
