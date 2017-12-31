"""Just a test"""

import numpy as np

x = 7
y = 7
z = 7

#U = np.zeros((x, y, z))
#
#for k in range(z):
#    for j in range(y):
#        for i in range(x):
#            U[i, j, k] = i*100+j*10+k

U = np.random.rand(x, y, z)

axis = 1
dsize = U.shape[axis]
# fm2 = U.take(indices=range(0, dsize-4), axis=axis)
# fm1 = U.take(indices=range(1, dsize-3), axis=axis)
# fc0 = U.take(indices=range(2, dsize-2), axis=axis)
# fp1 = U.take(indices=range(3, dsize-1), axis=axis)
# fp2 = U.take(indices=range(4, dsize), axis=axis)
# 
# Up = -fm2 + 16*(fm1+fp1) - 30*fc0 - fp2

# fm21 = U[:, 0:-4, :]
# fm11 = U[:, 1:-3, :]
# fc01 = U[:, 2:-2, :]
# fp11 = U[:, 3:-1, :]
# fp21 = U[:, 4:  , :]
# Up1 = -fm21 + 16*(fm11+fp11) - 30*fc01 - fp21
# 
# Usw = np.swapaxes(U,0,1)
# fm22 = Usw[0:-4, :, :]
# fm12 = Usw[1:-3, :, :]
# fc02 = Usw[2:-2, :, :]
# fp12 = Usw[3:-1, :, :]
# fp22 = Usw[4:  , :, :]
# Up2sw = -fm22 + 16*(fm12+fp12) - 30*fc02 - fp22
# Up2 = np.swapaxes(Up2sw,0,1)


fm21 = U[:, :, 0:-4]
fm11 = U[:, :, 1:-3]
fc01 = U[:, :, 2:-2]
fp11 = U[:, :, 3:-1]
fp21 = U[:, :, 4:  ]
Up1 = -fm21 + 16*(fm11+fp11) - 30*fc01 - fp21

Usw = np.swapaxes(U,0,2)
fm22 = Usw[0:-4, :, :]
fm12 = Usw[1:-3, :, :]
fc02 = Usw[2:-2, :, :]
fp12 = Usw[3:-1, :, :]
fp22 = Usw[4:  , :, :]
Up2sw = -fm22 + 16*(fm12+fp12) - 30*fc02 - fp22
Up2 = np.swapaxes(Up2sw,0,2)

