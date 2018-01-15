"""This module create 2D velocity models"""
import numpy as np
import matplotlib.pyplot as plt


class Model2D(object):
    """Returns a 2D velocity model"""

    def __init__(self, nx, nz, dx=1, dz=1):
        """Initialization parameters for 2D velocity model.

        Params:
            nx (int): Number of points in X direction.
            nz (int): Number of points in Z direction.
            dx (float): Distance between each X cell.
            dz (float): Distance between each Z cell.
        """
        self.nx = nx
        self.nz = nz
        self.dx = dx
        self.dz = dz

        # Create the empty velocity model when instantiating
        self.field = np.zeros((self.nx, self.nz))
        self.model = "empty"
        self.extra = "None"

    def __repr__(self):
        msgstr = "{}(model='{}', nx={}, nz={}, dx={}, dz={}, {})"
        msgfmt = msgstr.format(
                self.__class__.__name__,
                self.model,
                self.nx,
                self.nz,
                self.dx,
                self.dz,
                self.extra)
        return msgfmt


    def parallel_planes(self, velocities=(1500, 1700, 2000, 3000)):
        """Returns a parallel plane velocity model. By default 3 slices are
        created: water, sedment, salt.

        Params:
            velocities (float): Slice velocities.

        Returnx:
            ndarray: A 2D velocity profile
        """
        n = len(velocities)

        self.model = "parallel"
        self.extra = "velocities=[{}]".format(", ".join(str(v) for v in velocities))

        for idx, vel in enumerate(velocities):
            beg = int((self.nz/n)*idx)
            end = int((self.nz/n)*(idx+1))
            self.field[:, beg:end] = vel


    def semi_circle(self, velocities=(1500, 1700, 2000, 3000)):
        """Returns a velocity model with a dome in last velocity.

        Params:
            velocities (float): Slice velocities.

        Returnx:
            ndarray: A velocity profile
        """
        n = len(velocities)
        height = self.nz / n

        self.model = "semicircle"
        self.extra = "velocities=[{}]".format(", ".join(str(v) for v in velocities))

        vel = None
        for idx, vel in enumerate(velocities[:-1]):
            beg = int(height*idx)
            end = int(height*(idx+1))
            self.field[:, beg:end] = vel

        # Fill the last slice with the same velocity as the previous
        self.field[:, end:] = vel

        # Now we will create the last slice

        # Building the anticline
        radius = self.nx * .4
        border = self.nx * .5
        x, z = np.ogrid[0:self.nx, 0:self.nz]

        # Use the last velocity
        vel = velocities[-1]

        mask = -np.sqrt((radius**2) - ((x-border)**2)) + self.nz < z
        self.field[mask] = vel


    def double_slice(self, velocities=(1500, 1700, 2000, 2250, 3000)):
        """Returns a velocity model with a dome in last velocity.

        Params:
            velocities (float): Slice velocities.

        Returnx:
            ndarray: A velocity profile
        """
        n = len(velocities)
        height = self.nz / n

        self.model = "doubleslice"
        self.extra = "velocities=[{}]".format(", ".join(str(v) for v in velocities))

        vel = None
        idx = None
        for idx, vel in enumerate(velocities[:-2]):
            beg = int(height*idx)
            end = int(height*(idx+1))
            self.field[:, beg:end] = vel

        # Fill the last two slice with the same velocity as the previous
        self.field[:, end:] = vel

        # Now we will create the double slice

        # Building the anticline
        radius = self.nx * .5
        x, z = np.ogrid[0:self.nx, 0:self.nz]

        mask_up = np.sqrt((radius**2) - (x**2)) + (idx+1)*height < z
        mask_down = -np.sqrt((radius**2) - ((x-self.nx)**2)) + (idx+1)*height < z
        mask = mask_up + mask_down
        self.field[mask] = velocities[-1]


    def gom_velocity(self):
        """Returns a 2d velocity based on Gulf of Mexico Profile

        Below 10kms the velocity becomes negative, something isn't right here

        Params:
            dz (float): Step length to Z coordinate

        Returns:
            ndarray: 2d velocity profile
        """
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



        z = np.array([i * self.dz for i in range(self.nz)])
        gomvel = gom_profile(z)
        self.model = "gom"
        self.field[:] = gomvel


    def plot(self, title=None, cmap='plasma', show=True):
        """Plot a velocity profile

        Params:
            cmap (cmap): Colormap to display
            show (bool): Show the image (or not)

        Returns:
            figure: A matplotlib figure if show=False
        """
        cmap = plt.get_cmap(cmap)
        xmax = self.field.shape[0] * self.dx
        zmax = self.field.shape[1] * self.dz

        fig = plt.figure()
        plt.imshow(self.field.transpose(), origin='upper', cmap=cmap, extent=[0, xmax, zmax, 0])

        if title is None:
            titlestr="Velocity field {}: nx={}, nz={}, dx={}, dz={}"
            title=titlestr.format(self.model, self.nx, self.nz, self.dx, self.dz)

        plt.title(title)
        plt.ylabel("Depth")
        plt.colorbar()

        if show:
            plt.show()
        else:
            return fig
