from search_numeric import vals
import math,json
pi=math.pi

def solve(m,c):
 xmax=pi*(1-1/(2*c));lo=xmax*1e-15;hi=xmax*(1-1e-15)
 vl=vals(m,c,lo);vh=vals(m,c,hi)
 if vl*vh>=0:return None
 for _ in range(55):
  mid=(lo+hi)/2;vm=vals(m,c,mid)
  if vm*vl>0:lo=mid;vl=vm
  else:hi=mid
 z=vals(m,c,(lo+hi)/2,True)
 if z['r']>=c*c:return None
 return z

def boundary(m):
 lo=2/3+max(1e-14,(m-1)*1e-9);hi=1-1e-14
 for _ in range(55):
  mid=(lo+hi)/2;z=solve(m,mid)
  if z is None or z['Q']<0:hi=mid
  else:lo=mid
 return solve(m,(lo+hi)/2)

if __name__=='__main__':
 D=[]
 for i in range(121):
  m=1+10**(-6+i/10)
  z=boundary(m)
  if z:D.append(z);print(json.dumps(z),flush=True)
 json.dump(D,open('search_boundary_results.json','w'),indent=1)
