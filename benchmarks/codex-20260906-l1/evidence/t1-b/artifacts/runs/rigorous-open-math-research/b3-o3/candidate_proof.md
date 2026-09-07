# Exact proof of the B3 O3 root count

For every integer \(n\ge1\) and every \(R>1\), the assertion is true:
\(G_{n,s}\) has exactly \(2n\) zeros in \((0,\pi)\), all simple.
Here \(s=\sqrt R>1\). We prove the polynomial formulation as well.

Put
\[
r=s^{-1},\qquad h=s+s^{-1},\qquad K=h+2=\frac{(s+1)^2}{s},
\qquad z(x)=\frac{Kx^2-h}{2}.
\]
In particular \(0<r<1\), \(h>2\), and \(K>0\).

## O1: Matrix recurrence

Write \(c=\cos y\), \(q=\sin y\), and \(C=C_s(y)\). Direct expansion gives
\[
\begin{aligned}
\det C
&=(c^2-rq^2)(c^2-sq^2)+(1+r)(1+s)c^2q^2\\
&=c^4+2c^2q^2+q^4=1,\\
\operatorname{tr}C
&=2c^2-hq^2=Kc^2-h=2z(c).
\end{aligned}
\]
For any real two-by-two matrix \(B\), entrywise multiplication proves
\(B^2-(\operatorname{tr}B)B+(\det B)I=0\). Thus
\[
C^2-2z(c)C+I=0.
\]
For fixed \(y\), set \(g_m=(E(y)C^m)_{12}\), also allowing \(m=0\).
Multiplying the last identity by \(E(y)C^{m-2}\) gives, for \(m\ge2\),
\[
g_m=2z(c)g_{m-1}-g_{m-2}.
\]
The two initial values follow from direct multiplication:
\[
g_0=q,\qquad
g_1=q\big((2+r)c^2-sq^2\big)
   =q(Kc^2-s)=q(2z(c)+r).
\]

## O2: Polynomial representation and degree

Define real polynomials by
\[
U_{-1}(z)=0,\quad U_0(z)=1,\quad
U_m(z)=2zU_{m-1}(z)-U_{m-2}(z)\quad(m\ge1).
\]
Set \(P_m(z)=U_m(z)+rU_{m-1}(z)\) for \(m\ge0\).
Then \(P_0=1\), \(P_1=2z+r\), and
\(P_m=2zP_{m-1}-P_{m-2}\) for \(m\ge2\).
Induction using O1 therefore proves the identity, for every real \(y\),
\[
\boxed{G_{n,s}(y)=\sin y\,P_n(z(\cos y)).} \tag{1}
\]
For \(-1<x<1\), \(\sin(\arccos x)=\sqrt{1-x^2}>0\).
Consequently the function in the question equals
\[
\boxed{Q_{n,s}(x)=P_n\!\left(\frac{Kx^2-h}{2}\right).} \tag{2}
\]
The right side defines a polynomial on all of \(\mathbb R\), so it is a
polynomial extension of the prescribed function. It is the unique such
extension, since two polynomials agreeing on an interval have zero difference.

The recurrence shows inductively that \(U_m\) has degree \(m\) and leading
coefficient \(2^m\) for \(m\ge0\). Hence \(P_n\) has degree \(n\) and leading
coefficient \(2^n\), while \(Q_{n,s}\) is even, has degree exactly \(2n\),
and has leading coefficient \(2^n(K/2)^n=K^n>0\).

## O3: Exact location and simplicity of the scalar roots

We prove the needed polynomial root fact directly. The sine addition formula
and the defining recurrence give, by induction, for \(0<\theta<\pi\),
\[
U_m(\cos\theta)=\frac{\sin((m+1)\theta)}{\sin\theta}
\quad(m\ge0).
\]
The same recurrence at the endpoints gives
\[
U_m(1)=m+1,\qquad U_m(-1)=(-1)^m(m+1).
\]
For \(k=1,\ldots,n\), put
\[
t_k=\cos\frac{k\pi}{n+1}.
\]
These satisfy \(-1<t_n<\cdots<t_1<1\). The trigonometric identity yields
\[
U_n(t_k)=0,\qquad U_{n-1}(t_k)=(-1)^{k+1},\qquad
P_n(t_k)=r(-1)^{k+1}. \tag{3}
\]
Also
\[
P_n(-1)=(-1)^n\big((n+1)-rn\big), \tag{4}
\]
whose bracket is positive because \(0<r<1\).
Thus \(P_n\) has opposite, nonzero signs at the endpoints of each of the
following \(n\) pairwise disjoint open intervals:
\[
(-1,t_n),\qquad (t_{k+1},t_k)\quad(1\le k\le n-1). \tag{5}
\]
For \(n=1\), only the first interval occurs.

We use the intermediate value theorem in this form: a continuous real
function on \([a,b]\), with \(a<b\) and opposite signs at \(a,b\), has a
zero in \((a,b)\). Here each function is a real polynomial, so is continuous,
and (3)--(4) check the sign hypotheses on every interval (5). We obtain
\(n\) distinct real roots \(\zeta_1,\ldots,\zeta_n\), all in \((-1,1)\).

