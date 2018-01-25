"""
Implements the Finite Difference Euler Explicit Method.
"""
import numpy as np

# pylint: disable=locally-disabled,no-value-for-parameter, redundant-keyword-arg

class EulerExplicit(object):
    """Finite Differences Class using EulerExplicit"""

    def __init__(self, grid, dx, dt, 
            timeorder=2, apply_non_reflexive_border=True, apply_cerjan=0.98):
        """Creates a generator for the finite difference iteration, it uses 
        central in space and forward in time.

        Usage:

        ```
        field.shape
        Out: (100, 50, 50)

        fdmodel = EulerExplicit(field, dx=1, dt=0.1)
        ```

        Where `fdmodel[0]` is the `step-1` `fdmodel[1]` is step and `fdmodel[2]` is
        `step+1`  in Finite Differences step method.


        Params:
            grid (nparray): N-dimensional grid
            dx (nparray): Space interval in each axis. For 2d example: (1,5)
            for 1 in X and 5 in Z.
            dt (float): Time interval
            timeorder (int): Order of forward time derivative (1, 2). Default: 2
            apply_non_reflexive_border (bool):  If the model borders will be 
            non reflexive (except the top). Default: True.
            apply_cerjan (float): If Cerjan dampening will be applied in non 
            reflexive borders. Value of 1 means not apply. Default: 0.98.



        TODO:
            - In this code I always assume that 4th order derivatives will be in
              space and second order in time. I need to find a way to make this
              more abstract, and probably remove the differentiations from the
              Euler method and put in a stand alone finite difference class which
              Euler method uses some of them.

            - Abstract the dimensionality of grit from 1D to N-D. In all derivatives.

            - Find a way to calculate the derivative terms and
              coefficients for any chosen order and method.

            - Find a way to abstract which borders will be applied the
              non_reflexive_methods, instead assume that is in all borders
              except the top (because we are in seismic)
        """
        if grid.ndim > 3:
            raise ValueError("Grid must at maximum 3D")

        if timeorder == '2':
            timesteps = 3
        else:
            raise ValueError("timeorder must be '2'")

        if apply_cerjan < 0:
            raise ValueError("Cerjan values must be 0 < x <= 1")

        self.dx = dx
        self.dt = dt
        self.timeorder = timeorder
        self.apply_non_reflexive_border = apply_non_reflexive_border
        self.apply_cerjan  = apply_cerjan

        # Here we extend to one more dimension to fit the timeorder
        # timefield[0] is past 
        # timefield[1] is present
        # timefield[2] is future
        self.timefield = np.zeros((timesteps,) + grid.shape, dtype=grid.dtype)
        self.timefield[0] = grid
        self.timefield[1] = grid


    def __next__(self):
        """Executes a timestep, applies the border conditions and generates the
        next field"""

        if self.timeorder == '2':
            self.timestep_second_order()

        if self.apply_non_reflexive_border:
            self.non_reflexive_border()

        if self.apply_cerjan != 1:
            self.cerjan(dampening_factor)

        yield self.timefield[1]
        

    def fpp_fourth_order_term(self, axis=-1):
        """Returns the second derivative of fourth order term without the step

        Grid must have (at least) 5 points equally spaced.

        Args:
            values (nparray): Values of points in field

        Returns:
            float: List of fourth order derivatives
        """
        U = self.timefield[1].swapaxes(0, axis)

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
        U = self.timefield[1].swapaxes(0, axis)

        # Function slices
        fm1 = U[ :-2]
        fc0 = U[1:-1]
        fp1 = U[2:  ]

        return (fm1 - 2*fc0 + fp1).swapaxes(0, axis)


    def fp_second_order_explicit_terms(self, axis=-1):
        """Returns the terms of explicit second order first derivative

        Returns:
            float: Array of second order derivatives
        """
        # This is used for time step. The approach here is ugly since I ALWAYS
        # supose that the second orders first derivative will be in time, since
        # it uses the "time dimension". Need to rethink.
        # And since is called with axis=0, isn't swapped at all.
        U = self.timefield[0:2].swapaxes(0, axis)

        # Function slices
        fm1 = U[:-1]
        fc0 = U[1:]

        # The [0] here removes one dimension
        return (2*fc0 - fm1).swapaxes(0, axis)[0]


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
        U = self.timefield[1]

        # This is so sad and bad
        utemp = np.zeros_like(self.timefield)

        for axis in range(self.timefield[0].ndim):
            utemp += (self.dt/self.dx[axis])**2 * self.fpp_fourth_order_term(axis)[:, 2:-2]

        return -1/12 * utemp


    def wavestep_fourth_order2d(self):
        """Executes the discrete wave timestep forward in time 2d"""
        # pragma pylint: disable=redundant-keyword-arg
        return -1/12 * (
            (self.dt/self.dx[0])**2 * self.fpp_fourth_order_term(axis=0)[:, 2:-2] +
            (self.dt/self.dx[1])**2 * self.fpp_fourth_order_term(axis=1)[2:-2, :]
        )


    def wavestep_fourth_order3d(self):
        """Executes the discrete wave timestep forward in time 3d"""
        # TODO: Check if the dimensions here are correct for 3D
        # pragma pylint: disable=redundant-keyword-arg
        return -1/12 * (
                (self.dt/self.dx[0])**2 * self.fpp_fourth_order_term(axis=0)[:, 2:-2, 2:-2] +
                (self.dt/self.dx[1])**2 * self.fpp_fourth_order_term(axis=1)[2:-2, :, 2:-2] +
                (self.dt/self.dx[2])**2 * self.fpp_fourth_order_term(axis=2)[2:-2, 2:-2, :]
        )


    def wavestep_fourth_order(self):
        """Executes the discrete wave timestep forward in time"""
        # I would love to use wavestep_fourth_order_memcopy(), getting rid of
        # the memcopy, unfortunatelly I could not find a way to do it, because
        # that I have created this helper function that call the ones without
        # the memcopy but without the dimension abstraction that the for loop
        # created to me.
        if self.timefield[0].ndim == 2:
            self.wavestep_fourth_order2d()
        elif self.timefield[0].ndim == 3:
            self.wavestep_fourth_order3d()


    def timestep_second_order(self):
        """Executes a time step on wavefield"""
        return self.fp_second_order_explicit_terms(axis=0)


    def non_reflexive_border(self):
        """Apply non reflexive borders in a wave_field.

        This is a time dependent step

        Params:
            surfaces (ndarray): A list of booleans to match each surface. If
            true the border is non_reflexive, if false is reflexive
        """
        ## Left
        #P[2, 0:2, :] = P[1, 0:2, :] + (V[0:2, :]*dt/dz) * (P[1, 1:3, :] - P[1, 0:2, :])

        ## Right
        #P[2, -2:, :] = P[1, -2:, :] - (V[-2:, :]*dt/dz) * (P[1, -2:, :] - P[1, -3:-1, :])

        ## Bottom
        #P[2, :, -2:] = P[1, :, -2:] - (V[:, -2:]*dt/dx) * (P[1, :, -2:] - P[1, :, -3:-1])
        return NotImplemented


    def cerjan_border(self, dampening_factor=0.98):
        """Implements cerjam abosorption method"""
        return NotImplemented
