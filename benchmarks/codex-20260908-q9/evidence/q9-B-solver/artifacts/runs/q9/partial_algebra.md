# Exact algebraic partial theorem (candidate pending independent audit)

On the stated domain, even without C1--C3, Q_quad > 0 implies

sin(B)^2 < (c^2-r)/(c^2-r^2).

Proof: the subtracted second term in Q_quad is strictly positive, so c cos B > sqrt(r) cos A. Both sides are positive. Squaring and using cos² A=1-r sin² B gives c²-r>(c²-r²) sin² B. Here c²-r²>0 because 0<r<c²<1.

Consequently Q9 holds on the exact constrained subdomain

k(1-c²)r <= c²-r².                                          (P)

Indeed, k e r sin² B < (c²-r) k e r/(c²-r²) <= c²-r, so the supplied strict bound T_quad<r sin² B proves Q9. This is not a proof of Q9 globally; (P) is an additional restricted-domain condition. It converts Q positivity to the sufficient condition using a B-independent algebraic range.

In particular, (P) holds for every 1<m<=sqrt(2), because k<=1 and
c²-r²-e r=(c²-r)(1+r)>0.

# Nonempty exact branch

Fix any m>1 and use t=sqrt(r) as a parameter. Set A=asin(t sin B), d=asin(t sin g). Extend these smoothly to t around 0; for the implicit-function argument extend H_m(z)=atan(m tan z) to negative z near 0 as well. Only positive-t solutions are used in the original problem. At

t=0, c0=2/3, B0=g0=b=atan(sqrt(3)/m),

all three constraint residuals vanish. Their derivatives with respect to (B,g,c), with h=H_m'(b)=(m²+3)/(4m)>0, are

J = [[h,0,pi], [0,3h/2,-3pi/4], [1,-1,0]].

Its determinant is -9 pi h/4, nonzero. The real smooth implicit function theorem gives a unique local smooth (B(t),g(t),c(t)). Differentiating the constraints gives

h B'+pi c'=(2/3)m sin b,
h g'-(pi/2)c'=-(2/3)m sin b,
B'-g'=(4/3)sin b.

Therefore c'(0)=8(m-h)sin b/(9pi)>0, since m-h=3(m²-1)/(4m)>0. For sufficiently small t>0, c(t)>2/3 and c(t)<1; B,g remain acute and positive, r=t²<c², and C3 gives B>g. Then A,d>0 and all exact domain constraints hold.

At t=0, the continuous extension of Q_quad is

Q0 = c0 cos b/[sin b(1+k sin² b)]>0.

Hence Q_quad>0 for sufficiently small t>0. Also (P) is strict near t=0. Thus the partial subdomain contains exact admissible tuples with Q>0 for every fixed m>1, including the claimed interval 1<m<=sqrt2.

External theorem: smooth implicit function theorem: for a C¹ map E(t,x) from an open neighborhood in R x R^3 to R^3, E(0,x0)=0 and invertible D_x E(0,x0) imply a unique local C¹ x(t) with E(t,x(t))=0. Here arcsin arguments are near zero, B,g near b in (0,pi/2), c near 2/3, so the residual map is smooth on an open neighborhood. The theorem's hypotheses are all checked above.
