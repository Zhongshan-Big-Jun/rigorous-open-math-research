import math,random,json
rng=random.Random(397)
worst=(-1,None)
for i in range(200000):
 c=rng.uniform(2/3,1);t=c*rng.uniform(.5,1);u=c*t
 aa=c*(1+(c*c+2)*t*t);bb=t*(1+2*c*c+c*c*t*t);wm=aa/bb
 w=1+rng.random()*(wm-1)
 if wm<1:raise ValueError()
 z2=(w*w-1)/(1-t*t)
 j=.49*(1+c)**2*w*w/(w+u)**2
 # lower h² j; if j<z², m>1 lower only z².
 h2=max(j,z2)
 first=(aa-bb*w)/(1-u*u)
 upper=first-c*(1-t*t)**2*(h2-z2)/(1+u*w+h2*(1+c*t**3/w))
 normalized=upper/(1-t*t)**2
 if normalized>worst[0]:worst=(normalized,[c,t,w,j-z2,upper])
 if upper>1e-12:
  print('FAILED',worst);break
else:print('SURVIVED',worst)
