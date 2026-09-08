from explore import *
import random,time
rng=random.Random(191);start=time.monotonic();cnt=pos=0;fail=[]
while time.monotonic()-start<12:
 m=1+math.exp(rng.uniform(-6,14));c=rng.uniform(2/3,1)
 lo=math.atan2(math.sin((1-c)*pi),m*math.cos((1-c)*pi))
 # bias B scales, plus uniform
 if rng.random()<.5:B=lo+(pi/2-lo)*rng.random()
 else:B=lo*math.exp(rng.random()*math.log((pi/2)/lo))
 v=calc(m,c,B)
 if v is None or not v['g']<B:continue
 cnt+=1
 if v['Q']>0:
  pos+=1
  if v['suff']<0:
   fail.append(v);print(json.dumps(v,indent=2));break
print('valid',cnt,'Qpositive',pos,'strongerfail',len(fail))
Path('runs/q9/reproducibility/relax_c3.json').write_text(json.dumps(fail,indent=2))
