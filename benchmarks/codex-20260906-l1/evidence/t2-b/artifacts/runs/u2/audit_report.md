INDEPENDENTLY_AUDITED_PROOF

Verdict: PASS. No load-bearing gaps, critical errors, or repairs.

Reviewer: /root/completion_auditor. Candidate author: /root.
Reviewed at: 2026-09-07T23:40:53.592141+00:00.
Manifest SHA256: 3f0c2bbb40f5456e14ddf7f4ea4fee7ef39d61486513364ed5b055f209d465a1.
Canonical answer.md SHA256: 9f86ec2c20f883bbb038acd1afaf73773f8c0c68307194862d68f8a401dbf7f8.

This is the single fresh independent package audit for that frozen manifest. The reviewer received the frozen task and package, not the solver's exploration trace. The installed rigorous-open-math-research skill, its phase-78 audit instructions and closure protocol were read. All listed package hashes, root IDs, closed statuses and proof anchors were verified. The proof and manifest were not edited. No internet, git, repository history, prior solutions, sessions, external memory or other projects were consulted. The helper Markdown files listed in this run's manifest were hashed; their arguments were not needed as premises because answer.md contains the full proof.

## Definition audit — PASS

The chain is exactly the stated reset version of switch-walk-switch. Given a base path of positive length, every visited site has a final reset, including the initial site on its first departure. Last resets at different sites have distinct indices in the independent bit family, and those indices depend only on the independent base path. Thus conditioning on the path gives the uniform product law on the entire visited interval with every lamp outside it fixed at zero. This kernel depends only on the minimum, maximum and endpoint. Averaging over paths with a specified triple preserves the same kernel. In particular, a never-visited initial-zero site stays zero. The countable-kernel l1 inequality proves the asserted TV contraction with the convention TV=one-half l1. No coupling of incompatible lamp histories is assumed.

## Logic audit — PASS

The endpoint event gives the probability of -2<S_t<=0. Each time parity has exactly one accessible site in this interval, with mass a_t. The central-binomial recurrence and its two square inequalities prove the stated upper and lower coefficient bounds. The odd-time comparison and t=1 endpoint are valid. As an independent simple-case check, at t=1 the endpoint laws are uniform on {-1,1} and {1,3}; their half-l1 distance is 1/2, agreeing with the event calculation.

The sine kernel follows from the finite killed transition matrix; its eigenvectors and eigenvalues follow directly from the sine addition formula, and geometric-series orthogonality gives the normalization. Independently, the image formula has the correct time-zero delta, nearest-neighbor recurrence and zero absorbing boundaries, so induction identifies it with the same killed kernel. The two boundary finite differences are exactly inclusion-exclusion for attaining both extrema. The short and long interval sums cover the common support, and the remaining support consists precisely of one-sided failure to cover the opposite initial site. Every reduction is in the needed direction; there is no circular premise.

## Boundary audit — PASS

Both starts are even, so the endpoint parity is t for both laws. In the sine pairing the multiplier is (-1)^(t+x+y)=1 for these integer evaluations, including all four contracted kernels. The middle eigenvalue contributes zero for positive time. Real interpolation does not assert a probability formula at noninteger points; it is only an extension agreeing at the integer corners used by the finite differences.

At every corner where a contracted kernel loses its start or endpoint, that point is exactly an absorbing boundary and both formulas vanish. Throughout the interpolation box, L' lies in [2,L], and x',y' lie in [0,L']; this includes a=0, b=2, z=a and z=b. At the cutoff theta=pi/2, g and its first two derivatives vanish for the times used, so the required mixed derivatives are continuous, including when a new spectral summand enters. Local finiteness permits termwise differentiation. The s derivative does not differentiate g; only two derivatives in L occur, so the stated cutoff regularity suffices.

The free-walk third-difference identity is valid at support endpoints; outside the support of p_(t+3), all four shifted p_t terms vanish. Telescoping steps preserve the required parity. The first image term at k=0 and second term at k=0,-1 vanish exactly. Long intervals satisfy L>sqrt(t)>=32, which is sufficient for every displacement bound. The theorem excludes t=0 and only asserts its upper estimate for t>=1024.

## Adversarial audit of the quantitative steps — PASS

1. The probability-ratio logarithm sums to -(w^2-w0^2)/(2(N+1)), since its increments use (v+1)/(N+1). The central coefficient bound and e^(1/4)<=4/3 then give (5). This reasoning covers either parity and all in-support w.

