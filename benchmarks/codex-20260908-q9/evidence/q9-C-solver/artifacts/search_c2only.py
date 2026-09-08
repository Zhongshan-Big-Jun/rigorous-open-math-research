import math,random,json
pi=math.pi

def solve(m,c,r,Bfrac):
 s=math.sqrt(r);lo=0.;hi=pi/2
 for _ in range(45):
  g=(lo+hi)/2;d=math.asin(s*math.sin(g))
  if math.atan(m*math.tan(d))+math.atan(m*math.tan(g))/c>pi/2:hi=g
  else:lo=g
 g=(lo+hi)/2;d=math.asin(s*math.sin(g));B=g+(pi/2-g)*Bfrac;A=math.asin(s*math.sin(B));k=m*m-1;sb=math.sin(B);sg=math.sin(g);cg=math.cos(g);cd=math.cos(d)
 Q=(c*math.cos(B)-s*math.cos(A))/sb-c*k*(1-r)**2*sg*cd*cg/(cd*(1+k*sg*sg)+c*s*cg*(1+k*r*sg*sg))
 S=(c*c-r)-k*(1-c*c)*r*sb*sb
 return dict(m=m,c=c,r=r,B=B,g=g,A=A,d=d,Q=Q,S=S)
if __name__=='__main__':
 D=[]
 for j in range(200000):
  m=1+10**random.uniform(-5,5);c=2/3+random.random()/3;r=c*c*random.random();z=solve(m,c,r,random.random())
  if z['Q']>0 and z['S']<0:
   print('FAIL',json.dumps(z),flush=True);D.append(z)
   if len(D)>20:break
 print('done',len(D),flush=True);json.dump(D,open('search_c2only_results.json','w'),indent=1)
