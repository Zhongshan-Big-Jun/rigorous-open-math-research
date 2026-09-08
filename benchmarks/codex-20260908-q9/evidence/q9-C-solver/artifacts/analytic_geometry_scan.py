import math, random
random.seed(417)
def geometry(c,s,B):
 A=math.asin(s*math.sin(B));lo=0.;hi=B
 for _ in range(45):
  g=(lo+hi)/2;d=math.asin(s*math.sin(g))
  if g+c*d>B-c*A:hi=g
  else:lo=g
 return A,g,d
best=None;count=0
for i in range(300000):
 c=random.uniform(2/3,1);s=c*random.random();B=math.pi/2*random.random()
 A,g,d=geometry(c,s,B);r=s*s;e=1-c*c;t=c*c-r;x=math.sin(B)**2;y=math.sin(g)**2
 k0=t/(e*r*x)
 K2=c*math.cos(g)*math.cos(d)/(s*y)-1
 if K2<k0:continue
 q1=(c*math.cos(B)-s*math.cos(A))/math.sin(B)
 E=c*(1-r)**2*math.sin(g)*math.cos(d)*math.cos(g)
 D0=math.cos(d)+c*s*math.cos(g);D1=y*(math.cos(d)+c*r*s*math.cos(g))
 Q=q1-k0*E/(D0+k0*D1)
 if Q>0:
  count+=1
  if best is None or Q>best[0]: best=(Q,c,s,B,g,k0,K2)
print('counterexamples',count,'best',best)
