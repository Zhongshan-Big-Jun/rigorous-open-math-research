CANDIDATE_COMPLETE_PROOF

# Fourier derivative decay: claim O3-F

## Exact contract and provenance

For every integer \(t\ge32\), define, for every real \(x\),
\[
 f_t(x)=\frac1\pi\int_{-\pi/2}^{\pi/2}
           \cos(\theta)^t e^{ix\theta}\,d\theta.
\]
Then the following explicit constant works:
\[
 \boxed{A=\frac{8\,526\,336}{\pi}}.
\]
Precisely,
\[
 |f_t'''(x)|\le A t^{-2}
       \left(1+\frac{|x|}{\sqrt t}\right)^{-6}
       \qquad(t\in\mathbb Z,\ t\ge32,\ x\in\mathbb R).
\tag{F}
\]
The constant has no dependence on \(t\) or \(x\). The real-valuedness of
\(f_t\) follows by cancellation of the odd imaginary part of its integrand,
although the proof also works with complex absolute values.

Source contract: `runs/u2/analytic_packet.md`, claim O3-F. The parent supplied
the raw Gaussian estimate and the proposed six-integration-by-parts route.
This worker supplied the coefficient majorant and its explicit integral bound.
Only this packet and the applicable rigorous-open-math-research skill and
phase instructions were read. No external source, other project, repository
history, session, or memory was consulted. No computation supports the proof.
No novelty claim is made. This is a claim-local candidate proof, pending the
parent's independent audit; it does not claim completion of the parent theorem.

## Dependency chain and closure record

1. D1: elementary trigonometric bounds and exact odd Gaussian moments,
   derived below.
2. D2: an explicit coefficient bound for \(D^m\cos^t\), \(0\le m\le6\),
   derived by induction below.
3. D3: \(\|D^6(\theta^3\cos^t\theta)\|_{L^1[-\pi/2,\pi/2]}
   \le133224t\), proved from D1 and D2.
4. D4: six integrations by parts, with all endpoint terms proved zero.
5. D5: combination with the raw estimate, including \(x=0\), proves (F).

The first open load-bearing obligation received from the parent was D3.
The direct attempt closes it. Cheap exact falsification/boundary probes:
the derivative recurrence reproduces
\(D\cos^t=-t\sin\theta\cos^{t-1}\theta\) and
\(D^2\cos^t=-t\cos^t+t(t-1)\sin^2\theta\cos^{t-2}\theta\);
the least allowed exponent in the six-derivative argument is \(t-6\ge26\);
and the integration-by-parts bound is used only for \(x\ne0\).
No contradiction was found in these exact checks.

Gate decision: `CLOSED` for claim O3-F at candidate-proof level.
Decision delta: the previously unsupported sixth-derivative integral estimate
is replaced by a complete explicit bound, so O3-F is ready for independent
audit and assembly. No escalation or additional route is needed for this claim.

## Proof

### D1. Elementary bounds and moments

On \((-\pi/2,\pi/2)\),
\[
 \log\cos\theta\le-\theta^2/2.
\tag{1}
\]
Indeed, for \(\theta\ge0\), the derivative of
\(\log\cos\theta+\theta^2/2\) is \(-\tan\theta+\theta\le0\):
\(\tan0=0\) and \((\tan\theta)'=\sec^2\theta\ge1\).
The expression is even and zero at zero, proving (1). Continuity extends
\(\cos\theta\le e^{-\theta^2/2}\) to the endpoints.
Also \(|\sin\theta|\le|\theta|\), by the mean-value theorem and
\(|\cos\theta|\le1\).

For every positive integer \(q\) and every \(t>0\), substitution
\(u=t\theta^2/4\) gives
\[
 \int_{\mathbb R}|\theta|^{2q-1}e^{-t\theta^2/4}\,d\theta
 =\left(\frac4t\right)^q(q-1)!.
\tag{2}
\]
The identity \(\int_0^\infty u^{q-1}e^{-u}\,du=(q-1)!\) used here
follows by integration by parts starting with
\(\int_0^\infty e^{-u}\,du=1\). All boundary terms vanish; the limit of
\(u^n e^{-u}\) is zero because, for \(u>0\),
\(e^{u/2}\ge (u/2)^{n+1}/(n+1)!\) and \(e^{-u/2}\le1\).
Consequently, the five moment constants for powers \(p=1,3,5,7,9\) are
\[
 M_1=4,\quad M_3=16,\quad M_5=128,\quad
 M_7=1536,\quad M_9=24576,
\tag{3}
\]
where \(\int_{\mathbb R}|\theta|^p e^{-t\theta^2/4}\,d\theta
=M_p t^{-(p+1)/2}\).

### D2. Derivative coefficient majorant

Write \(c=\cos\theta\) and \(s=\sin\theta\). For \(0\le m\le6\),
there are coefficients \(b_{m,r}(t)\), supported on
\(0\le r\le m\) with \(r\equiv m\pmod2\), such that
\[
 D^m c^t=\sum_r b_{m,r}(t)s^r c^{t-r}.
\tag{4}
\]
To prove this, start with \(b_{0,0}=1\) and differentiate each summand using
\[
 D(s^r c^{t-r})
  =r s^{r-1}c^{t-r+1}-(t-r)s^{r+1}c^{t-r-1}.
\]
With missing coefficients interpreted as zero, this yields the recurrence
\[
 b_{m+1,r}(t)=(r+1)b_{m,r+1}(t)
                    -(t-r+1)b_{m,r-1}(t).
\tag{5}
\]
All powers used are nonnegative integers since \(t\ge32\) and \(r\le6\).

Define nonnegative integers \(H_{m,r}\) by
\(H_{0,0}=1\), zero outside the same support, and
\[
 H_{m+1,r}=(r+1)H_{m,r+1}+H_{m,r-1}.
\tag{6}
\]
Their needed values, all obtained directly from (6), are:

| \(m\) | Nonzero pairs \((r,H_{m,r})\) |
|---|---|
| 0 | \((0,1)\) |
| 1 | \((1,1)\) |
| 2 | \((0,1),(2,1)\) |
| 3 | \((1,3),(3,1)\) |
| 4 | \((0,3),(2,6),(4,1)\) |
| 5 | \((1,15),(3,10),(5,1)\) |
| 6 | \((0,15),(2,45),(4,15),(6,1)\) |

Induction in (5) gives
\[
 |b_{m,r}(t)|\le H_{m,r}t^{(m+r)/2}.
\tag{7}
\]
For the induction step, the first term of (5) is at most
\((r+1)H_{m,r+1}t^{(m+r+1)/2}\). For every nonzero second term,
\(0\le r-1\le m\le5\), so \(0\le t-r+1\le t\); that term is at most
\(H_{m,r-1}t^{(m+r+1)/2}\). Their sum is exactly the right-hand
side of (7) at index \((m+1,r)\), by (6).

For \(r\le6\), we have \(t-r\ge t/2\), so (1) and \(|s|\le|\theta|\)
give, first in the interior and then by continuity at the endpoints,
\[
 \boxed{
 |D^m\cos^t\theta|
  \le e^{-t\theta^2/4}
       \sum_r H_{m,r}t^{(m+r)/2}|\theta|^r
       \quad(0\le m\le6).
 }
\tag{8}
\]
The sum contains only the values of \(r\) displayed in the table.

### D3. The sixth-derivative integral

Set \(h(\theta)=\theta^3\cos^t\theta\). The product rule gives
\[
 h^{(6)}(\theta)
 =\sum_{j=0}^3 a_j\theta^{3-j}D^{6-j}\cos^t\theta,
 \qquad (a_0,a_1,a_2,a_3)=(1,18,90,120).
\tag{9}
\]
Here \(a_j=\binom6j3!/(3-j)!\); derivatives of \(\theta^3\) of order
larger than three vanish. In the term indexed by \(j,r\), put
\(m=6-j\) and \(p=3-j+r\). This \(p\) is a positive odd integer at
most nine. Equations (2) and (8), and extension of the nonnegative integral
to the real line, give
\[
\begin{aligned}
 \int_{-\pi/2}^{\pi/2}|\theta|^{3-j}
                   |D^{6-j}\cos^t\theta|\,d\theta
 &\le\sum_r H_{6-j,r} t^{(6-j+r)/2}
       M_{3-j+r}t^{-(4-j+r)/2}\\
 &=t\sum_r H_{6-j,r}M_{3-j+r}.
\end{aligned}
\tag{10}
\]
The exponent in every summand is exactly one, not merely bounded
asymptotically. All constants are explicit:

| \(j\) | \(\sum_r H_{6-j,r}M_{3-j+r}\) | Product with \(a_j\) |
|---|---|---|
| 0 | \(15\cdot16+45\cdot128+15\cdot1536+24576=53616\) | \(53616\) |
| 1 | \(15\cdot16+10\cdot128+1536=3056\) | \(55008\) |
| 2 | \(3\cdot4+6\cdot16+128=236\) | \(21240\) |
| 3 | \(3\cdot4+16=28\) | \(3360\) |

Summing (9)--(10) therefore proves
\[
 \boxed{\int_{-\pi/2}^{\pi/2}|h^{(6)}(\theta)|\,d\theta
        \le133224t.}
\tag{11}
\]

### D4. Differentiation and integration by parts

Differentiation under the defining integral for \(f_t\) is valid three
times: each differentiated integrand is continuous in \((x,\theta)\) and
bounded in modulus by \(|\theta|^k\) for \(k\le3\), an integrable function
on the fixed finite interval. The dominated differentiation theorem
(a difference-quotient consequence of dominated convergence) gives
\[
 f_t'''(x)=\frac{-i}{\pi}
              \int_{-\pi/2}^{\pi/2}h(\theta)e^{ix\theta}\,d\theta.
\tag{12}
\]
Here the derivative bound for each difference quotient follows from
\(e^{i(x+a)\theta}-e^{ix\theta}
  =\int_0^a i\theta e^{i(x+u)\theta}\,du\).

