# Q9 is true

For every tuple in the stated domain satisfying all three exact constraints,
\[
Q_{\rm quad}>0\quad\Longrightarrow\quad R_{\rm quad}>0.
\]
In fact, the argument below proves the stronger conclusion
\[
S:=c^2-r-(m^2-1)(1-c^2)r\sin^2 B>0. \tag{1}
\]
The proof includes a finite certificate consisting entirely of rational
polynomial calculations. All certificate data and a complete verifier are
included below. Floating-point experiments play no role in the proof.

## 1. Definitions and the reduction to (1)

Assume throughout that
\[
m>1,\quad \frac23<c<1,\quad 0<r<c^2,\quad 0<g<B<\frac\pi2.
\]
Set \(s=\sqrt r\), \(k=m^2-1\), \(e=1-c^2\), and
\[
H(z)=\arctan(m\tan z),\quad F(z)=H(z)-mz,\qquad
A=\arcsin(s\sin B),\quad d=\arcsin(s\sin g).
\]
All inverse functions use the principal branches. We assume the three
constraints in the question, in particular
\[
H(d)+H(g)/c=\pi/2,\qquad B-g=c(A+d). \tag{2}
\]
The first constraint, \(H(B)=(1-c)\pi+cH(A)\), remains a hypothesis;
the stronger estimate (1) will follow already from the two identities (2).

