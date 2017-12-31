# -*- coding: utf-8 -*-
"""
Created on Sat Feb 21 02:55:05 2015

@author: Marlon
"""

def least_square(A, d, k=0):
    import numpy as np
    dT = np.transpose([d])               # Data
    AT = np.transpose(A)
    ATA = np.dot(AT,A)        
    if k:
        M = np.shape(A)[1]
        Id = k*np.identity(M)            # Tikonovki zero-order    
        ATAi = np.linalg.inv(ATA+Id)     # Inverted matrix
    else:
        ATAi = np.linalg.inv(ATA)        # Inverted matrix    
    ATAiAT = np.dot(ATAi,AT)    
    p = np.dot(ATAiAT,dT)                # Least-Square solutions. p = parameters vector       
    return p.ravel()
    
def ponderate_adj(A, d, W, k=0):
    import numpy as np
    N,M = np.shape(A)
    dT = np.transpose([d])               # Data    
    AT = np.transpose(A)
    ATW = np.zeros_like(AT) 
    for i in range (M):
        ATW[i,:] = AT[i,:]*W      
    ATWA = np.dot(ATW,A)    
    if k>0:                              # Regularization
        ATWA[range(M),range(M)] += k    
    ATWAi = np.linalg.inv(ATWA) 
    ATWAiAT = np.dot(ATWAi,AT)
    ATWAiATW = np.zeros_like(AT)    
    for i in range (M):
        ATWAiATW[i,:] = ATWAiAT[i,:]*W 
    return np.dot(ATWAiATW,dT)
    
def pol_adjust(x,y,z,n):
    # Find the Least-Square solution of order n=polynomial order. 
    # Input data - x, y, z=data(x,y).
    import numpy as np

    M = 0                   # Number of parameters (function of n)
    x_exp = []
    y_exp = []
    for k in range(n+1):
        for l in range (k+1):
            x_exp.append(k-l)    
            y_exp.append(l) 
            M+=1             
    N = np.size(z)          # Number of observation points
    A = np.zeros((N,M))     # Sensibility Matrix
    # Find the sensibility matrix on each (i,j) points
    for i in range(N):
        for j in range(M):
            A[i][j] = (x[i]**x_exp[j])*(y[i]**y_exp[j])         
    # Matrix manipulation and Least-Square inversion         
    p = least_square(A, z, k=0.0)            
    # Return the polynomial adjusted in each (i,j) points as an 1D array
    return p, np.dot(A,p).ravel()

def robust_adjust(x,y,z,shp,n):
    # Find the Least-Square solution of order n=polynomial order. 
    # Input data - x, y, z=data(x,y).
    import numpy as np

    M = 0  #Number of parameters (function of n)
    x_exp = []
    y_exp = []
    for k in range(n+1):
        for l in range (k+1):
            x_exp.append(k-l)    
            y_exp.append(l) 
            M+=1    
    N = np.size(z)          # Number of observation points
    A = np.zeros((N,M))     # Sensibility Matrix
    
    # Set a new coordinate system with (0,0)     
    xp = x - np.min(x)
    yp = y - np.min(y)     
    
    # Find the sensibility matrix on each (i,j) points
    for i in range(N):
        for j in range(M):
            A[i][j] = xp[i]**x_exp[j]*yp[i]**y_exp[j]
            
    dT = np.transpose(np.array([z]))    # Data transposed    
    AT = np.transpose(A)                # Sensibility transposed
    ATW = np.zeros_like(AT)
    ATWAi = np.linalg.inv(np.dot(AT,A))     
    ATWAiATW = np.dot(ATWAi,AT)
    p = np.dot(ATWAiATW,dT) 
    r = z-np.dot(A,p).ravel()
    s = np.median(abs(r))
    
    for k in np.arange(1,3,1): 
        for i in range (M):
            for j in range(N):
                ATW[i][j] = AT[i][j]*np.exp(-(0.6745*(r[j]**(k-1))/s)**2)      
        ATWAi = np.linalg.inv(np.dot(ATW,A)) 
        ATAWAiAT = np.dot(ATWAi,AT)        
        for i in range (M):
            for j in range(N):
                ATWAiATW[i][j] = ATAWAiAT[i][j]*np.exp(-(0.6745*(r[j]**(k-1))/s)**2)
        p = np.dot(ATWAiATW,dT) 
        r = z-np.dot(A,p).ravel()
        s = np.median(abs(r))   
        
    #return the polynomial adjusted in each (i,j) points as an 1D array   
    return np.dot(A,p).ravel()

