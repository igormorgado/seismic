"""This modeule implements many different seismic sources"""

import numpy as np


def gauss_period(cut_frequency):
    """Returns the period of gaussian function of given cut frequency.

    Params:
        cutfrequency(float): Cut frequency (maximum frequency).

    Returns:
        float: Gauss source period.
    """
    return (2 * np.sqrt(np.pi))/cut_frequency


def gauss_central_frequency(cut_frequency):
    """Returns the central frequency of gaussian function of given cut frequency.

    Params:
        cut_frequency(float): Cut frequency

    Returns:
        float: Gauss central frequency.
    """
    return cut_frequency/(3 * np.sqrt(np.pi))


def gauss_cut_frequency(central_frequency):
    """Returns the cut frequency of gaussian function of given central frequency.

    Params:
        central_frequency(float): Central frequency (where the peak lies)

    Returns:
        float: Gauss cut down frequency.
    """
    return 3 * np.sqrt(np.pi) * central_frequency


def gauss_max_timesteps(cut_frequency, dt):
    """Returns the maximum number of timesteps of gaussian source

    Params:
        cut_frequency (float): The cut frequency
        dt (float): Timestep lenght

    Returns:
        int: Maximum number of time steps to completely draw the source
    """
    if dt > 1/cut_frequency:
        msg = "'dt' too big. Isn't able to represent the source with {}Hz"
        msgfmt = msg.format(cut_frequency)
        raise ValueError(msgfmt)
    return (4*np.sqrt(np.pi))/(cut_frequency * dt)

def gauss_timestep(n, dt, period=None, frequency=None):
    """Returns the positive values of time steps based on Gauss function period
    and time delta.

    Params:
        n (ndarray): The simulation step.
        dt (float): The simulation time step.
        period (float): Gauss source period.
        frequency (float): Gauss cut frequency

    Returns:
        ndarray: Time steps for the simulation based on Gauss period.
    """
    if period is not None and period > 0:
        return (n-1) * dt - period
    elif frequency is not None and frequency > 0:
        return (n-1) * dt - gauss_period(frequency)
    else:
        raise ValueError("Period or Frequency needs to be greater than 0")


def gauss(t, **kwargs):
    """A gaussian seismic source.

    Params:
        t (nparray): time (NOT timestep)

    kwargs:
        central_frequency (float): Central Frequency
        cut_frequency (float): cut frequency

    Returns:
        (nparray): Values of Gausian source in given time.
    """
    # Sanity check {{{
    if 'cut_frequency' in kwargs:
        cut_frequency = kwargs['cut_frequency']
        if cut_frequency > 0:
            central_frequency = gauss_central_frequency(cut_frequency)
        else:
            raise ValueError("Cut Frequency must be positive")
    elif 'central_frequency' in kwargs:
        central_frequency = kwargs['central_frequency']
        if central_frequency <= 0:
            raise ValueError("Central Frequency must be positive")
    else:
        raise ValueError("Cut Frequency or Central Frequency must be given")
    # }}}

    x = np.pi * (np.pi * central_frequency * t)**2
    f = (1 - 2 * x) * np.exp(-x)

    return f


def plot_gauss_source(cut_frequency=60, dt=None, samples=None, show=True):
    """Plot gauss source.

    Params:
        cut_frequency (float): Maximum frequency.
        dt (float): Simulation time step. If not give uses one based on
        source frequency.
        samples (int): Number of samples from Gauss Source. If not given will
        calculate one to display the source completely

    Returns:
        ndarray: Values to the Gauss source.
    """

    import matplotlib.pyplot as plt

    # Period of gauss source bassed on cutdown frequency
    tf = gauss_period(cut_frequency)

    # Number of points neccesary to plot the wavelet completely
    if dt is not None:
        if samples is None:
            samples = gauss_max_timesteps(cut_frequency, dt)
    else:
        # No 'dt' supplied
        if samples is None:
            samples = 2*cut_frequency

        dt = 2*tf/samples

    n = np.arange(samples)

    # Time discretization based on timestep and wavelet period
    t = n*dt - tf

    # Source values to the discretized timestep
    source = gauss(t, cut_frequency=cut_frequency)

    #Plot
    fig = plt.figure()
    plt.plot(n, -source)
    plt.plot(n, -source, 'ro', alpha=.5, ms=3)
    plt.title(r"Gauss Source @{}Hz $\Delta t = {:.4f}$".format(cut_frequency, dt))
    plt.ylabel("Amplitude")
    plt.xlabel("Time step")
    plt.legend()

    if show:
        plt.show()
    else:
        return fig


if __name__ == "__main__":
    plot_gauss_source(dt=1/960)
