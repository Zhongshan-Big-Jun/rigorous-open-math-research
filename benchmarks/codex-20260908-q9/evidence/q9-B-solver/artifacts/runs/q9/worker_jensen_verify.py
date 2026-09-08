#!/usr/bin/env python3
"""Exact audit: invert Bernstein certificate; compare original E on rational points."""
from fractions import Fraction as R
from math import comb,lcm,gcd
from functools import reduce
from collections import defaultdict
from pathlib import Path
import json,hashlib
from worker_jensen_poly import polynomial,affcube
q=json.loads(Path('runs/q9/worker_jensen_initial.json').read_text())
degree=tuple(q['degree']);coeff=list(map(int,q['bernstein']))
assert degree==(26,18,4)
assert len(coeff)==27*19*5
assert all(x>=0 for x in coeff)
assert all(x>0 for x in coeff[:19*5])
indices=[(i,j,k) for i in range(27) for j in range(19) for k in range(5)]
d=dict(zip(indices,coeff))
zeros=[k for k,v in d.items() if v==0]
for axis,n in enumerate(degree):
 out=defaultdict(int)
 for exp,v in d.items():
  k=exp[axis]
  for i in range(k,n+1):
   p=list(exp);p[axis]=i
   out[tuple(p)]+=v*comb(n,k)*comb(n-k,i-k)*((-1)**(i-k))
 d={k:v for k,v in out.items() if v}
p=polynomial();power=affcube(p,degree)
scale=1
for n in degree:scale*=lcm(*(comb(n,i) for i in range(n+1)))
assert d=={k:v*scale for k,v in power.items()}
# Direct original E evaluation is separate from polynomial construction.
def direct(c,s,z):
 t=c*s;u=c*t
 a=c*(1+(c*c+2)*t*t);b=t*(1+2*c*c+c*c*t*t)
 w=1+(a-b)*z/b;J=R(49,100)*(1+c)**2
 E=c*(1-t*t)*(1-u*u)*((1-t*t)*J*w*w-(w*w-1)*(w+u)**2)-(a-b*w)*((1+u*w)*(w+u)**2+J*w*(w+u*t*t))
 return 100*(b/c)**4*E/c

def evaluate(poly,c,s,z):
 return sum(v*c**i*s**j*z**k for (i,j,k),v in poly.items())
count=0
for c in [R(2,3),R(3,4),R(9,10),R(1)]:
 for s in [R(1,2),R(2,3),R(4,5),R(1)]:
  for z in [R(0),R(1,3),R(2,3),R(1)]:
   assert evaluate(p,c,s,z)==direct(c,s,z)
   count+=1
print('PASS inverse coefficient identity; PASS direct rational checks:',count)
print('zero indices:',zeros)
print('positive coefficients:',sum(v>0 for v in coeff),'zero:',len(zeros))
print('bernstein common scale:',scale)
print('affine common scale:',3**26*2**18)
print('gcd:',reduce(gcd,coeff))
print('first coefficient:',coeff[0])
print('minimal positive coefficient:',min(v for v in coeff if v>0))
print('max digits:',max(len(str(v)) for v in coeff))
