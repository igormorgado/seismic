# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 18:04:31 2016

@author: morga
"""

from __future__ import division
import numpy  as np

def calculate_matrix(phi0,alpha1,beta1,rho1,alpha2,beta2,rho2):
    """Calculate angles using Snell's law
    \frac{\sin(\phi_1)}{\sin(\phi_2)}=\frac{\alpha_1}{\alpha_2}    
    Parameters:
        phi0:   Wave incident angle media 1 on point over the interface
        alpha1: P-wave speed on media 0
        beta1:  S-wave speed on media 0
        rho1:   Media 1 Density
        alpha2: P-wave speed on media 1
        beta2:  S-wave speed on media 1
        rho2:   Media 2 Density
    """

    """Used variables:    
    pp:  Ray Parameter
    phi1: angle of reflected P-wave
    phi2: angle of transmitted P-wave
    psi1: angle of reflected S-wave
    psi2: angle of transmitted S-wave
    """
    
    # Ray Parameter
    pp=np.math.sin(phi0)/alpha1
    
    # phi1 is always equal incident angle
    phi1=phi0
    
    # Will never be greater than incident angle since V_s < V_p
    psi1=np.math.asin(pp*beta1)    

    # For angles that are in the second layer they might be critical
    alpha2pp=pp*alpha2    
    alpha2pp2=alpha2pp**2

    beta2pp=pp*beta2
    beta2pp2=beta2pp**2

    cc=1-2*beta2pp2

    # Calculate all imaginary coefficients
    if alpha2pp > 1:
        phi2=np.math.pi/2
        j20=(-((alpha2pp2-1)**(0.5)))*1j
        j23=(-rho2/rho1 * beta2**2 * alpha1/beta1**2*2*pp*(alpha2pp2-1)**(0.5))*1j
    elif alpha2pp < -1:
        phi2=-np.math.pi/2
        j20=((alpha2pp2-1)**(0.5))*1j
        j23=(rho2/rho1 * beta2**2 * alpha1/beta1**2*2*pp*(alpha2pp2-1)**(0.5))*1j        
    else:
        j20=0
        j23=0    
        phi2=np.math.asin(alpha2pp)

    if beta2pp > 1:
        psi2=np.math.pi/2
        j31=(beta2pp2-1)**(0.5)*1j
        j32=(-rho2/rho1*beta2*beta2/alpha1*2*pp*(beta2pp2-1)**(0.5))*1j
    elif beta2pp < -1:
        psi2=-np.math.pi/2
        j31=-((beta2pp2-1)**(0.5))*1j
        j32=(rho2/rho1*beta2*beta2/alpha1*2*pp*(beta2pp2-1)**(0.5))*1j
    else:
        j31=0
        j32=0
        psi2=np.math.asin(beta2pp)

    # Main matrix for an incident P wave    
    m = np.zeros((4,4),dtype="complex")
    v = np.zeros(4,dtype="complex")    

    m[0]=[  np.math.cos(phi1),
            -np.math.sin(phi1),
            -np.math.cos(2*psi1),
             np.math.sin(2*phi1)
             ]
    m[1]=[ -np.math.sin(psi1),
            -np.math.cos(psi1),
             np.math.sin(2*psi1)*(beta1/alpha1),
             np.math.cos(2*psi1)*(alpha1/beta1)
            ]

    if alpha2pp2 < 1:
        m[2]=[ 
            np.math.cos(phi2) + j20,
            alpha2pp,
            rho2/rho1 * alpha2/alpha1 * cc + j23,
            rho2/rho1 * beta2**2/beta1**2 * alpha1/alpha2 * np.math.sin(2*phi2)            
            ]
    else:
        m[2]=[ 
            0 + j20,        
            alpha2pp,
            rho2/rho1 * alpha2/alpha1 * cc + j23,
            0 
            ]

    if beta2pp2 < 1:
        m[3] = [
            beta2pp,
            -np.math.cos(psi2)+j31,
            rho2/rho1*beta2/alpha1*np.math.sin(2*psi2)+j32,
            -rho2/rho1*alpha1*beta2/beta1/beta1*cc
        ]
    else:
        m[3]= [
            beta2pp,
            0+j31,
            0+j32,
            -rho2/rho1*alpha1*beta2/beta1/beta1*cc            
        ]   

    v=[
        np.math.cos(phi1),
        np.math.sin(phi1),
        np.math.cos(2*psi1),
        np.math.sin(2*phi1),
    ]

    detm=np.linalg.det(m)    
    detm_norm=np.linalg.norm(detm)
    #print(detm)
    #print(detm_norm)
    
    vd=np.zeros(4,dtype="complex")
    vn=np.zeros(4,dtype="float")
    phase=np.zeros(4,dtype="float")
    for i in range(4):
        # Make a copy of i-th column vector from matrix m
        cvt=m[i]
        
        # Copy vector to matrix i-th column of matrix m
        m[i]=v
        
        # Calculate the determinant and store on a array
        vd[i]=np.linalg.det(m)
        vn[i]=np.linalg.norm(vd[i])/detm_norm
        phase[i]=np.math.atan2(vd[i].real*detm.real-vd[i].imag*detm.imag,
                               vd[i].real*detm.real+vd[i].imag*detm.imag )
        
        # Copy the vector back    
        m[i]=cvt

    # a1,b1,a2,b3
    return vd, vn, phase        

if __name__ == "__main__":

    phi0=np.math.pi/4       # Incident angle initial value
    incident_wave_p=1       # Incident p-wave, if zero it's Sv
    alpha1=3000             # Speed P waves above interface
    alpha2=4000             # Speed P waves below interface
    beta1=1500              # Speed S waves above interface
    beta2=2000              # Speed S waves below interface
    rho1=2000               # Density above interface
    rho2=2200               # Density below interface

    m1,m2,ph = calculate_matrix(phi0, alpha1, beta1, rho1, alpha2, beta2, rho2)