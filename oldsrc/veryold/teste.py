import pandas as pd
import numpy as np
import numpy.ma as ma
import matplotlib.pyplot as plt

msize=25
rrange=int(msize**0.5+1)
jump=5
start=int(jump/2)

# 0 to 24
X,Y=np.meshgrid(range(0,msize),range(0,msize))

dat=np.random.randint(rrange,size=(msize,msize))

fig = plt.figure()

cmap = plt.get_cmap('RdYlBu')
cmap.set_bad(color='k', alpha =1.)


msk=np.ones_like(dat)
msk[start::jump,start::jump].fill(0)
mdat = ma.masked_array(dat, mask=msk)

plot = plt.pcolormesh(X,Y,mdat,cmap=cmap)
plt.axis([0,msize-1,0,msize-1])
plt.colorbar()
fig.savefig("masked.png")




#plt.pcolormesh(X,Y,dat,cmap=cmap)
#fig.savefig("data.png")
#
#plt.pcolormesh(X,Y,msk,cmap=cmap)
#fig.savefig("mask.png")
#
# Method 2
#msk=np.zeros_like(dat)
#msk[start::jump,start::jump].fill(1)
#mdat=msk*dat
#
#plt.pcolormesh(X,Y,msk,cmap=cmap)
#fig.savefig("2mask.png")
#
#plt.pcolormesh(X,Y,mdat,cmap=cmap)
#fig.savefig("2masked.png")

