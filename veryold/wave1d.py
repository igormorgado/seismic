# -*- coding: utf-8 -*-
"""
Created on Sat Apr 16 13:37:33 2016

@author: morga
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as anim
import cython
from scipy import signal

dx=0.01
dt=0.05
tmin=0.0
tmax=2.0
xmin=-5.0
xmax=5.0
c=1.0

rsq=(c*dt/dx)**2

nx=int((xmax-xmin)/dx) + 1
nt=int((tmax-tmin)/dt) + 2

u = np.zeros((nt,nx))

def gaussian(x,std=1):
    return np.exp(-(1/2)*(x/std)**2)    

k=linspace(xmin,xmax,nx)    
u[0]=gaussian(k,.5)
u[1]=u[0]

def calc():
    for t in range(1,nt-1):
        for a in range(1, nx-1):
            u[t+1,a] = 2*(1-rsq)*u[t,a]-u[t-1,a]+rsq*(u[t,a-1]+u[t,a+1])
     

#Animation       
#fig = plt.figure()
#plts = []
#plt.hold("off")
#for i in range(nt):
#    p, = plt.plot(u[i,:], 'k')
#    plts.append([p])
#ani = anim.ArtistAnimation(fig,plts,interval=50, repeat_delay=3000)
#ani.save('wave.mp4')

