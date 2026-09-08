# Proof of Q9

**Q9 is true.** In fact, C2 and C3 already suffice: on the stated domain,
\[
Q_{\rm quad}>0\quad\Longrightarrow\quad r<c^2/4
\quad\Longrightarrow\quad
c^2-r>k(1-c^2)r\sin^2 B.
\tag{1}
\]
The last inequality implies the requested strict conclusion. The proof below includes a standalone exact integer certificate for one polynomial inequality. It uses no numerical approximations or floating-point evidence.

Throughout, let
\[
m>1,\quad \frac23<c<1,\quad 0<r<c^2,\quad 0<g<B<\frac\pi2,
\]
\[
k=m^2-1,\quad e=1-c^2,\quad t=\sqrt r,\quad
H(z)=\arctan(m\tan z),\quad
A=\arcsin(t\sin B),\quad d=\arcsin(t\sin g).
\]
All branches are the principal branches specified in the question. In particular, \(0<d<A<B<\pi/2\) and \(d<g\). We retain the exact constraints
\[
H(B)=(1-c)\pi+cH(A),\qquad
H(d)+H(g)/c=\pi/2,\qquad B-g=c(A+d).
\]
The proof does not require the first of these; it therefore applies, in particular, when all three hold. No additional constraint is introduced.

Set
\[
V=\pi+H(g)-H(B)+m(B-g),\qquad
U=(\pi-H(B))\sin^2B+H(g)\sin^2g,
\]
and use the question's expression
\[
Q=\frac{c\cos B-t\cos A}{\sin B}
-\frac{ck(1-t^2)^2\sin g\cos d\cos g}
{\cos d(1+k\sin^2g)+ct\cos g(1+kt^2\sin^2g)}.
\tag{2}
\]

## 1. The range \(t\le c/2\)

We prove, using only C2 and C3, that
\[
0<t\le c/2\quad\Longrightarrow\quad
ke t^2\sin^2B<c^2-t^2.
\tag{3}
\]
Write \(s_g=\sin g\). From C2,
\(H(g)=c(\pi/2-H(d))\). Strict convexity of \(\tan\) on \([0,\pi/2)\), together with \(0<c<1\), gives
\[
m\tan g
=\tan\bigl(c(\pi/2-H(d))\bigr)
<c\tan(\pi/2-H(d))=\frac{c}{m\tan d}.
\]
All arguments and factors here are positive. Since \(\tan d=t\sin g/\cos d\),
\[
m^2t\sin^2g<c\cos g\cos d<c,
\qquad k\sin^2g<c/t.
\tag{4}
\]

Concavity of sine gives \(\sin(tz)\ge t\sin z\) for \(0<t<1\) and \(0<z<\pi/2\); consequently \(\arcsin(t\sin z)\le tz\). C3 therefore implies
\[
B-g\le ct(B+g),\qquad
\frac Bg\le\frac{1+ct}{1-ct}.
\]
The function \(\sin z/z\) is strictly decreasing on this interval: \(\sin z-z\cos z\) vanishes at zero and has derivative \(z\sin z>0\). Hence
\[
\frac{\sin B}{\sin g}<\frac Bg\le\frac{1+ct}{1-ct}.
\]
Together with (4), this yields
\[
ke t^2\sin^2B<ec t\left(\frac{1+ct}{1-ct}\right)^2
\le \frac{ec^2}{2}\left(\frac{2+c^2}{2-c^2}\right)^2.
\tag{5}
\]
The last step uses \(t\le c/2\); each positive factor in
\(t((1+ct)/(1-ct))^2\) increases with \(t\).
For \(x=c^2\in(0,1)\), the exact identity
\[
3(2-x)^2-2(1-x)(2+x)^2=(3x-2)^2+2x^3>0
\]
shows that the last expression in (5) is strictly less than \(3c^2/4\), which is at most \(c^2-t^2\). This proves (3).

## 2. Excluding \(t\ge c/2\) when \(Q>0\)

Suppose, for a contradiction, that \(Q>0\) and \(c/2\le t<c\). Define
\[
X=\tan B,\quad z=\tan g,\quad h=mz,\quad
L=\sqrt{1+(1-t^2)X^2},\quad
w=\sqrt{1+(1-t^2)z^2},\quad u=ct,
\]
\[
a=c\bigl(1+(c^2+2)t^2\bigr),\qquad
b=t\bigl(1+2c^2+c^2t^2\bigr),\qquad
J=\frac{49}{100}(1+c)^2,\qquad
j=\frac{Jw^2}{(w+u)^2}.
\tag{6}
\]
Thus \(X>z>0\), \(L>w>1\), \(h>z\), and \(0<u<1\).

