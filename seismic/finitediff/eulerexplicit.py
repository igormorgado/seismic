"""
Implements the Finite Difference Euler Explicit Method.
"""

# pylint: disable=locally-disabled,no-value-for-parameter

class EulerExplicit(object):
    """Finite Differences Class using EulerExplicit"""

    def __init__(self, grid, dx, dt, timeorder=1):
        """Sets the finite difference iteration

        Params:
            grid (nparray): N-dimensional grid
            dx (nparray): Space interval in each axis
            dt (float): Time interval
            timeorder (int): Order of time derivative (1, 2)
        """
        self.grid = grid
        self.field = field
        self.dx = dx
        self.dim = len(self.grid.shape)
    

    def fpp_fourth_order_term(self, axis=-1):
        """Returns the second derivative of fourth order term without the step

        Grid must have (at least) 5 points equally spaced.

        Args:
            values (nparray): Values of points in grid

        Returns:
            float: List of fourth order derivatives
        """
        U = self.grid.swapaxes(0, axis)

        fm2 = U[ :-4]
        fm1 = U[1:-3]
        fc0 = U[2:-2]
        fp1 = U[3:-1]
        fp2 = U[4:  ]

        # Resorted to reduce the number of operations
        return (fm2 - 16*(fm1+fp1) + 30*fc0 + fp2).swapaxes(0, axis)


    def fpp_fourth_order(self, axis=-1):
        """Returns the second derivative of fourth order

        values must have (at least) 5 points equally spaced.

        Returns:
            float: List of fourth order derivatives
        """

        mul = 1/(12 * self.dx[axis]**2)

        return mul * self.fpp_fourth_order_term(axis=axis)


    def fp_second_order_term(self, axis=-1):
        """Returns the second derivative of second order without the step

        values must have (at least) 3 points equally spaced.

        Returns:
            float: List of second order derivatives
        """
        U = self.grid.swapaxes(0, axis)

        # Function slices
        fm1 = U[ :-2]
        fc0 = U[1:-1]
        fp1 = U[2:  ]

        return (fm1 - 2*fc0 + fp1).swapaxes(0, axis)


    def fp_second_order_explicit_terms(self, axis=-1):
        """Returns the terms of explicit second order first derivative

        Returns:
            float: List of second order derivatives
        """
        U = self.grid.swapaxes(0, axis)

        # Function slices
        fm1 = U[ :-1]
        fc0 = U[1:]

        return (2*fc0 - fm1).swapaxes(0, axis)


    def fp_second_order(self, axis=-1):
        """Returns the second derivative of second order

        values must have (at least) 3 points equally spaced.

        Returns:
            float: List of second order derivatives
        """
        mul = 1/self.dx[axis]**2

        return mul * self.fp_second_order_term(axis)



    def wavestep_fourth_order_memcopy(self):
        """Executes the discrete wave timestep forward in time"""
        U = self.grid

        # This is so sad and bad
        U_temp = np.zeroes_like(self.grid)

        for i in range(sef.dim):
            U_temp += self.dt/self.dx[i])**2 * self.fpp_fourth_order_term(U, axis=i)[:,2:-2]
        
        return -1/12 * U_temp



    def wavestep_fourth_order2d(self):
        """Executes the discrete wave timestep forward in time 2d"""
        return -1/12 * (
            self.dt/self.dx[0])**2 * self.fpp_fourth_order_term(U, axis=0)[:,2:-2]
            self.dt/self.dx[1])**2 * self.fpp_fourth_order_term(U, axis=1)[:,2:-2]
        )


    def wavestep_fourth_order3d(self):
        """Executes the discrete wave timestep forward in time 3d"""
        return -1/12 * (
            self.dt/self.dx[0])**2 * self.fpp_fourth_order_term(U, axis=0)[:,2:-2]
            self.dt/self.dx[1])**2 * self.fpp_fourth_order_term(U, axis=1)[:,2:-2]
            self.dt/self.dx[2])**2 * self.fpp_fourth_order_term(U, axis=2)[:,2:-2]
        )


    def wavestep_fourth_order(self):
        """Executes the discrete wave timestep forward in time"""
        if  self.dim == 2:
            return self.wavestep_fourth_order2d()
        elif self.dim == 3:
            return self.wavestep_fourth_order3d()
        else:
            return NotImplemented
        

    def non_reflexive_border(self, surfaces):
        """Apply non reflexive borders in a wave_field
        
        Params:
            surfaces (ndarray): A list of booleans to match each surface. If
            true the border is non_reflexive, if false is reflexive
        """
        b=border

        # Left
        P[2, 0:2, :] = P[1, 0:2, :] + (V[0:2, :]*dt/dz) * ( P[1, 1:3, :] - P[1, 0:2, :])

        # Right
        P[2, -2:, :] = P[1, -2:, :] - (V[-2:, :]*dt/dz) * ( P[1, -2:, :] - P[1, -3:-1, :])

        # Bottom
        P[2, :, -2:] = P[1, :, -2:] - (V[:, -2:]*dt/dx) * ( P[1, :, -2:] - P[1, :, -3:-1])


    def cerjan(wave_field, d, n, dampening_factor=0.98):
        """Implements cerjam abosorption method"""


    def timestep_second_order(self):
        """Executes a time step on wavefield"""
        return self.fp_second_order_explicit_terms(self.field[0:2], axis=0)[0]



