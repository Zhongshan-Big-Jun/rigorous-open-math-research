For every integer \(t\ge1024\),
\[
\boxed{\frac{1}{2\sqrt t}\le
 \|P_t^{(0,0)}-P_t^{(0,2)}\|_{\rm TV}
 \le\frac{10^{12}}{\sqrt t}.}
\]
Thus explicit choices are \(c=1/2\), \(C=10^{12}\), and \(t_0=1024\). The constants are deliberately loose. Here both initial lamp configurations are all zero.

<a id="1-the-exact-lamp-law-and-the-reduction"></a>

**1. The exact lamp law and the reduction.** Let \(S_0=s\), let \(S\) be the simple symmetric nearest-neighbor walk, and put
\[
m_t=\min_{0\le i\le t}S_i,\qquad M_t=\max_{0\le i\le t}S_i.
\]
For \(t\ge1\), conditional on its entire base path, the final lamp configuration consists of independent fair bits at all sites of \([m_t,M_t]\), and zeros elsewhere. Indeed, every visited site is reset at least once: the initial site is reset on the first departure, and every other visited site on an arrival. Take the last reset at each site. These are distinct independent fair bits; their indices depend only on the base path, which is independent of all reset bits. Nearest-neighbor paths visit every integer between their extrema. Consequently the same lamp law holds conditional only on \((m_t,M_t,S_t)\).

Write \(Q_t^s=\mathcal L_s(m_t,M_t,S_t)\). The preceding conditional law is one common probability kernel from triples to lamplighter states, for both initial positions. Therefore
\[
\|P_t^{(0,0)}-P_t^{(0,2)}\|_{\rm TV}
\le \|Q_t^0-Q_t^2\|_{\rm TV}. \tag{1}
\]
For completeness, contraction by a common kernel \(K\) follows directly from
\(\sum_v|\sum_u(\mu(u)-\nu(u))K(u,v)|\le\sum_u|\mu(u)-\nu(u)|\), since \(K(u,v)\ge0\) and \(\sum_vK(u,v)=1\). All spaces here are countable.

In particular, the zero at site 2 under the first start remains forced until that site is visited, and the zero at site 0 under the second start remains forced until that site is visited. No initially unvisited lamp has been randomized in this reduction.

<a id="2-elementary-free-walk-estimates-and-the-lower-bound"></a>

**2. Elementary free-walk estimates and the lower bound.** Define
\[
p_n(v)=\begin{cases}2^{-n}\binom n{(n+v)/2},& |v|\le n,\ v\equiv n\pmod2,\\0,&\text{otherwise},\end{cases}
\qquad a_n=2^{-n}\binom n{\lfloor n/2\rfloor}.
\]
These formulas follow by counting the independent signs. Put \(b_j=4^{-j}\binom{2j}j\). The recurrence
\[
\frac{b_{j+1}}{b_j}=\frac{2j+1}{2j+2}
\]
gives
\[
\frac1{2\sqrt j}\le b_j\quad(j\ge1),\qquad
b_j\le\frac1{\sqrt{j+1}}\quad(j\ge0). \tag{2}
\]
For the lower inequality, start at \(b_1=1/2\) and use
\((2j+1)^2\ge4j(j+1)\). For the upper inequality, start at \(b_0=1\) and use
\((2j+1)^2(j+2)\le4(j+1)^3\), whose right side minus left side is \(3j+2\). Also \(a_{2j+1}=b_{j+1}\). Binomial ratios show the central coefficients are maximal, so
\[
\sup_v p_n(v)=a_n\le\sqrt{2/n}\quad(n\ge1). \tag{3}
\]
Taking the lamplighter event \(A=\{(\eta,z):z\le0\}\) gives
\[
P_t^{(0,0)}(A)-P_t^{(0,2)}(A)
 =\mathbb P(-2<S_t\le0)=a_t, \tag{4}
\]
where here \(S_0=0\). For even \(t\) the unique accessible site in this interval is 0; for odd \(t\) it is \(-1\). If \(t=2j\ge2\), (2) implies \(a_t\ge1/(2\sqrt t)\). If \(t=2j+1\ge3\), then
\[
a_t=\frac{2j+1}{2j+2}b_j\ge\frac3{8\sqrt j}
\ge\frac1{2\sqrt{2j+1}},
\]
the last inequality following from \(9(2j+1)\ge16j\). At \(t=1\), \(a_1=1/2\). This proves the required lower bound for every \(t\ge1\).

