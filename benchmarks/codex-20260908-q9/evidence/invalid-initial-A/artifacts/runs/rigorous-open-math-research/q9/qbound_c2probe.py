"""C2,C3 Q-positive exploratory bounds, not proof."""
import sys, random, json
sys.path.insert(0,'runs/rigorous-open-math-research/q9/reproducibility')
from explore import vals, angles
rng=random.Random(290092)
best_r=best_ratio=None; valid=qp=0
for i in range(30000):
    c=2/3+rng.random()/3; q=c*rng.random(); m=1+10**rng.uniform(-3,4)
    if angles(m,c,q) is None:continue
    z=vals(m,c,q); valid+=1
    if z['Q']>0:
        qp+=1
        z['suff_ratio']=1-z['suff']/(c*c-q*q)
        if best_r is None or z['r']>best_r['r']:best_r=z
        if best_ratio is None or z['suff_ratio']>best_ratio['suff_ratio']:best_ratio=z
out=dict(valid=valid,qp=qp,best_r=best_r,best_ratio=best_ratio)
with open('runs/rigorous-open-math-research/q9/qbound_c2probe.json','w') as f:json.dump(out,f,indent=2)
print(json.dumps(out,indent=2))
