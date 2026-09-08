# Total-variation asymptotics for the specified switch-walk-switch chain

**Theorem.** For the chain in the question, with both initial lamp configurations all zero, the explicit constants
\[
c=\frac{1}{2\sqrt2},\qquad C=2^{43},\qquad t_0=16
\]
satisfy, for every integer \(t\ge t_0\),
\[
\frac{c}{\sqrt t}\le
\|P_t^{(0,0)}-P_t^{(0,2)}\|_{\mathrm{TV}}
\le\frac{C}{\sqrt t}.
\]
This is a proof; no conjecture or numerical evidence is used. All random-walk formulas and estimates used below are derived. No external probability theorem is invoked. For differentiation and integration we use the elementary fundamental theorem of calculus in the form \(f(v)-f(u)=\int_u^v f'(r)\,dr\) for continuously differentiable \(f\); the required differentiability of the interpolation used below is explicitly checked.

## 1. Lower bound

Write \(p_t(k)=\mathbb P(S_t=k\mid S_0=0)\). If \(t=2n\ge2\), the event that the final base position is at most 0 has probability difference
\[
\mathbb P_0(S_t\le0)-\mathbb P_2(S_t\le0)=p_t(0)=b_n,
\qquad b_n=4^{-n}\binom{2n}{n}.
\]
If \(t=2n+1\ge3\), the event that the final base position is at most 1 has probability difference
\[
\mathbb P_0(S_t\le1)-\mathbb P_2(S_t\le1)=p_t(1)=\frac{2n+1}{2n+2}b_n.
\]
Here the two distributions have the same parity, since their starting points differ by 2. Each indicated difference isolates exactly one point in that parity class.

For \(n\ge1\), \(b_n\ge1/(2\sqrt n)\). This follows by induction from \(b_1=1/2\) and
\[
\frac{b_{n+1}}{b_n}=\frac{2n+1}{2n+2}\ge\sqrt{\frac n{n+1}},
\]
where squaring reduces the inequality to \((2n+1)^2\ge4n(n+1)\). Thus, in both parity cases and for every \(t\ge2\),
\[
\|P_t^x-P_t^y\|_{\rm TV}\ge\frac1{2\sqrt{2t}}.
\]
This is a lower bound for the full state because the half-line event depends only on its base coordinate. At \(t=1\) the same method gives \(1/2\), and at \(t=0\) the total variation is 1.


## 2. Reduction to the range triple and exceptional ranges

Let \(S\) be simple symmetric random walk, put \(m_t=\min_{0\le j\le t}S_j\) and \(M_t=\max_{0\le j\le t}S_j\), and let \(Q_s\) be the law of
\((m_t,M_t,S_t)\) when \(S_0=s\), for \(s=0,2\). For every \(t\ge1\), conditional
on the whole base path, the lamps on \([m_t,M_t]\cap\mathbb Z\) are independent
fair bits, and all other lamps are zero. Indeed every visited site is resampled,
including the departure site at the first step, and the last resampling coins
at different sites are distinct independent coins. Their indices are determined by the base path, which is independent of all resampling coins. The conditional law only
depends on the range triple. Thus both lamplighter laws are obtained from
\(Q_0,Q_2\) by the same probability kernel, and

\[
\|P_t^{(0,0)}-P_t^{(0,2)}\|_{\rm TV}
\le\tfrac12\sum_{a,b,z}|Q_0(a,b,z)-Q_2(a,b,z)|.                 \tag{1}
\]

This inequality follows directly by the triangle inequality after summing the
common kernel; no coupling or independence after unproved conditioning is used.
It accounts for both initially zero lamps at sites 0 and 2: unvisited sites remain deterministically zero, while visited sites are fair. In particular, the initial zero at the starting site is overwritten before the first move, and the initial zero at the other site is retained until that site is visited. The arrival switch also covers a site first visited at the final time.

All endpoints have parity \(z\equiv t\pmod2\), since both starts are even.
Intervals not containing \([0,2]\) contribute at most
\(2\Pr_0(M_t<2)\) to the sum in (1). To compute this probability, reflect every increment after the first visit to 2. This is a probability-preserving bijection between paths that hit 2 and end below 2 and paths that end above 2. Therefore \(\Pr_0(M_t<2)=\Pr_0(S_t\le1)-\Pr_0(S_t\ge3)\). Symmetry and parity give

\[
\Pr_0(M_t<2)=
\begin{cases}
p_t(0)+p_t(2),&t\text{ even},\\
2p_t(1),&t\text{ odd},
\end{cases}                                                  \tag{2}
\]

where \(p_t(u)=\Pr_0(S_t=u)\). The kernel estimate proved below implies this is
at most \(4/\sqrt t\). The exceptional contribution to the full l1 sum is
therefore at most \(8/\sqrt t\).

For all remaining intervals write \(L=b-a\ge2\), \(a\le0\), \(b\ge2\),
\(a\le z\le b\). There are \(L-1\le L\) choices for \(a\), and at most
\(L+1\le2L\) choices for \(z\), so at most \(2L^2\) triples at each length.

## 3. Elementary one-dimensional estimates

For \(n\ge1\) and every integer \(u\),

\[
p_n(u)\le {2\over\sqrt n}\exp[-u^2/(4n)].                    \tag{3}
\]

For a proof, the central even mass obeys
\(p_{2m}(0)=\prod_{i=1}^m(2i-1)/(2i)\le(m+1)^{-1/2}\).
Induction proves this, since
\(((2m+1)/(2m+2))^2\le(m+1)/(m+2)\).
For \(u=2j\ge0\), the ratio to the central mass is
\(\prod_{i=1}^j(m-i+1)/(m+i)\). Using
\(\log(1-v)\le-v\) and \(m+i\le2m=n\), its logarithm is at most
\(-j^2/n=-u^2/(4n)\).
For odd \(n=2m+1\), the central mass at 1 is at most \((m+1)^{-1/2}\).
The corresponding ratio at \(u=2j+1\) has logarithm at most
\(-j(j+1)/n=-(u^2-1)/(4n)\).
Symmetry handles negative \(u\), while wrong parity and \(|u|>n\) give zero.
The prefactor is at most \(\sqrt2 e^{1/4}/\sqrt n<2/\sqrt n\);
one may check the last inequality from \(e^{1/4}\le4/3\).

Write \(D_h f(u)=f(u)-f(u-h)\), and write \(\Delta=D_2\). For \(t\ge3\),

\[
|\Delta^3p_t(u)|\le {4096\over t^2}\exp[-u^2/(32t)]
\qquad(u\in\mathbb Z).                                      \tag{4}
\]

Here is a direct verification. Put \(n=t+3\) and \(v=u-3\). The binomial
formula, with binomial coefficients outside their range interpreted as zero,
gives the exact identity

\[
\Delta^3p_t(u)=
-{8\{v^3-(3n-2)v\}\over n(n-1)(n-2)}p_n(v).                  \tag{5}
\]

For an explicit algebraic check, when the parity is correct put \(k=(n+v)/2=(t+u)/2\). Multiplication of the four binomial terms by the common denominator \(n(n-1)(n-2)\) leaves
\[
(n-k)(n-k-1)(n-k-2)-3k(n-k)(n-k-1)
+3k(k-1)(n-k)-k(k-1)(k-2)
=-\{v^3-(3n-2)v\}.
\]
The factor 8 comes from \(2^{-t}=8\,2^{-n}\). This also proves the identity at support endpoints by the convention of zero binomial coefficients. Outside \(0\le k\le n\), all four terms vanish; wrong parity likewise makes both sides zero. Since \(n\ge6\), the denominator is at least \(n^3/2\).
By (3), the absolute value in (5) is at most

\[
32n^{-2}(r^3+3r)e^{-r^2/4},\qquad r=|v|/\sqrt n.
\]

Differentiating \(r^3e^{-r^2/8}\) and \(3re^{-r^2/8}\) shows their suprema
are at most 48 and 6, respectively. Thus their sum is at most 64.
Finally \((u-3)^2\ge u^2/2-9\), \(n\le2t\), and
\(e^{9/(8n)}<2\), proving (4).

We will also use the elementary bounds

\[
\sum_{j\ge1}j^5e^{-j^2/4}<2^{11},\qquad
\sum_{j\ge1}j^2e^{-j^2/64}<2^{12},\qquad
\sum_{j\ge1}j^2e^{-j^2/(64t)}<2^{12}t^{3/2}\quad(t\ge1).     \tag{6}
\]

For the first, the sum is at most
\(\int_0^\infty(x+1)^5e^{-x^2/4}\,dx\).
Using \((x+1)^5\le16(x^5+1)\),
\(\int_0^\infty x^5e^{-x^2/4}dx=64\), and
\(\int_0^\infty e^{-x^2/4}dx<5\), gives an upper bound 1104.
The last integral bound follows by splitting at 1 and using \(x^2\ge x\)
on \([1,\infty)\). For the other estimates, compare the sum to
\(\int_0^\infty(x+1)^2e^{-x^2/(64t)}dx\), use
\((x+1)^2\le2(x^2+1)\), and substitute \(x=8\sqrt t\,y\).
The elementary estimates
\(\int_0^\infty e^{-y^2}dy<2\) and
\(\int_0^\infty y^2e^{-y^2}dy<3\)
follow by splitting at 1: the respective bounds are \(1+e^{-1}<2\) and \(1/3+5/e<3\), using \(e>2\).
The resulting bound is \(3072t^{3/2}+32\sqrt t\le3104t^{3/2}<2^{12}t^{3/2}\).

## 4. Large ranges: reflected images

For an interval \([a,b]\), let \(K_t^{a,b}(s,z)\) be the probability that
the walk started at \(s\) stays in \([a,b]\) through time \(t\) and ends at \(z\).
For \(N=b-a+2\), the exact image formula is

\[
K_t^{a,b}(s,z)=\sum_{k\in\mathbb Z}
\big[p_t(z-s+2kN)-p_t(z+s-2a+2+2kN)\big].                  \tag{7}
\]

For integer arguments the sum is finite. To prove it, check the nearest-neighbor
recurrence in \(z\), its zero values at \(z=a-1,b+1\) by pairing image terms,
and its value \(\mathbf1_{s=z}\) at time zero for interior \(s,z\).
These conditions uniquely determine the killed probabilities by induction in
time. More explicitly, in coordinates \(x=s-a+1\), \(y=z-a+1\), the two initial image arguments are \(y-x+2kN\) and \(y+x+2kN\). For interior \(1\le x,y\le N-1\), only the first term with \(k=0,x=y\) can be zero. At \(y=0\) or \(y=N\), symmetry \(p_t(u)=p_t(-u)\) and reindexing cancel the two image sums. Formula (7) also equals zero when either \(s\) or \(z\) is a boundary
point \(a-1,b+1\).

Put \(q_s(a,b,z)=Q_s(a,b,z)\). Inclusion-exclusion gives

\[
q_s=K_t^{a,b}-K_t^{a+1,b}-K_t^{a,b-1}+K_t^{a+1,b-1}.        \tag{8}
\]

The interval has \(L\ge2\), so every interval used here is valid; any start or
endpoint just outside a shortened interval is exactly its zero boundary point.
Substitution of (7) into (8), followed by taking the start difference, gives
the exact formula (all displayed operators act on \(p_t\))

\[
q_0-q_2=
\sum_{k\in\mathbb Z}D_2D_{2k}^2p_t(z+2kN)
+\sum_{k\in\mathbb Z}D_2D_{2k}D_{2k+2}p_t(z-2a+4+2kN).   \tag{9}
\]

For positive \(k\),
\(D_{2k}f(u)=\sum_{r=0}^{k-1}\Delta f(u-2r)\), and for \(k=-m<0\),
\(D_{-2m}f(u)=-\sum_{r=1}^{m}\Delta f(u+2r)\).
Consequently the first summand in (9) is a sum of \(k^2\) translates of
\(\Delta^3p_t\). Every translate's argument has absolute value at least
\((2|k|-1)L\) when \(k\ne0\). For example, for \(k>0\) its smallest
argument is at least
\(z+2kN-4k+4\ge(2k-1)L\), because \(z\ge a\ge2-L\);
for \(k=-m<0\), its largest argument is at most
\(z-2mN+4m\le-(2m-1)L\), because \(z\le b\le L\).

The second summand vanishes for \(k=0,-1\). For \(k\ge1\) it has
\(k(k+1)\) translates, each with argument at least \(2kL\).
For \(k=-m\le-2\) it has \(m(m-1)\) translates, each with argument at most
\(-2(m-1)L\). Indeed the relevant extremal arguments are bounded by
\(z-2a+6+2kL\ge2kL\) and
\(z-2a+2-2mL\le-2(m-1)L\), respectively.

By (4), therefore,

\[
|q_0-q_2|\le {6\cdot4096\over t^2}
\sum_{k\ge1}k^2e^{-k^2L^2/(32t)}.                         \tag{10}
\]

For \(L\ge\sqrt t\),
\(e^{-k^2L^2/(32t)}\le e^{-k^2/64}e^{-L^2/(64t)}\).
Counting at most \(2L^2\) triples and applying (6) bounds the entire large-range
l1 contribution by

\[
{12\cdot4096\over t^2}(2^{12})(2^{12}t^{3/2})
<2^{40}/\sqrt t.                                           \tag{11}
\]

## 5. Small ranges: sine expansion with differentiation

The killed kernel also has the finite sine expansion

\[
K_t^{a,b}(s,z)={2\over N}\sum_{j=1}^{N-1}
\cos^t(\pi j/N)
\sin(\pi j(s-a+1)/N)\sin(\pi j(z-a+1)/N).                  \tag{12}
\]

Here is a direct derivation. On coordinates \(x=1,\ldots,N-1\), the symmetric matrix sending a function to the average of its two neighbors (with zero boundary values) sends \(v_j(x)=\sin(\pi jx/N)\) to \(\cos(\pi j/N)v_j(x)\). The eigenvalues are distinct. Symmetry implies that vectors for distinct eigenvalues are orthogonal: \((\lambda_j-\lambda_k)\langle v_j,v_k\rangle=0\). Also
\[
\sum_{x=1}^{N-1}\sin^2(\pi jx/N)=N/2,
\]
since \(\sin^2 u=(1-\cos(2u))/2\) and the finite geometric sum \(\sum_{x=0}^{N-1}e^{2\pi ijx/N}=0\). These \(N-1\) nonzero orthogonal vectors form a basis, so
\[
\sum_{j=1}^{N-1}\sin(\pi jx/N)\sin(\pi jy/N)
=(N/2)\mathbf1_{x=y}.
\]
Consequently (12) has the correct time-zero values and obeys the killed recurrence; induction proves it.
It also holds with value zero at either boundary.

For \(t\ge1\), pair indices \(j,N-j\). Since \(s=0,2\) and
\(z\equiv t\pmod2\), the paired terms agree. The middle eigenvalue, if present,
is zero. Consequently (12) equals the following smooth interpolation at every
integer interval used in (8):

\[
H_t(a,b,s,z)={4\over N}\sum_{j\ge1}f_t(\pi j/N)
\sin(\pi j x/N)\sin(\pi j y/N),                            \tag{13}
\]

where \(N=b-a+2\), \(x=s-a+1\), \(y=z-a+1\), and
\(f_t(\theta)=\cos^t\theta\) for \(0\le\theta<\pi/2\), zero otherwise.
For \(t\ge3\), \(f_t\) is twice continuously differentiable at the cutoff.
The sum is locally finite in \(N>0\), so the mixed derivatives used next are
legitimate, including when \(N\) crosses an even integer.

In (8), let the left boundary vary through \([a,a+1]\), the right boundary
through \([b-1,b]\), and the start through \([0,2]\). Everywhere in this box,
\(L\le N\le L+2\) and \(0\le x,y\le N\), even when the start or endpoint
lies on a shortened interval's zero boundary. Repeated fundamental theorem
of calculus gives

\[
q_0-q_2=\int_0^2\int_a^{a+1}\int_{b-1}^{b}
\partial_s\partial_a\partial_b H_t\,db'\,da'\,ds.           \tag{14}
\]

Here and below the integrand's boundary arguments are the dummy variables.
For clarity, an explicit derivative bound is derived next. Write
\(J=\pi j\), \(\theta=J/N\), \(r=x/N\), \(w=y/N\). After differentiating the
\(j\)-term in (13) with respect to \(s\), it is

\[
4J N^{-2}f_t(\theta)B,
\qquad B=\cos(Jr)\sin(Jw).
\]

For each boundary derivative, \(|r_a|,|r_b|,|w_a|,|w_b|\le1/N\), and
\(|r_{ab}|,|w_{ab}|\le1/N^2\). Hence
\(|B_a|,|B_b|\le2J/N\) and \(|B_{ab}|\le(4J^2+2J)/N^2\).
Also \(\theta_a=\theta/N\), \(\theta_b=-\theta/N\),
\(\theta_{ab}=-2\theta/N^2\). The product rule therefore bounds the absolute
mixed derivative of this term by

\[
{4J\over N^4}\left[(6+10J+4J^2)f_t
 +(6+4J)\theta|f_t'|+\theta^2|f_t''|\right].                \tag{15}
\]

Since \(J\ge\pi>3\), the coefficients are at most \(8J^2\) and \(6J\).
For \(0\le\theta<\pi/2\),
\(\theta|f_t'|\le t\theta^2\cos^{t-1}\theta\) and
\(\theta^2|f_t''|\le(t^2\theta^4+t\theta^2)\cos^{t-2}\theta\).
The elementary inequality \(\cos\theta\le e^{-\theta^2/2}\) follows by
integrating \(\tan\theta\ge\theta\). For \(t\ge4\), putting \(v=t/N^2\),
the sum of (15) is consequently at most

\[
{32\over N^4}(1+v)^2
\sum_{j\ge1}(\pi j)^5e^{-v(\pi j)^2/4}.                    \tag{16}
\]

For small ranges \(2\le L<\sqrt t\), we have \(N\le L+2\le2L\), so
\(v\ge1/4\). Using \(3<\pi<4\),

\[
\sum_{j\ge1}(\pi j)^5e^{-v(\pi j)^2/4}
\le 2^{10}e^{-v}\sum_{j\ge1}j^5e^{-j^2/4}
\le2^{21}e^{-v}.                                          \tag{17}
\]

Indeed split \((9/4)vj^2\) in two equal halves: one is at least \(v\), the
other at least \(j^2/4\) because \(v\ge1/4\).
Writing \(u=t/L^2\ge1\), (16) is therefore at most

\[
2^{26}L^{-4}(1+u)^2e^{-u/4}.                               \tag{18}
\]

The integration box in (14) has volume 2. Counting triples, the small-range
l1 contribution is at most

\[
2^{28}\sum_{2\le L<\sqrt t}
L^{-2}(1+t/L^2)^2e^{-t/(4L^2)}.                            \tag{19}
\]

Each summand is \(t^{-1}u(1+u)^2e^{-u/4}\le
4t^{-1}u^3e^{-u/4}\le6912/t<2^{13}/t\).
The penultimate inequality follows by differentiation, whose maximum occurs
at \(u=12\), and dropping the factor \(e^{-3}\).
There are fewer than \(\sqrt t\) summands. Thus (19) is at most

\[
2^{41}/\sqrt t.                                           \tag{20}
\]

## 6. Conclusion and audit

Combining the exceptional contribution, (11), and (20), the full l1 distance
between the range triples is at most
\((8+2^{40}+2^{41})/\sqrt t\). Equation (1) proves the stated upper bound with
\(C=2^{43}\), for every integer \(t\ge16\).

Parity is used only where explicitly indicated: the two starts are both even,
all endpoints have parity \(t\), and this makes the positive sine interpolation
valid at the discrete corners. The interpolation need not describe any random
walk at noninteger starts or boundaries; it is an ordinary differentiable
function whose corner values agree with the killed kernels. In particular,
no probabilistic conditioning or coupling is hidden in that step.

At \(t=0\), the laws are distinct point masses and have total variation 1. At \(t=1\), their only common base position is 1. A state in their common support must have lamps 0 and 2 both zero; the lamp at 1 can have either value. Each of these two states has probability \(1/8\) under each law, so the total common mass is \(1/4\) and the total variation is \(3/4\). For \(2\le t<16\), the lower bound was already proved, and the elementary bound \(\|P_t^x-P_t^y\|_{\rm TV}\le1\le2^{43}/\sqrt t\) covers the upper bound as well. Thus there is no small-time obstruction, although the theorem only requires \(t\ge16\). The range-to-lamps reduction is asserted only for \(t\ge1\), as required by the departure switch. Every visited site, including the terminal site and both initial sites if visited, has precisely the final-lamp law specified by the question.
Together with Section 1, this proves the theorem with the stated \(c,C,t_0\). All sine, image, binomial, and integral estimates used here have proofs given above. The argument uses no numerical approximation and has no remaining gap.
