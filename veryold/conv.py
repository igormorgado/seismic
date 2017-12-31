#!/usr/bin/env python

import numpy as np

# The convolution matrix has 
# card = #F + # G - 1
#for t in range(cardF + cardG - 1 ):
#    c+=[0]
#    #print range(max(0,t-cardG+1), min(t+1, cardF))
#    for i in range(max(0,t-cardG+1), min(t+1, cardF)):
#        # There are at least 1 and maximum card G, summation
#        # terms on each convolution matrix element.
#
#        # The first element is  
#
#        #print "f({0})={1}    g({2})={3}"
#        #print "t={0} i={1}".format(t,i)
#        #print "cardF: {0}   cardG: {1}".format(cardF,cardG)
#        #print "\tt-cargG+1  :      {0} ".format( t-cardG+1)
#        #print "\tmax(0,t-cardG+1): {0}".format(max(0,t-cardG+1))
#        #print "\tt+1:              {0}".format( t+1)
#        #print "\tcardF:            {0}".format(cardF)
#        #print "\tmin(t+1,cardF):   {0}".format(min(t+1,cardF))
#        #print " f(i) * g(t-i) = f({0}) * g({1}-{2}) = f({3}) * g({4}) = {5} * {6} ".format(i,t,i,i,t-i,f[i],g[t-i],)
#        c[t]+=f[i]*g[t-i]
#    #print"========"
#

def convolve(f,g):
    cardF=len(f)
    cardG=len(g)
    c=[]
    for t in range(cardF + cardG -1 ): 
        c+=[0]
        for i in range(max(0,t-cardG+1), min(t+1, cardF)):
            c[t]+=f[i]*g[t-i]
    
    return c

# The cross correlation
def crosscorrelation(f,g):
    cardF=len(f)
    cardG=len(g)
    c=[]
    for t in range(cardF + cardG -1 ): 
        c+=[0]
        for i in range(max(0,t-cardG+1), min(t+1, cardF)):
            print "i+#F-(t+2) = {0}+{1}-({2}+2) = {3}".format(i,cardF,t,i+(cardF)-(t+2))
            #print "i+(#F+#G)-(t+2) = {0}+({1}+{2})-({3}+2) = {4}".format(i,cardF,cardG,t,i+(cardF+cardG)-(t+2))
            #c[t]+=f[i]*g[i+(cardF+cardG)-(t+2)]
    
    return c

f=np.array([ 1, 1, 2, -3,1,2 ])
g=np.array([ 1, 2 ,-3 ] )


print convolve(f,g)
print np.convolve(f,g)

print "Cross"
print crosscorrelation(f,g)
print "O resto"
print convolve(f,g[::-1])
print np.convolve(f,g[::-1], mode="valid")
print np.correlate(f,g)

