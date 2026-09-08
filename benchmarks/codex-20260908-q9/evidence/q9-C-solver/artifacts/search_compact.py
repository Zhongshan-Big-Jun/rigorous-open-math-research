import math,random,json

def compute(h,j,xi):
 s=1-h;c=1-(1-j)*h;L=(2-j)-(1-j)*h;M=2-h*L;N=j*L*(1-xi)/M
 t2=j*h*h*xi*(2*s+j*h*xi)*L*L/(s*s*(2-h)*M*M)
 y=s/math.sqrt(1+h*(2-h)*t2)
 D=c*(2-h)**2-N*(1+c*s*s*y)
 if D<=0:return dict(h=h,j=j,xi=xi,c=c,s=s,D=D,F=100.)
 v=N*(1+c*y)/D;u=math.sqrt(v*(1+t2)+t2)
 F=math.atan(y*u)+math.atan(u)/c
 return dict(h=h,j=j,xi=xi,c=c,s=s,N=N,D=D,t2=t2,v=v,u=u,y=y,F=F,margin=math.pi/2-F)

if __name__=='__main__':
 worst=None
 for i in range(1000000):
  h=random.random()*2/3;j=random.random();xi=random.random()
  if 1-(1-j)*h<2/3:continue
  z=compute(h,j,xi)
  if worst is None or z['F']>worst['F']:worst=z
 print('max',json.dumps(worst,indent=2))
 for xi in [0.,.25,.5,.75,1.]:print('corner',compute(2/3,.5,xi))
