# Unconditional small-r theorem (candidate pending independent audit)

For every tuple in the problem domain satisfying C2 and C3, if 0<r<=c²/4, then

c²-r > k e r sin²B,

so R_quad>0, regardless of the sign of Q_quad. C1 is not needed for this lemma; every tuple satisfying all three constraints is included.

Proof. Put t=sqrt(r), s=sin g, p=sin B, and e=1-c². Since H(g)=c(pi/2-H(d)), strict convexity of tan on [0,pi/2) gives

m tan g = tan(c(pi/2-H(d))) < c tan(pi/2-H(d)) = c/(m tan d).

The arguments are positive, 0<c<1, and tan(0)=0, so this use of strict convexity is valid. As tan d=t s/cos d, the inequality is

m² t s² < c cos g cos d < c.

Hence k s² < c/t. All factors are positive.

The concavity of sin on [0,pi/2] implies sin(tz)>=t sin z for 0<t<1 and z in (0,pi/2). Monotonicity of arcsin then gives asin(t sin z)<=tz. Thus C3 gives

B-g=c(A+d)<=ct(B+g),

and B/g <= (1+ct)/(1-ct). The function sin z/z strictly decreases on (0,pi/2), because its derivative has numerator z cos z-sin z<0 (the negative of a function with positive derivative z sin z and value zero at 0). Therefore

p/s < B/g <= (1+ct)/(1-ct).

Combining,

k e t² p² < e c t ((1+ct)/(1-ct))².

For 0<t<=c/2 the function t ((1+ct)/(1-ct))² is increasing, since each positive factor is increasing. Consequently

k e r p² < e c²/2 ((1+c²/2)/(1-c²/2))².

For x=c² in (0,1),

3(2-x)²-2(1-x)(2+x)² = (3x-2)²+2x³ >0.

Dividing by 4(2-x)²>0 proves

(1-x)/2 ((2+x)/(2-x))² <3/4.

Thus k e r p² <3c²/4 <=c²-r, as required.

This goes beyond the supplied starting facts by deriving their sufficient condition from the parameter-only range r<=c²/4 and the exact constraints C2,C3, uniformly for all m>1. The new sufficient range r<=c²/4 does not impose the m-dependent restriction (P), and its conclusion does not assume Q>0.