def par_adjust(x,y,z):
    #Find the Least - Square solution of a parabola
    #Input data - x, y, z=data(x,y) as a 1D array.
    import numpy as np

    x_exp = [0,1,0,2,1,0]
    y_exp = [0,0,1,0,1,2]
    dot = [1.,1.,1.,.5,1.,.5]
            
    N = np.size(z)          #Number of observation points
    A = np.zeros((N,6))     #Sensibility Matrix
    
    #Set a new coordinate system with (0,0)     
    xp = x - np.min(x)
    yp = y - np.min(y) 
    
    #Find the sensibility matrix in each (i,j) points
    for i in range(N):
        for j in range(6):
            A[i][j] = (xp[i]**x_exp[j])*(yp[i]**y_exp[j])*dot[j]
            
    #Matrix manipulation and Least-Square inversion                
    p = least_square(A, z, k=0.001)  
    #Return parameters. f(x,y) = a + bx*x + by*y + 0.5*cxx*x^2 + cxy*x*y + 0.5*cyy*y^2
    #p = [a, bx, by, cxx, cxy, cyy]
    return p

def automatic_edge(x,y,z,win=3,delta=1):
    import numpy as np    
   
    shape = np.shape(z)
    M = np.empty((win,win))
    xi = np.empty((win,win))
    yi = np.empty((win,win))
    nn = 0
    # falta colocar o delta em h1 e h2 para dessimar
    h1 = np.empty((shape[0]-(win-1),shape[1]-(win-1)))
    h2 = np.empty((shape[0]-(win-1),shape[1]-(win-1)))   
    # x,y solutions
    xo = np.empty((shape[0]-(win-1))*(shape[1]-(win-1)))
    yo = np.empty((shape[0]-(win-1))*(shape[1]-(win-1)))     
    
    for i in np.arange(0,shape[0]-(win-1),delta):
        for j in np.arange(0,shape[1]-(win-1),delta):
            M = z[i:i+win:1,j:j+win:1].ravel()
            xi = x[i:i+win:1,j:j+win:1].ravel()
            xi = xi - np.min(xi)
            yi = y[i:i+win:1,j:j+win:1].ravel()
            yi = yi - np.min(yi)
            p = par_adjust(xi,yi,M)
            k = (p[3]-p[5])**2 + 4.*p[4]**2     
            h1[i][j] = (p[3] + p[5] + np.sqrt(k))/2.
            h2[i][j] = (p[3] + p[5] - np.sqrt(k))/2.
            #EigenVectors
            den = (k**0.25) * np.sqrt(2.)                     
            l11 = sinal(p[4])*np.sqrt(np.sqrt(k)+(p[3]-p[5]))/den 
            l21 = np.sqrt(np.sqrt(k)-(p[3]-p[5]))/den          
            to = -(p[1]*l11+p[2]*l21)/(p[3]*l11**2+2.*p[4]*l11*l21+p[5]*l21**2)
            xo[nn] = l11*to + x[i+1][j+1]
            yo[nn] = l21*to + y[i+1][j+1]       
            nn+=1            
    
    xp = x[int((win-1)/2):shape[0]-int((win-1)/2):delta,int((win-1)/2):shape[1]-int((win-1)/2):delta]        
    yp = y[int((win-1)/2):shape[0]-int((win-1)/2):delta,int((win-1)/2):shape[1]-int((win-1)/2):delta] 
    nshp = np.shape(xp)            
    # Restrictin solutions    
    xo[xo>np.max(x)]=np.nan
    yo[xo>np.max(x)]=np.nan
    xo[xo<np.min(x)]=np.nan
    yo[xo<np.min(x)]=np.nan
    xo[yo>np.max(y)]=np.nan
    yo[yo>np.max(y)]=np.nan
    xo[yo<np.min(y)]=np.nan
    yo[yo<np.min(y)]=np.nan
    #h1 = h1[~np.isnan(h1)]
    #h2 = h2[~np.isnan(h2)]
    return xp.ravel(),yp.ravel(),h1.ravel(),h2.ravel(),nshp,zip(xo,yo)   
    
