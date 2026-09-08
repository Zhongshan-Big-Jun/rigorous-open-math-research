"""Numerical evidence only: C1 plus Q or its first-term positivity."""
from explore import *
from extended_scan import generalvals
rng=random.Random(933);out=[]
for _ in range(20000):
 c=rng.uniform(2/3,1);s=c*rng.random();m=1+10**rng.uniform(-4,6)
 H=lambda z:math.atan(m*math.tan(z));arc=lambda z:math.asin(s*math.sin(z))
 f=lambda z:H(z)-c*H(arc(z))-(1-c)*P
 grid=[0]+[P/2*10**(-10*(1-j/100)) for j in range(101)]
 old=0;of=f(old)
 for B in grid[1:]:
  nf=f(B)
  if nf*of<0:
   BB=bisect(f,old,B)
   g=BB*rng.random()
   z=generalvals(m,c,s,BB,g);z['Q0']=(c*math.cos(BB)-s*math.cos(arc(BB)))/math.sin(BB);out.append(z)
  old,of=B,nf
qp=[z for z in out if z['Q']>0];q0p=[z for z in out if z['Q0']>0]
print('C1 roots',len(out),'qpositive',len(qp),'suff fail',sum(z['suff']<0 for z in qp),'Rfail',sum(z['R']<=0 for z in qp),'Q0 Rfail',sum(z['R']<=0 for z in q0p))
print('worst Qpositive',sorted(qp,key=lambda z:z['ratio'],reverse=True)[:3])
json.dump([z for z in qp if z['R']<=0],open('runs/rigorous-open-math-research/q9/reproducibility/c1_failures.json','w'),indent=2)
