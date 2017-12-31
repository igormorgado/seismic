"""This module will evaluate model stability"""

def dispersion(V, dx, dy, dz, f, k=5):
    """Evalutate the model dispersion.

    Args:
        V (nparray): is the velocity model
        dx (float): is the x interval
        dy (float): is the y interval
        dz (float): is the z interval
        f (float): is the cutdown frequency
        k (float): maximum number of samples in a wavelength.

    Returns:
        bool: If the model is stable
    """
    return max(dx, dy, dz) <= (V.min()/(k*f))

def stability(V, dx, dy, dz, dt, mu=5):
    """Evalutate the model stability.

    Args:
        V (nparray): is the velocity model
        dx (float): is the x interval
        dy (float): is the y interval
        dz (float): is the z interval
        dt (float): is the t interval (timestep)
        mu (float): is stability constant

    Returns:
        bool: If the model is stable
    """
    return dt <= (max(dx, dy, dz)/(V.max()*mu))
