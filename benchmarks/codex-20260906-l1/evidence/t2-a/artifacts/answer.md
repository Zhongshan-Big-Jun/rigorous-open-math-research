For every integer \(t\ge32\),
\[
\boxed{\frac{1}{4\sqrt t}\le
 \|P_t^{(0,0)}-P_t^{(0,2)}\|_{\rm TV}
 \le\frac{10^{10}}{\sqrt t}.}
\]
Thus explicit constants are \(c=1/4\), \(C=10^{10}\), and \(t_0=32\).
The constants are deliberately coarse. Everything below is an exact proof;
no numerical evidence is used.

**1. The lamp convention and the lower bound.**
Write \(S_0=a,S_1,\ldots,S_t\) for the base walk started at \(a\in\{0,2\}\),
and write
\[
m_t=\min_{0\le s\le t}S_s,\qquad M_t=\max_{0\le s\le t}S_s.
\]
For \(t\ge1\), every site in the integer interval \([m_t,M_t]\) is visited
and is resampled at least once. This includes the departure site at time zero
and the terminal site at time \(t\). Conditional on the entire base path,
the final value at each visited site is its last resampling bit. Those bits
are distinct members of a family of independent fair bits, independent of
all base increments. Thus the final lamps are independent fair bits on this
interval and zero outside. The conditional law depends only on
\((m_t,M_t,S_t)\).

In particular both starts use exactly the same conditional lamp kernel.
There is no initially lit lamp at site \(2\). Initially the lamps at both
\(0\) and \(2\), and all other sites, are zero; a site that is not visited
retains that zero. Averaging over paths with the same triple does not change
the stated conditional distribution.

Let \(Q_t^a\) be the law of this triple. The triangle inequality applied to
the common probability kernel gives
\[
 \|P_t^{(0,0)}-P_t^{(0,2)}\|_{\rm TV}
 \le \|Q_t^0-Q_t^2\|_{\rm TV}.                 \tag{1}
\]
Explicitly, if the kernel is \(K(v,w)\), then
\(\sum_w|\sum_v(Q_t^0(v)-Q_t^2(v))K(v,w)|
\le\sum_v|Q_t^0(v)-Q_t^2(v)|\), since \(\sum_wK(v,w)=1\).
All sums are finite at a fixed time.

For the lower bound let \(p_t(j)\) be the probability that a walk from zero
is at \(j\) at time \(t\). The two base marginals are \(S_t\) and \(S_t+2\).
Use the event that the base is at most zero when \(t\) is even, and at most
one when \(t\) is odd. Its probability difference is respectively
\(p_t(0)\) and \(p_t(1)\). Indeed each difference is the mass of an interval
of two consecutive integers, only one of which has parity \(t\).

Set \(b_n=4^{-n}\binom{2n}{n}\). For \(n\ge1\),
\[
 b_n\ge\frac1{2\sqrt n}.                       \tag{2}
\]
The base case is equality, and
\[
 \frac{b_{n+1}}{b_n}=\frac{2n+1}{2n+2}
 \ge\sqrt{\frac n{n+1}},
\]
because \((2n+1)^2-4n(n+1)=1\). This proves (2) by induction.
For \(t=2n\ge2\), \(p_t(0)=b_n\); for \(t=2n+1\ge3\),
\(p_t(1)=\frac{2n+1}{2n+2}b_n\ge1/(4\sqrt n)\).
These imply the asserted lower bound for every \(t\ge2\), and at \(t=1\)
the event difference is \(1/2\). Preimages of these base events are events
in the full chain, so they give lower bounds for its total variation.

We also need a binomial upper estimate:
\[
 \max_j p_t(j)\le\frac2{\sqrt t}\qquad(t\ge1).   \tag{3}
\]
The binomial coefficients are maximized at their middle indices, as follows
from the ratio \(\binom t{k+1}/\binom tk=(t-k)/(k+1)\).
Induction gives \(b_n\le1/\sqrt{n+1}\): the ratio inequality needed is
\[
 \left(\frac{2n+1}{2n+2}\right)^2\le\frac{n+1}{n+2},
\]
whose numerator difference after clearing denominators is \(3n+2\ge0\).
The even and odd formulas above now give (3), including \(t=1\).

