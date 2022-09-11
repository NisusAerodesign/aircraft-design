import numpy as np

#%% Conversão
kg2lb = 2.20462
m2ft  = 3.28084

#%% Condições de Voo
a0      = 340.3             #[m/s]
g       = 9.80665           #[m/s^2]
Rsp     = 287.15            #[J/kg/K]
T0      = 288.15            #[K]
Lambda  = -0.0065           #[K/m]
gamma   = 1.4   

T       = lambda H: T0 + Lambda*H
a       = lambda H: (gamma*Rsp*T(H))**(0.5) 

#%% Aeronave

# Estimativa LDmax
Kld         = 15.5                                  # Kld for civil jets
wingspan    = np.array([21,   21.5, 19.2, 21.1])    # [m]
wingarea    = np.array([48.5, 44.85, 46,  49.9])    # [m²]
# Swet      = 
AR          = np.mean(wingspan**2/wingarea)
LDmax       = 

print(f'VALORES MÉDIOS DE ESTIMATIVA')
print(f'Envergadura\t-> {round(np.mean(wingspan), 2)} [m]')
print(f'Área da asa\t-> {round(np.mean(wingarea),2)} [m²]')
print(f'Razaão de aspecto\t-> {AR}')


SFCloi  = 0.42/3600         # [lb/(lbf.s)]
SFCcru  = 0.642 /3600       # [lb/(lbf.s)]
LDmax   = 16             

#%% Missão
R       = 6_500e3 * m2ft       # [m]
Hcru    = 11e3 *m2ft          # [m]
Mcru    = 0.8        
Vcru    = a(Hcru)*Mcru *m2ft  # [m/s] 
t_loiter = 20*60         # [s] 

pmed    = 75 *kg2lb         # kg
Qt_p    = 10  
crew    = 2
payload = 1500 *kg2lb      # kg
# %%

#%% PARAMETROS
# R = 6500 *3280.8399 
# LDmax = 16
# E = 20 *60
# M    = 0.8
# Ecruseiro = 120e3*m2ft/Vcru 

# sfc_cruize = 0.642/3600 # 1/s
# SFCloi = 0.42/3600  # 1/seg 
# V  = Vcru*m2ft # ft/s
# payload = 1500
# qtp = 10
# crew = 2
# pmed =75
# bg = 15 
