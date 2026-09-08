import math,random,json

def flat2(t):
 lo=0.;hi=2
 for _ in range(45):
  u=(lo+hi)/2
  if math.atan(u)+(2/3)*math.atan(t*u)>math.pi/3:hi=u
  else:lo=u
 return ((lo+hi)/2)**2

def calc(c,t,g):
 r=t*t;h=1-r;x=1/math.tan(g);M=math.sqrt(x*x+h);K=x-c*t*M
 if K<=c*t*math.sqrt(h):return None
 disc=math.sqrt(K*K+(1-c*c*r)*h)
 v=(K-c*t*disc)/(1-c*c*r)
 q1=c*v-t*math.sqrt(v*v+h)
 k=max(0,((3+2*t)/(1+6*t+3*t*t))*x*x-1)
 q2=c*k*h*h*x*M/(M*(1+x*x+k)+c*t*x*(1+x*x+k*r))
 return dict(c=c,t=t,g=g,bound=(q1-q2)/x,q1=q1/x,q2=q2/x)

random.seed(52615)
bad=[];mx=None
for _ in range(200000):
 c=random.uniform(2/3,1);t=random.uniform(1/3,c);g=random.uniform(.000001,math.pi/2)
 v=calc(c,t,g)
 if v is None:continue
 if mx is None or v['bound']>mx['bound']:mx=v
 if v['bound']>0:bad.append(v)
print('max',mx,'bad',len(bad));print(bad[:1])
json.dump({'max':mx,'bad':bad[:50]},open('root_rational_bound.json','w'),indent=2)
