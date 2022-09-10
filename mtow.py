#%% Librarys
import numpy as np
from inputs import *
from scipy.optimize import fsolve
import matplotlib.pyplot as plt

#%% Functions 

def Raymer_We(category:str)->any:
    coefs = {
        'Sail'         :[0.86, -0.05],
        'Sailpowerd'   :[0.91, -0.05],
        'HBmetal'      :[1.19, -0.09],
        'HBcomp'       :[0.99, -0.09],
        'GAsingle'     :[2.36, -0.18],
        'GAtwin'       :[1.51, -0.10],
        'Agricultural' :[0.74, -0.03],
        '2TurboP'      :[0.96, -0.05],
        'FlyBoat'      :[1.09, -0.05],
        'JetTrainer'   :[1.59, -0.10],
        'JetFighter'   :[2.34, -0.13],
        'MilitaryCargo':[0.93, -0.07],
        'JetTransport' :[1.02, -0.06]
        }
    A, C = coefs[category] 
    wewo = lambda wo: A*wo**(C)
    return wewo
 
def Raymer_Wf(fase:str)->any:
    coef = {
        'WuTo'      : 0.97,
        'Climb'     : 0.985,
        'Climb-Ac'  : lambda M: (1.0065 - 0.0325*M) if M < 1 else  (0.991 - 0.007*M - 0.01*M**2),
        'Landing'   : 0.995,
        'Cruise'    : lambda R, SFC, LD, V: np.exp(-R*SFC/(V*LD)),
        'Loiter'    : lambda R, SFC, LD   : np.exp(-R*SFC/LD),
    }
    wf = coef[fase]
    return wf
 

#%% Tripulação
Wcrew = crew*pmed*2.20462262            # [lb]

#%% Carga paga
Wpl = (payload + Qt_p*pmed)*2.20462262  # [lb]

#%% Combustível
We   = Raymer_We('JetTransport') 

# Warm Up and Take Off
W1W0 = Raymer_Wf('WuTo')

# Climb 1
W2W1 = Raymer_Wf('Climb-Ac')(Mcru)

# Cruise 1
R1    = R/0.3048                # [ft]
LD    = LDmax*0.866             
V1    = Vcru*0.911344415        # [ft/s]
W3W2  = lambda x: Raymer_Wf('Cruise')(x, SFCcru, LD, V1) 

# Loiter 1
LD    = LDmax
W4W3  = lambda x: Raymer_Wf('Loiter')(x,SFCloi,LD)

# Attempt to land
W5W4  = Raymer_Wf('Landing')
 
# Climb 2
W6W5  = W2W1 

# Cruise 2
tcru = R/Vcru
LD   = LDmax*0.866
W7W6 = Raymer_Wf('Loiter')(tcru, SFCcru, LD)

# Loiter 2
W8W7 = W4W3

# Landing
W9W8 = Raymer_Wf('Landing')

# Fração de combustível
def WfW0(R,t):
    R    *= 3.28084
    aux1 = W1W0*W2W1*W3W2(R)*W4W3(t)*W5W4*W6W5
    aux1 *= W7W6*W8W7(t)*W9W8
    
    return 1.06*(1 - aux1)

Res = lambda W0: Wpl + Wcrew + We(W0)*W0 + WfW0(R,loiter)*W0 - W0 
W0  = fsolve(Res, 18e3*2.20462)
print(f'W0 = {W0}')  
#%% plot
x = np.arange(0,1e7)

plt.plot(x,Res(x))
plt.show()

# %%
