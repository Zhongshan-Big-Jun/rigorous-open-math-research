import math,random,json

def calc(c,t,m):
 lo=0.;hi=math.pi/2
 for _ in range(46):
  g=(lo+hi)/2;d=math.asin(t*math.sin(g))
  if math.atan(m*math.tan(g))+c*math.atan(m*math.tan(d))>c*math.pi/2:hi=g
  else:lo=g
 g=(lo+hi)/2;d=math.asin(t*math.sin(g));r=t*t;h=1-r;k=m*m-1
 x=1/math.tan(g);M=math.sqrt(x*x+h);K=x-c*t*M
 if K<=c*t*math.sqrt(h):return None
 disc=math.sqrt(K*K+(1-c*c*r)*h)
 v=(K-c*t*disc)/(1-c*c*r)
 q1=c*v-t*math.sqrt(v*v+h)
 q2=c*k*h*h*x*M/(M*(1+x*x+k)+c*t*x*(1+x*x+k*r))
 return dict(c=c,t=t,m=m,g=g,bound=(q1-q2)/x,q1=q1/x,q2=q2/x)

if __name__=='__main__':
 random.seed(946105)
 bad=[];mx=None
 for _ in range(100000):
  c=random.uniform(2/3,1);t=random.uniform(1/3,c);m=1+10**random.uniform(-6,6)
  v=calc(c,t,m)
  if v is None:continue
  if mx is None or v['bound']>mx['bound']:mx=v
  if v['bound']>0:bad.append(v)
 print('max',mx,'bad',len(bad)); print(bad[:1])
 json.dump({'max':mx,'bad':bad[:50]},open('root_geo_envelope.json','w'),indent=2)
