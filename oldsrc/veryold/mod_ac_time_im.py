# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 16:33:33 2017
 
@author: Cintiaq
"""
 
#%% Biblioteca
 
import numpy as np
import matplotlib.pylab as pl
import time 
from scipy import signal
 
#%% Programa para a simulacao da propagacao de ondas: Modelagem 
 
 
#%% Declaração das variáveis 
start_time = time.time()
 
 
Nx = 500           # Numero de pontos no Grid (x)
Nz = 500          # Numero de pontos no Grid (z)
h = 5              # Espacamento do Grid
alfa = 10          # Parametro de dispersao
beta = 4           # Parametro de estabilidade
dt = 1.0e-04       # Incremento de tempo
T = 0.5              # Tempo final
nt = int(T/dt)     # Passos do tempo
Fx = int(Nx/2)     # Posicao da Fonte (x)
Fz = 2;            # Posicao da Fonte (z)
f_corte = 30       # Frequencia de Corte (Hz)
A = 1              # Amplitude
zi = 3             # Profundidade dos receptores
Nsnap = 20         # Numero de snapshots
fat = 1.0e-03      # Fator de amortecimento
nat = 10           # Numero de pontos do Grid que farao parte da camada de amortecimento
D = dt/h           # Variavel para simplificar os operadores finitos
 
 
 
#%% Declaração das matrizes
 
 
Pp = np.zeros((Nz,Nx))       # Matriz do tempo passado (t-1)
Pc = np.zeros((Nz,Nx))       # Matriz do tempo atual (t)
Pf = np.zeros((Nz,Nx))       # Matriz do tempo futuro (t+1)
C  = np.zeros((Nz,Nx))       # Matriz do modelo de velocidade
Sismo = np.zeros((nt,Nx))    # Matriz do Sismograma
                 
#%% Gerando o modelo de velocidade
 
C = np.copy(C) + 1500
            
for i in np.arange(np.round(Nz/3 + 1),np.round(2 * Nz/3)):
    for j in np.arange(0,Nx):
        C[i,j] = 2200
          
for i in np.arange(np.round(2 * Nz/3), Nz):
    for j in np.arange(0,Nx):
        C[i,j] = 2500
          
# Mostrandoo modelo de velocidade         
             
#pl.figure(1)            
#pl.imshow(C, cmap = pl.cm.Paired); pl.colorbar()
#pl.title("Modelo de Velocidade") 
#pl.show()
 
 
#%% Erro de Dispersao Numerica
 
 
if h > np.min(np.min(C)) / (alfa * f_corte):
    print "Erro de dispersao numerica"
     
     
#%% Erro de estabilidade
 
 
if dt > h / beta * np.max(np.max(C)):
     
    print "Erro de estabilidade"   
     
     
#%% Fonte Sismica
 
# Parametros
 
fc = f_corte/(3 * np.sqrt(np.pi)) 
 
t = np.arange(0, 2 * (2 * np.sqrt(np.pi)/fc), dt)
 
td = t - (2 * np.sqrt(np.pi)/fc) 
 
#%% Funcao fonte
 
gauss = (1 - 2 * np.pi * (np.pi * fc * td) ** 2) * np.exp(-np.pi * (np.pi*fc * td) ** 2)
 
###########################
# Descartando o excesso de zeros da fonte
 
ini_fonte = int(np.round(4.0/10 * len(gauss))) 
fim_fonte = int(np.round(6.0/10 * len(gauss))) 
 
gauss = gauss[ini_fonte:fim_fonte]
 
#############################  
 
# Plotando a fonte sismica
 
#pl.figure(2)
#pl.plot(gauss)
#pl.title("Fonte Sismica")
#pl.show()
 
 
#############################    
 
#%% Funcao amortecedora
 
w = np.zeros(nat-1)
 
conv_m = np.array([0,1,0,1,-4,1,0,1,0]).reshape(3,3)
  
for i in np.arange(0,(nat -1)): # Coloquei pra comecar do indice 0 pq no Python os vetores comecam por este indice. Outra opção seria cortar o indice 0 do vetor, utilizando o comando w = w[1:78]. Assim a função amortecedora é plotada corretamente. 
	w[i] = np.exp(-(fat * (nat-i)) ** 2)
       
#%% Fator de amortecimento
 
f_amort = w
#pl.figure(3)    
#pl.plot(f_amort)
#pl.title("Funcao de Amortecimento")
 
 
#%% Loop do tempo
 
aj_escala = 2.0e0
 
for k in np.arange(1,nt):
     
      
# Loop das diferenças finitas: 
 
    if k <= np.size(gauss) - 1:
    	Pc[Fz,Fx] = Pc[Fz,Fx] + gauss[int(k)]
 
    #M = C[1:Nz-1,1:Nx-1]
    #N = Pc[2:Nz,1:Nx-1]
    #O = Pc[1:Nz-1,1:Nx-1]
    #P = Pc[0:Nz-2,1:Nx-1] 
    #Q = Pc[1:Nz-1,2:Nx]
    #R = Pc[1:Nz-1,0:Nx-2]
    #S = Pp[1:Nz-1,1:Nx-1]

    #Z = (D**2) * M**2  * ( N - 2*O + P + Q - 2*O ) + R + 2*O - S 
    

#    Pf[1:Nz-1,1:Nx-1] =(  C[1:Nz-1,1:Nx-1] * C[1:Nz-1,1:Nx-1] * D * D) * (Pc[2:Nz,1:Nx-1] - 2 * Pc[1:Nz-1,1:Nx-1] + Pc[0:Nz-2,1:Nx-1] + Pc[1:Nz-1,2:Nx] - 2 * Pc[1:Nz-1,1:Nx-1] + Pc[1:Nz-1,0:Nx-2]) + 2 * Pc[1:Nz-1,1:Nx-1] - Pp[1:Nz-1,1:Nx-1]

    Pf = (C**2)*(D**2) + signal.convolve2d(Pc,conv_m,mode="same") + 2 * Pc - Pp
     
            
                         
# ###   %%Bordas
# 
#    
# ##%% Amortecimento (Cerjan)
#    
# 
# # Borda Direita
# 
#     aux = nat - 1
#     for i in np.arange(Nx - nat,Nx):
#         aux = aux - 1
#         for j in np.arange(Nz):            
#             Pc[j,i] = f_amort[aux] * Pc[j,i]  #np.dot(f_amort[aux], Pc[j,i])
#             Pf[j,i] = f_amort[aux] * Pf[j,i]  #np.dot(f_amort[aux], Pf[j,i])
#             
#             
# # Borda Esquerda
# 
#       
#     for i in np.arange(1, (nat - 1)):
#         for j in np.arange(Nz):
#             Pc[j,i] = np.dot(f_amort[i], Pc[j,i])
#             Pf[j,i] = np.dot(f_amort[i], Pf[j,i])
#          
# 
# # Borda Inferior
# 
#   
#     aux = nat - 1
#     for j in np.arange(Nz - nat,Nz):
#         aux = aux - 1
#         for i in np.arange(Nx):
#             Pc[j,i] = np.dot(f_amort[aux], Pc[j,i])  
#             Pf[j,i] = np.dot(f_amort[aux], Pf[j,i]) 
#             
# 
# ##%% Atenuacao das reflexoes nas bordas (Reynolds)
# 
# 
# # Borda Direita
# 
#     for n in np.arange(Nz):
#         
#         Pc[n,Nx - 1]= - D * C[n, Nx - 1] * (Pf[n, Nx - 1] - Pf[n, Nx - 2]) + Pf[n,Nx - 1] 
#              
# 
# # Borda Esquerda
#  
# 
#     for i in np.arange(Nz):
#         
#         Pc[i,0] = D * C[i,0] * (Pf[i,1] - Pf[i,0]) + Pf[i,0]
#         
#         
# # Borda Inferior
# 
#               
#     for i in np.arange(1, Nx - 1):
#         
#         Pc[Nz - 1,i] = - D * C[Nz - 1,i] * (Pf[Nz - 1,i] - Pf[Nz - 2,i]) + Pf[Nz - 1,i]          
   
         
##%% Troca das matrizes do tempo
 
 
    Pp = np.copy(Pc) 
    Pc = np.copy(Pf)
 
##%% Resolvendo a  escala de cor
 
    if (k % int(nt/Nsnap) == 0):
		A_max = np.max(np.max(np.abs(Pf))) # Amplitude maxima da fonte
		print "Interation:", k 
 
#        pl.figure(4)
#        pl.imshow(Pc, cmap = pl.cm.gray) ; pl.colorbar()
#        pl.clim(-A_max*aj_escala,A_max*aj_escala) # Para estabilizar a barra de cor
#        pl.show()
 
##%% Sismograma

#    Sismo[k,0:Nx] = Pf[zi,0:Nx]
 
    for j in np.arange(1,Nx):
		Sismo[k,j] = Pf[zi,j] #* (((k-2) * dt) * (k-2) * dt) 
    
#%% Plot Sismograma            
#pl.figure(5)
#pl.imshow(Sismo,extent=[0,nt,1,Nx],aspect=100)    
#pl.imshow(Sismo,aspect="auto")    
#pl.show()
 
elapsed_time = time.time() - start_time
 
print "%%%%%%%%%%%%%%%%%%%%%Time of Execution!%%%%%%%%%%%%%%%%%%%%%%"
print elapsed_time
