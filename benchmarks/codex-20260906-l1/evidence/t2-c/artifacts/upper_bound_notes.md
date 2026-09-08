# Exact audit of the simple-random-walk third-difference estimate

This is a proved auxiliary result for the requested upper bound. It does not by itself prove the total-variation upper bound.

Write

\[
p_t(u)=\begin{cases}2^{-t}\binom{t}{(t+u)/2},& |u|\le t,\quad u\equiv t\pmod 2,\\0,&\text{otherwise},\end{cases}
\qquad \Delta_2 f(u)=f(u+2)-f(u).
\]

For every integer \(t\ge16\) and every integer \(u\),

\[
\boxed{\quad |\Delta_2^3p_t(u)|\le1024\,t^{-2}\exp\{-u^2/(32t)\}.\quad}
\]

Thus the proposed constant 4096 is valid, including when the Gaussian is evaluated at the initial argument of the **forward** difference, rather than at its center.

## 1. Elementary local Gaussian estimate

For every integer \(n\ge1\) and every integer \(v\),

\[
p_n(v)\le 2n^{-1/2}e^{-v^2/(4n)}. \tag{1}
\]

All wrong-parity or out-of-support cases are zero. By symmetry it suffices to consider \(v\ge0\) of the correct parity. The central-binomial estimate

\[
4^{-m}\binom{2m}{m}\le (m+1)^{-1/2}\qquad(m\ge0) \tag{2}
\]

follows by induction: the ratio at consecutive values of \(m\) is \((2m+1)/(2m+2)\), and

\[
(2m+1)^2(m+2)\le4(m+1)^3
\]

because the difference of right and left sides is \(3m+2\).

If \(n=2m\ge2\) and \(v=2k\), \(0\le k\le m\), then

\[
\frac{p_{2m}(2k)}{p_{2m}(0)}
=\prod_{j=1}^k\frac{m-j+1}{m+j}
\le \exp\!\left(-\sum_{j=1}^k\frac{2j-1}{2m}\right)
=e^{-v^2/(4n)}.
\]

Here \(1-a\le e^{-a}\) and \(m+j\le2m\) were used. By (2), \(p_{2m}(0)\le\sqrt2/\sqrt n\).

If \(n=2m+1\) and \(v=2k+1\), \(0\le k\le m\), then

\[
\frac{p_{2m+1}(2k+1)}{p_{2m+1}(1)}
=\prod_{j=1}^k\frac{m-j+1}{m+j+1}
\le e^{-k(k+1)/n}
=e^{-(v^2-1)/(4n)}.
\]

Also

\[
p_{2m+1}(1)=\frac{2m+1}{2m+2}p_{2m}(0)
\le(m+1)^{-1/2}\le\sqrt2/\sqrt n.
\]

Finally \(\sqrt2 e^{1/(4n)}\le\sqrt2e^{1/4}<2\), proving (1). The last strict inequality follows, for example, from \(e^{1/2}<\sum_{j\ge0}(1/2)^j=2\).

## 2. Exact third-difference identity

Set \(n=t+3\) and \(v=u+3\). Then, for every integer \(u\),

\[
\Delta_2^3p_t(u)
=-\frac{8\{v^3-(3n-2)v\}}{(t+1)(t+2)(t+3)}p_n(v). \tag{3}
\]

On wrong parity both sides vanish. On the correct parity, put \(k=(n+v)/2\). The coefficient of \(z^k\) in \((z-1)^3(z+1)^{n-3}\) is

\[
\sum_{j=0}^3(-1)^{3-j}\binom3j\binom{n-3}{k-j}
=\frac{\binom nk}{n(n-1)(n-2)}
\sum_{j=0}^3(-1)^{3-j}\binom3j(k)_j(n-k)_{3-j},
\]

where \((a)_j=a(a-1)\cdots(a-j+1)\). Expanding the final cubic gives

\[
(2k-n)^3-(3n-2)(2k-n).
\]

Changing the index \(j\) to \(3-j\) shows that \(\Delta_2^3p_t(u)\) is minus \(2^{-t}\) times this coefficient, proving (3). At \(k<0\) or \(k>n\), both the coefficient and the finite difference vanish, so the support edges introduce no exception.

## 3. Explicit constant, with the uncentered Gaussian

Let \(r=|v|/\sqrt n\). From (1), (3), \((t+1)(t+2)(t+3)\ge t^3\), and \(n/t\le19/16\) for \(t\ge16\),

\[
|\Delta_2^3p_t(u)|
\le \frac{16n}{t^3}(r^3+3r)e^{-r^2/4}
\le19t^{-2}(r^3+3r)e^{-r^2/4}. \tag{4}
\]

Since \(u=v-3\),

\[
\frac{u^2}{32t}\le\frac{2v^2+18}{32t}
\le\frac{19r^2}{256}+\frac9{256}.
\]

Consequently (4), multiplied by \(e^{u^2/(32t)}\), is at most

\[
19e^{9/256}t^{-2}(r^3+3r)e^{-r^2/8}.
\]

Elementary differentiation yields

\[
\sup_{r\ge0} r^3e^{-r^2/8}=12^{3/2}e^{-3/2}<42,
\qquad
\sup_{r\ge0}3re^{-r^2/8}=6e^{-1/2}<6.
\]

Moreover \(19e^{9/256}\le19/(1-9/256)=4864/247<20\). The resulting constant is less than \(20(42+6)=960<1024\), as claimed.

No external probabilistic or analytic theorem is used here: only binomial coefficients, finite algebra, the elementary exponential inequality, and one-variable differentiation.

## Lamp and coupling observations

For the chain in the task and every \(t\ge1\), conditional on the complete base path, the final lamps are independent fair bits at precisely the visited sites, and are zero elsewhere. In one dimension the visited sites form the integer interval between the path minimum and maximum. This follows by selecting, for each visited site, its last independent resampling coin; each site has at least one such coin, including the initial site at time zero's first switch and the arrival site at the last switch. This representation is not valid at \(t=0\), where the initial lamp is forced zero.

If one adds independent fair initial lamps at any fixed finite set \(F\), a coupling with the original initialization can use identical base paths and resampling coins. Every initial discrepancy at \(a\in F\) disappears at the first visit to \(a\), so the final-state disagreement probability is at most \(\sum_{a\in F}\Pr(T_a>t)\). This is an optional reduction, not needed if the full visited-range law is treated directly.

Naive reflection coupling of the bases started at 0 and 2 meets at 1. It does not automatically couple the lamps, because its premeeting visited intervals are mirror images and may contain different sites. Any upper bound based only on the base meeting time leaves this obligation unresolved.
