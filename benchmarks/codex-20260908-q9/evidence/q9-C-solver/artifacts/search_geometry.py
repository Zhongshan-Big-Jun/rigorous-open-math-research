import math,random,json
pi=math.pi

def solve(c,r,g):
 s=math.sqrt(r);d=math.asin(s*math.sin(g));tar=g+c*d
 if tar>=pi/2-c*math.asin(s): return None
 lo=g;hi=pi/2
 for _ in range(45):
  B=(lo+hi)/2;A=math.asin(s*math.sin(B))
  if B-c*A>tar:hi=B
  else:lo=B
 B=(lo+hi)/2;A=math.asin(s*math.sin(B));sb=math.sin(B);cb=math.cos(B);sg=math.sin(g);cg=math.cos(g);cd=math.cos(d);ca=math.cos(A)
 J=(c*cb-s*ca)/sb
 if J<=0:return None
 D0=cd+c*s*cg;D1=sg*sg*(cd+c*s*r*cg);delta=c*c-r;e=1-c*c;k=delta/(e*r*sb*sb)
 Q=J-c*k*(1-r)**2*sg*cd*cg/(D0+k*D1)
 return dict(c=c,r=r,B=B,g=g,A=A,d=d,m=math.sqrt(1+k),Q=Q,J=J,Q_over_J=Q/J)
if __name__=='__main__':
 D=[];worst=None
 for j in range(200000):
  c=2/3+random.random()/3;r=c*c*random.random();g=random.random()*pi/2
  z=solve(c,r,g)
  if z is None:continue
  if worst is None or z['Q_over_J']>worst['Q_over_J']:worst=z
  if z['Q']>0:
   print('FAIL',json.dumps(z),flush=True);D.append(z)
   if len(D)>20:break
 print('worst',json.dumps(worst),flush=True)
 json.dump(D,open('search_geometry_results.json','w'),indent=1)
