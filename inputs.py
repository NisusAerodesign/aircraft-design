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
LD      = 17             
R       = 6_500e3       # [m]
C       = 800/3600      # kg/h
Hcru    = 13.7e3        # [m]
Mcru    = 0.8        
Vcru    = a(Hcru)*Mcru  # [m/s] 

#%% Missão
pmed    = 75         # kg
Qt_p    = 10  
crew    = 2
payload = 1500       # kg