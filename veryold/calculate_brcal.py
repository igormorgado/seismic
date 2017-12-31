#!/usr/bin/env python


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

seqs = ( 249, 251, 252, 253, 254, 255, 256, 257, 258, 260, 261, 262 )
seqs = ( 249, )
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



# FIGURE 
for seq in seqs:
    print("{}".format(seq))

    dftr = pd.read_csv("{}{}.csv".format(tgain_fn, seq))

    dfbr = pd.read_csv("{}{}.csv".format(brcal_fn, seq), 
                        names=['channel','brcal','none'],
                        sep=';', 
                        header=0, 
                        usecols=[0,1])

    dfntrg = pd.read_csv("boat_tr_gainx_seq{}.csv".format(seq),sep=';',names=['channel','sequence','cablenb','receiver','serial','tr_gainx'], header=1)

    #dfmr = pd.merge(dftr,dfbr, how='left', on=['channel'])

    #dfmr['tr_calc'] = G(dfmr.brcal)
    #dfmr['tr_error'] = abs(dfmr['tr_gainx'] - dfmr['tr_calc'])
    #dfmr['tr_errat'] = dfmr['tr_gainx'] / dfmr['tr_calc'] 
    #dfmr['tr_errat'] = map(abs,100*(dfmr['tr_errat']-1))

    # Draw the figure
    #fig, ax = plt.subplots(nrows=2, sharex=True, figsize=(16,9), dpi=150)
    #ax2=ax[1].twinx()
    # 
    #fig.suptitle('Trace Gain', 
    #          **{'family': 'Arial Black', 'size': 22, 'weight': 'bold'})

    #ax[0].spines["top"].set_visible(False)
    #ax[0].spines["bottom"].set_visible(False)
    #ax[0].spines["right"].set_visible(False)
    #ax[0].spines["left"].set_visible(False)
    #ax[1].spines["top"].set_visible(False)
    #ax[1].spines["bottom"].set_visible(False)
    #ax[1].spines["right"].set_visible(False)
    #ax[1].spines["left"].set_visible(False)

    #ax[0].plot(dfmr['channel'],dfmr['tr_gainx'],'b-',label='tr_gainx')
    #ax[0].plot(dfmr['channel'],dfmr['tr_calc'],'g-',label='tr_calc')
    #ax[1].plot(dfmr['channel'],dfmr['tr_error'],'r-',label='error')
    #ax2.plot(dfmr['channel'],dfmr['tr_errat'],'b-',label='error ratio')
    #
    #legend = ax[0].legend(loc='upper center')
    #legend = ax[1].legend(loc='upper left')
    #legend = ax2.legend(loc='upper right')

    #frame = legend.get_frame()
    #frame.set_facecolor('0.95')

    #for label in legend.get_texts():
    #    label.set_fontsize('small')
    # 
    #for label in legend.get_lines():
    #    label.set_linewidth(0.5)

    #fig.subplots_adjust(bottom=0.05, top=0.95)
    #plt.savefig("brcal_tracegain_seq{}.png".format(seq), bbox_inches="tight")
    #plt.clf()
    #plt.cla()
    #plt.close()
