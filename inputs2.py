#%%
import numpy as np
from scipy.optimize import fsolve
from inputs import Vcru, m2ft, kg2lb



#%% PARAMETROS
R = 6500 *3280.8399 
LDmax = 16
E = 20 *60
M    = 0.8
Ecruseiro = 120e3*m2ft/Vcru 

SFCcru = 0.642/3600 # 1/s
SFCloi = 0.42/3600  # 1/seg 
V  = Vcru*m2ft # ft/s
payload = 1500
qtp = 10
crew = 2
pmed =75
bg = 15 

'''
Valores professor
R = 3200 *3280.8399 
LDmax = 16
E = 45 *60
Ecruseiro = 45 *60
M = 850/3.6/342
SFCcru = 0.52/3600 # 1/s
SFCloi = 0.4/3600  # 1/seg 
V  = 850*0.911344415 # ft/s
payload = 1000
qtp = 100
crew = 7
pmed =75
bg = 15 
'''

#%%
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
    wewo = lambda wo: A*(wo**(C))
    return wewo
 
def Raymer_Wf(fase:str)->any:
    coef = {
        'WuTo'      : 0.97,
        'Climb'     : 0.985,
        'Climb-Ac'  : lambda M: (1.0065 - 0.0325*M) if M < 1 else  (0.991 - 0.007*M - 0.01*M**2),
        'Landing'   : 0.995,
        'Cruise'    : lambda R, SFC, LD, V: np.exp(-R*SFC/(V*LD)),
        'Loiter'    : lambda E, SFC, LD   : np.exp(-E*SFC/LD),
    }
    wf = coef[fase]
    return wf


print('Trecho Fortaleza - Porto Alegre')
print(f'Alcance adotado: {R/3280.8399}')
print(' ')

We = Raymer_We('JetTransport')
##  W1/W0 -> Warmup and Take Off
W1W0 = Raymer_Wf('WuTo')
print(f'WarmUp TakeOff    -> {W1W0}')

## W2/W1 -> Climb
W2W1 = Raymer_Wf('Climb-Ac')
W2W1 = W2W1(M)
print(f'Climb             -> {W2W1}')

## W3/W2 -> Cruise
LD = LDmax*0.866     # L/Dmax * 86.6# -> 13.9
W3W2f = Raymer_Wf('Cruise')
W3W2 = lambda x: W3W2f(x,SFCcru,LD,V)
print(f'Cruise1           -> {W3W2(R)}')


## W4/W3 -> Loiter 1
LD = LDmax     # L/Dmax 
W4W3f = Raymer_Wf('Loiter')
W4W3 = lambda x: W4W3f(x,SFCloi,LD)
print(f'Loiter1           -> {W4W3(E)}')
 
## W5/W4 -> Tentativa de Pouso
W5W4 = Raymer_Wf('Landing')
print(f'Attempt to Land   -> {W5W4}')

## W6/W5 -> Climb
W6W5 = W2W1
print(f'Climb             -> {W6W5}')

## W7/W6 -> Cruseiro 2 - tempo
LD = LDmax*.866   # L/Dmax 
W7W6 = Raymer_Wf('Loiter')
W7W6 = W7W6(Ecruseiro,SFCcru,LD)
print(f'Cruise2           -> {W7W6}')

## W8/W7 -> Loiter
W8W7 = W4W3
print(f'Landing           -> {W8W7(E)}')

## W9/W8 -> Landing 
W9W8=Raymer_Wf('Landing')
print(f'Final Landing     -> {W9W8}')

## Fracao de Combustivel
WfW0 = lambda R, E: 1.06*(1-W1W0*W2W1*W3W2(R)*W4W3(E)*W5W4*W6W5*W7W6*W8W7(E)*W9W8)
print(f'Wf/W0             -> {WfW0(R,E)}')

## Carga Paga
Wpl = (payload + qtp*(pmed+bg)) * 2.20462262
print(f'Carga Paga        -> {Wpl/2.20462262}')

## Tripulacao
Wcrew = (crew*(pmed+bg)) * 2.20462262
print(f'TripulaÃ§Ã£o        -> {Wcrew/2.20462262}')

## Calculo dos Pesos
W0 = fsolve(lambda W0: W0*(1-WfW0(R,E)-We(W0))-Wpl-Wcrew, 60000)

print(f'                              {W0/2.204}')
print(' ')
print(f'Qde de CombustÃ­vel:           {WfW0(R,E)*W0}')
print(f'                              {WfW0(R,E)*W0/2.204}')
print(f'                              {WfW0(R,E)*W0/2.204/0.775}')
print(' ')
print(f'Peso Vazio:                   {We(W0)*W0}')
print(f'                              {We(W0)*W0/2.204}')
print(' ')
print(f'Carga Paga + Tripulacao:      {Wpl+Wcrew}') 
print(f'                              {(Wpl+Wcrew)/2.204}')

# %%