For completeness, the algebraic fact used to finish the count is the factor
theorem: if a real polynomial \(p\) satisfies \(p(a)=0\), division by
\(z-a\) has zero remainder. Repeated division at distinct roots implies that
their product divides \(p\). Since \(P_n\) has degree exactly \(n\),
\[
P_n(z)=2^n\prod_{j=1}^n(z-\zeta_j). \tag{6}
\]
In particular these are all its roots and every root is simple:
\(P_n'(\zeta_j)=2^n\prod_{i\ne j}(\zeta_j-\zeta_i)\ne0\).
The same factor argument justifies the uniqueness assertion in O2.

## O4: Pullback, complete count, and simplicity for G

Define
\[
a_j=\frac{h+2\zeta_j}{K}\qquad(1\le j\le n).
\]
Since \(-1<\zeta_j<1\) and \(h>2\),
\[
0<\left(\frac{s-1}{s+1}\right)^2
 =\frac{h-2}{h+2}<a_j<\frac{h+2}{h+2}=1. \tag{7}
\]
The \(a_j\) are distinct because the map from \(\zeta_j\) is strictly
increasing. Combining (2) and (6) gives the exact factorization
\[
\boxed{Q_{n,s}(x)=K^n\prod_{j=1}^n(x^2-a_j).} \tag{8}
\]
It has precisely the \(2n\) distinct real roots
\(x=\pm\sqrt{a_j}\), all in \((-1,1)\). More precisely every one satisfies
\[
\frac{s-1}{s+1}<|x|<1.
\]
Each root is simple. For example, the chain rule at a root gives
\[
Q_{n,s}'(x)=KxP_n'(z(x))\ne0,
\]
because \(K>0\), \(x\ne0\), and \(z(x)\) is a simple root of \(P_n\).

On \((0,\pi)\), cosine is a bijection onto \((-1,1)\), and sine is
strictly positive. Identity (1) therefore gives a bijection between the roots
of \(Q_{n,s}\) in \((-1,1)\) and the roots of \(G_{n,s}\) in \((0,\pi)\).
At any such root \(y_0\), differentiating (1) gives
\[
G_{n,s}'(y_0)
=\cos y_0\,Q_{n,s}(\cos y_0)
 -\sin^2y_0\,Q_{n,s}'(\cos y_0)
=-\sin^2y_0\,Q_{n,s}'(\cos y_0)\ne0.
\]
This proves exactly \(2n\) interior zeros, all simple, uniformly for all
\(n\ge1\) and \(R>1\).

## O5: Separate audits of the required cases

- **\(n=1\).** Direct multiplication already gives
  \[
  G_{1,s}(y)=\sin y\,(K\cos^2y-s),\qquad Q_{1,s}(x)=Kx^2-s.
  \]
  Its roots are \(x=\pm s/(s+1)\), both strictly between \(-1\) and \(1\)
  and nonzero. Thus the two interior zeros are
  \(y=\arccos(s/(s+1))\) and \(\pi-\arccos(s/(s+1))\).
  At either, \(G_{1,s}'(y)=-2K\cos y\sin^2y\ne0\).

- **\(y=0\).** Here \(E=I\), \(C=I\), hence \(G_{n,s}(0)=0\).
  This endpoint is excluded. In addition,
  \[
  Q_{n,s}(1)=P_n(1)=n+1+\frac ns>0,\qquad
  G_{n,s}'(0)=n+1+\frac ns.
  \]

- **\(y=\pi\).** Here \(E=-I\), \(C=I\), hence \(G_{n,s}(\pi)=0\).
  This endpoint is excluded. Evenness gives
  \[
  Q_{n,s}(-1)=n+1+\frac ns,\qquad
  G_{n,s}'(\pi)=-\left(n+1+\frac ns\right).
  \]
  Thus neither \(x=1\) nor \(x=-1\) is a polynomial root.

- **\(y=\pi/2\).** Directly,
  \[
  E=\begin{pmatrix}0&1\\-1&0\end{pmatrix},\qquad
  C=\begin{pmatrix}-s^{-1}&0\\0&-s\end{pmatrix},
  \qquad G_{n,s}(\pi/2)=(-s)^n\ne0.
  \]
  Accordingly \(Q_{n,s}(0)=(-s)^n\ne0\).

- **Boundary \(R=1\), hence \(s=1\).** Directly \(C_1(y)=E(2y)\).
  The sine and cosine addition formulas give \(E(a)E(b)=E(a+b)\), whence
  \[
  M_{n,1}(y)=E((2n+1)y),\qquad G_{n,1}(y)=\sin((2n+1)y).
  \]
  Its interior zeros are exactly
  \(y=k\pi/(2n+1)\), \(k=1,\ldots,2n\); their derivatives are
  \((2n+1)(-1)^k\ne0\). Its endpoint zeros remain excluded, and
  \(G_{n,1}(\pi/2)=(-1)^n\ne0\).
  The quotient has polynomial extension
  \(Q_{n,1}(x)=U_{2n}(x)\), of degree \(2n\) with leading coefficient
  \(2^{2n}\); its \(2n\) roots are the distinct numbers
  \(\cos(k\pi/(2n+1))\), all in \((-1,1)\), so are simple by the factor theorem.

All conclusions above are exact proofs. No numerical scan, conjectural
assertion, spectral theorem, or external literature result is used. The only
root-existence theorem invoked is the intermediate value theorem, with its
hypotheses checked above; the root count and multiplicities use the stated
factor theorem. There is no remaining mathematical gap.
