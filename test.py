import seismic

T = 0.7
t = np.linspace(0,T,101)

ricker01 = seismic.source.Ricker(cut_frequency=1)
ricker10 = seismic.source.Ricker(cut_frequency=10)
ricker10m = seismic.source.Ricker(cut_frequency=10, phase='minimum')
ricker10z = seismic.source.Ricker(cut_frequency=10, phase='zero')
ricker10z.cut_frequency = 5
ricker60 = seismic.source.Ricker(cut_frequency=60)

fig, ax  = plt.subplots()
ricker01.plot(t, -ricker01.period, show=False)
ricker10m.plot(t, show=False)
ricker10z.plot(t)
ricker60.plot(t, -ricker60.period, show=False)
plt.legend()
plt.show()

