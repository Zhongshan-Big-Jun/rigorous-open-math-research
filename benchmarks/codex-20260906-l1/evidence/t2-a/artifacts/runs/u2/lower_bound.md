# Exact lower bound (O2)

Let S_t be the sum of t independent fair signs and p_t(k)=P(S_t=k). Under the two chains the base marginals are S_t and S_t+2. For even t use the event that the base is at most 0; for odd t use the event that the base is at most 1. In either case the difference of event probabilities is p_t(r), where r=0 for even t and r=1 for odd t. This explicitly handles the common parity class; the two starts differ by 2, so their base supports do not have opposite parity.

Put b_n=binom(2n,n)/4^n. For n>=1,

b_n >= 1/(2 sqrt(n)).

Indeed b_1=1/2 and b_{n+1}/b_n=(2n+1)/(2n+2)>=sqrt(n/(n+1)), because (2n+1)^2-4n(n+1)=1. Induction proves the bound. For t=2n>=2, p_t(0)=b_n>=1/(4 sqrt(t)). For t=2n+1>=3,
p_t(1)=((2n+1)/(2n+2))b_n>=1/(4 sqrt(n))>=1/(4 sqrt(t)). At t=1, p_1(1)=1/2>=1/4. Consequently

TV(P_t^x,P_t^y) >= 1/(4 sqrt(t)) for every integer t>=1.

All ingredients follow by binomial counting and the displayed induction; no external theorem is used. Passing to the base marginal is justified by using the preimage of its half-line event in the full chain state space.
