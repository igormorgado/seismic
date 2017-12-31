"""
Imaging functions
"""
# pylint: disable=locally-disabled,no-value-for-parameter

def show_wave(pressure_field, timestep, t, dt):
    """Show the wave"""
    cmap = plt.get_cmap('plasma')
    plt.imshow(pressure_field.transpose(), origin='upper', cmap=cmap)
    plt.title("Pressure field ts: {}, t: {:.4f}, dt: {:.4f}".format(timestep, t, dt))
    plt.colorbar()
    plt.show()


def savefig(pressure_field, timestep, t, dt):
    """Save the fig"""
    cmap = plt.get_cmap('Greys')
    plt.imshow(pressure_field.transpose(), origin='upper', vmin=-0.2, vmax=0.2, cmap=cmap)
    plt.title("Pressure field ts: {}, t: {:.4f}, dt: {:.4f}".format(timestep, t, dt))
    plt.colorbar()
    plt.savefig("simul-{:05d}.png".format(timestep), dpi=300)
    plt.close()


#def sismogram(P)