**2. A smooth interpolation of killed-walk probabilities.**
Throughout the upper-bound proof \(t\) is an integer at least \(32\).
Define the compactly supported function
\[
 B_t(\theta)=
 \begin{cases}\cos^t\theta,&|\theta|\le\pi/2,\\0,&|\theta|>\pi/2,
 \end{cases}
 \qquad
 f_t(x)=\frac1\pi\int_{-\pi/2}^{\pi/2}
                  \cos^t\theta\,e^{ix\theta}\,d\theta.
                                                               \tag{4}
\]
The cutoff in this definition is a single interval, not a periodic positive
part of cosine. For integers \(j\equiv t\pmod2\),
\[
 f_t(j)=p_t(j).                                      \tag{5}
\]
To see this, expand \(\cos^t\theta\) into exponentials in the integral
\((2\pi)^{-1}\int_{-\pi}^{\pi}\cos^t\theta e^{ij\theta}\,d\theta\).
It extracts the appropriate binomial probability. Its integrand is
\(\pi\)-periodic when \(j+t\) is even, so this integral is (4).

For real \(l<r\), put \(L=r-l\) and
\[
 H(l,r;a,z)=\sum_{k\in\mathbb Z}
 \{f_t(z-a+2kL)-f_t(z+a-2l+2kL)\}.                  \tag{6}
\]
There is also the exact spectral expression
\[
 H(l,r;a,z)=\frac4L\sum_{j\ge1}
 \sin\!\left(\frac{\pi j(a-l)}L\right)
 \sin\!\left(\frac{\pi j(z-l)}L\right)
 B_t\!\left(\frac{\pi j}L\right).                  \tag{7}
\]
Here the sum is finite, and the identity holds for all real \(a,z,l,r\)
with \(l<r\).

For precision, the only Fourier theorems used to obtain (7) are the following
standard forms of inversion and uniqueness:

- If \(g\in C_c^2(\mathbb R)\) and
  \(F(x)=(2\pi)^{-1}\int g(u)e^{ixu}\,du\), then \(F\in L^1(\mathbb R)\)
  and \(\int F(x)e^{-ixu}\,dx=g(u)\) for every real \(u\).
- A continuous periodic function is determined by all its Fourier
  coefficients: if every coefficient is zero, the function is zero.

Here \(g=2B_t\) is \(C_c^2\), because its zero at either cutoff has order
\(t\ge32\). Twice integrating (4) by parts proves that \(f_t\) decays as
\(O((1+|x|)^{-2})\). Consequently its \(2L\)-periodization is continuous,
and its Fourier coefficient at frequency \(\pi j/L\) is, by inversion,
\(B_t(\pi j/L)/L\). Unfolding the integral is justified by absolute
integrability. Only finitely many coefficients are nonzero. Uniqueness
therefore identifies this periodization with
\[
 L^{-1}\left(1+2\sum_{j\ge1}B_t(\pi j/L)\cos(\pi jv/L)\right).
\]
Subtract its values at \(v=z-a\) and \(v=z+a-2l\), and use
\(\cos(U-V)-\cos(U+V)=2\sin U\sin V\), proving (7).
This verifies every hypothesis of both Fourier theorems.

For integer boundaries \(l<r\) and integer \(a,z\in[l,r]\) with
\(a+z+t\) even, \(H(l,r;a,z)\) is the probability that the walk from
\(a\) ends at \(z\) at time \(t\) without hitting either boundary, where
this probability is zero if \(a\) or \(z\) is on a boundary. This claim
uses no additional probabilistic theorem. By (5), (6) is the image sum with
\(p_t\) replacing \(f_t\). At every nonnegative integer time this finite
image sum satisfies the nearest-neighbor heat recurrence in \(z\), is zero
at \(z=l,r\) by symmetry and reindexing, and at time zero is the point mass
at the interior start \(a\). Induction gives exactly the killed transition
probabilities. If the start is a boundary, the two image sums cancel.

The function \(H\) is \(C^3\) in its real parameters on \(l<r\). In (7)
only locally finitely many terms occur, and \(B_t\) is \(C^3\), including
at its cutoffs. Alternatively, six integrations by parts in the Fourier
integrals for \(f_t\) and its first three derivatives give decay
\(O_t((1+|x|)^{-6})\); all boundary terms vanish. Differentiated image sums
through order three have coefficients at most cubic in \(k\), so converge
locally uniformly. This also justifies differentiating (6).

