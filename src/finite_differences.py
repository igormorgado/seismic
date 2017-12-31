"""
Implements the Finite difference method.
"""

# pylint: disable=locally-disabled,no-value-for-parameter

def fpp_fourth_order_term(U, axis=-1):
    """Returns the second derivative of fourth order term without the step

    values must have (at least) 5 points equally spaced.

    Args:
        values (nparray): Values of points in grid

    Returns:
        float: List of fourth order derivatives
    """
    U = U.swapaxes(0, axis)

    fm2 = U[ :-4]
    fm1 = U[1:-3]
    fc0 = U[2:-2]
    fp1 = U[3:-1]
    fp2 = U[4:  ]

    # Resorted to reduce the number of operations
    return (fm2 - 16*(fm1+fp1) + 30*fc0 + fp2).swapaxes(0, axis)


def fpp_fourth_order(U, interval, axis=-1):
    """Returns the second derivative of fourth order

    values must have (at least) 5 points equally spaced.

    Args:
        values (nparray): Values of points in grid
        interval (float): Interval

    Returns:
        float: List of fourth order derivatives
    """
    mul = 1/(12 * interval**2)

    return mul * fpp_fourth_order_term(U, axis=axis)


def fp_second_order_term(U, axis=-1):
    """Returns the second derivative of second order without the step

    values must have (at least) 3 points equally spaced.

    Args:
        U (nparray): Value points in grid

    Returns:
        float: List of second order derivatives
    """
    U = U.swapaxes(0, axis)

    # Function slices
    fm1 = U[ :-2]
    fc0 = U[1:-1]
    fp1 = U[2:  ]

    return (fm1 - 2*fc0 + fp1).swapaxes(0, axis)


def fp_second_order_explicit_terms(U, axis=-1):
    """Returns the terms of explicit second order first derivative

    Args:
        U (nparray): Values of points in grid

    Returns:
        float: List of second order derivatives
    """
    U = U.swapaxes(0, axis)

    # Function slices
    fm1 = U[ :-1]
    fc0 = U[1:]

    return (2*fc0 - fm1).swapaxes(0, axis)


def fp_second_order(values, interval, axis=-1):
    """Returns the second derivative of second order

    values must have (at least) 3 points equally spaced.

    Args:
        values (nparray): Values of points in grid
        interval (float): Interval

    Returns:
        float: List of second order derivatives
    """
    mul = 1/interval**2

    return mul * fp_second_order_term(values, axis)
