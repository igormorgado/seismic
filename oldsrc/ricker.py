"""This module implements many different seismic sources"""

import numpy as np
import zarr

from .source import Source

class Ricker(Source):

    """Defines a Ricker seismic source (Gauss second derivative

    By definition a Ricker seismic source a wavelet with peak centered in
    the origin (zero offset). Generated by the equation:

    $$ s(t) = \[ 1 - 2 \pi ( \pi f_c t )^2 \] e^{-\pi ( \pi f_c t )^2} $$

    Where:
    
    $f_c$ is the central frequency.
    $t$ is the time instant

    Pay attention that Sampling Rate is deeply related with wavelet maximum
    frequency that is related with central frequency.

    Is possible to infer the maximum frequency from the central frequency.

    Also the ricker source is related to time not the timestep
    """

    def __init__(self, central_frequency=None, cut_frequency=None, sample_rate=None):
        """Initialize the Ricker source"""
        data = [i for i in [central_frequency, cut_frequency ] if i is not None]
        if len(data) > 1:
            raise ValueError("You need to specify only 'central_frequency' or 'cut_frequency'.")
        if central_frequency is not None:
            self.central_frequency = central_frequency
        elif cut_frequency is not None:
            self.cut_frequency = cut_frequency
        elif sample_rate is not None:
            self.sample_rate = sample_rate
        else:
            raise ValueError("You must define 'central_frequency', 'cut_frequency'")


    def __str__(self):
        msgstr = "Ricker(central_frequency={}, cut_frequency={})"
        msgfmt = msgstr.format(self.central_frequency, self.cut_frequency)
        return fmt


    @property
    def cut_frequency(self):
        """Returns the 'cut' frequency of Ricker source wavelet"""
        return self._cut_frequency


    @cut_frequency.setter
    def cut_frequency(self, value):
        """Sets the cut frequency of gaussian function of given central frequency.

        Params:
            central_frequency(float): Central frequency (where the peak lies)
        """
        self._cut_frequency = value


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
        self._cut_frequency = 2*value


    @property
    def central_frequency(self):
        """Returns the 'central' frequency of Ricker source wavelet"""
        return self._cut_frequency/(3 * np.sqrt(np.pi))


    @central_frequency.setter
    def central_frequency(self, value):
        """Sets the central frequency of gaussian function of given cut frequency.

        Params:
            value(float): Cut frequency
        """
        self._cut_frequency = 3 * np.sqrt(np.pi) * value


    @property
    def period(self):
        """Returns the period (+/-) of gaussian function of given cut frequency."""
        return (2 * np.sqrt(np.pi))/self._cut_frequency


    


    # TODO: Probably sample rate need to be passed as parameter
    # @property
    # def sample_rate(self):
    #     return 500/(self._cut_frequency)

    # @sample_rate.setter
    # def sample_rate(self, value):
    #     """Returns the sampling rate based on self.cut_frequency."""
    #     self._cut_frequency = 500/(value)

    
    # @property
    # def max_timesteps(self):
    #     """Returns the maximum number of timesteps of Ricker source"""
    #     return np.ceil((4*np.sqrt(np.pi))/(self._cut_frequency * (self.sample_rate/1000)))


    # def timestep(self, t):
    #     """Returns the positive values of time steps based on source period"""
    #     return (t-1) * (self.sample_rate/1000) - self.period
 

    # def values(self):
    #     """A ricker seismic source."""
    #     t = np.arange(self.max_timesteps)
    #     t = (t * (self.sample_rate/1000)) - self.period
    #     x = np.pi * (np.pi * self.central_frequency * t)**2
    #     f = (1 - 2 * x) * np.exp(-x)
    #     return f
 
    # def plot(self, show=True):
    #     """Plot the ricker source"""

    #     import matplotlib.pyplot as plt

    #     source = self.values()
    #     n = np.arange(len(source))
    #     t = self.sample_rate/1000 * n

    #     #Plot
    #     fig = plt.figure()
    #     plt.plot(t, source)
    #     plt.plot(t, source, 'ro', alpha=.5, ms=3)

    #     msgtitle=r"Gauss Source @{}Hz $\Delta t = {:.4f}$"
    #     fmttitle=msgtitle.format(self.cut_frequency, self.sample_rate/1000)
    #     plt.title(fmttitle)

    #     plt.ylabel("Amplitude")
    #     plt.xlabel("Time(s)")

    #     if show:
    #         plt.show()
    #     else:
    #         return fig

    # def save(self):
    #     """Save source to disk"""
