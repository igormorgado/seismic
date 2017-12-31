"""
Implements the Wave propagation with finite differences

"""

# pylint: disable=locally-disabled,no-value-for-parameter

import finite_differences as fd
import source


def discrete_wave_step_2d(wave_field, velocity_field, dx, dz, dt):
    """Executes the discrete wave timestep forward in time"""
    U = wave_field
    V = velocity_field

    return -1/12 * (
        ((V[2:-2, 2:-2]*dt/dx)**2 * fd.fpp_fourth_order_term(U, axis=0)[:,2:-2]) +
        ((V[2:-2, 2:-2]*dt/dz)**2 * fd.fpp_fourth_order_term(U, axis=1)[2:-2,:])
        ) 


def discrete_wave_step_3d(wave_field, velocity_field, dx, dy, dz, dt):
    """Executes the discrete wave timestep forward in time"""
    U = wave_field
    V = velocity_field

    return -1/12 * (
        ((V[2:-2, 2:-2, 2:-2]*dt/dx)**2 * fd.fpp_fourth_order_term(U, axis=0)[:, 2:-2, 2:-2]) +
        ((V[2:-2, 2:-2, 2:-2]*dt/dy)**2 * fd.fpp_fourth_order_term(U, axis=1)[2:-2, :, 2:-2]) +
        ((V[2:-2, 2:-2, 2:-2]*dt/dz)**2 * fd.fpp_fourth_order_term(U, axis=2)[2:-2, 2:-2, :])
        ) 


def discrete_time_step_2d(wave_field):
    """TODO"""
    return fd.fp_second_order_explicit_terms(wave_field[0:2], axis=0)[0]


def non_reflexive_border_2d(wave_field, V, dx, dz, dt):
    """Apply non reflexive borders in a wave_field"""
    P = wave_field

    # Left
    P[2, 0:2, :] = P[1, 0:2, :] + (V[0:2, :]*dt/dz) * ( P[1, 1:3, :] - P[1, 0:2, :])

    # Right
    P[2, -2:, :] = P[1, -2:, :] - (V[-2:, :]*dt/dz) * ( P[1, -2:, :] - P[1, -3:-1, :])

    # Bottom
    P[2, :, -2:] = P[1, :, -2:] - (V[:, -2:]*dt/dx) * ( P[1, :, -2:] - P[1, :, -3:-1])


def cerjan(wave_field, d, n, dampening_factor=0.98):
    """Implements cerjam abosorption method"""



