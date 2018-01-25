"""This module create 2D velocity models"""
import numpy as np
import matplotlib.pyplot as plt


def parallel_planes(nx, nz, velocities=(1500, 1500, 2500, 3000)):
    """Returns a parallel plane velocity model. By default 3 slices are
    created: water, sedment, salt.

    Params:
        nx (int): Grid size in X direction.
        nz (int): Grid size in Z direction.
        velocities (float): Slice velocities.

    Returnx:
        ndarray: A velocity profile
    """

    V = np.zeros((nx, nz))
    n = len(velocities)

    for idx, vel in enumerate(velocities):
        beg = int((nz/n)*idx)
        end = int((nz/n)*(idx+1))
        V[:, beg:end] = vel

    return V


def semi_circle(nx, nz, velocities=(1500, 2500, 3000)):
    """Returns a velocity model with a dome in last velocity.

    Params:
        nx (int): Grid size in X direction.
        nz (int): Grid size in Z direction.
        velocities (float): Slice velocities.

    Returnx:
        ndarray: A velocity profile
    """

    V = np.zeros((nx, nz))
    n = len(velocities)
    height = nz / n

    vel = None
    for idx, vel in enumerate(velocities[:-1]):
        beg = int(height*idx)
        end = int(height*(idx+1))
        V[:, beg:end] = vel

    # Fill the last slice with the same velocity as the previous
    V[:, end:] = vel

    # Now we will create the last slice

    # Building the anticline
    radius = nx * .4
    border = nx * .5
    x, z = np.ogrid[0:nx, 0:nz]

    # Use the last velocity
    vel = velocities[-1]

    mask = -np.sqrt((radius**2) - ((x-border)**2)) + nz < z
    V[mask] = vel

    return V


def double_slice(nx, nz, velocities=(1500, 2500, 3000)):
    """Returns a velocity model with a dome in last velocity.

    Params:
        nx (int): Grid size in X direction.
        nz (int): Grid size in Z direction.
        velocities (float): Slice velocities.

    Returnx:
        ndarray: A velocity profile
    """

    V = np.zeros((nx, nz))
    n = len(velocities)
    height = nz / n

    vel = None
    idx = None
    for idx, vel in enumerate(velocities[:-2]):
        beg = int(height*idx)
        end = int(height*(idx+1))
        V[:, beg:end] = vel

    # Fill the last two slice with the same velocity as the previous
    V[:, end:] = vel

    # Now we will create the double slice

    # Building the anticline
    radius = nx * .5
    x, z = np.ogrid[0:nx, 0:nz]

    mask_up = np.sqrt((radius**2) - (x**2)) + (idx+1)*height < z
    mask_down = -np.sqrt((radius**2) - ((x-nx)**2)) + (idx+1)*height < z
    mask = mask_up + mask_down
    V[mask] = velocities[-1]

    return V


def gom_profile(depth):
    """Returns a vertical profile of Gulf of Mexico velocity

    Params:
        depth (ndarray): Depths to be evaluated

    Returns:
        ndarray: Velocities for each depth.
    """
    return 0.3048 * (5056.75
                     - 0.18026     * depth
                     + 6.48904e-5  * depth**2
                     - 1.07238e-8  * depth**3
                     + 9.29217e-17 * depth**4
                     - 3.98934e-17 * depth**5
                     + 6.64516e-22 * depth**6)


def gom_velocity(nx, nz, dz):
    """Returns a 2d velocity based on Gulf of Mexico Profile

    Below 10kms the velocity becomes negative, something isn't right here

    Params:
        nx (int): Number of elements of X coordinate
        nz (int): Number of elements in Z coordinate
        dz (float): Step length to Z coordinate

    Returns:
        ndarray: 2d velocity profile
    """

    V = np.zeros((nx, nz))
    z = np.array([i * dz for i in range(nz)])
    gomvel = gom_profile(z)
    V[:] = gomvel

    return V


def plot_velocity(velocity, dx=1, dz=1, title=None, cmap='plasma', show=True):
    """Plot a velocity profile

    Params:
        velocity (ndarray): 2d velocity map
        dz (float): step length in z direction
        dx (float): step lenght in x direction
        cmap (cmap): Colormap to display
        show (bool): Show the image (or not)

    Returns:
        figure: A matplotlib figure if show=False
    """
    cmap = plt.get_cmap(cmap)
    fig = plt.figure()
    xmax = velocity.shape[0] * dx
    zmax = velocity.shape[1] * dz
    plt.imshow(velocity.transpose(), origin='upper', cmap=cmap, extent=[0, xmax, zmax, 0])
    if title is not None:
        plt.title(title)
    plt.ylabel("Depth")
    plt.colorbar()

    if show:
        fig.show()
    else:
        return fig
