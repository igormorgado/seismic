"""
Imaging functions
"""
# pylint: disable=locally-disabled,no-value-for-parameter

import matplotlib.pyplot as plt
import os

def wave2image(directory):
    """Convert all wave data from a dir to image"""
    for filepath in os.listdir(directory):
        basename = os.path.basename(filepath)
        filename, extension = os.path.splitext(basename)
        if extension == ".npz":
            print(filepath)

            # Read the wavefield
            datafile = os.path.join(directory, filepath )
            fnpz = np.load(datafile)['arr_0']

            # Save to disk
            timestep = filename.split('-')[-1]
            timestep = int(timestep)
            savefig(fnpz , timestep, 1, 1)


def show_wave(pressure_field, timestep=1, t=1, dt=1):
    """Show the wave"""
    cmap = plt.get_cmap('Greys')
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
    plt.savefig("wavefield-{:04d}.png".format(timestep), dpi=300)
    plt.close()


#def sismogram(P)
