# Analytic work: proved lemmas and current gap

All claims below are on the domain of the task, with `s=sqrt(r)`, `e=1-c^2`, and `h=1-r`.

## Proved unconditional subdomain (all m)

If C2 and C3 hold and

\[
 c^2-s^2\ge (1-c^2)c s\left(\frac{1+cs}{1-cs}\right)^2,\tag{P}
\]
then the supplied sufficient inequality `c^2-r>k e r sin(B)^2` holds strictly. Consequently `R_quad>0`, irrespective of Q's sign. In particular this is true whenever `0<r<=1/9` and `2/3<c<1`.

Proof: C2 says `H(g)=c(pi/2-H(d))`. Strict convexity of tangent, with `0<c<1`, gives

\[
 m^2\tan g\tan d<c.
\]
Since `tan d=s sin(g)/cos(d)`, this is

\[
 m^2r\sin^2g<c s\cos g\cos d<c s.
\]
For `0<s<1`, the function `asin(s sin z)` has derivative `s cos z/sqrt(1-s^2 sin^2z)<s` for `0<z<pi/2`, and vanishes at zero. Thus `A<sB`, `d<sg`. C3 gives

\[
 \frac B g<\frac{1+cs}{1-cs}.
\]
The function `sin z/z` strictly decreases on `(0,pi/2)`, so `sin B/sin g<B/g`. Therefore

\[
 k e r\sin^2B<m^2 e r\sin^2B
 <e c s\left(\frac{1+cs}{1-cs}\right)^2.
\]
This proves the first assertion.

To prove the uniform corollary define

\[
 G(c,s)=\frac{(1-c^2)c s}{c^2-s^2}
       \left(\frac{1+cs}{1-cs}\right)^2.
\]
For fixed `c`, this is strictly increasing in `s`. For `c>=2/3`, `0<s<=1/3`,

\[
 \partial_c\log G=
 \frac{1-3c^2}{c(1-c^2)}-\frac{2c}{c^2-s^2}
 +\frac{4s}{1-c^2s^2}<0.
\]
Indeed the first summand is negative, the second is less than `-2`, and the third is at most `3/2`. Therefore

\[
 G(c,s)\le G(2/3,1/3)=\frac{1210}{1323}<1.
\]
This proves (P) strictly on that subdomain. This goes beyond the supplied fact by proving a parameter-only sufficient condition independent of m, directly from C2 and C3.

A somewhat larger uniform constant is possible. For `s<=sqrt(2)-1`, the same derivative argument works because `4s/(1-s^2)<=2`. The maximal uniform s obtained this way is the unique positive root in `(1/3,sqrt(2)-1)` of

\[
108-234s-315s^2+284s^3-108s^4=0.
\]
No explicit numerical value is needed for the simple `r<=1/9` theorem.

## Proved geometric cotangent bound

C3 and strict concavity of sine on `[0,pi]` give

\[
\sin(B-g)=\sin(c(A+d))>c\sin(A+d),
\]
so

\[
 \cot B+c r\cot A<\cot g-c r\cot d.\tag{G}
\]
All divisions are by positive sines. Here `A+d<pi` and `0<c<1`, which are sufficient to apply sine's strict concavity between zero and `A+d`.

Put `x=cot g`, `M=sqrt(x^2+h)` and `L=x-cs M`. Since `r cot A=s sqrt(cot(B)^2+h)`, (G) states

\[
 v+cs\sqrt{v^2+h}<L,\quad v=\cot B.
\]
The left side is strictly increasing in `v>=0`; if `L>cs sqrt h`, its nonnegative root is

\[
 v_* =\frac{L-cs\sqrt{L^2+(1-c^2r)h}}{1-c^2r},
\]
so `v<v_*` and

\[
 Q_1=c\cot B-r\cot A<c v_*-s\sqrt{v_*^2+h}.
\]
If the root is nonpositive, no admissible positive v satisfies (G).

The subtracted term in Q is

\[
 Q_2=\frac{c k h^2 x M}{M(1+x^2+k)+csx(1+x^2+kr)}.
\]
Thus `Q<=0` would follow from showing the displayed envelope for Q1 is at most Q2.

## Proved elementary consequence of C2

Let `w=m tan g`. Then `tan d/tan g=s cosg/cosd<s`. C2 implies

\[
 H(g)+H(d)=c\pi/2+(1-c)H(d)>c\pi/2.
\]
Consequently

\[
 \arctan w+\arctan(sw)>c\pi/2.
\]
Also, since tangent is convex and vanishes at zero,

\[
\tan((1-c)\pi/2)\le \sqrt3(1-c),\quad c\ge2/3.
\]
It follows that

\[
 s w^2+\sqrt3(1-c)(1+s)w>1.\tag{L}
\]
Proof of the last implication: it is immediate if `s w^2>=1`; otherwise the tangent addition formula and `tan(c pi/2)>=1/[sqrt3(1-c)]` give it.

## Numerical evidence / exact remaining analytic gap

