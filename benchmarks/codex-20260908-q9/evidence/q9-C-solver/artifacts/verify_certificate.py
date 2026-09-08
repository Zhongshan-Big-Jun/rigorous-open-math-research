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
