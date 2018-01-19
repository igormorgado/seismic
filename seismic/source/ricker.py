"""This module implements many different seismic sources"""

import numpy as np

class Ricker(object):
    r"""Defines a Ricker seismic source (Gauss second derivative)

    By definition a Ricker seismic source a wavelet with peak centered in
    the origin (zero offset). Generated by the equation:

    $$ A(t) = \[ 1 - 2 ( \pi f t )^2 \] e^{-( \pi f t )^2} $$

    Where:

    $f$ is the central frequency.
    $t$ is the time instant

    Pay attention that Sampling Rate is deeply related with wavelet maximum
    frequency that is related with central frequency.

    Is possible to infer the maximum frequency from the central frequency.

    Also the ricker source is related to time not the timestep

    Params:

        central_frequency (float): Defines the central frequency of ricker
        wavelet, if defined you cannot define cut_frequency.
        cut_frequency(float): Maximum frequency of wavelet, if defined you
        cannot define central_frequency.
        phase (str): Can be 'zero' (default),  or 'minimum', if 'zero', the 0
        time will be on peak, if minimum the 0 will be on the begin of wavelet
        period.
        amplitude (float): The multiplier of amplitude in every point, if -1
        the phase will shift \pi degrees.
        sample_rate(float):  The interval between samples in seconds

    Returns:
        Ricker object
    """

    def __init__(self,
                 central_frequency=None,
                 cut_frequency=None,
                 sample_rate=None,
                 phase='zero',
                 amplitude=1):
        """Initialize the Ricker source"""
        data = [i for i in [central_frequency, cut_frequency] if i is not None]
        if len(data) > 1:
            raise ValueError("You need to specify only 'central_frequency' or 'cut_frequency'.")
        if central_frequency is not None and central_frequency > 0:
            self.central_frequency = central_frequency
        elif cut_frequency is not None and cut_frequency > 0:
            self.cut_frequency = cut_frequency
        else:
            raise ValueError("You must define positive 'central_frequency', 'cut_frequency'")

        if phase not in ('zero', 'minimum'):
            raise ValueError("Phase must be 'minimum'  or 'zero'")

        self.sample_rate = sample_rate
        self.phase = phase
        self.amplitude = amplitude


    def __repr__(self):
        msgstr = "{}(Amplitude={:g}, period={:g}, central_frequency={:g}, cut_frequency={:g})"
        msgfmt = msgstr.format(
            self.__class__.__name__,
            self.amplitude,
            self.period,
            self.central_frequency,
            self._cut_frequency)
        return msgfmt


    @property
    def cut_frequency(self):
        """Returns the 'cut' frequency of Ricker source wavelet also know as
        aparent frequency"""
        return self._cut_frequency


    @cut_frequency.setter
    def cut_frequency(self, value):
        """Sets the cut frequency of gaussian function of given central frequency.

        Params:
            central_frequency(float): Central frequency (where the peak lies)
        """
        # pragma pylint: disable=attribute-defined-outside-init
        self._cut_frequency = value


    @property
    def central_frequency(self):
        """Returns the 'central' frequency of Ricker source wavelet also know
        as dominant frequency"""
        #return self._cut_frequency/(3 * np.sqrt(np.pi))
        return self._cut_frequency * (np.sqrt(6)/np.pi)


    @central_frequency.setter
    def central_frequency(self, value):
        """Sets the central frequency of gaussian function of given cut frequency.

        Params:
            value(float): Cut frequency
        """
        #self._cut_frequency = 3 * np.sqrt(np.pi) * value
        # pragma pylint: disable=attribute-defined-outside-init
        self._cut_frequency = (value * np.pi)/np.sqrt(6)


    @property
    def period(self):
        """Returns the period (+/-) of gaussian function of given cut frequency."""
        #return 1.5 * (np.sqrt(6)/(np.pi * self.central_frequency))
        return (2 * np.sqrt(np.pi))/self._cut_frequency


    @property
    def nyquist_frequency(self):
        """Returns the 'nyquist' frequency of Ricker source wavelet"""
        return self._cut_frequency/2


    @nyquist_frequency.setter
    def nyquist_frequency(self, value):
        """Sets the cut frequency of gaussian function of given central frequency.

        Params:
            central_frequency(float): Central frequency (where the peak lies)
        """
        # pragma pylint: disable=attribute-defined-outside-init
        self._cut_frequency = 2*value


    def values(self, timestep, timeshift=0):
        """A ricker seismic source.

        Evaluates the ricker values to a given time step. The time step can be
        a single float or iterable

        Params:
            timestep (numeric): The time steps evaluated in seconds
            timeshift (float): The time skew in seconds, if 0 the ricker is 0
            phase. You can use -self.period to start on 0

        Returns:
            numeric: values of ricker in time steps given

        """
        if self.phase == 'minimum':
            timeshift -= self.period

        p = (np.pi * self.central_frequency * (timestep+timeshift))**2
        f = (1 - 2 * p) * np.exp(-p)
        return self.amplitude * f


    def plot(self, timestep, timeshift=0, show=True):
        """Plot the ricker source"""

        import matplotlib.pyplot as plt

        label = "Ricker {}Hz".format(self.cut_frequency)

        lines = []
        lines.append(plt.plot(timestep, self.values(timestep, timeshift), label=label))
        lines.append(plt.plot(timestep, self.values(timestep, timeshift), 'ro', alpha=.5, ms=3))

        if show:
            ax.legend()
            plt.ylabel("Amplitude")
            plt.xlabel("Time(s)")
            plt.show()
            return 

        return lines
