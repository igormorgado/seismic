#!/usr/bin/env python


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

seqs = ( 249, 251, 252, 253, 254, 255, 256, 257, 258, 260, 261, 262 )
brcal_fn = "OFL_BRCAL1_seq"
rdscl_fn = "120P_RD_SCALAR_seq"
tgain_fn = "tr_gainx_seq"


def cB(mL):
    """Convert millilog to centibel"""
    return mL/5 
        
def mL(cB):
    """Convert centibel to millilog"""
    return 5*cB

def G(g):
    return 10**(-g/200)

def g(G):
    return -200*np.log10(G)


channels=7776
cables=12
channels_per_cable=channels/cables
receivers=12
receivers_per_cable=channels_per_cable/receivers

#seqs= (249,)


for seq in seqs:
    # This data is what is on the dataset
    dftr = pd.read_csv("{}{}.csv".format(tgain_fn, seq))
    dftr['brcal'] = g(dftr.tr_gainx)
    
    # This data was calculated with the boat new information
    dfbr = pd.read_csv("{}{}.csv".format(brcal_fn, seq), 
                        names=['channel','brcal','none'],
                        sep=';', 
                        header=0, 
                        usecols=[0,1])
    dfbr['tr_gainx'] = G(dfbr.brcal)


    # tr_gainx as nparray
    bef = dftr.tr_gainx.as_matrix()
    aft = dfbr.tr_gainx.as_matrix()
    
    # 2d array each line is one cable
    try:
        imageaft=np.concatenate((imageaft,np.split(aft,cables)))
    except NameError:
        imageaft=np.split(aft,cables)

    try:
        imagebef=np.concatenate((imagebef,np.split(bef,cables)))
    except NameError:
        imagebef=np.split(bef,cables)



# DRAW THE FIGURE
cmap = plt.cm.RdYlBu_r
figsize=(16,9)

fig, ax = plt.subplots(nrows=2, sharex=True, figsize=(16,9), dpi=150)

fig.suptitle('BRCal scalars comparison', fontsize=20)

im = ax[0].imshow(imagebef, aspect='auto', origin=0, cmap=cmap,label='Before')
ax[0].set_title('Before')
ax[0].set_ylabel('Seq*Cable')
ax[0].set_xlabel('Receiver')

im = ax[1].imshow(imageaft, aspect='auto', origin=0, cmap=cmap,label='After')
ax[1].set_title('After')
ax[1].set_ylabel('Seq*Cable')
ax[1].set_xlabel('Receiver')

fig.subplots_adjust(right=0.8)
cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
plt.colorbar(im, cax=cbar_ax)
plt.show()


#    #fig, ax = plt.subplots(nrows=2, sharex=True, figsize=(16,9), dpi=150)
#    #ax2=ax[1].twinx()
#    # 
#    #fig.suptitle('Trace Gain', 
#    #          **{'family': 'Arial Black', 'size': 22, 'weight': 'bold'})
#
#    #ax[0].spines["top"].set_visible(False)
#    #ax[0].spines["bottom"].set_visible(False)
#    #ax[0].spines["right"].set_visible(False)
#    #ax[0].spines["left"].set_visible(False)
#    #ax[1].spines["top"].set_visible(False)
#    #ax[1].spines["bottom"].set_visible(False)
#    #ax[1].spines["right"].set_visible(False)
#    #ax[1].spines["left"].set_visible(False)
#
#    #ax[0].plot(dfmr['channel'],dfmr['tr_gainx'],'b-',label='tr_gainx')
#    #ax[0].plot(dfmr['channel'],dfmr['tr_calc'],'g-',label='tr_calc')
#    #ax[1].plot(dfmr['channel'],dfmr['tr_error'],'r-',label='error')
#    #ax2.plot(dfmr['channel'],dfmr['tr_errat'],'b-',label='error ratio')
#    #
#    #legend = ax[0].legend(loc='upper center')
#    #legend = ax[1].legend(loc='upper left')
#    #legend = ax2.legend(loc='upper right')
#
#    #frame = legend.get_frame()
#    #frame.set_facecolor('0.95')
#
#    #for label in legend.get_texts():
#    #    label.set_fontsize('small')
#    # 
#    #for label in legend.get_lines():
#    #    label.set_linewidth(0.5)
#
#    #fig.subplots_adjust(bottom=0.05, top=0.95)
#    #plt.savefig("brcal_tracegain_seq{}.png".format(seq), bbox_inches="tight")
#    #plt.clf()
#    #plt.cla()
#    #plt.close()
