#!/usr/bin/env python

# Near: Recommended, -25%, +25%
# Mid:  Recommended, -25%, +25%
# Far:  Recommended, -25%, +25%
import numpy as np

over = lambda x: int(round(1.25*x))
under = lambda x: int(round(0.75*x))

stdapper = np.array([1050, 5050])
apperture = np.array([ stdapper, map(over,stdapper), map(under,stdapper) ])
seisshot_count = np.arange(1,4000,100)

fmt = "045\t1\t6\t045_06\t{:04d}\t{:04d}\t{:04d}"

#for l in apperture:
#    for s in seisshot_count:
#        print fmt.format(l[0],l[1],s)

lines = [ fmt.format(l[0],l[1],s) for s in seisshot_count for l in apperture ]
for l in lines:
    print l


