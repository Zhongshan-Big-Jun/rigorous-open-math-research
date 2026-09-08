# Search agent exact result and numerical leads

## Exact subdomain theorem

Let the problem's domain hold, and assume (C2) and (C3). If
`sqrt(r) <= 1-c`, then

\[
c^2-r-k(1-c^2)r\sin^2 B>0.
\]

Consequently the problem's Q9 conclusion holds without assuming `Q_quad>0` on this subdomain. Neither C1 nor a mass balance equation is used.

**Proof.** Put \(s=\sqrt r\), \(p=H_m(g)\). Constraint C2 says
\(H_m(d)=\pi/2-p/c\). The function \(x\mapsto\tan x/x\) is strictly increasing on \((0,\pi/2)\), because its derivative has numerator \(x\sec^2x-\tan x\), whose derivative is \(2x\sec^2x\tan x>0\) and whose limit at zero is zero. Hence
\[
m^2\tan d\tan g=\frac{\tan p}{\tan(p/c)}<c,
\quad\text{so}\quad
m^2s\sin^2g<c\cos d\cos g.
\]
For fixed \(0<s<1\), the function \(a(z)=\arcsin(s\sin z)\) has
\[
a''(z)=-\frac{s(1-s^2)\sin z}{(1-s^2\sin^2z)^{3/2}}<0
\quad(0<z<\pi/2).
\]
Since \(a(0)=0\), \(a'(0)=s\), this gives \(A<sB\) and \(d<sg\). C3 gives
\[
\frac Bg<\lambda:=\frac{1+cs}{1-cs}.
\]
The function \(\sin z/z\) is strictly decreasing on \((0,\pi/2)\), since \(\sin z-z\cos z>0\). Thus \(\sin B/\sin g<B/g<\lambda\). Consequently
\[
k(1-c^2)s^2\sin^2B
<m^2(1-c^2)s^2\lambda^2\sin^2g
<c(1-c^2)s\lambda^2.
\]
If \(s\le1-c\) and \(c\ge2/3\), then \(cs\le c(1-c)\le2/9\), so \(\lambda\le11/7\). Moreover
\(c(1-c^2)s\le c(1-c)^2(1+c)\le10/81\): the last polynomial is decreasing for \(c\in[2/3,1]\), as follows from its logarithmic derivative
\(1/c-2/(1-c)+1/(1+c)<0\).
Therefore
\[
k(1-c^2)r\sin^2B<\frac{1210}{3969}<\frac13\le 2c-1\le c^2-s^2.
\]
The supplied strict sufficient condition now proves Q9. \(\square\)

## Exact geometric Q upper bound

For all the problem's domain satisfying C3, put
\(s=\sqrt r\), \(t=\tan g\), \(v=k\sin^2g\), \(y=s\cos g/\cos d\), and \(\lambda=(1+cs)/(1-cs)\). Then
\[
Q_{\rm quad}\,t<
\frac{c-s\sqrt{1+\lambda^2(1-s^2)t^2}}{\lambda}
-\frac{c(1-s^2)^2v}{1+cy+v(1+cs^2y)}.
\]
Indeed, \(\sin(B-g)=\sin(c(A+d))>c\sin(A+d)>cs\sin(B+g)\); both strict inequalities follow from sine concavity and \(A<B,d<g\). Thus \(\tan B/\tan g>\lambda\). If \(z=t\cot B<1/\lambda\), the first term of \(Q_{\rm quad}\,t\) is
\(cz-s\sqrt{z^2+(1-s^2)t^2}\). This is strictly increasing in \(z>0\), because its derivative exceeds \(c-s>0\). Evaluating it at \(1/\lambda\) gives the asserted bound, and the displayed second term follows by cancelling \(\cos d\).

## Numerical evidence (not proof)

- `search_numeric.py` enforces C1 by parameterizing \(x=H_m(A)\in(0,\pi(1-1/(2c)))\), setting \(y=(1-c)\pi+cx\), then \(A=\arctan(\tan x/m)\), \(B=\arctan(\tan y/m)\), and \(r=\sin^2A/\sin^2B\). C2 is solved monotonically for g and C3 is solved for x. Initial 1000 random pairs produced 519 admissible roots, 92 with Q>0, 9 with R<0, no overlap. Every Q>0 point satisfied the supplied stronger sufficient condition.
- `search_boundary.py` finds Q=0 along the C1-C3 solution branch. Its large-m limit numerically is c≈0.722329296, r≈0.0239806605; target ratio is approximately 0.0614163. Numerical only.
- `search_relaxed.py` and additional scans sampled more than 400,000 triples (m,c,r) satisfying C2 and C3, with C1 dropped. No Q>0 point failed the stronger sufficient condition. Largest observed r for Q>0 was approximately 0.05946.
- C2 alone and C3 alone are insufficient for the stronger implication, as demonstrated by floating-point examples retained in `search_c2only_results.json` and `search_geometry_results.json`. Several C2-only samples also fail Q9 itself. These are not certified counterexamples to the original task and are used only to guide proof attempts.
- The exact upper bound above was negative in 150,000 tested C2 tuples with s≥1/3. When its positive first summand was nonzero, the ratio of the second summand to the first appeared bounded below by approximately 1.186199, approached at c=2/3,s=1/3,m→∞. No proof of this last assertion is known here.