**3. Two explicit derivative estimates.**
We first establish
\[
 |f_t'''(x)|\le A t^{-2}(1+|x|/\sqrt t)^{-6},
 \qquad A=9000000.                                \tag{8}
\]
Here are details, including the constants. For \(|\theta|\le\pi/2\),
\(\cos\theta\le e^{-\theta^2/2}\) and \(|\sin\theta|\le|\theta|\).
For the first inequality, differentiate
\(\log\cos\theta+\theta^2/2\) on the positive half-interval and use
\(\tan\theta\ge\theta\); symmetry and continuity give the rest.

For \(0\le m\le6\) write
\[
 D^m\cos^t\theta=\sum_r b_{m,r}(t)
                   \sin^r\theta\cos^{t-r}\theta.
\]
The nonzero indices satisfy \(0\le r\le m\), \(r\equiv m\pmod2\).
Differentiation gives
\(b_{m+1,r}=(r+1)b_{m,r+1}-(t-r+1)b_{m,r-1}\).
It follows by induction that
\( |b_{m,r}(t)|\le H_{m,r}t^{(m+r)/2}\), where
\(H_{0,0}=1\) and
\(H_{m+1,r}=(r+1)H_{m,r+1}+H_{m,r-1}\).
Since \(t-r\ge t/2\), we obtain
\[
 |D^m\cos^t\theta|\le e^{-t\theta^2/4}
       \sum_r H_{m,r}t^{(m+r)/2}|\theta|^r.         \tag{9}
\]
The nonzero rows needed are
\[
\begin{array}{c|l}
m& (r,H_{m,r})\\\hline
3&(1,3),(3,1)\\
4&(0,3),(2,6),(4,1)\\
5&(1,15),(3,10),(5,1)\\
6&(0,15),(2,45),(4,15),(6,1).
\end{array}
\]
Substitution and integration by parts give, for positive integers \(q\),
\[
 \int_{\mathbb R}|\theta|^{2q-1}e^{-t\theta^2/4}\,d\theta
 =(4/t)^q(q-1)!.
\]
Thus for powers \(1,3,5,7,9\) the moment constants are respectively
\(4,16,128,1536,24576\), with scaling \(t^{-(p+1)/2}\).
Set \(h(\theta)=\theta^3\cos^t\theta\). The product rule gives
\[
 h^{(6)}=\theta^3D^6\cos^t+18\theta^2D^5\cos^t
                      +90\theta D^4\cos^t+120D^3\cos^t.
\]
Using (9) and these moments, the four terms have integral upper bounds
\(53616t,55008t,21240t,3360t\). Their sum proves
\[
 \int_{-\pi/2}^{\pi/2}|h^{(6)}(\theta)|\,d\theta\le133224t.
\tag{10}
\]
Every derivative \(h^{(k)}\), \(k\le5\), vanishes at both endpoints,
since each of its terms retains a positive power of cosine. Six integrations
by parts in \(f_t'''=(-i/\pi)\int h(\theta)e^{ix\theta}\,d\theta\) give,
for \(x\ne0\),
\[
 |f_t'''(x)|\le\frac{133224t}{\pi|x|^6}.
\]
Direct integration also gives
\( |f_t'''(x)|\le4/(\pi t^2)\) for every real \(x\).
Finally \(\min(1,y^{-6})\le64(1+y)^{-6}\) for \(y>0\).
These bounds, with the direct bound at \(x=0\), prove (8), because
\(64\cdot133224/\pi=8526336/\pi<A\).

Assume now \(l\le a,z\le r\). Differentiating (6) gives
\[
 H_{alr}=\sum_{k\in\mathbb Z}
 \{4k^2f_t'''(z-a+2kL)
       +4k(k+1)f_t'''(z+a-2l+2kL)\}.             \tag{11}
\]
In the first part, the \(k=0\) coefficient is zero, and all other argument
moduli are at least \(|k|L\). In the second part the \(k=0,-1\)
coefficients vanish. Indexing its remaining terms by \(j=k\ge1\) or
\(j=-k-1\ge1\), their argument moduli are at least \(2jL\), and their
coefficients are at most \(8j^2\). Hence (8) implies
\[
 |H_{alr}|\le24At^{-2}\sum_{j\ge1}j^2(1+jL/\sqrt t)^{-6}
 \le32AtL^{-6},                                  \tag{12}
\]
since \(\sum_{j\ge1}j^{-4}\le1+\int_1^\infty x^{-4}\,dx=4/3\).