For each \(0\le k\le5\), the product rule expresses \(h^{(k)}\) as a
finite sum of polynomials in \(\theta\) times \(D^q\cos^t\theta\), with
\(0\le q\le k\). Formula (4) shows that every latter summand contains
\(\cos^{t-r}\theta\) with \(r\le q\le5\). Since \(t-r\ge27>0\),
every such summand vanishes at \(\theta=\pm\pi/2\). Thus
\[
 h^{(k)}(-\pi/2)=h^{(k)}(\pi/2)=0\qquad(0\le k\le5).
\tag{13}
\]
Because \(t\) is an integer, \(h\) is smooth on the closed interval.
For \(x\ne0\), ordinary integration by parts six times in (12), with
(13) removing every boundary term, gives
\[
 |f_t'''(x)|\le\frac1{\pi|x|^6}
                  \int_{-\pi/2}^{\pi/2}|h^{(6)}(\theta)|\,d\theta
             \le\frac{133224}{\pi}\frac{t}{|x|^6}.
\tag{14}
\]

### D5. Uniform estimate and the point \(x=0\)

Directly from (1) and (12), for every real \(x\),
\[
 |f_t'''(x)|
 \le\frac1\pi\int_{\mathbb R}|\theta|^3e^{-t\theta^2/2}\,d\theta
 =\frac4\pi t^{-2}.
\tag{15}
\]
The last identity is (2) with \(q=2\) and with \(t\) replaced by \(2t\).
Put \(y=|x|/\sqrt t\) and \(B=133224/\pi\). Since \(B\ge4/\pi\),
(14)--(15) show, for \(y>0\),
\[
 |f_t'''(x)|\le B t^{-2}\min\{1,y^{-6}\}.
\]
For \(0<y\le1\), \((1+y)^6\le64\). For \(y\ge1\),
\((1+y)^6y^{-6}=(1+y^{-1})^6\le64\). Hence
\[
 \min\{1,y^{-6}\}\le64(1+y)^{-6}.
\]
The same resulting inequality holds at \(y=0\) directly from (15).
Thus (F) holds with
\(A=64B=8\,526\,336/\pi\), as claimed.

## Claim-local audit and exact remaining frontier

This worker performed a separate self-check of semantic fidelity, recurrence
indices, the Gaussian exponent, all four finite arithmetic rows, endpoint
orders, and the split between \(x=0\) and \(x\ne0\). The check found no
load-bearing gap. It is not an independent audit or Lean verification.

Exact mathematical dependencies: product and chain rules for elementary
smooth functions; the fundamental theorem of calculus and mean-value
theorem; substitution and integration by parts for one-dimensional
integrals; dominated convergence in the explicitly dominated
differentiation argument. The trigonometric and moment estimates and the
coefficient recurrence are proved here. No unverified external theorem
or numerical assertion is used.

Remaining gaps in O3-F: none identified in the candidate proof.
Remaining verification: independent review by the parent or its assigned
auditor; no formal verification is claimed.
Outside scope: the parent spectral small-interval estimate, its assembly
with O3-F, and the parent theorem's other obligations.
Failed routes: none; no alternate route was investigated.

Reproducibility: the proof is exact symbolic mathematics; no search code,
randomness, external data, compiler, repository state, or numerical check
is required. File writes used the provided `apply_patch` tool. The parent
can bind this file's SHA-256 in its package manifest. No repository command
was run because the delegated task forbids repository/history inspection.

Confidence by axis: semantic fidelity—checked against the supplied packet;
mathematical correctness—complete explicit derivation, self-checked,
independent audit pending; completeness—complete for O3-F only;
novelty—unassessed; reproducibility—self-contained exact proof.