2. Expanding W^3 gives (3N-2)W plus the sum over ordered distinct triples. Exchangeability conditional on W=w gives the cubic quotient in (7); conditioning on the first three signs gives its factor 8 and signs +,-,+,-. The denominator is at least N^3/2 for N>=6. Consequently the bound is 32 N^-2 (u^3+3u)e^(-u^2/4). Splitting the Gaussian and bounding the two polynomial maxima gives the claimed 1728, hence the looser 10^4 bound in (6).

3. In coordinates (L,x,y), the derivatives are partial_a=-(partial_L+partial_x+partial_y), partial_b=partial_L and partial_s=partial_x. For F=L^-1 f(d/L), independent differentiation gives F_LL=L^-3(2f+4 theta f'+theta^2 f''). Expanding f=theta h R produces exactly
   6d+12d^2+4d^3+(7d+4d^2)v+dv^2
   after extracting L^-4 e^(-v/4). The xL and yL terms have coefficients 3d^2+2d^3+d^2v. Bounds (14) follow from cos(theta)<=e^(-theta^2/2), sin(theta)<=theta and t-2>=t/2. The constants 34, 6, 6 and the outer factor 4 are covered by 200.

4. Multiplying the derivative sum by t^2 transforms u^2 d^3 into d^-1 v^2. The inequality v^2(1+v)^2<=2(v^2+v^4) and the separate polynomial-Gaussian maxima bound its first exponential half by less than 3*10^6. The remaining series is bounded by the decreasing Gaussian integral sqrt(2/pi)<1. Thus the derivative constant can be 6*10^8, which is smaller than the stated 10^9. The FTC rectangle has volume 2, and there are at most L^2 triples at each L and at most t^(3/2) such weighted short-interval choices. This proves (11).

5. Independently deriving image inclusion-exclusion: for the direct image A=z-s+2kL, either boundary contraction changes A by -2k, so its extremal difference is D_(2k)^2 p(A). For the reflected image B=z+s-2a+2+2kL, the boundary shifts are -(2k+2) and -2k. Its kernel sign is minus; subtracting the start-2 term shifts B by +2 and reverses that sign, giving +D_(2k)D_(2k+2)D_2 p(B_0+2). This is exactly (16).

6. Each D_(2k) telescopes into |k| signed D_2 translates. The direct-image multiplicity is k^2. The reflected-image multiplicity is |k(k+1)|. The third difference has center w=v-3 and differs from the expression in (6) only by an overall sign. For the direct images |z|<=L-2, and the claimed loss allowance 4m+3 bounds all shifts and centering. For reflected images 4<=r+y+2<=2L-2, the original displacement has magnitude at least 2mL+2, and the loss allowance 4m+5 is sufficient. Thus both |w|>=mL/2 estimates hold. The two signs of k contribute total multiplicity at most 6m^2, giving 60000 in (19).

7. For X,Y>=1, 2XY>=X+Y. The separated exponentials therefore dominate the long-interval series. On [n-1,n], (r+1)^2 e^(-r^2/(128T)) is pointwise at least n^2 e^(-n^2/(128T)). The three Gaussian integrals yield (20); the loose numerical estimates give less than (768+128+12)T^(3/2)<1000T^(3/2). Applying this once with T=1 and once with T=t gives 60000*1000*1000=6*10^10 in (21). All majorants are nonnegative and summable.

8. Reflection after the first hit on 2 maps endpoints below 2 to endpoints above 2, bijectively and with equal path probability. Thus P_0(M_t<=1)=P_0(-2<=S_t<2). There are two possible parity sites, so this is at most 2 sqrt(2/t)<3/sqrt(t). Reflection about 1 gives the equal exceptional mass for the start at 2. Their contribution to half-l1 is one of these equal masses. The common-support half-factors give the final constant 3+10^9+3*10^10<10^12.

## Obligations and residual risk

O1 passes: the full-chain upper bound 10^12/sqrt(t) holds for every integer t>=1024. O2 passes: the full-chain lower bound 1/(2sqrt(t)) holds even for every integer t>=1. Therefore the requested constants c=1/2, C=10^12 and t0=1024 satisfy the frozen theorem contract simultaneously for both parities.

All load-bearing calculations and transitions in the canonical proof were independently re-derived. Elementary calculus, finite-dimensional algebra and countable probability were checked in the forms used; no outside research theorem is invoked. No mathematical computation was used to establish a universal claim. This is an independent manual audit, with the usual residual possibility of human-style oversight; it is not Lean or other formal verification. No Lean verification was requested or run, and no novelty or literature-priority claim was assessed.
