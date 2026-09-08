"""Probe beta-retaining Q upper bound; binary64 evidence only."""
import math, random, json
from qbound_probe import bisection
rng=random.Random(290093); failures=valid=0; best=None
for _ in range(10000):
    c=2/3+rng.random()/3; q=c*(.5+.5*rng.random()); a=q*rng.random()
    x=bisection(lambda x:math.atan(x)+c*math.atan(a*x)-c*math.pi/2,0,math.tan(c*math.pi/2))
    y=(q*q-a*a)/(q*q*(1-a*a)); w=(1-y)*x*x-y
    if w<=0:continue
    valid+=1
    U=(c-q)*(1-c*q*q/a)/(1+c*q)
    f=U-c*w*(1-q*q)**2/(1+c*a+w*(1+c*a*q*q))
    row=dict(c=c,q=q,a=a,x=x,y=y,w=w,f=f)
    if f>0:failures+=1
    if best is None or f>best['f']:best=row
print(json.dumps(dict(valid=valid,failures=failures,best=best),indent=2))
