# -*- coding: utf-8 -*-
"""
Created on Wed Aug 09 14:26:00 2017

@author: mcabrera
"""
from __future__ import division
import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt("ang.txt")
ang = data[:, 0]
amp = data[:, 1]

ang = np.deg2rad(ang)

N = np.size(ang)
M = 3

lamb = 0.0

A = np.ones((N, M))
A[:, 1] = np.sin(ang)**2
if M==3:
    A[:, 2] = (np.sin(ang)**2)*(np.tan(ang)**2)

AT = np.transpose(A)
ATA = np.dot(AT, A)
ATA[range(M), range(M)] += lamb*np.ones(M)  
INV = np.linalg.inv(ATA)
p = np.dot(np.dot(INV, AT), amp)

adj = np.dot(A, p)

seno = np.sin(ang)**2
ang = np.rad2deg(ang)
plt.figure()
plt.plot(ang, amp, 'x')
plt.plot(ang, adj)
plt.show()

print p