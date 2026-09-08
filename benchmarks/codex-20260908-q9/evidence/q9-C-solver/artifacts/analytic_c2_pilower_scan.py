import math,random
random.seed(302)
worst=(-1,None)
for i in range(300000):
 c=random.uniform(2/3,1);s=random.uniform(1/3,c);r=s*s
 g=random.uniform(0,math.pi/2);d=math.asin(s*math.sin(g))
 target=g+c*d
 if target>=math.pi/2-c*math.asin(s):continue
 lo=g;hi=math.pi/2
 for j in range(40):
  B=(lo+hi)/2;A=math.asin(s*math.sin(B))
  if B-c*A>target:hi=B
  else:lo=B
 q1=(c*math.cos(B)-s*math.cos(A))/math.sin(B)
 tc=math.sqrt(3)
 K=(2*tc/(1+s+math.sqrt((1+s)**2+4*s*tc*tc)))**2
 k=max(0,K/math.tan(g)**2-1)
 q2=c*k*(1-r)**2*math.sin(g)*math.cos(d)*math.cos(g)/(math.cos(d)*(1+k*math.sin(g)**2)+c*s*math.cos(g)*(1+k*r*math.sin(g)**2))
 norm=(q1-q2)*math.tan(g)
 if norm>worst[0]:worst=(norm,(c,s,g,B,k,q1,q2))
print(worst)
