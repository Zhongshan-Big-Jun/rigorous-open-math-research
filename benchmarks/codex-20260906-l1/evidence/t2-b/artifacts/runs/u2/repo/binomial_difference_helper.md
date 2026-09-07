# Exact third-difference helper (root)

For p_n(v)=2^{-n} binom(n,(n+v)/2) when v is an integer of the correct parity with |v|<=n, and p_n(v)=0 otherwise, the following holds for every integer t>=3 and integer w with w congruent to t+3 modulo 2:

|p_t(w-3)-3p_t(w-1)+3p_t(w+1)-p_t(w+3)|
<= 2048 t^{-2} exp(-w^2/(16t)).

This also proves the requested weaker constant 10000. All assertions below are elementary and proved here.

## Local Gaussian estimate

For every integer N>=1 and allowed integer w,

p_N(w) <= 2 N^{-1/2} exp(-w^2/(4N)).

Proof. Set b_n=4^{-n} binom(2n,n). Induction gives b_n<=1/sqrt(n+1) for n>=0: b_0=1, b_{n+1}/b_n=(2n+1)/(2n+2), and

(2n+1)^2(n+2) <= 4(n+1)^3

because the right side minus the left is 3n+2. Thus the central mass of p_N is at most sqrt(2/N). For odd N=2n+1 the central mass equals b_{n+1}, so the same bound holds. Put w0=0 for even N and w0=1 for odd N. By symmetry we may suppose w>=w0. The successive ratios are

p_N(v+2)/p_N(v)=(N-v)/(N+v+2).

For v<N this ratio is (1-u)/(1+u), u=(v+1)/(N+1) in [0,1). The inequality log((1-u)/(1+u))<=-2u follows by differentiation and equality at u=0. Multiplying the ratios yields

p_N(w) <= sqrt(2/N) exp(-(w^2-w0^2)/(2(N+1))).

Since 2(N+1)<=4N, w0^2<=1, and exp(1/(2(N+1)))<=exp(1/4)<=4/3, the claimed bound follows from (4/3)sqrt(2)<2. Here exp(1/4)<=4/3 follows by comparing the exponential power series termwise with the geometric series. For |w|>N the claim is immediate because p_N(w)=0.

## Exact discrete identity

Write N=t+3. For |w|<=N with the allowed parity,

D3 p_t(w) = 8 p_N(w) [w^3-(3N-2)w]/[N(N-1)(N-2)],

where D3 is the displayed third difference. To prove this, let xi_1,...,xi_N be independent uniform signs and S their sum. Multiplying the generating functions, or conditioning on the last three signs, gives

D3 p_t(w)=8 p_N(w) E[xi_1 xi_2 xi_3 | S=w].

The conditional sign vector is exchangeable, and the pointwise identity

S^3 = (3N-2)S + sum_{i,j,k all distinct} xi_i xi_j xi_k

gives the formula. This is valid at the support endpoints as well. For |w|>N both sides are zero, so no conditional expectation on a null event is needed.

## Uniform bound

For t>=3, N>=6, N<=2t, and N(N-1)(N-2)>=N^3/2. Put u=|w|/sqrt(N). The preceding results give

|D3 p_t(w)| <= 32 N^{-2}(u^3+3u) exp(-u^2/4).

For u>=0, differentiation shows that u^3 exp(-u^2/8) attains its maximum at sqrt(12), and u exp(-u^2/8) at 2. Consequently

(u^3+3u) exp(-u^2/8) <= 12 sqrt(12)+6 <54.

Therefore |D3 p_t(w)| <=1728 N^{-2} exp(-w^2/(8N))
<=2048 t^{-2} exp(-w^2/(16t)), as asserted.

Parity audit: all four p_t arguments have parity t exactly when w has parity t+3. The support boundaries are covered by the combinatorial identity. No numerical check is used as proof, and no external theorem is assumed.
