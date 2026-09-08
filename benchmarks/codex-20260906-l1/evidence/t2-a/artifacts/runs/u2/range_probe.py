# Falsification probe only; not a proof.
from collections import defaultdict
from math import sqrt
p={(0,0,0):1.0}
for t in range(1,81):
 q=defaultdict(float)
 for (a,b,z),v in p.items():
  for d in (-1,1):
   w=z+d
   q[min(a,w),max(b,w),w]+=v/2
 p=q
 if t in (5,10,20,40,80):
  ks=set(p)|{(a+2,b+2,z+2) for a,b,z in p}
  tv=sum(abs(p.get((a,b,z),0)-p.get((a-2,b-2,z-2),0)) for a,b,z in ks)/2
  print(t,len(p),tv,tv*sqrt(t),flush=True)
