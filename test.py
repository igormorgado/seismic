import seismic

T = 0.7
t = np.linspace(0,T,101)

ricker10m = seismic.source.Ricker(cut_frequency=10, phase='minimum')
ricker10z = seismic.source.Ricker(cut_frequency=10, phase='zero')

ricker10m.plot(t, show=False)
ricker10z.plot(t, show=False)
plt.legend(loc='upper right')
plt.show()

