#!/usr/bin/env python

from __future__ import division

def sma( datapoints, window):
    r=[]
    #for n in range(1,window):
    #    r+=[0.]

    for n in range(len(datapoints)-window+1):
         r+=[sum(datapoints[n:n+window])/window]

    return r


