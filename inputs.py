#%% Conversão
kg2lb = 2.20462
m2ft = 3.28084

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
Kld     = 15.5
Sref    = 49*m2ft*m2ft      # [m²]
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
