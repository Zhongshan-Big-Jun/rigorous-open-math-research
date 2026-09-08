from search_relaxed import solve
import math,random,json
bad=[];worst=None
for j in range(2000):
 c=2/3+random.random()/3;r=c*c*random.random()
 prev=None
 for m in [1+10**(-6+i*.3) for i in range(41)]:
  z=solve(m,c,r)
  if z is None:continue
  z['q']=z['Q']*math.sin(z['B'])
  if prev and z['q']>prev['q']+1e-8:
   record=dict(prev=prev,next=z,increase=z['q']-prev['q'])
   bad.append(record)
   if worst is None or record['increase']>worst['increase']:worst=record
  prev=z
print('violations',len(bad),'worst',json.dumps(worst,indent=2))
json.dump(bad[:100],open('search_monotonic_results.json','w'),indent=1)