For narrow intervals we need the additional estimate
\[
 |H_{alr}|\le D L^{-4}e^{-t/(2L^2)},\qquad
 0<L\le\sqrt t,\quad D=1500000.                  \tag{13}
\]
We supply the parameter differentiation to avoid an implicit heat-kernel
estimate. In one summand of (7), set
\(q=\pi j\), \(u=a-l\), \(v=z-l\), \(U=u/L\), \(V=v/L\),
\(w=q/L\), and \(s=tw^2\). After differentiating in \(a\), that summand is
\[
 F=4qL^{-2}A_0B,\qquad
 A_0=\cos(qU)\sin(qV),\quad B=B_t(w).
\]
Here \(0\le U,V\le1\). At fixed \(a,z\),
\(\partial_r=\partial_L\) and
\(\partial_l=-\partial_L-\partial_u-\partial_v\), so
\( |\partial_l\partial_rF|\le|F_{LL}|+|F_{uL}|+|F_{vL}|\).
For an active summand put \(E=e^{-s/4}\). Direct differentiation and
\(t-2\ge t/2\) give
\[
 |B|\le E,\quad |B_L|\le L^{-1}sE,\quad
 |B_{LL}|\le L^{-2}(3s+s^2)E.
\]
These hold at cutoff points by continuity; inactive summands are zero.
Also
\[
\begin{gathered}
 |(A_0)_L|\le2q/L,\qquad
 |(A_0)_{LL}|\le(4q^2+4q)/L^2,\\
 |(A_0)_u|,|(A_0)_v|\le q/L,\qquad
 |(A_0)_{uL}|,|(A_0)_{vL}|\le(q+2q^2)/L^2.
\end{gathered}
\]
The product rule therefore gives
\[
\begin{aligned}
 |F_{LL}|&\le4qL^{-4}[6+12q+4q^2+(7+4q)s+s^2]E,\\
 |F_{uL}|,|F_{vL}|&\le4qL^{-4}[3q+2q^2+qs]E.
\end{aligned}
\]
Since \(q>1\), their sum is at most
\[
 4q^3L^{-4}(32+13s+s^2)e^{-s/4}
 \le1568q^3L^{-4}e^{-s/8}.                        \tag{14}
\]
Indeed \(s e^{-s/8}\le8\) and \(s^2e^{-s/8}\le256\), by differentiating
these functions, and \(32+13\cdot8+256=392\).

Write \(\alpha=t/L^2\ge1\). Using the elementary bounds \(3<\pi<4\),
\[
 \sum_{j\ge1}(\pi j)^3e^{-\alpha(\pi j)^2/8}
 \le64e^{-\alpha/2}\sum_{j\ge1}j^3e^{-j^2/2}
 <64\cdot13 e^{-\alpha/2}.
\]
Here \(\alpha j^2\ge(\alpha+j^2)/2\). To verify the last numerical
constant without a Gaussian-integral formula, compare each term to the
integral of \((x+1)^3e^{-x^2/2}\) on \([j-1,j]\). The total integral is
\(5+4\int_0^\infty e^{-x^2/2}\,dx<13\); the remaining integral is less
than two by splitting at one and bounding its tail by
\(\int_1^\infty x e^{-x^2/2}\,dx<1\).
The inequalities \(3<\pi<4\) follow, for example, by comparing the unit
circle with its inscribed regular hexagon and circumscribed square.
As \(1568\cdot64\cdot13=1304576<D\), summing (14) proves (13).

**4. Exact ranges, exceptional paths, and the summation.**
Write \(q_t^a(m,M,z)=Q_t^a\{(m,M,z)\}\).
First take common ranges, meaning integers \(m\le0\), \(M\ge2\), and
\(z\in[m,M]\) with \(z\equiv t\pmod2\). Inclusion-exclusion gives
\[
\begin{aligned}
q_t^a(m,M,z)={}&H(m-1,M+1;a,z)-H(m,M+1;a,z)\\
              &-H(m-1,M;a,z)+H(m,M;a,z).
\end{aligned}                                                   \tag{15}
\]
Indeed the first probability confines the path to \([m,M]\); subtracting
paths missing either endpoint, then adding those missing both, imposes the
exact minimum and maximum. At all four corners, \(a\in\{0,2\}\) and \(z\)
are inside or on the absorbing boundaries. Therefore the killed-kernel
identity applies, including its zero-boundary cases, with the required
parity. No assertion about a start outside a killed interval is needed.

Repeated use of the fundamental theorem of calculus in (15) gives
\[
 q_t^2(m,M,z)-q_t^0(m,M,z)
 =-\int_0^2\int_{m-1}^m\int_M^{M+1}
               H_{alr}(l,r;a,z)\,dr\,dl\,da.                  \tag{16}
\]
Every interpolated point satisfies \(l\le a,z\le r\), and \(L>0\).
Thus both derivative estimates apply whenever their width condition holds.

