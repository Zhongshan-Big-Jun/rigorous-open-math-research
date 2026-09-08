from explore import *
import random,time
rng=random.Random(219);t0=__import__('time').monotonic();out=[];cnt=0;pos=0
while __import__('time').monotonic()-t0<15:
 m=1+math.exp(rng.uniform(-7,12));c=rng.uniform(2/3,1);t=c*rng.random();r=t*t
 H=lambda z:math.atan2(m*math.sin(z),math.cos(z))
 dfunc=lambda g:math.asin(t*math.sin(g))
 g=bisect(lambda g:H(dfunc(g))+H(g)/c-pi/2,0,pi/2)
 d=dfunc(g);a=lambda b:math.asin(t*math.sin(b))
 f=lambda b:b-g-c*(a(b)+d)
 if f(pi/2)<=0:continue
 B=bisect(f,g,pi/2);A=a(B);k=m*m-1;e=1-c*c
 Q=(c*math.cos(B)-t*math.cos(A))/math.sin(B)-c*k*(1-r)**2*math.sin(g)*math.cos(d)*math.cos(g)/(math.cos(d)*(1+k*math.sin(g)**2)+c*t*math.cos(g)*(1+k*r*math.sin(g)**2))
 S=c*c-r-k*e*r*math.sin(B)**2
 cnt+=1
 if Q>0:
  pos+=1
  if S<=0:
   v=dict(m=m,c=c,r=r,B=B,g=g,A=A,d=d,Q=Q,S=S,C1=H(B)-(1-c)*pi-c*H(A));out.append(v)
   print(json.dumps(v));break
print('valid',cnt,'Qpositive',pos,'strongerfail',len(out))
Path('runs/q9/reproducibility/relax_probe.json').write_text(json.dumps(out,indent=2))
