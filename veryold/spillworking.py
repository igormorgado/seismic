# WORKING!
import numpy as np
import numpy.ma as ma
import matplotlib.pyplot as plt

def spill(arr, nval=[0,], m=1):
    narr=np.copy(arr)
    nval=np.asarray(nval)
    for i in range(arr.shape[0]):
        for j in range(arr.shape[1]):
            if (not np.isnan(arr[i][j])) and (arr[i][j]  not in nval):  
                # print "{0},{1}: {2}".format(i,j,arr[i][j])
                # print narr[i-m:i+m+1:1,j-m:j+m+1:1]
                narr[i-m:i+m+1:1,j-m:j+m+1:1]=arr[i][j]                    
    return narr

def spill2(arr, nval=0, m=1):
    return convolve2d(arr, np.ones((2*m+1, 2*m+1)), mode='same')


msize=50
rrange=10
jump=10
start=5
dpi=96
h=500
w=500

X,Y=np.meshgrid(range(0,msize),range(0,msize))
dat=np.random.rand(msize,msize)*rrange


msk=np.zeros_like(dat)
msk[start::jump,start::jump].fill(1)
mdat=msk*dat
mdat[mdat==0]=np.nan


# I would like to be able to apply spill after the change all 0 to np.nan
# but inside spill function the NaNs from input array are being considered
# float, while np.nan is numpy.float64. The If is failing because that.
sdat = spill(mdat,m=3)

mmdat = ma.masked_where(np.isnan(mdat),mdat)
smdat = ma.masked_where(np.isnan(sdat),sdat)

#sdat[sdat==0]=np.nan
#smdat = ma.masked_where(np.isnan(sdat),sdat)

cmap = plt.get_cmap('RdYlBu')
cmap.set_bad(color='#cccccc', alpha=1.)

fig1 = plt.figure(figsize=(w/dpi,h/dpi),dpi=dpi)
plot = plt.pcolormesh(X,Y,mmdat,cmap=cmap)
plot.axes.set_ylim(0,msize-1)
plot.axes.set_xlim(0,msize-1)
fig1.savefig("masked.png",dpi=dpi)

fig2 = plt.figure(figsize=(w/dpi,h/dpi),dpi=dpi)
plot2 = plt.pcolormesh(X,Y,smdat,cmap=cmap)
plot2.axes.set_ylim(0,msize-1)
plot2.axes.set_xlim(0,msize-1)
fig2.savefig("spilled.png",dpi=dpi)

plt.show()

