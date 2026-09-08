RIGOROUS_PARTIAL_RESULT

# Local audit: image/spectral interpolation identity

Scope: the exact relation between the continuous Fourier interpolation, its image sum, and the killed discrete walk; parity and parameter regularity. No inspection of root candidate files was made. Inputs are the frozen problem contract and the formulas communicated in the task. This is not an audit of derivative estimates or of the full TV proof.

## Definitions

Fix an integer n>=4. Define

    psi_n(theta) = cos(theta)^n for |theta|<=pi/2, and 0 otherwise,
    f_n(u) = (1/pi) integral_R psi_n(theta) exp(i u theta) dtheta.

The function psi_n is compactly supported and C^(n-1). In particular, f_n and its first three derivatives decay at least quadratically in u: integrate by parts twice in the compactly supported Fourier integral for (i theta)^j psi_n(theta), j=0,1,2,3. Boundary values and first derivatives vanish because n>=4. This justifies absolute, locally uniform convergence of all image sums used below when L stays bounded away from zero, as well as the integrations defining Fourier coefficients.

For real l<r, let L=r-l and let a,z be real. Set

    I_n(l,r;a,z) = sum_{k in Z} [ f_n(z-a+2kL) - f_n(z+a-2l+2kL) ].

Then exactly

    I_n(l,r;a,z)
      = (4/L) sum_{j>=1} psi_n(pi j/L)
          sin(pi j(a-l)/L) sin(pi j(z-l)/L).                 (1)

The right side is a finite sum for each L. The support cutoff is essential: writing `max(cos(theta),0)^n` without restricting |theta|<=pi/2 would produce a periodic function, which is NOT psi_n and would invalidate this series.

## Proof of (1), including constants

Let G_L(v)=sum_k f_n(v+2kL). It is continuous and 2L-periodic by absolute local uniform convergence. Its j-th Fourier coefficient is

    (1/(2L)) integral_0^(2L) G_L(v) exp(-i pi j v/L) dv
      = (1/(2L)) integral_R f_n(v) exp(-i pi j v/L) dv
      = psi_n(pi j/L)/L.

The last equality follows from the normalization f_n=(1/(2pi)) integral 2 psi_n exp(iu theta). A direct inversion justification, avoiding a distributional assertion, is given below. Only finitely many coefficients are nonzero. Thus Fourier-series uniqueness yields

    G_L(v) = (1/L)[psi_n(0)+2 sum_{j>=1} psi_n(pi j/L) cos(pi j v/L)].

Subtract the values at v=z-a and v=z+a-2l. The constant term cancels. The identity

    cos(U-V)-cos(U+V)=2 sin U sin V

with U=pi j(z-l)/L and V=pi j(a-l)/L proves (1).

For completeness, inversion in the displayed coefficient formula can be proved by Gaussian regularization. Insert exp(-epsilon v^2/2) into the integral of f_n(v) exp(-i xi v), interchange integrals (the Gaussian and compact theta support give absolute integrability), and evaluate the elementary Gaussian Fourier integral. The result is

    2 integral_R psi_n(theta) (2pi epsilon)^(-1/2)
          exp(-(theta-xi)^2/(2epsilon)) dtheta.

As epsilon decreases to0 this tends to 2 psi_n(xi), by continuity and boundedness of psi_n and the approximate-identity property of the Gaussian. The unregularized v-integral is the same limit by dominated convergence, since f_n is integrable. Fourier-series uniqueness here can equivalently be obtained by convolving a continuous periodic function with Fejer kernels: if all coefficients vanish, every Fejer mean is zero; these means converge uniformly to the continuous function, which must therefore be zero. Uniform convergence follows directly from positivity, mass one, and decay of the Fejer kernels away from zero.

## Exact killed-walk interpretation at integer parameters

Let l<r be integers. Let K_n(l,r;a,z) be the probability that simple symmetric nearest-neighbor walk, started at integer a in {l+1,...,r-1}, is at integer z after n steps and has not hit l or r by that time. For integer a,z in this interior with n+a+z even,

    K_n(l,r;a,z)=I_n(l,r;a,z).                              (2)

For a or z on either absorbing boundary both sides are zero, so (2) extends to that case. It is NOT asserted for arbitrary a or z outside [l,r].

First, for integer u with n+u even, the binomial Fourier formula gives

    p_n(u) = (1/(2pi)) integral_(-pi)^pi cos(theta)^n exp(iu theta)dtheta
           = (1/pi) integral_(-pi/2)^(pi/2) cos(theta)^n exp(iu theta)dtheta
           = f_n(u).

Indeed the integrand is pi-periodic exactly when n+u is even. The first equality itself follows by expanding ((e^(i theta)+e^(-i theta))/2)^n and integrating individual exponentials. Every image argument in I_n has parity a+z, since 2kL and2l are even. Thus every f_n in I_n equals p_n when n+a+z is even.

The method-of-images identity for p_n is proved, rather than assumed, as follows. The sum

    J_n(a,z)=sum_k [p_n(z-a+2kL)-p_n(z+a-2l+2kL)]

is finite for each n because p_n(u)=0 for |u|>n. It satisfies the nearest-neighbor heat recurrence in z, vanishes at z=l by symmetry p_n(u)=p_n(-u) and reindexing k, and vanishes at z=r by the same symmetry and the reindexing k to -k-1 for one term. At time0 and interior a,z the first image contributes1 precisely if z=a; its other terms and all reflected-image terms are0. Therefore J_n and the killed transition probabilities agree by induction on n. This proves (2).

Equivalently, the ordinary finite-interval sine formula contains j=1,...,L-1 with factor2/L. Terms j and L-j coincide when n+a+z is even, because their relative sign is (-1)^(n+a+z-2l)=1. Pairing gives factor4/L and leaves j<L/2. When j=L/2, cos(pi/2)^n=0 for n>=1. This independently checks the parity and factor in (1)-(2).

## Regularity needed for finite differences

For n>=4 the right side of (1) is C^3 in (l,r,a,z) on l<r: on each compact subset only finitely many j have nonzero terms, and psi_n is C^3, including at its cutoff. Thus there are no missing derivative terms from a varying cutoff j<L/2 through third order. Formula (1), already established for every real parameter tuple, allows the same C^3 interpolation to be represented by either the spectral or image expression.

When applying the identity to exact ranges [m,M] with m<=0 and M>=2, the four killed intervals arising from inclusion-exclusion have absorbing left boundary in {m-1,m} and right boundary in {M,M+1}. Both starting points0,2 and all terminal z in[m,M] are interior or exactly on an absorbing boundary. Consequently (2) is applicable at all required integer corners. Along continuous interpolation a in[0,2], l in[m-1,m], r in[M,M+1], one has l<=a<=r, so no invalid extension of the killed probability outside its interval is invoked. (The analytic identity itself holds for all real a,z.)

Ranges failing to contain both starting points need a separate bound; they cannot be silently represented as killed kernels with the starting point outside the absorbing interval. This is outside the present audit scope.

## Verdict

PASS for identities (1)-(2), their stated parity restriction, the normalization4/L, and C^3 parameter interpolation under n>=4 and the compact-support convention for psi_n. No derivative-estimate constant, width sum, exceptional-range probability, lamp marginal, or final TV conclusion was audited here.

Decision delta: the proposed real-parameter spectral interpolation is legitimate, so finite-difference estimates may use it provided the cutoff is written explicitly and excluded-start ranges are handled separately. No independent gap remains in this bounded identity obligation.
