#!/usr/bin/env python

import math
import numpy as np
import numpy.linalg as la

class ellipsoid(object):
    def __init__(self,x=0,y=0,a=1,b=1):
        self.a = a
        self.b = b
        self.x = x
        self.y = y


    def flatenning(self):
        """Returns the flatenning"""
        assert (self.a!=0), "Semiaxis 'a' cannot be zero"
        return (self.a-self.b)/self.a


    def eccentricitySquared(self):
        """Return the eccentricity squared"""
        assert (self.a!=0), "Semiaxis 'a' cannot be zero"
        return ((self.a**2-self.b**2)/self.a**2)


    def eccentricity(self):
        """Return the eccentricity"""
        assert (self.a!=0), "Semiaxis 'a' cannot be zero"
        return ((self.a**2-self.b**2)/self.a**2)**.5


    def greatNormal(self,angle):
        """Return the great normal of latitude angle"""
        return ( self.a / (1-self.eccentricitySquared()*math.sin(angle)**2))


    def geocentricCoords(self,latitude,longitude,height)
        """ Return a tuple (x,y,z) coordinates of a poing given
        latitude, longitude and height"""
        x=(self.greatNormal(latitude)+height) * math.cos(latitude) * math.cos(longitude)
        y=(self.greatNormal(latitude)+height) * math.cos(latitude) * math.sin(longitude)
        z=((1-self.eccentricitySquared)*self.greatNormal+height) * math.sin(longitude)

        return (x,y,z)


class datumshift(object):

    def bursawolfModel(dx,dy,dz,rx,ry,rz,k):
        """ T:U->V C R3
        V = d + (1+k) * T U
        T = np.matrix( 1, -rz, ry ; rz, 1, -rx; -ry, rx, 1)
        k (scale factor)
        d (translation)
        d=(dx,dy,dz)

        """
        pass

    def molodenskybadekasModel():
        """
        V = d + U + T * ( U - M)
        T = np.matrix( k, -rz, ry ; rz, k, -rx; -ry, rx, k)
        M is average position. M_i = (\sum_{j=1->n} M_i_j )/n (n is the number
        of samples)
        """
        pass

    def simpMolodenskyModel():
        """
        V = d + U
        """
        pass
    



        

if __name__ == "__main__":
    elp = ellipsoid(a=1,b=.5)


