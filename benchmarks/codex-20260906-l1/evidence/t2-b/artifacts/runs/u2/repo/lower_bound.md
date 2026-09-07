# Exact lower bound (root)

For every integer t>=1, TV(P_t^x,P_t^y) >= 1/(2 sqrt(t)).

Let S_t be the sum of t independent fair signs. The two base endpoints have laws S_t and 2+S_t. Take A={(eta,z):z<=0}. Then

P_t^x(A)-P_t^y(A)=P(-2<S_t<=0)=a_t,

a_t=2^{-t} binom(t,floor(t/2)). For even t the unique attainable site in (-2,0] is 0; for odd t it is -1. Lamps play no role in this event.

Put b_n=4^{-n} binom(2n,n), n>=1. We claim b_n>=1/(2 sqrt(n)). It holds at n=1. The recurrence b_{n+1}/b_n=(2n+1)/(2n+2) and

((2n+1)/(2n+2))^2 >= n/(n+1)

prove the induction, since (2n+1)^2-4n(n+1)=1. Thus for t=2n, a_t=b_n>=1/(2 sqrt(n))>=1/(2 sqrt(t)). For t=2n+1 with n>=1,

a_t=((2n+1)/(2n+2))b_n >= 3/(8 sqrt(n)) >=1/(2 sqrt(2n+1)),

where the last squared inequality is 9(2n+1)>=16n. For t=1, a_1=1/2. This proves the claim with c=1/2 and t0=1 independently of any upper bound. No external theorem beyond counting the independent sign choices is used. At t=0 the two deterministic initial states have TV=1; the asserted asymptotic formula is not evaluated there.
