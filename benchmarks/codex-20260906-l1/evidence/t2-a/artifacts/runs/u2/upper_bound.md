RIGOROUS_PARTIAL_RESULT

# O3 worker record

Contract read: `problem_contract.md`, stated SHA256 6ad9b5e431af4324739f13f1204b49e9c530ee5bb84f6c957177f218988cc436. Scope: TV upper bound for SWS starts (zero,0), (zero,2). No external mathematical sources inspected. Skill and route/audit/reporting phase instructions inspected. No children.

## Route U1: direct range/endpoint comparison

Mechanism: condition lamps on visited interval; it suffices to bound total variation of the integer triple (minimum,maximum,endpoint) for SRWs started at0 and2. Marked transition probabilities are a double boundary difference of killed interval heat kernels. Candidate next lemma is an l1 spatial-gradient estimate for this marked kernel. Status ACTIVE, first bottleneck is controlling the sum over interval widths without losing a logarithm. This is only a reduction so far.

## Route U2: excursion re-rooting

A walk from1 of length t+1 conditioned on its first direction, with its first step removed, has precisely the base path law starting0 or2. If the shortened path hits1, its lamp1 is resampled and the extra first-step lamp information disappears. No-return probability is O(t^-1/2). Conditional first-direction influence can therefore be reduced to range/endpoint influence of the first excursion from1. The maximal-excursion argument may lose a logarithm; no upper bound claimed.

## Exact caution from supplied failed route

Reflection coupling before meeting1 yields different old extrema. Any subsequent claim of immediate lamp agreement is false. Erasing the extrema after meeting needs a new quantitative argument and does not follow from the usual base coupling estimate.

## Decision delta

No O3 closure yet. The desired law comparison has been isolated at the one-dimensional marked random-walk kernel; neither route is promoted to a proof.

## Numerical falsification probe (2026-09-08, not proof)

`python3 runs/u2/range_probe.py` enumerates base-path triple distributions exactly up to binary floating arithmetic, t<=80. TV times sqrt(t) was 1.74693,2.09377,2.32991,2.49708,2.62477 at t=5,10,20,40,80. This does not falsify O(t^-1/2), and supplies no theorem. Initial `python` invocation failed because that executable is absent; `python3` succeeded. Root now owns analytic killed-kernel route; worker specializes in excursion re-rooting to avoid duplicate ownership.

### Excursion obstruction

Conditioning on the number of completed excursions and permuting them preserves the final range and endpoint, so first-sign influence is an average over their signs. The direct absolute bound by sign-count fluctuation is O(N^-1/2), potentially t^-1/4, and does not close O3. Bounding by the event that the first excursion is extremal threatens a logarithm through E[1/N]. These are blocked coarse estimates, not impossibility claims for the excursion route.

## Freeze / handoff (05:08 UTC)

Root requested stopping excursion exploration and switched this worker to a bounded identity audit for the analytic route. The excursion route is BLOCKED at cancellation of first-excursion-sign influence; no unsupported O(t^-1/2) claim is made. Material decision delta: the worker's range-law reduction and logarithmic-loss warning were accepted by root; the independent analytic route now addresses this using small/large-width splitting. Final local contribution is written separately in `kernel_identity_audit.md`.