We will use the following additional, fully proved estimates:
\[
p_N(w)\le 2N^{-1/2}e^{-w^2/(4N)}\quad(N\ge1), \tag{5}
\]
and, for integer \(t\ge3\) and \(w\equiv t+3\pmod2\),
\[
\left|p_t(w-3)-3p_t(w-1)+3p_t(w+1)-p_t(w+3)\right|
 \le 10^4t^{-2}e^{-w^2/(16t)}. \tag{6}
\]
To prove (5), symmetry allows \(w\ge w_0\), where \(w_0\) is 0 or 1 according to the parity of \(N\); outside the support there is nothing to prove. The ratio
\[
\frac{p_N(v+2)}{p_N(v)}=\frac{N-v}{N+v+2}
\]
and \(\log((1-u)/(1+u))\le-2u\) for \(0\le u<1\) give
\[
p_N(w)\le\sqrt{2/N}\exp\!\left(-\frac{w^2-w_0^2}{2(N+1)}\right).
\]
The logarithmic inequality follows by differentiation. Now \(2(N+1)\le4N\), and
\(e^{1/(2(N+1))}\le e^{1/4}\le4/3\), the last inequality following by comparing the exponential and geometric series termwise. Since \((4/3)\sqrt2<2\), (5) follows.

For (6), set \(N=t+3\) and let \(\xi_1,\ldots,\xi_N\) be independent fair signs with sum \(W\). Conditioning on the first three signs, and then using exchangeability conditional on \(W=w\), gives the exact identity
\[
\begin{split}
&p_t(w-3)-3p_t(w-1)+3p_t(w+1)-p_t(w+3)\\
&\quad=8p_N(w)\frac{w^3-(3N-2)w}{N(N-1)(N-2)}. \tag{7}
\end{split}
\]
Indeed \(W^3=(3N-2)W+\sum_{i,j,k\ {
m distinct}}\xi_i\xi_j\xi_k\). This proves (7) on the support, including its endpoints; outside it both sides are zero, so no conditioning on a null event is used. For \(t\ge3\), \(6\le N\le2t\) and \(N(N-1)(N-2)\ge N^3/2\). With \(u=|w|/\sqrt N\), (5) bounds the absolute value of (7) by
\[
32N^{-2}(u^3+3u)e^{-u^2/4}.
\]
Differentiation shows
\((u^3+3u)e^{-u^2/8}\le12\sqrt{12}+6<54\). Thus the last display is at most
\(1728N^{-2}e^{-w^2/(8N)}\le2048t^{-2}e^{-w^2/(16t)}\), proving (6).

<a id="3-exact-interval-kernels"></a>

**3. Exact interval kernels.** For integers \(a\le b\), define
\[
K_t(a,b;s,z)=\mathbb P_s(S_t=z,\ a\le S_i\le b\text{ for }0\le i\le t),
\qquad L=b-a+2.
\]
With \(x=s-a+1\), \(y=z-a+1\), its sine formula is
\[
K_t(a,b;s,z)=\frac2L\sum_{j=1}^{L-1}
 \cos^t\!\left(\frac{\pi j}L\right)
 \sin\!\left(\frac{\pi jx}L\right)
 \sin\!\left(\frac{\pi jy}L\right). \tag{8}
\]
Here initially \(1\le x,y\le L-1\). To verify (8), the killed one-step transition matrix on \(1,\ldots,L-1\), with zero boundary values at 0 and \(L\), has eigenvectors \(r\mapsto\sin(\pi jr/L)\) and eigenvalues \(\cos(\pi j/L)\), by the sine addition formula. The vectors are orthogonal and have squared norm \(L/2\), by the finite geometric series or the product-to-sum identity. Their number is \(L-1\), so they form a basis, and expanding the matrix power proves (8).

