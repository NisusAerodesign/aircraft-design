import numpy as np
from scipy.optimize import fsolve
import matplotlib.pyplot as plt

#%% Constants - Valores temporários
LD      = 17         # 
R       = 6_200e3    #[m] - range
C       = 1          # consumo específico de combustível
M       = 0.8        
V       = 1          # velocidade
pmed    = 75         # kg
Qt_p    = 5  
crew    = 2
payload = 23         # kg/pessoa
 
#%% Functions 

# Empty Weight
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
    A, C = coefs(category) 
    wewo = lambda wo: A*wo**(C)
    return wewo

# Fuel 
def Raymer_Wf(fase:str)->any:
    coef = {
        'WuTo'      : 0.97,
        'Climb'     : 0.985,
        'Climb-Ac'  : lambda M: (1.0065 - 0.0325*M)*(M<1)+ (0.991 - 0.007*M - 0.01*M**2)*(M>1),
        'Landing'   : 0.995,
        'Cruise'    : lambda R, C, LD, V: np.exp(-R*C/(V*LD)),
        'Loiter'    : lambda R, C, LD   : np.exp(-R*C/LD),
    }
    wf = coef(fase)
    return wf
 
#%% MTOW
Wt  = (Qt_p+crew)*pmed  # peso tripulação
Wpl = (Qt_p)*payload    # peso payload

