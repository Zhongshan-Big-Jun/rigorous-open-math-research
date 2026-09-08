import math,random,json,time
from search_numeric import vals
random.seed(53053)
N=50000
bad=[];mx=None;n=0
for j in range(N):
 c=random.uniform(2/3,1);m=1+10**random.uniform(-4,5)
 a=random.random()*math.pi*(1-1/(2*c))
 v=vals(m,c,a,True)
 if not (0<v['r']<c*c and v['g']<v['B']):continue
 if v['Q']>0:
  n+=1
  if mx is None or v['ratio']>mx['ratio']:mx=v
  if v['sufficient']<=0:bad.append(v)
print('Q positive',n,'sufficient fails',len(bad),'max ratio',mx)
if bad:print('bad first',bad[0])
with open('root_stronger_scan.json','w') as f:json.dump({'max_ratio':mx,'bad':bad[:100]},f,indent=2)