There is also the image formula
\[
K_t(a,b;s,z)=\sum_{k\in\mathbb Z}
 \left[p_t(z-s+2kL)-p_t(z+s-2a+2+2kL)\right]. \tag{9}
\]
For each fixed \(t\) this sum is finite. Its right side has the same nearest-neighbor recurrence in \(z\) as the killed kernel, vanishes at \(a-1,b+1\) by symmetry and reindexing, and at time zero is the point mass at \(s\) in the interior. Induction on time proves (9). Both (8) and (9) also vanish when \(s\) or \(z\) is either absorbing boundary point.

Put
\[
q_s(a,b,z)=\mathbb P_s(m_t=a,M_t=b,S_t=z).
\]
Inclusion-exclusion yields
\[
q_s(a,b,z)=K_t(a,b;s,z)-K_t(a+1,b;s,z)
 -K_t(a,b-1;s,z)+K_t(a+1,b-1;s,z). \tag{10}
\]
A contracted-interval term is zero if its start or endpoint lies outside that interval. Whenever this occurs below, that point is precisely an absorbing boundary, so the kernel formulas remain applicable.

**4. Short intervals.** We prove, for \(t\ge1024\),
\[
\sum_{\substack{a\le0,\ b\ge2,\ a\le z\le b\\ b-a+2\le\sqrt t}}
 |q_0(a,b,z)-q_2(a,b,z)|\le\frac{2\cdot10^9}{\sqrt t}. \tag{11}
\]
Only \(z\equiv t\pmod2\) matters. At integer parameters of this parity, pair \(j\) and \(L-j\) in (8). The combined sign is \((-1)^{t+x+y}=1\); the middle eigenvalue, if present, is zero for positive \(t\). Hence (8) equals the following extension to real parameters:
\[
H_t(a,b;s,z)=\frac4L\sum_{j\ge1}g_t(\pi j/L)
 \sin(\pi jx/L)\sin(\pi jy/L), \tag{12}
\]
where \(g_t(\theta)=\cos^t\theta\) on \([0,\pi/2]\), and zero for \(\theta>\pi/2\). This function is twice continuously differentiable across the cutoff for \(t\ge4\), and the sum is locally finite in \(L>0\). The extension vanishes when either \(x\) or \(y\) is 0 or \(L\).

The derivative estimate needed is
\[
|\partial_s\partial_a\partial_bH_t|\le10^9t^{-2}
\quad\text{if }2\le L\le\sqrt t,\quad 0\le x,y\le L. \tag{13}
\]
Here are detailed bounds for it. In one summand put \(d=\pi j\), \(\theta=d/L\), \(h=g_t(\theta)\), \(v=t\theta^2\), and
\[
F=L^{-1}\theta h\cos(\theta x)\sin(\theta y).
\]
The \(s\)-derivative of that summand is \(4F\); in the independent coordinates \((L,x,y)\),
\(\partial_a=-(\partial_L+\partial_x+\partial_y)\) and \(\partial_b=\partial_L\).
Integrating \(\tan\theta\ge\theta\) proves \(\cos\theta\le e^{-\theta^2/2}\). Direct differentiation therefore gives, for \(t\ge4\),
\[
|h|\le e^{-v/4},\qquad |h'|\le t\theta e^{-v/4},\qquad
|h''|\le t(1+v)e^{-v/4}. \tag{14}
\]
These bounds extend across the cutoff, where the derivatives vanish.

