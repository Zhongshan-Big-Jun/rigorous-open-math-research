import math,random
random.seed(4901)
def bisect(f,a,b):
 for _ in range(55):
  h=(a+b)/2
  if f(h)>0:b=h
  else:a=h
 return (a+b)/2
found=[]
for n in range(20000):
 c=random.uniform(2/3,1);m=math.exp(random.uniform(0,12));r=c*c*random.random();a=math.sqrt(r);k=m*m-1;e=1-c*c
 H=lambda z: math.atan(m*math.tan(z))
 dfn=lambda z:math.asin(a*math.sin(z))
 g=bisect(lambda z:H(z)+c*H(dfn(z))-c*math.pi/2,0,math.pi/2)
 d=dfn(g);C=g+c*d
 if math.pi/2-c*math.asin(a)<=C:continue
 B=bisect(lambda z:z-c*dfn(z)-C,0,math.pi/2);A=dfn(B)
 sg=math.sin(g);cg=math.cos(g);cd=math.cos(d)
 Q=(c*math.cos(B)-a*math.cos(A))/math.sin(B)-c*k*(1-r)**2*sg*cd*cg/(cd*(1+k*sg*sg)+c*a*cg*(1+k*r*sg*sg))
 S=c*c-r-k*e*r*math.sin(B)**2
 if Q>0 and S<0:
  found.append((m,c,r,B,g,Q,S,H(B)-c*H(A)-(1-c)*math.pi));break
print('violations',found)
