import seismic

T = 6       # 6 seconds
t = np.linspace(0,T,1001)

ricker01 = seismic.source.Ricker(cut_frequency=1)
ricker10 = seismic.source.Ricker(cut_frequency=10)
ricker60 = seismic.source.Ricker(cut_frequency=60)

ricker01.plot(t, -ricker01.period, show=False)
ricker10.plot(t, -ricker10.period, show=False)
ricker60.plot(t, -ricker60.period, show=False)
plt.legend()
plt.show()