For clarity, write the quantity whose positivity is assumed as
\[
Q=\frac{c\cos B-s\cos A}{\sin B}
-\frac{ck(1-s^2)^2\sin g\cos d\cos g}
 {\cos d(1+k\sin^2g)+cs\cos g(1+ks^2\sin^2g)}.
\]
Also set
\[
V=\pi+F(g)-F(B),\qquad
U=(\pi-H(B))\sin^2B+H(g)\sin^2g.
\]
Direct differentiation gives
\(F'(z)=-mk\sin^2z/(1+k\sin^2z)\), so \(V>\pi\).
Expansion of the definitions gives
\[
V\sin^2B-U
=H(g)(\sin^2B-\sin^2g)+m(B-g)\sin^2B>0. \tag{3}
\]
Consequently, (1) implies the required strict inequality because
\[
R_{\rm quad}
=(c^2-r)V-kerU
=SV+ker(V\sin^2B-U)>0. \tag{4}
\]
Thus it suffices to prove (1) whenever \(Q>0\).

## 2. Bounds obtained from the exact angular constraint

The following calculations apply on the entire domain above with
\(B-g=c(A+d)\). Define
\[
w=k\sin^2g,\quad K=\frac{1+cs}{1-cs},\quad
X=\cot B,\quad Y=\cot g,\quad v_0=1-s^2.
\]
All these quantities are positive.

For \(a(z)=\arcsin(s\sin z)\),
\[
0<a'(z)=\frac{s\cos z}{\sqrt{1-s^2\sin^2z}}\le s.
\]
Hence \(A\le sB\), \(d\le sg\), and the angular constraint gives
\(B/g\le K\). The function \(\sin z/z\) strictly decreases on
\((0,\pi/2)\): its derivative has numerator \(z\cos z-\sin z<0\),
as follows by differentiating that numerator from its value zero at zero.
Therefore
\[
\frac{\sin B}{\sin g}\le K. \tag{5}
\]

A second consequence retains more of the exact constraint. Since
\(0<A+d<\pi\) and \(0<c<1\), strict concavity of sine on
\([0,\pi]\) gives
\(\sin(c(A+d))>c\sin(A+d)\).
Use \(c(A+d)=B-g\), expand the two sines, and divide by
\(\sin B\sin g>0\). Because \(\sin A=s\sin B\) and
\(\sin d=s\sin g\), the result is
\[
Y-X>cs\bigl(\sqrt{Y^2+v_0}+\sqrt{X^2+v_0}\bigr). \tag{6}
\]
Both square roots exceed the corresponding positive cotangent. Thus
\((1+cs)X<(1-cs)Y\). If
\[
f=cX-s\sqrt{X^2+v_0}
=\frac{c\cos B-s\cos A}{\sin B},
\]
then
\[
f\tan g< L:=\frac{(c-s)(1-cs)}{1+cs}.
\]

Put \(\rho=s\cos g/\cos d\), so \(0<\rho<s\). The definition of
\(Q\) yields the exact identity
\[
Q\tan g=f\tan g-
\frac{c(1-s^2)^2w}{1+w+c\rho(1+s^2w)}.
\]
If \(Q>0\), it follows that
\[
L>\frac{c(1-s^2)^2w}{1+cs+(1+cs^3)w}.
\]
Define
\[
P=1+2c^2-3cs-3c^2s^2+c(2+c^2)s^3.
\]
The identity
\[
c(1-s^2)^2(1+cs)-(c-s)(1-cs)(1+cs^3)=sP
\]
allows this inequality to be rearranged. We first check its sign.
For fixed \(0<c<1\),
\[
P_s=3c\bigl((2+c^2)s^2-2cs-1\bigr)<0\quad(0\le s\le c).
\]
Indeed the bracket is convex in \(s\), with endpoint values \(-1\)
and \(c^4-1\), both negative. Therefore
\(P\ge P(c,c)=(1-c^2)(1-c^4)>0\). Division is legitimate, and gives
\[
w<W:=\frac{(c-s)(1-c^2s^2)}{sP}. \tag{7}
\]

## 3. The case \(0<s\le12/25\)

Combining (5) and (7), and using \(c^2-r=(c-s)(c+s)\), gives
\[
\frac{ker\sin^2B}{c^2-r}
<\frac{(1-c^2)s(1+cs)^3}{(c+s)(1-cs)P}.
\]
It is therefore enough that the polynomial
\[
E=(c+s)(1-cs)P-(1-c^2)s(1+cs)^3
\]
be positive. The following is an exact certificate for that positivity
on the closed rectangle \(2/3\le c\le1\), \(0\le s\le12/25\).
Let \(b_i^n(t)=\binom ni t^i(1-t)^{n-i}\). Then
\[
E\left(\frac{2+u}{3},\frac{12v}{25}\right)
=\frac1{1054687500}\sum_{i=0}^4\sum_{j=0}^5
N_{ij}b_i^4(u)b_j^5(v), \tag{8}
\]
where the rows of \(N\) are

```text
1328125000 1243125000 1051925000  765469000  412948680  12607112
1650390625 1534140625 1300215625  966327625  571546705 138478561
2050781250 1891406250 1603781250 1216202250  781848450 330011178
2548828125 2329453125 1972378125 1522315125 1052902845 604001061
3164062500 2860312500 2410762500 1885396500 1387790820 974492532
```

Every entry is positive. The Bernstein basis functions are nonnegative
on \([0,1]\) and sum to one. Thus \(E>0\) throughout the rectangle.
Identity (8) is a polynomial identity; the verifier in Section 6 checks
all of its coefficients exactly. We have proved (1) in this case.

## 4. The complementary range is incompatible with \(Q>0\)

We now show that (2) and \(Q>0\) force \(s<12/25\).
For this section suppose \(12/25\le s<c<1\).

The second term subtracted in \(Q\) is positive, so \(f>0\). Therefore
\[
X>X_0:=\frac{s\sqrt{1-s^2}}{\sqrt{c^2-s^2}}.
\]
All sides are positive, so this follows by squaring without changing
the orientation. From (6),
\[
Y-cs\sqrt{Y^2+v_0}>X+cs\sqrt{X^2+v_0}.
\]
The functions on both sides, viewed as functions of their respective
positive arguments, are strictly increasing. Solving the equality with
\(X=X_0\) gives
\[
Y>Y_0:=
\frac{s\sqrt{1-s^2}(1+2c^2+c^2s^2)}
 {(1-c^2s^2)\sqrt{c^2-s^2}}.
\]
For verification of the branch: the inverse of
\(y\mapsto y-a\sqrt{y^2+v_0}\) at a positive value \(h\), for
\(0<a<1\), is
\((h+a\sqrt{h^2+v_0(1-a^2)})/(1-a^2)\).
Substitution checks the equality with positive square roots; strict
monotonicity proves uniqueness. Taking \(a=cs\) and
\(h=s(1+c^2)\sqrt{v_0}/\sqrt{c^2-s^2}\) gives the displayed \(Y_0\).

Set
\[
\Lambda=Y_0^{-2}
=\frac{(1-c^2s^2)^2(c^2-s^2)}
 {s^2(1-s^2)(1+2c^2+c^2s^2)^2},
\quad
Z=W+(1+W)\Lambda,
\quad
D_* =\frac{s^2Z}{1+(1-s^2)\Lambda}. \tag{9}
\]
These are positive on the present domain. Write
\(z=m\tan g\), \(t=m\tan d\), and \(\ell=Y^{-2}<\Lambda\).
The definitions give
\[
z^2=w+(1+w)\ell,
\qquad
t^2=\frac{s^2\{w+(1+w)\ell\}}{1+(1-s^2)\ell}.
\]
Both expressions increase strictly with \(w\) and \(\ell\).
For the second expression, its derivative in \(\ell\) is
\(s^2(1+s^2w)/(1+(1-s^2)\ell)^2>0\).
Consequently (7) and (9) imply
\[
z^2<Z,\qquad t^2<D_*. \tag{10}
\]

Here are exact rational bounds for (9). Their complete polynomial
certificate is provided immediately below.

| Range of \(c\) | Range of \(s\) | \(\sqrt Z\le z_0\) | \(\sqrt{D_*}\le t_0\) |
|---|---|---:|---:|
| \([2/3,7/10]\) | \([12/25,c)\) | \(19/20\) | \(21/50\) |
| \([7/10,3/4]\) | \([12/25,c)\) | \(101/100\) | \(9/20\) |
| \([3/4,1)\) | \([12/25,3/5]\) | \(27/25\) | \(1/2\) |
| \([3/4,1)\) | \([3/5,c)\) | \(9/10\) | \(3/5\) |

These ranges cover the whole complementary domain. Since
\(H(g)=\arctan z\), \(H(d)=\arctan t\), (10) and this table contradict
\(H(d)+H(g)/c=\pi/2\), as follows.

For every \(x\ge0\), concavity of arctangent gives
\[
\arctan x\le\frac\pi4+\frac{x-1}{2}.
\]
For \(0\le x\le1\), integrating
\(1/(1+x^2)\le1-x^2+x^4\) also gives
\(\arctan x\le x-x^3/3+x^5/5\).
In particular,
\[
\arctan(9/20)<43/100,\quad
\arctan(1/2)<223/480,\quad
\arctan(3/5)<11/20.
\]
Together with \(\arctan(21/50)<21/50\), the four rows imply, respectively,
\[
H(d)+H(g)/c <
\begin{cases}
3\pi/8+153/400,\\
5\pi/14+153/350,\\
\pi/3+1243/2400,\\
\pi/3+29/60.
\end{cases} \tag{11}
\]
Each right-hand side is strictly below \(\pi/2\).
Only the elementary bound \(\pi>25/8\) is needed: the corresponding
thresholds for \(\pi\) are \(153/50,153/50,1243/400,29/10\), all
smaller than \(25/8\).
For completeness, the arctangent addition formula on the positive
branches gives
\(\pi/4=\arctan(1/2)+\arctan(1/3)\).
Integrating finite geometric sums gives
\[
\pi>
4\left(\frac12-\frac1{24}+\frac1{160}-\frac1{896}
       +\frac13-\frac1{81}\right)
=\frac{284663}{90720}>\frac{25}{8}. \tag{12}
\]
This proves the asserted contradiction to (2).

We have now excluded \(s\ge12/25\) when \(Q>0\). Section 3 proves
(1) for the remaining range, and (4) proves Q9.

## 5. Exact certificate for the table

Here are the precise polynomials whose signs certify every entry of the
table. They also specify the full certificate without a list of 1,890
individual coefficients. Define
\[
\begin{aligned}
J&=1-c^2s^2,&N_w&=(c-s)J,&D_w&=sP,\\
N_\ell&=J^2(c^2-s^2),&
D_\ell&=s^2(1-s^2)(1+2c^2+c^2s^2)^2,\\
N_z&=N_wD_\ell+(D_w+N_w)N_\ell,&D_z&=D_wD_\ell,\\
N_t&=s^2N_z,&D_t&=D_w\{D_\ell+(1-s^2)N_\ell\}.
\end{aligned} \tag{13}
\]
Thus \(Z=N_z/D_z\), \(D_*=N_t/D_t\), and the denominators are positive
where the table is applied. For each row it is enough to certify
\[
z_0^2D_z-N_z\ge0,\qquad t_0^2D_t-N_t\ge0. \tag{14}
\]

Map the unit square to each row by putting
\(c=a+(b-a)u\). In rows 1, 2 and 4 put
\(s=h+(c-h)v\), where \(h\) is that row's lower endpoint for \(s\).
In row 3 put \(s=12/25+(3/25)v\).
These maps cover the closed versions of the indicated ranges.
Certification takes place for the polynomials on these closed sets;
division is used only on the original open domain.

After these substitutions the two polynomials in (14) have the
following respective bidegrees, and all their Bernstein coefficients
are nonnegative:
\[
(19,12),(19,13);\quad
(19,12),(19,13);\quad
(9,12),(9,13);\quad
(19,12),(19,13).
\]
There are 1,890 coefficients in total, of which exactly 12 are zero.
The following explicit rule specifies each coefficient. If a substituted
polynomial is \(p(u,v)=\sum_{a,b}p_{ab}u^av^b\) of bidegree \((n,m)\),
its coefficient in front of \(b_i^n(u)b_j^m(v)\) is
\[
\beta_{ij}=
\sum_{a\le i,\,b\le j}
p_{ab}\frac{\binom ia}{\binom na}\frac{\binom jb}{\binom mb}. \tag{15}
\]
All inputs in (13)-(15) and the table are rational. The complete exact
calculation of their signs is below.

To justify the method, the binomial theorem gives
\[
u^a=\sum_{i=a}^n\frac{\binom ia}{\binom na}b_i^n(u).
\]
Indeed \(\binom ni\binom ia/\binom na=\binom{n-a}{i-a}\), so the
sum is \(u^a(u+(1-u))^{n-a}\). Applying this identity in each variable
proves (15). Nonnegative coefficients therefore prove nonnegativity
throughout the full square, with no sampling or rounding.

## 6. Complete rational verifier

The following Python 3 program is the entire certificate verifier.
It needs only the standard library, uses exact integers and fractions,
and performs no floating-point arithmetic. In the workspace the same
code is retained as `runs/q9/reproducibility/verify_certificate.py`.
Running it prints the `PASS` message shown at its end.

```python
"""Q9 certificate: exact rational arithmetic, no numerical sampling."""
from fractions import Fraction as F
from math import comb

# Sparse polynomials: (degree in c, degree in s) -> rational coefficient.
def add(*ps):
    q = {}
    for p in ps:
        for ij, a in p.items():
            q[ij] = q.get(ij, F(0)) + a
    return {ij: a for ij, a in q.items() if a}

def scale(p, a):
    return {ij: a*b for ij, b in p.items() if a*b}

def sub(p, q):
    return add(p, scale(q, -1))

def mul(p, q):
    r = {}
    for (i, j), a in p.items():
        for (k, l), b in q.items():
            ij = (i+k, j+l)
            r[ij] = r.get(ij, F(0)) + a*b
    return {ij: a for ij, a in r.items() if a}

def power(p, n):
    q = {(0, 0): F(1)}
    for _ in range(n):
        q = mul(q, p)
    return q

def substitute(p, C, S):
    cp = [power(C, i) for i in range(max(i for i,j in p)+1)]
    sp = [power(S, j) for j in range(max(j for i,j in p)+1)]
    return add(*(scale(mul(cp[i], sp[j]), a)
                 for (i, j), a in p.items()))

def bernstein(p):
    n = max(i for i,j in p)
    m = max(j for i,j in p)
    b = [[sum((a*F(comb(i,k),comb(n,k))*F(comb(j,l),comb(m,l))
               for (k,l),a in p.items() if k<=i and l<=j), F(0))
          for j in range(m+1)] for i in range(n+1)]
    return n, m, b

one = {(0,0): F(1)}
c = {(1,0): F(1)}
s = {(0,1): F(1)}
c2, s2 = power(c,2), power(s,2)
cs = mul(c,s)
P = add(one, scale(c2,2), scale(cs,-3),
        scale(mul(c2,s2),-3), mul(mul(c,add(scale(one,2),c2)),power(s,3)))
E = sub(mul(mul(add(c,s),sub(one,cs)),P),
        mul(mul(sub(one,c2),s),power(add(one,cs),3)))

# Small-s certificate, equation (8).
C = add(scale(one,F(2,3)),scale(c,F(1,3)))
S = scale(s,F(12,25))
n,m,b = bernstein(substitute(E,C,S))
N = [
 [1328125000,1243125000,1051925000,765469000,412948680,12607112],
 [1650390625,1534140625,1300215625,966327625,571546705,138478561],
 [2050781250,1891406250,1603781250,1216202250,781848450,330011178],
 [2548828125,2329453125,1972378125,1522315125,1052902845,604001061],
 [3164062500,2860312500,2410762500,1885396500,1387790820,974492532]]
assert (n,m)==(4,5)
assert all(b[i][j]==F(N[i][j],1054687500)>0
           for i in range(5) for j in range(6))

# Complementary certificate, equations (13)-(14).
J = sub(one,mul(c2,s2))
Nw, Dw = mul(sub(c,s),J), mul(s,P)
Nl = mul(power(J,2),sub(c2,s2))
Dl = mul(mul(s2,sub(one,s2)),
         power(add(one,scale(c2,2),mul(c2,s2)),2))
Nz = add(mul(Nw,Dl),mul(add(Dw,Nw),Nl))
Dz = mul(Dw,Dl)
Nd = mul(s2,Nz)
Dd = mul(Dw,add(Dl,mul(sub(one,s2),Nl)))
# (c lower, c upper, s lower, s upper or None meaning c, z bound, d bound).
rows = [
 (F(2,3),F(7,10),F(12,25),None,F(19,20),F(21,50)),
 (F(7,10),F(3,4),F(12,25),None,F(101,100),F(9,20)),
 (F(3,4),F(1),F(12,25),F(3,5),F(27,25),F(1,2)),
 (F(3,4),F(1),F(3,5),None,F(9,10),F(3,5))]
expected = [((19,12),(19,13)),((19,12),(19,13)),
            ((9,12),(9,13)),((19,12),(19,13))]
count = zero_count = 0
for row_number,(a,b,t,h,z,d) in enumerate(rows):
    C = add(scale(one,a),scale(c,b-a))
    S = (add(scale(one,t),mul(sub(C,scale(one,t)),s)) if h is None
         else add(scale(one,t),scale(s,h-t)))
    for which,p in enumerate((sub(scale(Dz,z*z),Nz),sub(scale(Dd,d*d),Nd))):
        n,m,bb = bernstein(substitute(p,C,S))
        assert (n,m)==expected[row_number][which]
        values = [v for rr in bb for v in rr]
        assert all(v>=0 for v in values)
        count += len(values)
        zero_count += sum(v==0 for v in values)
assert (count,zero_count)==(1890,12)

# Rational comparisons used in the final trigonometric contradiction.
def atan_upper(t):
    return t-t**3/F(3)+t**5/F(5)
assert atan_upper(F(9,20)) < F(43,100)
assert atan_upper(F(1,2)) == F(223,480)
assert atan_upper(F(3,5)) < F(11,20)
pi_lower = 4*(F(1,2)-F(1,24)+F(1,160)-F(1,896)+F(1,3)-F(1,81))
assert pi_lower == F(284663,90720) > F(25,8)
assert all(F(25,8)>v for v in [F(153,50),F(1243,400),F(29,10)])
print('PASS: 30 positive small-s coefficients; 1890 nonnegative')
print('complementary coefficients (12 zero); all rational angle bounds.')
```

The proof uses elementary differentiation, integration, concavity,
trigonometric addition formulas, and the binomial theorem, with their
needed forms derived or checked above. There is no appeal to an external
research theorem. No mathematical gap remains in Q9. The finite
certificate was executed successfully with Python 3.14.4. Lean was not
available and no Lean formal-verification claim is made. No literature,
prior solutions, other projects, sessions, or internet sources were
consulted; external novelty is unknown.
