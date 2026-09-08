"""Exact rational positivity tests for the complementary Q9 region."""
from fractions import Fraction as F
from math import comb
import json,sys
sys.path.insert(0,'runs/q9/repo')
from worker_stronger_bound_check import add,scale,mul,power,one,c,s,P
neg=lambda p:scale(p,-1)
sub=lambda p,q:add(p,neg(q))
c2=power(c,2);s2=power(s,2)
cs2=mul(c2,s2)
J=sub(one,cs2)
Nw=mul(sub(c,s),J)
Dw=mul(s,P)
Nl=mul(power(J,2),sub(c2,s2))
Dl=mul(mul(s2,sub(one,s2)),power(add(one,scale(c2,2),cs2),2))
Nz=add(mul(Nw,Dl),mul(add(Dw,Nw),Nl))
Dz=mul(Dw,Dl)
Dd=mul(Dw,add(Dl,mul(sub(one,s2),Nl)))
Nd=mul(s2,Nz)

def subst(poly,C,S):
    cps=[power(C,j) for j in range(max(i for i,j in poly)+1)]
    sps=[power(S,j) for j in range(max(j for i,j in poly)+1)]
    return add(*(scale(mul(cps[i],sps[j]),v) for (i,j),v in poly.items()))

def bern(poly):
    n=max(i for i,j in poly);m=max(j for i,j in poly)
    return [[sum(v*F(comb(i,a),comb(n,a))*F(comb(j,b),comb(m,b))
                  for (a,b),v in poly.items() if a<=i and b<=j)
             for j in range(m+1)] for i in range(n+1)]

def aff(a,b,axis):return add(scale(one,a),{axis:b-a})
rows=[
 (F(2,3),F(7,10),F(12,25),None,F(19,20),F(21,50)),
 (F(7,10),F(3,4),F(12,25),None,F(101,100),F(9,20)),
 (F(3,4),F(1),F(12,25),F(3,5),F(27,25),F(1,2)),
 (F(3,4),F(1),F(3,5),None,F(9,10),F(3,5)),
]

def maps(row):
    a,b,t,v,z,d=row
    C=aff(a,b,(1,0))
    S=add(scale(one,t),mul(sub(C,scale(one,t)),s)) if v is None else aff(t,v,(0,1))
    return C,S

if __name__=='__main__':
 for no,row in enumerate(rows):
    C,S=maps(row)
    for label,poly in [('z',sub(scale(Dz,row[4]**2),Nz)),('d',sub(scale(Dd,row[5]**2),Nd))]:
     pp=subst(poly,C,S);bb=bern(pp)
     vals=[x for rr in bb for x in rr]
     print(no,label,'degree',len(bb)-1,len(bb[0])-1,'min',float(min(vals)),'negative',sum(x<0 for x in vals),'zeros',sum(x==0 for x in vals),flush=True)
