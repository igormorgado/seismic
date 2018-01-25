a=np.ones((5,4,3))

b=np.expand_dims(a, axis=0)
b=np.concatenate((b, np.zeros_like(b), np.zeros_like(b)), axis=0)

c=np.tile(a, (3,) + (1,) * a.ndim)
c[1] = 0
c[2] = 0

d=np.broadcast_to(a, (3, *a.shape)).copy()
d[1] = 0
d[2] = 0

