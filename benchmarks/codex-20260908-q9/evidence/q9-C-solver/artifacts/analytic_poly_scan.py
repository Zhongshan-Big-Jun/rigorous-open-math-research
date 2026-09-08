import random, math
random.seed(53)
mn=(1e9,None);mnD=(1e9,None);mnW=(1e9,None);mxP=(0,None)
for _ in range(500000):
 c=random.uniform(2/3,1);t=random.uniform(1/3,c);r=t*t;h=1-r
 L=(3+2*t)/(1+6*t+3*r);W=1+L*h
 P=c*(1+c*c*r+2*r)/(1-c*c*r);D=t*(1+2*c*c+c*c*r)/(1-c*c*r)
 vmax=P/D
 if vmax<1:continue
 v=1+(vmax-1)*random.random()
 A3=c*(D*t-h);A2=D*(1+L)-P*c*t;A1=c*h*W-P*(1+L)+D*c*t*r*L;A0=-P*c*t*r*L
 N=((A3*v+A2)*v+A1)*v+A0
 ND=(3*A3*v+2*A2)*v+A1
 NW=W-vmax*vmax
 if N<mn[0]:mn=(N,(c,t,v,vmax,A3,A2,A1,A0))
 if ND<mnD[0]:mnD=(ND,(c,t,v,vmax,A3,A2,A1,A0))
 if NW<mnW[0]:mnW=(NW,(c,t))
print('N',mn,'derivative',mnD,'W',mnW)
