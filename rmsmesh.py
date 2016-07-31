import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import sys

if len(sys.argv) > 1:
    dataset=sys.argv[1]
else:
    dataset="rms.csv"

df = pd.read_csv(dataset)

# Fields
x=df.columns.values.tolist()[1]
y=df.columns.values.tolist()[0]
attributes=df.columns.values.tolist()[2:]

# Organizing the data
imgp = df.pivot(index=y, columns=x)

ymin=df[y].min()
ymax=df[y].max()
xmin=df[x].min()
xmax=df[x].max()

extent = [xmin - 0.5, xmax + 0.5, ymin - 0.5, ymax + 0.5]
X,Y = np.meshgrid(range(xmin,xmax),range(ymin,ymax))


# Defining matplotlib params
matplotlib.rcParams['xtick.labelsize'] = 8
matplotlib.rcParams['ytick.labelsize'] = 8

vlim={ 'RMS_DEEPATTR':1500,'RMS_MIDATTR': 3500, 'RMS_SHALLOWATTR': 2000 }

for attribute in attributes:

    img = imgp[attribute].reindex(index=range(ymin,ymax+1),columns=range(xmin,xmax+1))
    C = img.values
    Cm = np.ma.masked_invalid(C)
    
    fig = plt.figure(1,figsize=(10,8),dpi=100,facecolor='w',edgecolor='k')
    plot = fig.add_subplot(111)
    
    figtitle="{0} - {1}".format(attribute, '.'.join(dataset.replace("___","/").split(".")[:-1]))
    print figtitle
    plot.set_title(figtitle, y=-0.11)

    plot.spines["top"].set_visible(False)
    plot.spines["bottom"].set_visible(False)
    plot.spines["right"].set_visible(False)
    plot.spines["left"].set_visible(False)

    plot.get_xaxis().tick_bottom()
    plot.get_yaxis().tick_left()

    plot.set_axis_bgcolor("#e9e9e9")

    plt.ylim(ymin,ymax)
    plt.xlim(xmin,xmax)
    plt.xlabel(x)
    plt.ylabel(y)

    plt.pcolormesh(X,Y,Cm,vmax=vlim[attribute])
    plt.xlim(xmin,xmax)
    plt.ylim(ymin,ymax)

    plt.colorbar()

    figname='_'.join(dataset.split('.')[:-1]) + "_" + attribute + '.png'
    fig.savefig(figname, dpi=100,bbox_inches='tight')

    plt.clf()
