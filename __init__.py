from cProfile import label
from turtle import color
import matplotlib.pyplot as plt
from src.pre_selection import *

a = aircraft_pre_select(
    first_range=6000.0,
    second_range=300.0,
    LDmax=15.8,
    sfc_cruise=18.2,
    sfc_sea_level=12.0,
    b=20.7,
    S=47.3,
)

WS_stall, WS_land, TW_to, TW_cruise, TW_ceiling = a.__restriction_diagram__(5_000)
ptos = 1000

# WS_vector = np.linspace(10, 694.223,ptos)

# WS_fill = np.linspace(0,WS_land,ptos)
# plt.fill_between(WS_fill, TW_cruise(WS_fill), 1, alpha=0.3, label='Região de interesse')

# plt.plot(WS_land + WS_vector * 0, np.linspace(0, 2, ptos), 'r',label='Land Condition')

# plt.plot(WS_vector, TW_to(WS_vector),'g', label='TW takeoff')

# plt.plot(WS_vector, TW_cruise(WS_vector),'b', label='TW cruise')

# plt.plot(WS_vector, TW_ceiling(WS_vector),'y', label='TW ceiling')

# plt.plot(WS_stall + WS_vector * 0, np.linspace(0, 2, ptos),'orange', label='WS stall')

# plt.plot([56.926],[0.3392], 'ko', label='Ponto ótimo')
# plt.xlim(10, 750)
# plt.ylim(0, 1)
# plt.legend()
# plt.grid(linestyle='dotted')
# plt.xlabel(r'W/S {lb/ft²}')
# plt.ylabel('T/W0')
# plt.title('Diagrama de restrição')
# plt.show()

WS_fill = np.linspace(0,WS_land,ptos)
plt.fill_between(WS_fill, TW_cruise(WS_fill), 1, alpha=0.3, label='Região de interesse')
plt.plot([(50.1845 + 56.926)/2], [(2*33.60)/(18*9.80665)], 'kx', label='Configuração adotada')

WS_vector = np.linspace(51.9060, 56.926)
plt.plot(WS_vector, (2*32.57)/(18*9.80665) + WS_vector*0, label='HTF735')

WS_vector = np.linspace(54.2069, 56.926)
plt.plot(WS_vector, (2*31.30)/(18*9.80665) + WS_vector*0, label='HTF7500E')

WS_vector = np.linspace(49.6893, 56.926)
plt.plot(WS_vector, (2*33.91)/(18*9.80665) + WS_vector*0, label='HTF7250G')

WS_vector = np.linspace(50.1845, 56.926)
plt.plot(WS_vector, (2*33.60)/(18*9.80665) + WS_vector*0, label='HTF7700L')

WS_vector = np.linspace(37.5, 57.5)
plt.plot(WS_vector, (2*25.67)/(18*9.80665) + WS_vector*0,'--', label='PW306C')

WS_vector = np.linspace(37.5, 57.5)
plt.plot(WS_vector, (2*26.28)/(18*9.80665) + WS_vector*0,'--', label='PW306D')

WS_vector = np.linspace(37.5, 57.5)
plt.plot(WS_vector, (2*25.60)/(18*9.80665) + WS_vector*0,'--', label='PW306D1')

WS_vector = np.linspace(37.5, 57.5)
plt.plot(WS_vector, (2*28.49)/(18*9.80665) + WS_vector*0,'--', label='PW307A')

WS_vector = np.linspace(55.3893, 56.926)
plt.plot(WS_vector, (2*30.69)/(18*9.80665) + WS_vector*0, label='PW308A')

WS_vector = np.linspace(54.5116, 56.926)
plt.plot(WS_vector, (2*31.14)/(18*9.80665) + WS_vector*0, label='PW308C')

WS_vector = np.linspace(54.1690, 56.926)
plt.plot(WS_vector, (2*31.32)/(18*9.80665) + WS_vector*0, label='AE 3007 C')

WS_vector = np.linspace(39.2882, 56.926)
plt.plot(WS_vector, (2*42.30)/(18*9.80665) + WS_vector*0, label='AE 3007 A')

WS_vector = np.linspace(43.6015, 56.926)
plt.plot(WS_vector, (2*38.32)/(18*9.80665) + WS_vector*0, label='CF34-3B')


plt.xlim(37,58)
plt.ylim(0.28, 0.5)
plt.legend()
plt.grid(linestyle='dotted')
plt.xlabel(r'W/S {lb/ft²}')
plt.ylabel('T/W0')
plt.title('Comportamento dos motores selecionados no diagrama de restrição')
plt.show()

