# -*- coding: utf-8 -*-
"""
Created on Sat Apr 16 18:15:57 2016

@author: morga
"""

import numpy as np                      
import matplotlib.pyplot as plt
import matplotlib.animation as animation

#defining dimensions
xdim=720
time_tot = 100000
xsource = xdim/2

#stability factor
S=1

#Speed of light
c=1
epsilon0=1
mu0=1

delta =1
deltat = S*delta/c

Ez = np.zeros(xdim)
Hy = np.zeros(xdim)

epsilon = epsilon0*np.ones(xdim)
mu = mu0*np.ones(xdim)

fig , axis = plt.subplots(1,1)
axis.set_xlim(len(Ez))
axis.set_ylim(-3,3)
axis.set_title("E Field")
line, = axis.plot([],[])

def init():
    line.set_data([],[])
    return line,

def animate(n, *args, **kwargs):
    Hy[0:xdim-1] = Hy[0:xdim-1]+(delta/(delta*mu[0:xdim-1]))*(Ez[1:xdim]-Ez[0:xdim-1])
    Ez[1:xdim]= Ez[1:xdim]+(delta/(delta*epsilon[1:xdim]))*(Hy[1:xdim]-Hy[0:xdim-1])
    Ez[xsource] = Ez[xsource] + 30.0*(1/np.sqrt(2*np.pi))*np.exp(-(n-80.0)**2/(100))
    ylims = axis.get_ylim()
    if (abs(np.amax(Ez))>ylims[1]):
        axis.set_ylim(-(np.amax(Ez)+2),np.amax(Ez)+2)
    line.set_data(np.arange(len(Ez)),Ez)
    return line,

ani = animation.FuncAnimation(fig, animate, init_func=init, frames=(time_tot), interval=10, blit=False, repeat =False)
fig.show()