Scans in `analytic_c2_rational_scan.py` (not proof) suggest that C3 together with (L), `m>1`, `2/3<c<1`, and `1/3<=s<c` already forces `Q<=0`. A proof of this purely algebraic/geometric assertion would combine with the unconditional `r<=1/9` theorem to prove all Q9. Neither that assertion nor the corresponding exact cotangent envelope inequality is proved here.

## Final audited C2 rational bound (proved)

For `0<s<1`, `c>2/3`, `m>0`, `0<g<pi/2`, `d=asin(s sin g)`, impose C2. Then

\[
 m^2\tan^2g>\ell(s):=\frac{3+2s}{1+6s+3s^2}.\tag{C2-L}
\]

Proof: put `w=m tan g`, `alpha=atan w=H_m(g)`, and `beta=atan(sw)`. Since `cos g<cos d`,

\[
 m\tan d=s\frac{\cos g}{\cos d}w<sw,
\]
so `H_m(d)<beta`. C2 and `c>2/3` give

\[
 \frac32\alpha+H_m(d)>\frac\alpha c+H_m(d)=\frac\pi2,
\]
therefore `theta(w):=3 atan w+2 atan(sw)>pi`.

Write `X=w^2`, `D_s=1+6s+3s^2`, `N_s=3+2s`. By the sine addition and triple-angle formulas,

\[
 \sin\theta(w)=
 \frac{w\,[s^2X^2-D_sX+N_s]}
 {(1+X)^{3/2}(1+s^2X)}.
\]
The polynomial has two distinct positive roots because its coefficients have signs `+,-,+` and

\[
 D_s^2-4s^2N_s=1+12s+30s^2+28s^3+9s^4>0.
\]
The function `theta(w)` is strictly increasing from zero to `5pi/2` as `w` increases from zero to infinity. Its two positive sine zeros consequently occur at `theta=pi` and `theta=2pi`, in that order. Hence `theta(w)>pi` implies that `X` is strictly larger than the smaller polynomial root, which is

\[
 X_- =\frac{2N_s}{D_s+\sqrt{D_s^2-4s^2N_s}}
      >\frac{N_s}{D_s}=\ell(s).
\]
This proves (C2-L) without squaring an unoriented constraint.

## Final audited envelope reduction (proved)

Set `t=s`, `h=1-t^2`, `x=cot g>0`, `M=sqrt(x^2+h)`, and `a=ct<1`. The cotangent inequality (G) reads

\[
 b+a\sqrt{b^2+h}<K:=x-aM,
 \qquad b=\cot B>0.
\]
Thus `K>a sqrt(h)`, and the unique positive solution of the corresponding equality is

\[
 b_* =\frac{(1+a^2)x-2aM}{1-a^2}>0.
\]
To check the formula directly, use

\[
 \sqrt{K^2+(1-a^2)h}=M-ax>0.
\]
Furthermore

\[
 \sqrt{b_*^2+h}=
 \frac{(1+a^2)M-2ax}{1-a^2}>0.
\]
The function `b -> c b-t sqrt(b^2+h)` is strictly increasing because its derivative is greater than `c-t>0`. Hence, putting

\[
 P=\frac{c(1+c^2t^2+2t^2)}{1-c^2t^2},\qquad
 D=\frac{t(1+2c^2+c^2t^2)}{1-c^2t^2},\qquad
 v=M/x=\sqrt{1+h\tan^2g}>1,
\]
we get the strict bound

\[
 Q_1<c b_*-t\sqrt{b_*^2+h}=x(P-Dv).
\]
In particular `Q>0` implies `1<v<P/D`; also

\[
 P-D=\frac{(c-t)(1-ct)}{1+ct}>0.
\]

Put `L=ell(t)` and `W=1+Lh`. By (C2-L), `k>Lx^2-1`. If a proved algebraic lemma gives `(P/D)^2<W`, then on the Q-positive locus `v^2<W`, so the lower bound `Lx^2-1` is positive. The subtracted expression Q2 is strictly increasing in k, since it has the form `k E/(D0+k D1)` with all `E,D0,D1>0`. At `k=Lx^2-1`, direct cancellation gives

\[
 \frac{Q_2}{x}>
 \frac{c h v(W-v^2)}{v(1+L)+ct(v^2+t^2L)}.
\]
Thus the cubic

\[
 N(v)=c h v(W-v^2)
       -(P-Dv)[v(1+L)+ct(v^2+t^2L)]
\]
being nonnegative on `[1,P/D]` contradicts `Q>0`. There is no circularity in recovering the auxiliary inequality from the cubic: if `N(P/D)>0`, its definition immediately gives `W>(P/D)^2`, since the second term then vanishes and all other factors are positive.

The root agent has reported exact rational Bernstein certificates for the requisite polynomial inequalities; these certificates are not independently reproduced in this notes file. The derivative argument that uses them is valid as follows. Write `N(v)=a3 v^3+a2 v^2+a1 v+a0`. If `a2>0`, `N'(1)>0`, and `N'(P/D)>0`, then `N'>0` on `[1,P/D]`: for `a3>=0`, `N''(v)=6a3 v+2a2>0`; for `a3<0`, `N'` is a concave quadratic and is at least the minimum of its endpoint values. Combining this with `N(1)>=0` gives `N(v)>0` for `v>1`, and in particular at `v=P/D>1`.