def curvatures(delx,z):
    import numpy as np
    shape = np.shape(z)
    dip = np.float64(np.empty(shape)) 
    az = np.float64(np.empty(shape))
    km = np.float64(np.empty(shape))
    kg = np.float64(np.empty(shape))  
    kpos = np.float64(np.empty(shape))
    kneg = np.float64(np.empty(shape)) 
    M = np.empty((3,3))
    for i in np.arange(0,shape[0]-2,1):
        for j in np.arange(0,shape[1]-2,1):
            M = z[i:i+3:1,j:j+3:1].ravel()
            a = (M[0]+M[2]+M[3]+M[5]+M[6]+M[8])/(12.*delx**2) - (M[1]+M[4]+M[7])/(6.*delx**2)
            b = (M[0]+M[1]+M[2]+M[6]+M[7]+M[8])/(12.*delx**2) - (M[3]+M[4]+M[5])/(6.*delx**2)
            c = (M[2]+M[6]-M[0]-M[8])/(4.*delx**2)
            d = (M[2]+M[5]+M[8]-M[0]-M[3]-M[6])/(6.*delx)
            e = (M[0]+M[1]+M[2]-M[6]-M[7]-M[8])/(6.*delx)
            #f = (2*(M[1]+M[3]+M[5]+[7])-(M[0]+M[2]+M[6]+M[8])+5*M[4])/(9.)
            #Attributes            
            dip[i+1][j+1] = np.arctan(np.sqrt(d**2+e**2))
            az[i+1][j+1] = np.arctan(e/d)
            km[i+1][j+1] = (a*(1+e**2)+b*(1+d**2)-c*d*e)/(1+d**2+e**2)**1.5
            kg[i+1][j+1] = (4.*a*b-c**2)/(1+d**2+e**2)**2
            kpos[i+1][j+1] = (a+b)+np.sqrt((a-b)**2+c**2)
            kneg[i+1][j+1] = (a+b)-np.sqrt((a-b)**2+c**2) 
    kmax = km + np.sqrt(km**2+kg)    
    kmin = km - np.sqrt(km**2-kg) 
    si = (2./np.pi)*np.arctan2((kmin+kmax),(kmax-kmin))
    return dip,az,km,kg,kmax,kmin,kpos,kneg,si  
                                  
def dTFdh_prism(xp,yp,zp,p,I,D,amp):
    #x,y 1D array and p the prism location like [X1,X2,Y1,Y2,Z1,Z2]
    import numpy as np
    V1 = -0.5773503
    V2 = -V1       
    L = p[1]-p[0]
    W = p[3]-p[2]
    H = p[5]-p[4]               
    xc = (p[0]+p[1])/2.    
    yc = (p[2]+p[3])/2.    
    XL = [xc+.5*L*V1,xc+.5*L*V2]
    YL = [yc+.5*W*V1,yc+.5*W*V2]
    ZL = [.5*(V1*(p[5]-p[4])+p[5]+p[4]),.5*(V2*(p[5]-p[4])+p[5]+p[4])]
    R = np.zeros(np.size(xp))            
    DX = 0
    DZ = 0
    for i in range(2):
       for j in range(2):
           for k in range(2):
                R = np.sqrt((XL[i]-xp)**2 + (YL[j]-yp)**2 + (ZL[k]-zp)**2)                
                div = R**5
                R2 = R**2
                DX += amp*np.cos(I)*np.cos(D)*(3*(XL[i]-xp)**2-R2)/div + amp*np.cos(I)*np.sin(D)*(3*(XL[i]-xp)*(YL[j]-yp))/div + amp*np.sin(I)*(3*(XL[i]-xp)*(ZL[k]-zp))/div
                DZ += amp*np.cos(I)*np.cos(D)*(3*(XL[i]-xp)*(ZL[k]-zp))/div + amp*np.cos(I)*np.sin(D)*(3*(YL[j]-yp)*(ZL[k]-zp))/div + amp*np.sin(I)*(3*(ZL[k]-zp)**2-R2)/div
    DX = DX*(H*L*W/8.)
    DZ = DZ*(H*L*W/8.)
    DTF = DX*np.cos(I) + DZ*np.sin(I)
    return DTF

