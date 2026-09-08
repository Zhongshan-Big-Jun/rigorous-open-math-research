"""Exact polynomial certificate exploration for the constrained Q implication.

Only Python's standard library is used. Bivariate polynomials have rational
coefficients, indexed by their monomial exponent tuple.
"""
from fractions import Fraction as F
from math import comb
import json

def const(a): return {(0,0): F(a)} if a else {}
def clean(a): return {k:v for k,v in a.items() if v}
def add(a,b):
    o=a.copy()
    for k,v in b.items():o[k]=o.get(k,0)+v
    return clean(o)
def scale(a,b):return clean({k:v*b for k,v in a.items()})
def neg(a):return scale(a,-1)
def sub(a,b):return add(a,neg(b))
def mul(a,b):
    o={}
    for (i,j),v in a.items():
      for (k,l),w in b.items():
        p=(i+k,j+l);o[p]=o.get(p,0)+v*w
    return clean(o)
def power(a,n):
    o=const(1)
    for _ in range(n):o=mul(o,a)
    return o
def summ(*args):
    o={}
    for a in args:o=add(o,a)
    return o
def prod(*args):
    o=const(1)
    for a in args:o=mul(o,a)
    return o
def subst(p,a,b):
    ap=[power(a,i) for i in range(1+max(i for i,j in p))]
    bp=[power(b,j) for j in range(1+max(j for i,j in p))]
    o={}
    for (i,j),v in p.items():o=add(o,scale(mul(ap[i],bp[j]),v))
    return o
def bernstein(p,n=None,m=None):
    n=max(i for i,j in p) if n is None else n
    m=max(j for i,j in p) if m is None else m
    return [[sum(v*F(comb(i,k),comb(n,k))*F(comb(j,l),comb(m,l))
                   for (k,l),v in p.items() if k<=i and l<=j)
             for j in range(m+1)] for i in range(n+1)]
def evaluate(p,x,y):return sum(v*x**i*y**j for (i,j),v in p.items())

one=const(1);c={(1,0):F(1)};t={(0,1):F(1)}
r=power(t,2);c2=power(c,2);h=sub(one,r)
d0=sub(one,mul(c2,r));ld=summ(one,scale(t,6),scale(r,3));ln=add(const(3),scale(t,2))
p=mul(c,summ(one,scale(r,2),mul(c2,r)))
d=mul(t,summ(one,scale(c2,2),mul(c2,r)))
a3=prod(c,sub(mul(summ(const(2),scale(c2,3)),r),one),ld)
a2=sub(mul(d,add(ld,ln)),prod(p,c,t,ld))
a1=summ(prod(c,h,add(ld,mul(ln,h)),d0),neg(mul(p,add(ld,ln))),prod(d,c,power(t,3),ln))
a0=neg(prod(p,c,power(t,3),ln))
derivative_one=summ(scale(a3,3),scale(a2,2),a1)
derivative_star=summ(scale(prod(a3,p,p),3),scale(prod(a2,p,d),2),prod(a1,d,d))

def summary(label,pol):
    x=c;y=t
    cp=scale(add(const(2),x),F(1,3))
    tp=scale(add(one,mul(add(one,x),y)),F(1,3))
    z=subst(pol,cp,tp)
    b=bernstein(z)
    low=min(v for row in b for v in row)
    print(label,'terms',len(pol),'degree',(max(i for i,j in pol),max(j for i,j in pol)),
          'transformed_degree',(len(b)-1,len(b[0])-1),'min Bernstein',str(low),float(low),
          'nonpos',sum(v<=0 for row in b for v in row),'negative',sum(v<0 for row in b for v in row),flush=True)
    return z,b

if __name__=='__main__':
    zs,bs=summary('derivative_star',derivative_star)
    z2,b2=summary('a2',a2)
    for label,z in [('derivative_star',zs),('a2',z2)]:
      with open('structure_'+label+'_power.json','w') as f:
        json.dump([[i,j,str(v)] for (i,j),v in sorted(z.items())],f,indent=1)
