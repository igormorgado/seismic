"""This module implements many different seismic sources"""

import abc


class Source(object):
    """Defines a base class for a seismic source.

    By definition a seismic source has the following attributes:
        sample_rate (float):  Sampling rate in miliseconds
        coordinates (
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, sample_rate):
        """A Source must have a sample rate"""

    @abc.abstractproperty
    def sample_rate(self):
        return NotImplemented