For \(R=\cos(\theta x)\sin(\theta y)\),
\(|R|\le1\), \(|R'|\le2L\), \(|R''|\le4L^2\). Writing \(f=\theta hR\), one has
\[
F_{LL}=L^{-3}(2f+4\theta f'+\theta^2f'').
\]
Expansion using (14) gives
\[
\begin{split}
|F_{LL}|&\le L^{-4}e^{-v/4}
 [6d+12d^2+4d^3+(7d+4d^2)v+dv^2]\\
&\le34L^{-4}d^3(1+v)^2e^{-v/4},\\
|F_{xL}|,\ |F_{yL}|&\le L^{-4}e^{-v/4}[3d^2+2d^3+d^2v]
 \le6L^{-4}d^3(1+v)^2e^{-v/4}.
\end{split} \tag{15}
\]
Thus the left side of (13) is at most
\[
200L^{-4}\sum_{j\ge1}d^3(1+v)^2e^{-v/4}.
\]
Set \(u=t/L^2\ge1\), so \(v=ud^2\). Multiplication by \(t^2\) changes a summand to
\(d^{-1}v^2(1+v)^2e^{-v/4}\). Differentiation of \(v^re^{-v/8}\) shows
\[
v^2(1+v)^2e^{-v/8}\le2(16^2+32^4)<3\cdot10^6.
\]
Moreover
\[
\sum_{j\ge1}d^{-1}e^{-v/8}
\le\sum_{j\ge1}e^{-\pi^2j^2/8}
\le\int_0^\infty e^{-\pi^2r^2/8}\,dr
=\sqrt{2/\pi}<1.
\]
This proves (13), even with \(6\cdot10^8\) in place of \(10^9\).

Apply (10) to (12), and use the fundamental theorem of calculus over
\[
s\in[0,2],\qquad a'\in[a,a+1],\qquad b'\in[b-1,b].
\]
Throughout this box, \(2\le L'=b'-a'+2\le L\le\sqrt t\), and
\(x'=s-a'+1\), \(y'=z-a'+1\) lie in \([0,L']\): their lower bounds follow from \(a\le0\) and \(z\ge a\), and their upper bounds from \(b\ge2\) and \(z\le b\). All needed mixed derivatives are continuous there by (12). The box has volume 2, so
\[
|q_0(a,b,z)-q_2(a,b,z)|\le2\cdot10^9t^{-2}.
\]
For each integer \(L\) there are at most \(L\) eligible choices of \(a\), and at most \(L\) choices of \(z\). Since \(\sum_{1\le L\le\sqrt t}L^2\le t^{3/2}\), (11) follows.

**5. Long intervals.** For \(D_hf(v)=f(v)-f(v-h)\), equations (9)–(10) give exactly
\[
\begin{split}
q_0-q_2=\sum_{k\in\mathbb Z}\big[&D_{2k}^2D_2p_t(z+2kL)\\
 &+D_{2k}D_{2k+2}D_2p_t(z-2a+4+2kL)\big].
\end{split} \tag{16}
\]
The sign of the second term includes the minus in the reflected image and the start's increase of its argument by 2. The first expression vanishes at \(k=0\); the second vanishes at \(k=0,-1\).

For integer \(k\ne0\), \(D_{2k}\) is a signed sum of \(|k|\) translates of \(D_2\). For \(k>0\), use arguments shifted by \(-2r\), \(0\le r\le k-1\); for \(k<0\), use \(k\le r\le-1\) with an overall minus sign. Therefore the two expressions in (16) contain respectively \(k^2\) and \(|k(k+1)|\) translates of \(D_2^3p_t\).

Suppose \(L>\sqrt t\ge32\). In the first expression put \(m=|k|\ge1\). Since \(|z|\le L-2\), every resulting centered argument \(w\) of the third difference satisfies
\[
|w|\ge(2m-1)L-4m-1\ge mL/2. \tag{17}
\]
The centering is \(w=v-3\) for \(D_2^3p_t(v)\); its absolute value is that in (6). In the second expression put \(m=\min(|k|,|k+1|)\ge1\). Write \(r=1-a\), \(y=z-a+1\); then
\(1\le r\le L-3\), \(1\le y\le L-1\), and \(4\le r+y+2\le2L-2\).
Thus the original argument \(r+y+2+2kL\) has magnitude at least \(2mL+2\), and all shifts and centering alter it by at most \(4m+5\). Consequently
\[
|w|\ge2mL-4m-3\ge mL/2. \tag{18}
\]
There are two first-image indices per \(m\), of total multiplicity \(2m^2\), and two second-image indices, of total multiplicity \(2m(m+1)\le4m^2\). Every \(w\) has parity \(t+3\) because \(z\equiv t\pmod2\). Hence (6), (17), and (18) imply
\[
|q_0-q_2|\le60000t^{-2}\sum_{m\ge1}m^2e^{-m^2L^2/(64t)}. \tag{19}
\]
The bounds also cover third differences outside the free-walk support.

For \(X,Y\ge1\), \(XY\ge(X+Y)/2\). With \(X=L^2/t\), \(Y=m^2\), it follows that
\[
e^{-m^2L^2/(64t)}\le e^{-m^2/128}e^{-L^2/(128t)}.
\]
For every real \(T\ge1\), comparison on each interval \([n-1,n]\) gives
\[
\begin{split}
\sum_{n\ge1}n^2e^{-n^2/(128T)}
&\le\int_0^\infty(r+1)^2e^{-r^2/(128T)}\,dr\\
&=\frac{(128T)^{3/2}\sqrt\pi}{4}+128T+
 \frac{\sqrt{128\pi T}}2
<1000T^{3/2}. \tag{20}
\end{split}
\]
The last bound uses \(\sqrt{128}<12\), \(\sqrt\pi<2\), and \(T\ge1\). Counting at most \(L^2\) triples per \(L\), summing (19), and using (20) twice now yield
\[
\sum_{\substack{a\le0,\ b\ge2,\ a\le z\le b\\ b-a+2>\sqrt t}}
|q_0(a,b,z)-q_2(a,b,z)|
\le\frac{6\cdot10^{10}}{\sqrt t}. \tag{21}
\]
Only nonnegative convergent majorants were summed; the exact image expressions before majorization have finitely many nonzero terms for each fixed \(t\).

<a id="6-boundary-support-assembly-and-theorem-audit"></a>

**6. Boundary support, assembly, and theorem audit.** Outside \(a\le0,b\ge2\), the \(q_0\) law can occur only when \(b\le1\), and the \(q_2\) law only when \(a\ge1\). Their masses are equal by reflection about 1. Reflecting a 0-start path after its first hit on 2 is a probability-preserving bijection from paths with \(M_t\ge2,S_t<2\) to paths with \(S_t>2\). Thus, by symmetry,
\[
\mathbb P_0(M_t\le1)=\mathbb P_0(-2\le S_t<2)
\le2\sup_vp_t(v)\le3/\sqrt t. \tag{22}
\]
There are exactly two possible parity sites in \([-2,2)\). The total-variation contribution outside the common support is one half of the sum of these two equal masses, hence at most \(3/\sqrt t\).

Equations (11), (21), and (22), with the factor \(1/2\) in total variation, give
\[
\|Q_t^0-Q_t^2\|_{\rm TV}
\le\frac{3+10^9+3\cdot10^{10}}{\sqrt t}
<\frac{10^{12}}{\sqrt t}\qquad(t\ge1024).
\]
Together with (1) and (4), this proves the displayed theorem.

All formulas include both time parities: both starting positions are even, so both endpoints have parity \(t\); inaccessible endpoints were discarded only when both probabilities vanish. The sine pairing explicitly retains that parity, and the third-difference bound has its required parity. The argument does not use a replacement lamp convention or couple unequal lamp histories by assumption. At \(t=0\) both laws are distinct point masses, so their total variation is 1; the asymptotic assertion does not cover that time. The lower bound was proved even for \(1\le t<1024\); the upper bound is asserted only for \(t\ge1024\).

The elementary analysis facts used above are: if \(f\) is continuously differentiable on \([A,B]\), then \(f(B)-f(A)=\int_A^Bf'(u)\,du\); this is applied iteratively only on the compact rectangle where the indicated mixed derivatives are continuous. The Gaussian identities, for \(\alpha>0\), are
\[
\int_0^\infty e^{-\alpha r^2}dr=\frac{\sqrt\pi}{2\sqrt\alpha},\quad
\int_0^\infty re^{-\alpha r^2}dr=\frac1{2\alpha},\quad
\int_0^\infty r^2e^{-\alpha r^2}dr=\frac{\sqrt\pi}{4\alpha^{3/2}}.
\]
The first follows by squaring the nonnegative integral and using polar coordinates in the quadrant; the second follows by the substitution \(u=\alpha r^2\); the third follows by integration by parts from the first. All integrals converge by exponential decay, and their parameters here are positive. These identities explain every Gaussian integral used in (13) and (20). The finite-dimensional expansion (8), image identity (9), reflection identity (22), and probabilistic contraction (1) were proved above rather than imported as external results. No external research theorem, numerical evidence, or conjecture is used in the proof. This is an ordinary mathematical proof, with no claim of Lean formal verification or of novelty.
