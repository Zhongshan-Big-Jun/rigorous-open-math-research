import math,random,json
p=math.pi

def solve(m,c,r):
 s=math.sqrt(r)
 lo=0.;hi=p/2
 for _ in range(45):
  g=(lo+hi)/2; d=math.asin(s*math.sin(g))
  if math.atan(m*math.tan(d))+math.atan(m*math.tan(g))/c>p/2: hi=g
  else: lo=g
 g=(lo+hi)/2;d=math.asin(s*math.sin(g));target=g+c*d
 if target>p/2-c*math.asin(s):return None
 lo=g;hi=p/2
 for _ in range(45):
  B=(lo+hi)/2;A=math.asin(s*math.sin(B))
  if B-c*A>target:hi=B
  else:lo=B
 B=(lo+hi)/2;A=math.asin(s*math.sin(B))
 k=m*m-1;e=1-c*c;sg=math.sin(g);cg=math.cos(g);cd=math.cos(d);sb=math.sin(B)
 hb=math.atan(m*math.tan(B));hg=math.atan(m*math.tan(g));V=p+hg-hb+m*(B-g);U=(p-hb)*sb*sb+hg*sg*sg
 Q=(c*math.cos(B)-s*math.cos(A))/sb-c*k*(1-r)**2*sg*cd*cg/(cd*(1+k*sg*sg)+c*s*cg*(1+k*r*sg*sg))
 R=(c*c-r)*V-k*e*r*U
 return dict(m=m,c=c,r=r,B=B,g=g,A=A,d=d,Q=Q,R=R,sufficient=(c*c-r)-k*e*r*sb*sb,C1=hb-c*math.atan(m*math.tan(A))-(1-c)*p,ratio=k*e*r*U/((c*c-r)*V))
if __name__=='__main__':
 candidates=[];worst=None
 for j in range(100000):
  m=1+10**random.uniform(-5,5);c=2/3+random.random()/3;r=c*c*random.random()
  z=solve(m,c,r)
  if z is None: continue
  if z['Q']>0:
   if worst is None or z['ratio']>worst['ratio']:worst=z
   if z['sufficient']<0:
    print('UNSUFFICIENT',json.dumps(z),flush=True);candidates.append(z)
    if len(candidates)>30:break
 print('worst',json.dumps(worst))
 json.dump(candidates,open('search_relaxed_results.json','w'),indent=1)