def inv_sus(x,y,z,data,bounds,dx,dy,inc,dec,amp,k):
    #x,y,z,data - 1D array
    #bounds, dx,dy,dz - Discretization model
    import numpy as np  
    import geolib as gb
    model = gb.mesher_Layerprism(bounds,dx,dy,15000,20000)            
    I = np.deg2rad(inc)     #Geomagnetic inclination
    D = np.deg2rad(dec)     #Geomagnetic declination           
    N = np.size(z)          #Number of data points
    M = np.shape(model)[0]  #Number of data parameters 
    #Sensibility matrix    
    A = np.zeros((N,M))        
    #find the dTF/dhj for all colums (points)    
    for j in range(M):
            A[:,j] = dTFdh_prism(x,y,z,model[j],I,D,amp)                    
    #Matrix manipulation and Least-Square inversion                   
    p = least_square(A, data, k)        
    return p, np.dot(A,p), model

def euler_profile(x,tf,dx, dz, n=1.):
    # Find the 2D Euler solution of a fixed window
    from numpy import size, ones
    N = size(tf)
    #Sensibility Matrix        
    A = ones((N,3))*n    
    A[:,0] = dx
    A[:,1] = dz
    A[:,2] = tf
    #Observed data Matrix    
    d = x*dx   
    #Matrix manipulation and Least-Square inversion                
    p = least_square(A, d, k=0)    
    return p
    
def werner_profile(x, tf):
    # Find the 2D Euler solution of a fixed window
    from numpy import size, ones, sqrt
    N = size(tf)
    #Sensibility Matrix        
    A = ones((N,6))    
    A[:,1] = x
    A[:,2] = tf
    A[:,3] = x*tf
    A[:,4] = x**2
    A[:,5] = x**3
    #Observed data Matrix    
    d = tf*x**2
    #Matrix manipulation and Least-Square inversion                 
    p = least_square(A, d, k=0)    
    xc = p[3]/2.
    zc = sqrt(-4.*p[2]-p[3]**2)/2.    
    return xc, zc
    
def euler_grid(x,y,z,tf,shp,n,dx,dy,dz):
    #Find the 3D Euler solution of a fixed window
    import numpy as np
    #import filtering as ft
    N = np.size(tf)
  
    #Sensibility Matrix        
    A = np.ones((N,4))*n    
    A[:,0] = dx
    A[:,1] = dy
    A[:,2] = dz
    #Observed data Matrix    
    d = np.zeros(N)
    for i in range(N):
        d[i] = x[i]*dx[i]+y[i]*dy[i]+z[i]*dz[i]+n*tf[i]    
    #Matrix manipulation and Least-Square inversion                
    p = least_square(A, d, k=0)               #Least-Square solutions. p = parameters vector
    return p

def tf2d_inv(xp, alt, tf_ob, x_vert, z_vert, inc, dec, amp, sus, k, ninter=3):
   import foward as fw 
   import numpy as np 
   N = np.size(xp)          # Number of observation points
   M = np.size(x_vert)      # Number of vertices (parameters)
   # Sensibility matrix    
   A = np.zeros((N,M))           
   d = np.transpose(np.array([tf_ob]))   # Observation data 
   p = np.transpose(np.array([z_vert]))  # Initial quest
   # Run the interactions
   for i in range(ninter):
       # Find the sensibility matrix A
       p_inv = np.copy(p.ravel())
       for j in range(M):           
           save = np.copy(p_inv[j])
           p_inv[j] = save + 1*save
           tf_p1 = fw.tf_talwani(xp, alt, x_vert[::-1], p_inv[::-1], inc, dec, amp, sus)  
           p_inv[j] = save - 1*save            
           tf_p2 = fw.tf_talwani(xp, alt, x_vert[::-1], p_inv[::-1], inc, dec, amp, sus)
           A[:,j] = (tf_p1-tf_p2)/(2*save)     # Fill the colums whit the derivative of the field referent to heach parameter         
           p_inv[j] = save
       # Matrix manipulation and Least-Square inversion                    
       kRTR = k*np.identity(M)                    # Tikonovki zero-order  
       AT = np.transpose(A)
       ATA = np.dot(AT,A)
       ATAi = np.linalg.inv(ATA + kRTR)  # Inverted matrix       
       CAL = np.transpose(np.array([fw.tf_talwani(xp, alt, x_vert[::-1], p[::-1].ravel(), inc, dec, amp, sus)]))
       MIS   = d - CAL       
       ATM = np.dot(AT,MIS) - k*p
       DPP = np.dot(ATAi,ATM)        
       p += DPP

   return p.ravel()