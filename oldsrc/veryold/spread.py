import numpy as np
import matplotlib.pyplot as plt

t=np.array([
[ 0,0,0,0,0,0,0,0 ],
[ 0,0,0,0,0,0,0,0 ],
[ 0,0,2,0,0,4,0,0 ],
[ 0,0,0,0,0,0,0,0 ], 
[ 0,0,0,0,0,0,0,0 ],
[ 0,0,3,0,0,1,0,0 ],
[ 0,0,0,0,0,0,0,0 ],
[ 0,0,0,0,0,0,0,0 ]])


def spill(arr, nval=0, m=1):
    narr=np.copy(arr)
    for i in range(arr.shape[0]):
        for j in range(arr.shape[1]):
            if arr[i][j] != nval:
                narr[i-m:i+m+1:1,j-m:j+m+1:1]=arr[i][j]                    
    return narr


l=spill(t)

plt.figure()
plt.pcolormesh(t)
plt.savefig("notspilled.png")
plt.figure()
plt.pcolormesh(l)
plt.savefig("spilled.png")

plt.show()