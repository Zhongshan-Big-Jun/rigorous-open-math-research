# Analytic prerequisites for a possible Q9 completion

These lemmas are exact. The polynomial inequality in jensen_algebra_task.md remains an independent open obligation; the present file alone does not settle Q9.

Assume the original domain, C2, C3, Q_quad>0, and t=sqrt(r)>=c/2. Introduce

X=tan B, z=tan g, L=sqrt(1+(1-t²)X²), w=sqrt(1+(1-t²)z²),
u=ct, h=mz, a=c(1+(c²+2)t²), b=t(1+2c²+c²t²),
J=(49/100)(1+c)², j=Jw²/(w+u)².

Here 0<t<c<1, X>z>0, L>w>1, u<1, h>z, and all denominators below are positive when used.

## 1. Sharp algebraic consequence of C3

For x=A+d in (0,pi), strict concavity of sine gives sin(cx)>c sin x. Thus C3 gives

sin(B-g)>c sin(A+d).

Writing both sides over sqrt((1+X²)(1+z²)) gives

X-z>ct(Xw+zL),

hence 1-uw>0 and X/z>(1+uL)/(1-uw). Using L²-1=(1-t²)X² and w²-1=(1-t²)z², squaring this positive inequality gives

(L²-1)(1-uw)²-(w²-1)(1+uL)²>0.

The left hand side factors as

(L+w)[(1+u²)(L-w)-2u(Lw-1)].

Put D=1+u²-2uw and N=(1+u²)w-2u. Since N>(1-u)²>0, the preceding inequality gives LD>N, so D>0 and L>N/D.

The first term of Q_quad equals P=(c-tL)/X. Its second term is strictly positive, so Q_quad>0 implies c-tL>0. Therefore

Pz < (c-tL)(1-uw)/(1+uL).

The function ell -> (c-t ell)/(1+u ell) has negative derivative -(t+uc)/(1+u ell)². Consequently, using L>N/D and D+uN=(1-u²)(1-uw),

0<Pz < (cD-tN)/(1-u²)=(a-bw)/(1-u²)=:f.

In particular 1<w<a/b. Note a-b=(c-t)(1-ct)²>0.

## 2. Explicit Jensen bound from C2

We have tan d=tz/w, H_m(g)=atan h, and H_m(d)=atan(th/w). Strict concavity of arctan on (0,infinity), with weights c/(1+c),1/(1+c), gives

c pi/[2(1+c)]
 = [c atan(th/w)+atan h]/(1+c)
 < atan( h(1+ct/w)/(1+c) ).

The weights are positive and sum to one. The two arctan inputs differ because t/w<1. Since c>=2/3, c/[2(1+c)]>=1/5. Thus

h > (1+c)/(1+ct/w) tan(pi/5) > (7/10)(1+c)w/(w+ct),

and h²>j.

For completeness, tan(pi/5)>7/10 follows without a numerical approximation to pi. Set theta=atan(7/10) in (0,pi/4). The five-angle formulas give sin(5theta)>0 and cos(5theta)<0: their numerators after division by cos(theta)^5 are respectively

5(7/10)-10(7/10)^3+(7/10)^5 = 23807/100000>0,
1-10(7/10)^2+5(7/10)^4 = -5399/2000<0.

Since 0<5theta<5pi/4, these signs force pi/2<5theta<pi. Hence theta<pi/5, which proves the bound by monotonicity of tan.

## 3. Exact reduction to the polynomial certificate

Direct substitution into the given definition of Q_quad yields

Q_quad z = Pz - c(1-t²)²(h²-z²)/[1+uw+h²(1+ut²/w)].

Also z²=(w²-1)/(1-t²). Define

K(x)=c(1-t²)²(x-z²)/[1+uw+x(1+ut²/w)].

For x>=0 the denominator is positive and

K'(x)=c(1-t²)²[1+uw+z²(1+ut²/w)]/[1+uw+x(1+ut²/w)]²>0.

Thus h²>j implies K(h²)>K(j). If the polynomial

E = c(1-t²)(1-u²)[(1-t²)Jw²-(w²-1)(w+u)²]
    -(a-bw)[(1+uw)(w+u)²+Jw(w+ut²)]

is nonnegative on 2/3<=c<1, c/2<=t<c, 1<=w<=a/b, then multiplying by the positive denominators shows K(j)>=f. This would give

Q_quad z < f-K(h²) < f-K(j)<=0,

contradicting Q_quad>0. Therefore that exact polynomial inequality, if proved, excludes all remaining t>=c/2 cases. The small-r theorem then proves Q9 on the whole original domain.