**A consequence of C3.** Since \(0<A+d<\pi\), strict concavity of sine on \([0,\pi]\) gives
\[
\sin(B-g)=\sin(c(A+d))>c\sin(A+d).
\]
Writing both sides with denominator \(\sqrt{(1+X^2)(1+z^2)}\) gives
\[
X-z>ct(Xw+zL).
\tag{7}
\]
In particular \(1-uw>0\) and
\(X/z>(1+uL)/(1-uw)\). Squaring this positive inequality and using
\(L^2-1=(1-t^2)X^2\), \(w^2-1=(1-t^2)z^2\), gives
\[
\begin{aligned}
0&<(L^2-1)(1-uw)^2-(w^2-1)(1+uL)^2\\
 &=(L+w)\bigl((1+u^2)(L-w)-2u(Lw-1)\bigr).
\end{aligned}
\]
Put \(D=1+u^2-2uw\) and \(N=(1+u^2)w-2u\).
Here \(N>(1-u)^2>0\); the preceding inequality says \(LD>N\), so \(D>0\) and \(L>N/D\).

The first term of (2) is \(P=(c-tL)/X\). Its subtracted term is strictly positive, so \(Q>0\) implies \(c-tL>0\). Equation (7) now implies
\[
Pz<\frac{(c-tL)(1-uw)}{1+uL}.
\]
The function \(\ell\mapsto(c-t\ell)/(1+u\ell)\) has derivative
\(-(t+uc)/(1+u\ell)^2<0\). Using \(L>N/D\) and
\(D+uN=(1-u^2)(1-uw)\), we obtain
\[
0<Pz<\frac{cD-tN}{1-u^2}
=\frac{a-bw}{1-u^2}=:f.
\tag{8}
\]
Thus
\[
1<w<a/b,
\qquad a-b=(c-t)(1-ct)^2>0.
\tag{9}
\]

**A consequence of C2.** We have
\(H(g)=\arctan h\), \(H(d)=\arctan(th/w)\).
The function \(\arctan x\) has negative second derivative for \(x>0\). Jensen's inequality with the positive weights \(c/(1+c)\), \(1/(1+c)\) is strict because \(t/w<1\). Consequently C2 gives
\[
\frac{c\pi}{2(1+c)}
=\frac{c\arctan(th/w)+\arctan h}{1+c}
<\arctan\left(\frac{h(1+ct/w)}{1+c}\right).
\]
Since \(c\ge2/3\), the expression on the left is at least \(\pi/5\). Therefore
\[
h>\frac{(1+c)w}{w+ct}\tan(\pi/5)
>\frac7{10}\frac{(1+c)w}{w+ct},
\qquad h^2>j.
\tag{10}
\]
Here the rational bound \(\tan(\pi/5)>7/10\) has an elementary exact verification. Set \(\theta=\arctan(7/10)\in(0,\pi/4)\). The five-angle formulas give
\[
\frac{\sin5\theta}{\cos^5\theta}=\frac{23807}{100000}>0,
\qquad
\frac{\cos5\theta}{\cos^5\theta}=-\frac{5399}{2000}<0.
\]
Because \(0<5\theta<5\pi/4\), these signs force \(\pi/2<5\theta<\pi\). Thus \(\theta<\pi/5\), proving the stated bound.

**The polynomial inequality used below.** For every
\[
\frac23\le c<1,\qquad c/2\le t<c,\qquad 1\le w\le a/b,
\]
with (6), one has
\[
\begin{aligned}
E:={}&c(1-t^2)(1-u^2)
 \bigl((1-t^2)Jw^2-(w^2-1)(w+u)^2\bigr)\\
&-(a-bw)\bigl((1+uw)(w+u)^2+Jw(w+ut^2)\bigr)\ \ge0.
\tag{11}
\end{aligned}
\]
An exact, self-contained certificate for (11) is given in Section 4.

