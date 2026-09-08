from explore import *
import random,time
rng=random.Random(20260908)
t0=time.monotonic();out=[];num=0
while time.monotonic()-t0<35:
 lm=rng.uniform(-8,18)
 m=1+math.exp(lm)
 if rng.random()<.5:c=2/3+math.exp(rng.uniform(-14,math.log(1/3-.0000001)))
 else:c=1-math.exp(rng.uniform(-14,math.log(1/3-.0000001)))
 vals=roots(m,c,n=140);num+=1
 out+=vals
 if any(v['Q']>0 and v['suff']<0 for v in vals):
  print('stronger failure',json.dumps(vals));break
Path('runs/q9/reproducibility/random_scan.json').write_text(json.dumps(out,indent=2))
print('pairs',num,'roots',len(out),'positive',sum(v['Q']>0 for v in out),'multiple maximum',max([sum(v['m']==w['m'] and v['c']==w['c'] for w in out) for v in out],default=0))
pos=[v for v in out if v['Q']>0]
print('max c positive',json.dumps(max(pos,key=lambda v:v['c']),indent=2) if pos else 'none')
print('closest suff',json.dumps(min(pos,key=lambda v:v['suff']),indent=2) if pos else 'none')
