# Affirmative solution of Q9

The implication is true. In fact, on the stated domain, (C2) and (C3) alone imply
\[
 Q_{\rm quad}>0\ \Longrightarrow\ r<\frac19,
 \qquad
 r\le\frac19\ \Longrightarrow\ R_{\rm quad}>0.
 \tag{1}
\]
Consequently every tuple satisfying all three exact constraints satisfies Q9. No mass-balance equation is used.

The proof below is exact. Its only computational component is a finite polynomial-positivity certificate using rational arithmetic. The complete certificate and its checking code are included in this file. Numerical searches are not premises of the proof.

Write
\[
 s=\sqrt r,\quad h=1-s^2,\quad e=1-c^2,\quad k=m^2-1.
\]
Thus \(m>1,\ 2/3<c<1,\ 0<s<c\). Throughout,
\[
 H(z)=\arctan(m\tan z),\qquad
 A=\arcsin(s\sin B),\qquad d=\arcsin(s\sin g),
\]
with \(0<d<A<B<\pi/2\) and \(d<g<B\). The constraints used in the proof are exactly
\[
 H(g)+cH(d)=c\pi/2,\qquad B-g=c(A+d).
 \tag{2}
\]

## 1. The range \(s\le1/3\)

We first prove that (2) implies
\[
 c^2-s^2>ke s^2\sin^2 B
 \qquad(0<s\le1/3).
 \tag{3}
\]

Put \(\theta=\pi/2-H(d)\in(0,\pi/2)\). By (2), \(H(g)=c\theta\). Strict convexity of tangent and \(0<c<1\) give
\[
 \tan H(g)=\tan(c\theta)<c\tan\theta=c\cot H(d).
\]
Therefore
\[
 m^2\tan g\tan d<c,\qquad
 m^2s^2\sin^2g<cs\cos g\cos d<cs.
 \tag{4}
\]
For \(0<s<1\), the function \(\phi(z)=\arcsin(s\sin z)\) satisfies
\[
 \phi'(z)=\frac{s\cos z}{\sqrt{1-s^2\sin^2z}}<s
 \quad(0<z<\pi/2),\qquad \phi(0)=0.
\]
Thus \(A<sB\) and \(d<sg\). Using (2),
\[
 \frac Bg<\lambda:=\frac{1+cs}{1-cs}.
\]
Also \(\sin z/z\) strictly decreases on \((0,\pi/2)\): its derivative has the sign of \(z\cos z-\sin z<0\), since the latter expression vanishes at zero and has derivative \(-z\sin z<0\). Hence
\[
 \frac{\sin B}{\sin g}<\frac Bg<\lambda.
\]
Together with (4) and \(k<m^2\), this yields
\[
 ke s^2\sin^2 B<ecs\lambda^2.
 \tag{5}
\]

To compare the last expression with \(c^2-s^2\), define
\[
 J(c,s)=\frac{(1-c^2)cs}{c^2-s^2}
       \left(\frac{1+cs}{1-cs}\right)^2.
\]
For fixed \(c\), every positive factor in this expression increases with \(s\). For \(c\ge2/3\), \(0<s\le1/3\), and \(c<1\),
\[
 \partial_c\log J
 =\frac{1-3c^2}{c(1-c^2)}
  -\frac{2c}{c^2-s^2}
  +\frac{4s}{1-c^2s^2}<0.
\]
Indeed, the first summand is negative, the second is less than \(-2\), and the third is at most \(3/2\). It follows that
\[
 J(c,s)\le J(2/3,1/3)=\frac{1210}{1323}<1.
\]
This proves (3).