Direct substitution in (2) gives the identity
\[
Qz=Pz-
\frac{c(1-t^2)^2(h^2-z^2)}{1+uw+h^2(1+ut^2/w)}.
\tag{12}
\]
For \(x\ge0\), define
\[
K(x)=\frac{c(1-t^2)^2(x-z^2)}{1+uw+x(1+ut^2/w)}.
\]
Its denominator is positive and
\[
K'(x)=\frac{c(1-t^2)^2\bigl(1+uw+z^2(1+ut^2/w)\bigr)}
{\bigl(1+uw+x(1+ut^2/w)\bigr)^2}>0.
\]
Also \(z^2=(w^2-1)/(1-t^2)\). A common-denominator calculation gives
\[
K(j)-f=
\frac{E}{(1-u^2)\bigl((1+uw)(w+u)^2+Jw(w+ut^2)\bigr)}\ge0.
\tag{13}
\]
All factors in this denominator are positive. From (8), (10), and (12),
\[
Qz<f-K(h^2)<f-K(j)\le0,
\]
contrary to \(Q>0\) and \(z>0\). This proves \(Q>0\Rightarrow t<c/2\).

<a id="q9-proof"></a>

## 3. The requested conclusion

Combining Sections 1 and 2 proves (1). To verify its last implication directly, differentiation gives
\[
(H(z)-mz)'=-\frac{mk\sin^2z}{1+k\sin^2z},
\qquad
V=\pi+mk\int_g^B\frac{\sin^2z}{1+k\sin^2z}\,dz>\pi.
\]
Furthermore,
\[
V\sin^2B-U
=H(g)(\sin^2B-\sin^2g)+m(B-g)\sin^2B>0.
\]
Since \(U>0\), it follows that \(0<rU/V<r\sin^2B\). Equation (1), with \(ke>0\), therefore yields
\[
\boxed{\quad Q_{\rm quad}>0\ \Longrightarrow\
\frac{c^2-r}{ke}>r\sin^2B>\frac{rU}{V}=T_{\rm quad}.\quad}
\]
Equivalently, \(R_{\rm quad}>0\), as required.

## 4. Exact certificate for the polynomial inequality

This section proves (11) by expanding a polynomial in the nonnegative Bernstein basis. The executable certificate below uses only arbitrary-precision integers from the Python standard library. It has no external input, numerical tolerance, sampling step, or third-party dependency.

Put \(s=t/c\in[1/2,1)\), and define
\[
\alpha=1+(c^4+2c^2)s^2,\quad
\beta=s(1+2c^2+c^4s^2),\quad
\delta=(1-s)(1-c^2s)^2=\alpha-\beta.
\]
Thus \(a=c\alpha\), \(b=c\beta\), \(\beta>0\), \(\delta>0\).
Every \(w\in[1,a/b]\) is represented as
\[
w=1+\frac{\delta}{\beta}\zeta,\qquad 0\le\zeta\le1.
\]
Let
\[
F(c,s,\zeta)=\frac{100\beta^4}{c}
E\left(c,cs,1+\frac{\delta}{\beta}\zeta\right).
\tag{14}
\]
The denominators cancel, and \(F\) is an integer polynomial of respective degrees \((26,18,4)\). Its exact expression is constructed in the code below. Now form the integer polynomial
\[
G(\xi,\eta,\zeta)=3^{26}2^{18}
F\left(\frac{2+\xi}{3},\frac{1+\eta}{2},\zeta\right).
\tag{15}
\]
The desired parameter region maps into \([0,1]^3\).

For \(0\le i\le n\), write
\(B_i^n(x)=\binom ni x^i(1-x)^{n-i}\ge0\) on \([0,1]\).
The elementary identity
\[
x^p=\sum_{i=p}^n\frac{\binom ip}{\binom np}B_i^n(x)
\tag{16}
\]
follows by cancelling binomial coefficients and applying the binomial theorem to \((x+(1-x))^{n-p}\). Apply (16) independently to the three variables of \(G\).
The certificate calculates all its \(27\cdot19\cdot5=2565\) Bernstein coefficients, multiplied by the positive integer
\[
\prod_{n\in\{26,18,4\}}
\operatorname{lcm}\{\tbinom n0,\ldots,\tbinom nn\}.
\]
It verifies that **2,535 are positive and 30 are zero**. Hence every coefficient is nonnegative; (16) proves \(G\ge0\) on the cube. Equations (14)–(15), whose scaling factors are positive in the original domain, prove \(E\ge0\). The checker also verifies that every coefficient with first index zero is positive. Since \(\xi<1\), their contribution is positive (the other two Bernstein bases each sum to one), so it actually proves \(E>0\).

