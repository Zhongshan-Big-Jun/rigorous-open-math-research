# Small-interval derivative estimate (root candidate O3-S)

For t>=32, define B_t(w)=cos(w)^t on |w|<=pi/2 and 0 outside that single interval. For L=r-l>0 and l<=a,z<=r let
H(l,r,a,z)=(4/L) sum_{j>=1} sin(pi*j*(a-l)/L) sin(pi*j*(z-l)/L) B_t(pi*j/L).
The sum is locally finite, and cutoff crossings are C^3 since t>=32.

Claim: when 0<L<=sqrt(t),
|d_a d_l d_r H| <= 603000 L^(-4) exp(-t/(2L^2)).

Proof. Put q=pi*j, u=a-l, v=z-l, U=u/L, V=v/L, w=q/L, s=t*w^2. After d_a, the summand is F=4q L^(-2) A B with A=cos(qU)sin(qV), B=B_t(w). At fixed a,z, d_r=d_L and d_l=-d_L-d_u-d_v, hence |d_l d_r F|<=|F_LL|+|F_uL|+|F_vL|.
For an active summand 0<w<pi/2, write E=exp(-s/4). Since sin(w)<=w and cos(w)<=exp(-w^2/2), and t>=4,
|B|<=E, |B_L|<=L^(-1)sE, |B_LL|<=L^(-2)(3s+s^2)E.
The endpoint/cutoff values follow by continuity. Also
|A|<=1; |A_L|<=2q/L; |A_LL|<=(4q^2+4q)/L^2;
|A_u|,|A_v|<=q/L; |A_uL|,|A_vL|<=(q+2q^2)/L^2.
Product differentiation gives
|F_LL|<=4q L^(-4)[6+12q+4q^2+(7+4q)s+s^2]E,
|F_uL|,|F_vL|<=4q L^(-4)[3q+2q^2+qs]E.
Since q>=pi>1, their sum is at most
4q^3 L^(-4)(32+13s+s^2)exp(-s/4)
<=1568 q^3 L^(-4) exp(-s/8).
Here x exp(-x/8)<=8 and x^2 exp(-x/8)<=256 for x>=0, so (32+13x+x^2)exp(-x/8)<=392.

Set alpha=t/L^2>=1. Since pi^2/8>1 and alpha*j^2>=(alpha+j^2)/2,
sum_{j>=1}q^3 exp(-alpha*q^2/8)
<=pi^3 exp(-alpha/2) sum_{j>=1} j^3 exp(-j^2/2).
For each j, compare with the integral on [j-1,j] of (x+1)^3 exp(-x^2/2); therefore this sum is at most
integral_0^infty (x+1)^3 exp(-x^2/2) dx
=5+4 integral_0^infty exp(-x^2/2) dx<13.
A sharper elementary bound integral<3/2 gives <11, or use the exact Gaussian integral sqrt(pi/2)<3/2. Taking the safe bound12 (from exact Gaussian integral), and pi^3<32, gives 1568*32*12=602112<603000. This proves the claim. The Gaussian integral identity used here must be stated exactly, or replace 603000 by 700000 using only integral<2 and sum<13.

For final assembly prefer 700000: then 1568*32*13=652288<700000, and integral<2 follows by splitting [0,1] and using exp(-x^2/2)<=x exp(-x^2/2) for x>=1. No Gaussian integral identity is needed.