For completeness, set
\[
 U=(\pi-H(B))\sin^2B+H(g)\sin^2g,\qquad
 R_{\rm quad}=(c^2-s^2)V-ke s^2U,\qquad T_{\rm quad}=s^2U/V.
\]
The comparison with \(R_{\rm quad}\) is elementary. Namely,
\[
 V=\pi+H(g)-H(B)+m(B-g)>0,
\]
because \(F(z)=H(z)-mz\) has derivative \(F'(z)=-mk\sin^2z/(1+k\sin^2z)<0\), giving \(V>\pi\). Furthermore,
\[
 V\sin^2 B-U
 =H(g)(\sin^2B-\sin^2g)+m(B-g)\sin^2B>0.
\]
Thus (3) gives
\[
 R_{\rm quad}
 =(c^2-s^2)V-ke s^2U
 >ke s^2\bigl(V\sin^2B-U\bigr)>0.
 \tag{6}
\]

## 2. A rational consequence of (C2)

For every \(0<s<c\), \(2/3<c<1\), and acute \(g,d\) satisfying (C2) and \(\sin d=s\sin g\), we claim
\[
 m^2\tan^2g>\ell(s):=\frac{3+2s}{1+6s+3s^2}.
 \tag{7}
\]

Let \(w=m\tan g>0\), and let
\[
 \eta=\frac{\tan d}{\tan g}
      =\frac{s\cos g}{\cos d}<s.
\]
Constraint (C2) says
\[
 \arctan w=c\bigl(\pi/2-\arctan(\eta w)\bigr).
\]
Since \(c>2/3\) and \(\eta<s\), it follows that
\[
 \Theta(w):=3\arctan w+2\arctan(sw)>\pi.
 \tag{8}
\]
The function \(\Theta\) is strictly increasing from \(0\) to \(5\pi/2\). The addition formulas give, with \(X=w^2\),
\[
 \sin\Theta(w)
 =\frac{w\,[s^2X^2-(1+6s+3s^2)X+3+2s]}
 {(1+w^2)^{3/2}(1+s^2w^2)}.
 \tag{9}
\]
For positive \(w\), the two zeros of this expression occur in order at \(\Theta=\pi\) and \(\Theta=2\pi\). Thus the smaller root of the displayed quadratic corresponds to \(\Theta=\pi\). Put
\[
 W=1+6s+3s^2,\qquad Z=3+2s.
\]
Its smaller root is
\[
 X_-=\frac{2Z}{W+\sqrt{W^2-4s^2Z}}>\frac ZW=\ell(s),
\]
where
\[
 W^2-4s^2Z=1+12s+30s^2+28s^3+9s^4>0,
\]
and the square root is strictly smaller than \(W\). By (8), \(w^2>X_-\), proving (7). This argument keeps track of the trigonometric orientation; no implication is obtained merely by squaring a constraint.

## 3. A geometric upper bound for the first term of \(Q_{\rm quad}\)

This part needs only (C3), \(0<s<c<1\), and the acute-angle relations. Write
\[
 Q_{\rm quad}=Q_1-Q_2,\qquad
 Q_1=c\cot B-s^2\cot A,
\]
where \(Q_2\) is the strictly positive subtracted term in the question.

Since \(0<A+d<\pi\), strict concavity of sine on \([0,\pi]\) and (C3) imply
\[
 \sin(B-g)=\sin(c(A+d))>c\sin(A+d).
\]
Expanding both sides and dividing by \(\sin B\sin g>0\) gives
\[
 \cot B+cs^2\cot A<\cot g-cs^2\cot d.
 \tag{10}
\]
Define
\[
 x=\cot g>0,\qquad M=\sqrt{x^2+h},\qquad
 v=\frac Mx=\sqrt{1+h\tan^2g}>1,\qquad a=cs.
\]
For \(b=\cot B>0\), the sine relations imply
\[
 s^2\cot A=s\sqrt{b^2+h},\qquad s^2\cot d=sM.
\]
Consequently (10) is
\[
 b+a\sqrt{b^2+h}<x-aM.
 \tag{11}
\]
The function on the left is strictly increasing in \(b\ge0\). Because a positive \(b\) satisfies (11), its equality solution \(b_0\) is positive. Direct inversion gives
\[
 b_0=\frac{(1+a^2)x-2aM}{1-a^2},\qquad
 \sqrt{b_0^2+h}=\frac{(1+a^2)M-2ax}{1-a^2}.
 \tag{12}
\]
These formulas retain the positive square-root branch. In particular, the numerator in the second formula is positive since \(M>x\) and \(a<1\). They also follow from
\[
 \sqrt{(x-aM)^2+(1-a^2)h}=M-ax>0.
\]
The function \(b\mapsto cb-s\sqrt{b^2+h}\) is strictly increasing, because its derivative exceeds \(c-s>0\). Thus \(b<b_0\) and (12) show that
\[
 \frac{Q_1}{x}<\alpha-\beta v,
 \tag{13}
\]
where
\[
 \Delta=1-c^2s^2,\qquad
 \alpha=\frac{c[1+(c^2+2)s^2]}{\Delta},\qquad
 \beta=\frac{s(1+2c^2+c^2s^2)}{\Delta}.
 \tag{14}
\]
Notice that
\[
 \alpha-\beta
 =\frac{(c-s)(1-cs)}{1+cs}>0.
 \tag{15}
\]

The second term has the exact form
\[
 Q_2=
 \frac{ckh^2xM}
 {M(1+x^2+k)+csx(1+x^2+ks^2)}.
 \tag{16}
\]
For fixed \(c,s,x\), it is strictly increasing as a function of \(k\ge0\): it is a positive constant times \(k/(A_0+A_1k)\), with \(A_0,A_1>0\).

## 4. The polynomial inequality

The following lemma is purely algebraic.

**Lemma.** Suppose \(2/3\le c<1\) and \(1/3\le s<c\). Use (14), and put
\[
 \ell=\frac{3+2s}{1+6s+3s^2},\qquad
 \omega=1+\ell(1-s^2),\qquad v_*=\frac{\alpha}{\beta}>1.
\]
Then
\[
 \omega>v_*^2,
 \tag{17}
\]
and, for \(1\le v\le v_*\),
\[
 \begin{split}
 N(v):={}&c(1-s^2)v(\omega-v^2)\\
 &-(\alpha-\beta v)\,[v(1+\ell)+cs(v^2+s^2\ell)]>0.
 \end{split}
 \tag{18}
\]

**Proof.** Set \(r=s^2,\ h=1-r,\ a=cs,\ \Delta=1-c^2r\), and define the following polynomials in \(c,s\):
\[
 W=1+6s+3r,\quad Z=3+2s,\quad
 C=c[1+(c^2+2)r],\quad D=s(1+2c^2+c^2r).
\]
Here \(\alpha=C/\Delta\), \(\beta=D/\Delta\), and
\[
 \Delta WN(v)=n_0+n_1v+n_2v^2+n_3v^3,
\]
where
\[
 \begin{aligned}
 n_3&=W(Da-ch\Delta),\\
 n_2&=D(W+Z)-CaW,\\
 n_1&=ch(W+Zh)\Delta-C(W+Z)+DarZ,\\
 n_0&=-CarZ.
 \end{aligned}
 \tag{19}
\]
Consider four further polynomials:
\[
 \begin{aligned}
 E_0&=n_0+n_1+n_2+n_3,\\
 E_1&=n_1+2n_2+3n_3,\\
 E_2&=n_2,\\
 E_3&=n_1D^2+2n_2CD+3n_3C^2.
 \end{aligned}
 \tag{20}
\]
The exact certificate below proves that, on the larger rectangle
\(2/3\le c\le1,\ 1/3\le s\le1\), \(E_1,E_2,E_3\) are strictly positive and \(E_0\) is nonnegative. It also proves \(E_0>0\) when \(c<1,s<1\).

Since \(\Delta,W,D>0\) in the lemma's domain, these signs imply
\[
 N(1)>0,\quad N'(1)>0,\quad n_2>0,\quad N'(v_*)>0.
\]
If \(n_3\ge0\), then \(\Delta WN''(v)=2n_2+6n_3v>0\) for \(v\ge1\), so \(N'(v)>0\). If \(n_3<0\), the quadratic \(\Delta WN'(v)\) is concave and is positive at both endpoints of \([1,v_*]\); it is therefore positive throughout that interval. In both cases \(N(v)\ge N(1)>0\), proving (18).

Finally, at \(v=v_*\), the second line of (18) vanishes. Hence
\[
 0<N(v_*)=chv_*(\omega-v_*^2),
\]
which proves (17). \(\square\)

### Exact certificate for (20)

For a polynomial \(P(c,s)\), substitute
\[
 c=\frac{2+X}{3},\qquad s=\frac{1+2Y}{3}.
\]
Write the resulting polynomial as
\[
 \widetilde P(X,Y)=\sum_{p,q} A_{pq}X^pY^q
\]
with degrees at most \(n,m\). Its Bernstein coefficients are the rational numbers
\[
 b_{ij}=\sum_{\substack{p\le i\\q\le j}}
 A_{pq}\frac{\binom{i}{p}}{\binom{n}{p}}
        \frac{\binom{j}{q}}{\binom{m}{q}},
 \quad 0\le i\le n,\quad0\le j\le m.
 \tag{21}
\]
Indeed, the binomial theorem gives
\[
 X^p=\sum_{i=p}^n
 \frac{\binom{i}{p}}{\binom{n}{p}}
 \binom ni X^i(1-X)^{n-i}.
\]
Multiplying the corresponding identities in \(X\) and \(Y\) proves the representation with coefficients (21). Every basis polynomial is nonnegative on \([0,1]^2\), and their sum is one. Thus nonnegative coefficients certify nonnegativity; strictly positive coefficients certify strict positivity on the whole square.

For the polynomials in (20), exact calculation from (19) gives:

| Polynomial | Degrees \((n,m)\) | Smallest Bernstein coefficient |
|---|---:|---:|
| \(E_0\) | \((4,6)\) | \(0\) |
| \(E_1\) | \((4,6)\) | \(9382/6561\) |
| \(E_2\) | \((4,5)\) | \(25553/6561\) |
| \(E_3\) | \((9,12)\) | \(134561396/387420489\) |

For \(E_0\), additionally \(b_{00}=15169/59049>0\). Its associated basis polynomial is \((1-X)^4(1-Y)^6>0\) when \(c<1,s<1\), proving the required strictness.

The complete exact computation establishing this table is included at the end of this file. It uses integer and rational operations only, and explicitly checks every coefficient in (21); it is not an evaluation of the polynomials at finitely many sample points.

## 5. Exclusion of \(s\ge1/3\), and conclusion

Suppose \(s\ge1/3\) and \(Q_{\rm quad}>0\). Since \(Q_2>0\), (13) gives
\[
 0<Q_1/x<\alpha-\beta v,
 \qquad 1<v<v_*.
\]
By (17), \(v^2<\omega\). As \(x^2=h/(v^2-1)\), this says
\[
 k_0:=\ell x^2-1>0.
\]
The exact consequence (7) of (C2) implies \(k>k_0\). Substituting \(k_0\) into (16), using its strict monotonicity in \(k\), and simplifying yields
\[
 \frac{Q_2}{x}>
 \frac{chv(\omega-v^2)}
 {v(1+\ell)+cs(v^2+s^2\ell)}.
 \tag{22}
\]
Every denominator here is positive. By (18), the right side of (22) exceeds \(\alpha-\beta v\), which in turn exceeds \(Q_1/x\) by (13). Thus \(Q_2>Q_1\), contradicting \(Q_{\rm quad}>0\).

We have proved \(Q_{\rm quad}>0\Rightarrow s<1/3\), equivalently \(r<1/9\). Equation (6) then gives \(R_{\rm quad}>0\), and division by the positive quantities \(keV\) gives exactly
\[
 \boxed{\displaystyle
 Q_{\rm quad}>0\ \Longrightarrow\
 \frac{c^2-r}{k(1-c^2)}>T_{\rm quad}.}
\]

There is no unproved remainder. The argument uses elementary trigonometric identities, elementary calculus, the binomial theorem, and the exact rational certificate below. It does not rely on numerical evidence or an external theorem whose hypotheses remain unchecked.

## Complete rational certificate code

The following is a self-contained Python 3 program. It is also retained as the supporting file verify_certificate.py. In its variable names, N1, Np1, n2, Npstar denote \(E_0,E_1,E_2,E_3\), respectively.

```python
from fractions import Fraction as F
from math import comb

class P:
 def __init__(self,a=0):
  self.d=dict(a.d) if isinstance(a,P) else ({(0,0):F(a)} if not isinstance(a,dict) else {ij:F(v) for ij,v in a.items() if v})
 def __add__(self,other):
  other=P(other);d=dict(self.d)
  for ij,v in other.d.items():d[ij]=d.get(ij,F(0))+v
  return P({ij:v for ij,v in d.items() if v})
 __radd__=__add__
 def __neg__(self):return P({ij:-v for ij,v in self.d.items()})
 def __sub__(self,other):return self+-P(other)
 def __rsub__(self,other):return P(other)+-self
 def __mul__(self,other):
  other=P(other);d={}
  for (i,j),v in self.d.items():
   for (k,l),w in other.d.items():
    ij=(i+k,j+l);d[ij]=d.get(ij,F(0))+v*w
  return P({ij:v for ij,v in d.items() if v})
 __rmul__=__mul__
 def __pow__(self,n):
  r=P(1);a=self
  while n:
   if n%2:r=r*a
   a=a*a;n//=2
  return r
 def compose(self,c,t):
  out=P(0)
  for (i,j),v in self.d.items():out+=v*c**i*t**j
  return out
 def degree(self):return max(i for i,j in self.d),max(j for i,j in self.d)
 def at(self,c,t):return sum(v*c**i*t**j for (i,j),v in self.d.items())
 def bern(self):
  n,m=self.degree();out=[]
  for i in range(n+1):
   row=[]
   for j in range(m+1):
    b=sum(v*F(comb(i,k),comb(n,k))*F(comb(j,l),comb(m,l)) for (k,l),v in self.d.items() if k<=i and l<=j)
    row.append(b)
   out.append(row)
  return out
 def __repr__(self):return str(self.d)

c=P({(1,0):1});t=P({(0,1):1})
r=t*t;h=1-r;a=c*t;den=1-c*c*r
W=1+6*t+3*r;Z=3+2*t
C=c*(1+(c*c+2)*r);D=t*(1+2*c*c+c*c*r)
n3=W*(D*a-c*h*den)
n2=D*(W+Z)-C*a*W
n1=c*h*(W+Z*h)*den-C*(W+Z)+D*a*r*Z
n0=-C*a*r*Z
N1=n0+n1+n2+n3
Np1=n1+2*n2+3*n3
Npstar=n1*D*D+2*n2*C*D+3*n3*C*C
polys={'N1':N1,'Np1':Np1,'n2':n2,'Npstar':Npstar}

if __name__ == '__main__':
 expected = {
  'N1': ((4, 6), F(0)),
  'Np1': ((4, 6), F(9382, 6561)),
  'n2': ((4, 5), F(25553, 6561)),
  'Npstar': ((9, 12), F(134561396, 387420489)),
 }
 for name, p in polys.items():
  transformed = p.compose((2+c)*F(1,3), (1+2*t)*F(1,3))
  coefficients = transformed.bern()
  minimum = min(v for row in coefficients for v in row)
  assert (transformed.degree(), minimum) == expected[name]
  assert all(v >= 0 for row in coefficients for v in row)
  if name == 'N1':
   assert coefficients[0][0] == F(15169, 59049)
  else:
   assert minimum > 0
  print(name, transformed.degree(), minimum)
 print('All exact polynomial certificates passed.')
```
