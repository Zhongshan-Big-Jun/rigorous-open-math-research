"""Numerical evidence only: broaden endpoint, branch, and reduced-constraint probes."""
from explore import *

def generalvals(m,c,s,B,g):
 r=s*s;k=m*m-1;e=1-c*c;A=math.asin(s*math.sin(B));d=math.asin(s*math.sin(g));H=lambda z:math.atan(m*math.tan(z))
 V=P+H(g)-H(B)+m*(B-g);U=(P-H(B))*math.sin(B)**2+H(g)*math.sin(g)**2
 Q=(c*math.cos(B)-s*math.cos(A))/math.sin(B)-c*k*(1-r)**2*math.sin(g)*math.cos(d)*math.cos(g)/(math.cos(d)*(1+k*math.sin(g)**2)+c*s*math.cos(g)*(1+k*r*math.sin(g)**2))
 return dict(m=m,c=c,r=r,B=B,g=g,Q=Q,R=(c*c-r)*V-k*e*r*U,ratio=k*e*r*U/((c*c-r)*V),suff=(c*c-r)-k*e*r*math.sin(B)**2)

def c2only(n=30000):
 rng=random.Random(923);bad=[];qp=[]
 for _ in range(n):
  c=rng.uniform(2/3,1);s=c*rng.random();m=1+10**rng.uniform(-5,6)
  H=lambda z:math.atan(m*math.tan(z)); arc=lambda z:math.asin(s*math.sin(z))
  g=bisect(lambda z:H(z)+c*H(arc(z))-c*P/2,0,P/2)
  # Mostly B scaled off g, but also broad angular sampling.
  B=g*(P/2/g)**rng.random()
  z=generalvals(m,c,s,B,g)
  if z['Q']>0:
   qp.append(z)
   if z['suff']<0:bad.append(z)
 print('C2 only n',n,'qpositive',len(qp),'suff failure',len(bad),'R failure',sum(z['R']<=0 for z in qp))
 print('C2 only worst',sorted(qp,key=lambda z:z['ratio'],reverse=True)[:3])
 json.dump(bad,open('runs/rigorous-open-math-research/q9/reproducibility/c2_only_failures.json','w'),indent=2)

def fullscan(n=2000):
 rng=random.Random(929);out=[]
 for _ in range(n):
  c=2/3+(1/3)*rng.random()**3
  s=c*(rng.random() if rng.random()<.7 else 10**rng.uniform(-6,-1))
  out+=roots(c,s)
 json.dump(out,open('runs/rigorous-open-math-research/q9/reproducibility/extended_roots.json','w'),indent=2)
 qp=[z for z in out if z['Q']>0]
 print('full roots',len(out),'qpositive',len(qp),'suff failure',sum(z['suff']<0 for z in qp),'R failure',sum(z['R']<=0 for z in qp))
 print('full worst',sorted(qp,key=lambda z:z['ratio'],reverse=True)[:5])
 print('max c Qpositive',max((z['c'] for z in qp),default=None))
if __name__=='__main__':c2only();fullscan()