The following is the complete certificate and verifier. Running it prints the sign counts and a PASS result; it also asserts the stated degree. In the code, `A`, `B`, and `D` denote the polynomials \(\alpha,\beta,\delta\), respectively.

```python
#!/usr/bin/env python3
# Exact certificate for E >= 0. Standard library; integer arithmetic only.
from collections import defaultdict
from math import comb, lcm

class P(dict):
    def __add__(a, b):
        if not isinstance(b, P): b = P({(0, 0, 0): b})
        d = P(a)
        for k, v in b.items(): d[k] = d.get(k, 0) + v
        return P({k: v for k, v in d.items() if v})
    __radd__ = __add__
    def __neg__(a): return P({k: -v for k, v in a.items()})
    def __sub__(a, b): return a + -b
    def __rsub__(a, b): return -a + b
    def __mul__(a, b):
        if not isinstance(b, P):
            return P({k: v*b for k, v in a.items() if v*b})
        d = defaultdict(int)
        for (i,j,k), v in a.items():
            for (l,m,n), w in b.items(): d[i+l,j+m,k+n] += v*w
        return P({k: v for k, v in d.items() if v})
    __rmul__ = __mul__
    def __pow__(a, n):
        r = P({(0, 0, 0): 1})
        while n:
            if n & 1: r = r*a
            a = a*a
            n //= 2
        return r

c, s, z = (P({e: 1}) for e in ((1,0,0),(0,1,0),(0,0,1)))
t2, u = c*c*s*s, c*c*s
A = 1 + (c**4 + 2*c*c)*s*s
B = s*(1 + 2*c*c + c**4*s*s)
D = (1-s)*(1-u)**2
assert A-B == D
W, J100 = B + D*z, 49*(1+c)**2
V = W + u*B
F = ((1-t2)*(1-u*u)*((1-t2)*J100*W*W*B*B
     - 100*(W*W-B*B)*V*V)
     - D*(1-z)*(100*B*(B+u*W)*V*V
     + J100*W*(W+u*t2*B)*B*B))
N = (26,18,4)
assert tuple(max(e[a] for e in F) for a in range(3)) == N
assert len(F) == 637

# G(x,y,z) = 3**26 * 2**18 * F((2+x)/3,(1+y)/2,z).
G = defaultdict(int)
for (a,b,k), v in F.items():
    for i in range(a+1):
        vi = v*comb(a,i)*2**(a-i)*3**(26-a)
        for j in range(b+1): G[i,j,k] += vi*comb(b,j)*2**(18-b)
G = {e: v for e, v in G.items() if v}
assert len(G) == 2103

# Convert power coefficients to Bernstein coefficients, with positive
# common scale L = product_a lcm_{0<=i<=N[a]} binom(N[a],i).
C, L = G, 1
for axis, n in enumerate(N):
    ell = lcm(*(comb(n,i) for i in range(n+1)))
    L *= ell
    out = defaultdict(int)
    for e, v in C.items():
        i = e[axis]
        for k in range(i,n+1):
            f = list(e); f[axis] = k
            out[tuple(f)] += v*comb(k,i)*(ell//comb(n,i))
    C = dict(out)
index = [(i,j,k) for i in range(27) for j in range(19) for k in range(5)]
values = [C.get(e,0) for e in index]
assert len(values) == 2565
assert sum(v > 0 for v in values) == 2535
assert sum(v == 0 for v in values) == 30
assert all(v >= 0 for v in values)
assert all(C[i,j,k] > 0 for i,j,k in index if i == 0)
assert all((C.get((i,j,k),0) == 0) == (i+j >= 42) for i,j,k in index)

# Independently invert the basis change and check the exact identity.
back = C
for axis, n in enumerate(N):
    out = defaultdict(int)
    for e, v in back.items():
        k = e[axis]
        for i in range(k,n+1):
            f = list(e); f[axis] = i
            out[tuple(f)] += v*comb(n,k)*comb(n-k,i-k)*(-1)**(i-k)
    back = {e: v for e, v in out.items() if v}
assert back == {e: v*L for e, v in G.items()}
print('PASS: exact Bernstein identity; 2535 positive, 30 zero; E > 0 for c < 1.')
```

No conjectural step or numerical evidence is used in this proof. The computation in Section 4 is a finite exact algebraic certificate. Lean formalization is not claimed.
