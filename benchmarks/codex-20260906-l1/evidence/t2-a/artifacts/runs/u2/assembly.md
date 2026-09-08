# Upper-bound assembly (root)

Set A=9000000, t>=32. The Fourier lemma gives |f_t'''(x)|<=A t^-2(1+|x|/sqrt(t))^-6. Its constant8526336/pi is <A.

For l<=a,z<=r and L=r-l, the image formula yields
H_alr=sum_k [4k² f_t'''(z-a+2kL)+4k(k+1) f_t'''(z+a-2l+2kL)].
Direct terms k!=0 have argument modulus at least |k|L. Reflected terms k>=1 and k<=-2, indexed respectively by j=k and j=-k-1, have argument modulus at least2jL and coefficient at most8j². Thus
|H_alr|<=24A t^-2 sum_{j>=1}j²(1+jL/sqrt(t))^-6
<=32A t L^-6,
using sum j^-4<=4/3. All differentiated sums converge locally uniformly: integrate by parts at least six times in Fourier representations for derivatives through order3; polynomial image coefficients are at most cubic and the spatial decay is sixth order.
For L<=sqrt(t), the spectral estimate gives the sharper700000 L^-4 exp(-t/(2L²)).

Let q_t^a(m,M,z) denote the law of minimum, maximum and endpoint of the base from a. For common ranges m<=0, M>=2, z in[m,M] of parity t, four killed kernels give exact range mass by inclusion-exclusion. The difference q_t^2-q_t^0 is minus the integral of H_alr over a in[0,2], l in[m-1,m], r in[M,M+1]. Starts/endpoints always lie in[l,r], including boundary corners; killed kernels zero on a boundary agree with the image kernel.

For N=M-m>=2 there are N-1 possible m with m<=0,M>=2, and at most N+1 possible z. L belongs to[N,N+2] subset[N,2N]. Hence half the common-range l1 difference is at most the sum over N>=2 of N² times the supremum derivative bound on this L interval (factor2 from a integration cancels half-l1).
For N<=sqrt(t)/2, use L<=2N<=sqrt(t): contribution at most
700000 sum N^-2 exp(-t/(8N²))<=2800000/sqrt(t),
since u exp(-u)<=1 gives each summand<=8/t and there are at most sqrt(t)/2 indices.
For N>sqrt(t)/2 use the image bound. With q=sqrt(t)/2 and floor(q)>=q/2, contribution at most
32A t sum_{N>q}N^-4 <=32A t/(3 floor(q)^3)
<= (2048A/3)/sqrt(t)=6144000000/sqrt(t).

Excluded ranges have total TV contribution at most P_0(max_{s<=t}S_s<2). Reflection after first hit of2 gives this probability=sum_{j=-2}^1 p_t(j), with only two values of the correct parity. Central-binomial induction gives max_j p_t(j)<=2/sqrt(t), so the contribution is <=4/sqrt(t). The two exceptional total masses are equal by reflection z->2-z, and half their sum is that probability. Therefore triple TV <=(6146800004)/sqrt(t)<10^10/sqrt(t).

This is an exact proof candidate, not numerical evidence. All external analytic identities need exact statements/hypothesis checks in integrated answer; no unresolved mathematical estimate identified.