Put \(N=M-m\ge2\). There are \(N-1\) choices of \(m\) for common ranges
of this width, and at most \(N+1\) possible endpoints \(z\); dropping the
parity restriction only enlarges this count. In (16),
\(N\le L\le N+2\le2N\). The integration in \(a\) has length two,
which cancels the factor one half in total variation. Consequently the
common-range contribution is at most the sum over \(N\ge2\) of
\(N^2\) times a uniform bound on \(|H_{alr}|\) for \(L\in[N,N+2]\).

For \(N\le\sqrt t/2\), (13) gives contribution at most
\[
 D\sum_{2\le N\le\sqrt t/2}N^{-2}e^{-t/(8N^2)}
 \le\frac{4D}{\sqrt t}=\frac{6000000}{\sqrt t}.                \tag{17}
\]
To check this explicitly, \(u e^{-u}\le1\) implies each summand without
\(D\) is at most \(8/t\), and there are at most \(\sqrt t/2\) indices.
For the remaining widths use (12). Put \(v=\sqrt t/2\); since \(t\ge32\),
\(\lfloor v\rfloor\ge v/2>0\). Thus
\[
\begin{aligned}
 32At\sum_{N>v}N^{-4}
 &\le\frac{32At}{3\lfloor v\rfloor^3}
 \le\frac{2048A}{3\sqrt t}
 =\frac{6144000000}{\sqrt t}.                              \tag{18}
\end{aligned}
\]
The first comparison integrates the decreasing function \(x^{-4}\) over
\([\lfloor v\rfloor,\infty)\). Bounds (17)-(18) also justify all infinite
upper sums; the original fixed-time probability sums have finite support.

It remains to bound ranges that do not contain both starting sites. Under
start zero these are exactly the paths with \(M_t<2\); under start two
they are exactly those with \(m_t>0\). Their masses are equal by the
path bijection \(S_s\mapsto2-S_s\), and their triple supports are disjoint.
Their combined contribution to half the \(\ell^1\) distance is therefore
\(\Pr_0(M_t<2)\).

Reflect a path after its first visit to \(2\). For each terminal
\(z\le1\), this is a probability-preserving bijection from paths hitting
\(2\) and ending at \(z\) to all paths ending at \(4-z\ge3\).
Consequently, using symmetry of \(p_t\),
\[
 \Pr_0(M_t<2)=\Pr_0(S_t\le1)-\Pr_0(S_t\ge3)
             =\sum_{j=-2}^{1}p_t(j)\le\frac4{\sqrt t}.       \tag{19}
\]
Exactly two of those four integers have parity \(t\), so (3) gives the
last inequality. The reflection is a finite path bijection, not an
unjustified conditioning or a lamp coupling.

Combining (17)-(19) proves
\[
 \|Q_t^0-Q_t^2\|_{\rm TV}
 \le\frac{6150000004}{\sqrt t}
 <\frac{10^{10}}{\sqrt t}.
\]
Together with (1) and the lower bound, this proves the stated theorem.

**5. Scope and audit of prerequisites.**
The two base starts differ by two, so they share the parity class \(t\).
Parity was retained in (5), in the killed-kernel identity, and in (15);
it was dropped only in an upper count of endpoints. At time zero the states
are distinct and total variation equals one; the fair-lamp-on-range
representation was explicitly restricted to positive times. The lower
bound holds for every \(t\ge1\); the upper proof requires \(t\ge32\),
which is the claimed \(t_0\). Thus no small-time or parity case is silently
used outside its range of validity.

Apart from the two Fourier theorems stated with checked hypotheses above,
the proof uses elementary differentiation, the fundamental theorem of
calculus, substitution, and integration by parts. The fundamental theorem
is used only for continuously differentiable functions on compact intervals;
all boundary terms in integrations by parts were specified or vanish by
exponential decay. Differentiation under the finite integral (4) is valid
because its derivative of order \(j\le3\) is bounded by the integrable
function \(|\theta|^j\). This is the dominated-differentiation rule: if a
parameter derivative exists and is dominated locally by one integrable
function, its integral can be differentiated by integrating that derivative.
Exchanging a sum and integral uses the absolute-integrability form of
Fubini's theorem: an absolutely integrable family has either iterated
integral equal to its joint integral. Its applications above have the
explicit integrable bound on \(f_t\) or locally uniformly summable
sixth-order decay. Differentiation of the image series uses the familiar
uniform-derivative rule: locally uniform convergence of a series and of
its derivatives through a given order permits termwise differentiation
through that order; the bound \(O(|k|^{-3})\) verifies it here.
All probabilistic identities, the lamp reduction, the reflection formula,
and the binomial and analytic estimates were proved explicitly. There is
no conjectural or numerical step and no appeal to an external random-walk
limit theorem. No Lean formal verification is claimed.
