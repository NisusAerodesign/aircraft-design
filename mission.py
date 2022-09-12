from cProfile import label
import numpy as np
from flightfunctions import mission_estimation, return_fuel_mass
import matplotlib.pyplot as plt

#%% Aeronave
wingspan = np.array([21,   21.5,  19.2, 21.1])
wingarea = np.array([48.5, 44.85, 46,   49.9])

print('Valores Geométricos Médios')
print(f'Envergadura\t-> {round(np.mean(wingspan),2)} [m]')
print(f'Área da Asa\t-> {round(np.mean(wingarea), 2)} [m²]')
# Estimativa LDmax
LDmax    = 15.8
SFCloi  = 0.42         # [lb/(lbf.h)]
SFCcru  = 0.642        # [lb/(lbf.h)]

#%% Missão
R1          = 6_300e3        # [m]
R2          = 200            # [m]
Mcru        = 0.8        
loiter_time = 20             # [min] 
crew        = 3
payload     = 1500           # [kg]

print('\n New York to London - Biggin Hill ')
LGA_LCY_a = mission_estimation( f_range=5542, s_range=19, LDmax=15.8, sfc_cruize=0.642, sfc_sea_level=0.42 )
print('\n New York to London - Rochester ')
LGA_LCY_b = mission_estimation( f_range=5542, s_range=21, LDmax=15.8, sfc_cruize=0.642, sfc_sea_level=0.42 )
print('\n New York to London - London Southend ')
LGA_LCY_c = mission_estimation( f_range=5542, s_range=45, LDmax=15.8, sfc_cruize=0.642, sfc_sea_level=0.42 )

print('\n London to Dubai - Xarja ')
LCY_DXB_a = mission_estimation( f_range=5440, s_range=20, LDmax=15.8, sfc_cruize=0.642, sfc_sea_level=0.42 )
print('\n London to Dubai - al Maktoum ')
LCY_DXB_b = mission_estimation( f_range=5440, s_range=45, LDmax=15.8, sfc_cruize=0.642, sfc_sea_level=0.42 )
print('\n London to Dubai - Ras al Khaimah ')
LCY_DXB_c = mission_estimation( f_range=5440, s_range=70, LDmax=15.8, sfc_cruize=0.642, sfc_sea_level=0.42 )

print('\n Dubai to Beijing - Daxing  ')
DXB_PEC_a = mission_estimation( f_range=5834, s_range=64, LDmax=15.8, sfc_cruize=0.642, sfc_sea_level=0.42 )
print('\n Dubai to Beijing - Tangshan Sannvhe  ')
DXB_PEC_b = mission_estimation( f_range=5834, s_range=120, LDmax=15.8, sfc_cruize=0.642, sfc_sea_level=0.42 )
print('\n Dubai to Beijing - Tianjin  ')
DXB_PEC_c = mission_estimation( f_range=5834, s_range=118, LDmax=15.8, sfc_cruize=0.642, sfc_sea_level=0.42 )

print(f'Para {round(DXB_PEC_b[0]*DXB_PEC_b[-2], 2)} é necessário {round(DXB_PEC_b[0]*DXB_PEC_b[-2]/0.84, 2)} litros de JET-A')

print('\n Worst case')
worst_case = mission_estimation( f_range=6300, s_range=200, LDmax=15.8, sfc_cruize=0.642, sfc_sea_level=0.42 )

wf_LGA_LCY_a = return_fuel_mass(LGA_LCY_a)
wf_LGA_LCY_b = return_fuel_mass(LGA_LCY_b)
wf_LGA_LCY_c = return_fuel_mass(LGA_LCY_c)

wf_LCY_DXB_a = return_fuel_mass(LCY_DXB_a)
wf_LCY_DXB_b = return_fuel_mass(LCY_DXB_b)
wf_LCY_DXB_c = return_fuel_mass(LCY_DXB_c)

wf_DXB_PEC_a = return_fuel_mass(DXB_PEC_a)
wf_DXB_PEC_b = return_fuel_mass(DXB_PEC_b)
wf_DXB_PEC_c = return_fuel_mass(DXB_PEC_c)


plt.plot(range(0,10), wf_LGA_LCY_a, 'r',label='New York - London - Biggin Hill')
plt.plot(range(0,10), wf_LGA_LCY_b, 'r',label='New York - London - Rochester')
plt.plot(range(0,10), wf_LGA_LCY_c, 'r',label='New York - London - London Southend')

plt.plot(range(0,10), wf_LCY_DXB_a, 'y',label='London - Dubai - Xarja')
plt.plot(range(0,10), wf_LCY_DXB_b, 'y',label='London - Dubai - al Maktoum')
plt.plot(range(0,10), wf_LCY_DXB_c, 'y',label='London - Dubai - Ras al Khaimah')

plt.plot(range(0,10), wf_DXB_PEC_a, 'm',label='Dubai - Beijing - Daxing')
plt.plot(range(0,10), wf_DXB_PEC_b, 'm',label='Dubai - Beijing - Tangshan Sannvhe')
plt.plot(range(0,10), wf_DXB_PEC_c, 'm',label='Dubai - Beijing - Tianjin')
plt.ylabel('Fuel mass [kg]')
plt.xlabel('Flight stage')
plt.xticks(range(0,10),['Mfuel', 'Warmup and Take Off', 'Climb', 'Cruise', 'Loiter', 'Attempt to Land', 'Climb', 'Cruise', 'Landing', 'Final Landing'])
plt.grid(axis='y')
plt.legend()
plt.show()
