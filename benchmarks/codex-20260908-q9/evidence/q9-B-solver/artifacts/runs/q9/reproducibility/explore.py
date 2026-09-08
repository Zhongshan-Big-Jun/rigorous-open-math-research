"""Floating-point exploration only; no certified conclusions."""
import math,json
from pathlib import Path
pi=math.pi

def bisect(f,a,b,it=55):
 fa=f(a);fb=f(b)
 if fa*fb>0: raise ValueError((a,b,fa,fb))
 for _ in range(it):
  z=(a+b)/2;fz=f(z)
  if fz*fa>0:a=z;fa=fz
  else:b=z
 return (a+b)/2

def calc(m,c,B):
 H=lambda z:math.atan2(m*math.sin(z),math.cos(z))
 aH=(H(B)-(1-c)*pi)/c
 if not 0<aH<pi/2:return None
 A=math.atan2(math.sin(aH),m*math.cos(aH))
 r=(math.sin(A)/math.sin(B))**2
 if not 0<r<c*c:return None
 sr=math.sqrt(r)
 dfunc=lambda g:math.asin(sr*math.sin(g))
 g=bisect(lambda g:H(dfunc(g))+H(g)/c-pi/2,0,pi/2)
 d=dfunc(g);k=m*m-1;e=1-c*c
 V=pi+H(g)-H(B)+m*(B-g)
 U=(pi-H(B))*math.sin(B)**2+H(g)*math.sin(g)**2
 Q=(c*math.cos(B)-sr*math.cos(A))/math.sin(B)-c*k*(1-r)**2*math.sin(g)*math.cos(d)*math.cos(g)/(math.cos(d)*(1+k*math.sin(g)**2)+c*sr*math.cos(g)*(1+k*r*math.sin(g)**2))
 R=(c*c-r)*V-k*e*r*U
 return dict(m=m,c=c,r=r,B=B,g=g,A=A,d=d,Q=Q,R=R,T=r*U/V,margin=(c*c-r)/(k*e)-r*U/V,res=B-g-c*(A+d),suff=c*c-r-k*e*r*math.sin(B)**2)

def roots(m,c,n=200):
 lo=math.atan2(math.sin((1-c)*pi),m*math.cos((1-c)*pi))
 vals=[];last=None
 for i in range(n+1):
  # Cluster toward both ends.
  t=(1-math.cos(pi*(i+.000001)/(n+.000002)))/2
  B=lo+(pi/2-lo)*t
  v=calc(m,c,B)
  if v is None:continue
  if last and last['res']*v['res']<0:
   z=bisect(lambda b:calc(m,c,b)['res'],last['B'],B)
   vals.append(calc(m,c,z))
  last=v
 return vals

if __name__=='__main__':
 out=[]
 for m in [1.001,1.01,1.1,1.5,2,3,5,10,20,50,100,300,1000,10000]:
  for c in [2/3+.00001,.67,.68,.7,.75,.8,.85,.9,.95,.98,.99,.999,.9999]:
   out+=roots(m,c)
 Path('runs/q9/reproducibility/scan.json').write_text(json.dumps(out,indent=2))
 pos=[v for v in out if v['Q']>0]
 print('roots',len(out),'Qpositive',len(pos),'counterexamples',sum(v['R']<=0 for v in pos))
 if pos:
  print('smallest margins',json.dumps(sorted(pos,key=lambda v:v['margin'])[:8],indent=2))
  print('Qpositive where supplied sufficient condition fails',len([v for v in pos if v['suff']<0]))
 print('sample',json.dumps(out[::max(1,len(out)//10)],indent=2))
