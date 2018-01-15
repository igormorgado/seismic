import pandas as pd
import numpy as np
import numpy.ma as ma
import matplotlib.pyplot as plt

msize=25
rrange=int(msize**0.5)
jump=3
start=int(jump/2)

X,Y=np.meshgrid(range(0,msize),range(0,msize))
dat=np.random.rand(msize,msize)*rrange

msk=np.zeros_like(dat)
msk[start::jump,start::jump].fill(1)
mdat=msk*dat
mdat[mdat==0]=np.nan
mmdat = ma.masked_where(np.isnan(mdat),mdat)

fargs={ 'edgecolor': 'w',
        'facecolor': 'w',
        'frameon': True,
        }

fig, ax = plt.subplots(figsize=(10,10),**fargs)
ax.axis('equal')

cmap = plt.get_cmap('RdYlBu')
cmap.set_bad(color='#cccccc', alpha=1.)

plot = ax.pcolormesh(X,Y,mmdat,cmap=cmap)

ax.set_ylim(0,msize-1)
ax.set_xlim(0,msize-1)

fargs['bbox_inches']='tight'

fig.savefig("masked100.png",dpi=100,**fargs)
fig.set_size_inches(10,8)
fig.colorbar(plot)
fig.savefig("masked101.png",dpi=100,**fargs)
