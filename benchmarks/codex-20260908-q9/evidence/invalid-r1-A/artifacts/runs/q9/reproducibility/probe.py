import math, json, time
pi=math.pi
H=lambda m,z: math.atan2(m*math.sin(z),math.cos(z))
def bisect(f,a,b,n=52):
 fa=f(a)
 for _ in range(n):
  h=(a+b)/2; fh=f(h)
  if (fa<0)==(fh<0): a=h; fa=fh
  else:b=h
 return (a+b)/2
def geometry(c,r,B):
 s=math.sqrt(r); A=math.asin(s*math.sin(B))
 target=B-c*A
 g=bisect(lambda g:g+c*math.asin(s*math.sin(g))-target,0,B,n=40)
 d=math.asin(s*math.sin(g))
 # solve for t=m tan(g); ratio tan(d)/tan(g)
 q=math.tan(d)/math.tan(g)
 t=bisect(lambda t: math.atan(q*t)+math.atan(t)/c-pi/2,0,math.tan(c*pi/2),n=44)
 m=t/math.tan(g)
 res=H(m,B)-(1-c)*pi-c*H(m,A)
 return res,m,A,d,g

def values(c,r,B):
 res,m,A,d,g=geometry(c,r,B);k=m*m-1;e=1-c*c;s=math.sqrt(r)
 hb=H(m,B);hg=H(m,g)
 V=pi+hg-hb+m*(B-g)
 U=(pi-hb)*math.sin(B)**2+hg*math.sin(g)**2
 Q=(c*math.cos(B)-s*math.cos(A))/math.sin(B)-c*k*(1-r)**2*math.sin(g)*math.cos(d)*math.cos(g)/(math.cos(d)*(1+k*math.sin(g)**2)+c*s*math.cos(g)*(1+k*r*math.sin(g)**2))
 R=(c*c-r)*V-k*e*r*U
 return dict(c=c,r=r,B=B,g=g,m=m,A=A,d=d,Q=Q,R=R,T=r*U/V,threshold=(c*c-r)/(k*e) if k else None,res=res)

def scan(cs,fs,steps=80):
 results=[]; best=None
 for c in cs:
  for f in fs:
   r=c*c*f
   Bs=[.00001+(pi/2-.00002)*i/steps for i in range(steps+1)]
   old=geometry(c,r,Bs[0])[0]
   for i in range(1,len(Bs)):
    new=geometry(c,r,Bs[i])[0]
    if new*old<0:
     B=bisect(lambda B: geometry(c,r,B)[0],Bs[i-1],Bs[i])
     v=values(c,r,B)
     if v['m']>1:
      results.append(v)
      if best is None or (v['Q']>0 and (best['Q']<=0 or v['R']<best['R'])):best=v
    old=new
 return results,best
if __name__=='__main__':
 start=time.monotonic()
 res,best=scan([.67,.7,.75,.8,.85,.9,.95,.98,.99],[.001,.005,.01,.03,.06,.1,.2,.35,.5,.7,.85,.95,.99],50)
 with open('runs/q9/reproducibility/probe_results.json','w') as f:json.dump(res,f,indent=2)
 print('seconds',time.monotonic()-start,'roots',len(res),'Q-positive',sum(v['Q']>0 for v in res))
 print('best',best)
 for c in sorted(set(v['c'] for v in res)):
  vs=[v for v in res if v['c']==c]
  print(c,'m range',min(v['m'] for v in vs),max(v['m'] for v in vs),'Q range',min(v['Q'] for v in vs),max(v['Q'] for v in vs),'R range',min(v['R'] for v in vs),max(v['R'] for v in vs))
