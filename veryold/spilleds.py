import numpy as np
import numpy.ma as ma
import matplotlib.pyplot as plt
from scipy.signal import convolve2d


def spill(arr, nval=0, m=1):
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

def demo_mesh(mesh_size=15,random_range=5, start=2, increment=3):
    
    # Full random array
    mesh = np.random.rand(mesh_size,mesh_size)*random_range

    # A zeroed array
    mask_mesh=np.zeros_like(mesh)

    # Fill ones in special places
    mask_mesh[start::increment,start::increment].fill(1)

    # Element wise product
    weighted_mask=mask_mesh*mesh
    
    return weighted_mask

def mask_mesh(source_mesh):
    # Turns zero into np.nans and returns a masked mesh
    temp_mesh=np.copy(source_mesh)

    temp_mesh[temp_mesh==0]=np.nan
    masked_mesh = ma.masked_where(np.isnan(temp_mesh),temp_mesh)

    return temp_mesh

def plot_mesh(mesh,height=500,weigth=500, dpi=96):

    x = mesh.shape[0]
    y = mesh.shape[1]

    X,Y=np.meshgrid(range(0,x),range(0,y))

    cmap = plt.get_cmap('RdYlBu')
    cmap.set_bad(color='#cccccc', alpha=1.)

    fig = plt.figure(figsize=(weigth/dpi,weigth/dpi),dpi=dpi)

    plot = plt.pcolormesh(X,Y,mesh,cmap=cmap)
    plot.axes.set_ylim(0,y-1)
    plot.axes.set_xlim(0,x-1)
    
    return fig


if __name__ == '__main__':

    # Mesh attributes
    mesh_size=50
    random_range=10
    start=5
    increment=10
    m=3

    # Figure attributes
    dpi=96
    height=500
    weigth=500

    mesh = demo_mesh(mesh_size, random_range, start, increment)

    # Here we convert the zeroes to nans and return a mask
    mesh_masked = mask_mesh(mesh)
    fig = plot_mesh(mesh_masked, height, weigth, dpi)
    fig.savefig("masked.png",dpi=dpi)

    # for m in range(1,6):
    #     # print "M: {0}".format(m)
    #     spill_mesh = spill2(mesh,m=m)
    #     spill_mesh_masked = mask_mesh(spill_mesh)
    #     fig = plot_mesh(spill_mesh_masked, height, weigth, dpi)
    #     filename="spill{0}.png".format(m)
    #     # print filename
    #     #fig.savefig(filename,dpi=dpi)

    # plt.show()

