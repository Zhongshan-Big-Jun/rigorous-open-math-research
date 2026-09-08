import math,random
random.seed(4902)
def bisect(f,a,b):
 for _ in range(55):
  h=(a+b)/2
  if f(h)>0:b=h
  else:a=h
 return (a+b)/2
found=[];best=(-1e100,None)
for n in range(30000):
 c=random.uniform(2/3,1);r=c*c*random.random();a=math.sqrt(r);e=1-c*c
 B=random.uniform(1e-8,math.pi/2);A=math.asin(a*math.sin(B));C=B-c*A
 g=bisect(lambda z:z+c*math.asin(a*math.sin(z))-C,0,B);d=math.asin(a*math.sin(g))
 sg=math.sin(g);cg=math.cos(g);cd=math.cos(d);k=(c*c-r)/(e*r*math.sin(B)**2)
 Q=(c*math.cos(B)-a*math.cos(A))/math.sin(B)-c*k*(1-r)**2*sg*cd*cg/(cd*(1+k*sg*sg)+c*a*cg*(1+k*r*sg*sg))
 if Q>best[0]:best=(Q,(c,r,B,g,k))
 if Q>0:
  found.append((c,r,B,g,k,Q));break
print('violations',found,'best',best)
