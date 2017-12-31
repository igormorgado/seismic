import pandas as pd
import numpy as np
import numpy.ma as ma
import matplotlib.pyplot as plt

msize=25
rrange=5
jump=3
start=1
dpi=96
h=500
w=500

X,Y=np.meshgrid(range(0,msize),range(0,msize))
dat=np.random.rand(msize,msize)*rrange

msk=np.zeros_like(dat)
msk[start::jump,start::jump].fill(1)
mdat=msk*dat
mdat[mdat==0]=np.nan
mmdat = ma.masked_where(np.isnan(mdat),mdat)

fig = plt.figure(figsize=(w/dpi,h/dpi),dpi=dpi)

cmap = plt.get_cmap('RdYlBu')
cmap.set_bad(color='#cccccc', alpha=1.)

plot = plt.pcolormesh(X,Y,mmdat,cmap=cmap)

plot.axes.set_ylim(0,msize-1)
plot.axes.set_xlim(0,msize-1)


fig.savefig("masked.png",dpi=dpi)

