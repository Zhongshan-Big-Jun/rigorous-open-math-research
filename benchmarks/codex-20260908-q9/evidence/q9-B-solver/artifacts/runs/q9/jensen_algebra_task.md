# Algebra target for Q9 completion route

Let 2/3<=c<1, c/2<=t<c, u=ct,

a=c(1+(c²+2)t²), b=t(1+2c²+c²t²),
J=(49/100)(1+c)²,
1<=w<=a/b.

Prove the following polynomial is nonnegative (ideally strictly positive):

E = c(1-t²)(1-u²)[(1-t²)J w²-(w²-1)(w+u)²]
    -(a-bw)[(1+uw)(w+u)²+Jw(w+u t²)].

No transcendental functions occur. Note a-b=(c-t)(1-ct)²>0, so the w interval is nonempty. At c=t=1 (excluded) degeneracy occurs. Numerical testing of 200000 random points survived, evidence only.

Origin (parent will prove prerequisites): with z=tan g, w=sqrt(1+(1-t²)z²), h=m tan g, C3 + Q>0 give Q z < f-c(1-t²)²(h²-z²)/(1+uw+h²(1+ut²/w)), f=(a-bw)/(1-u²)>0. Jensen+C2 gives h²>J w²/(w+u)². E>=0 contradicts Q>0. This closes remaining t>=c/2 region. Deliver exact algebraic proof/certificate (Bernstein rational coefficients acceptable), or precise failure.
