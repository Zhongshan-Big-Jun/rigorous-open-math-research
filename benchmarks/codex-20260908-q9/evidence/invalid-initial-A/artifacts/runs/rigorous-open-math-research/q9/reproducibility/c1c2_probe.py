"""Numerical evidence only; C1,C2 probe with C3 deliberately absent."""
from explore import *
from extended_scan import generalvals
rng=random.Random(931);out=[]
for _ in range(15000):
 c=rng.uniform(2/3,1);s=c*rng.random();m=1+10**rng.uniform(-4,5)
 H=lambda z:math.atan(m*math.tan(z));arc=lambda z:math.asin(s*math.sin(z))
 g=bisect(lambda z:H(z)+c*H(arc(z))-c*P/2,0,P/2)
 f=lambda z:H(z)-c*H(arc(z))-(1-c)*P
 grid=[g*(P/2/g)**(j/80) for j in range(81)]
 old=grid[0];of=f(old)
 for B in grid[1:]:
  nf=f(B)
  if nf*of<0:
   BB=bisect(f,old,B)
   z=generalvals(m,c,s,BB,g);z['C3residual']=BB-g-c*(arc(BB)+arc(g));out.append(z)
  old,of=B,nf
qp=[z for z in out if z['Q']>0];bad=[z for z in qp if z['suff']<0]
print('C1C2 roots',len(out),'qpositive',len(qp),'suff fail',len(bad),'Rfail',sum(z['R']<=0 for z in qp))
print('worst',sorted(qp,key=lambda z:z['ratio'],reverse=True)[:3])
json.dump(bad,open('runs/rigorous-open-math-research/q9/reproducibility/c1c2_failures.json','w'),indent=2)
