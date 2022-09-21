import matplotlib.pyplot as plt
from src.pre_selection import *

a = aircraft_pre_select(
    first_range=6000.0,
    second_range=300.0,
    LDmax=15.8,
    sfc_cruise=18.2,
    sfc_sea_level=12.0,
)

WSpouso, TWto, TW_cruise = a.__restriction_diagram__(5_000)
WS = np.linspace(10, 200)
cons = np.linspace(0,2)
plt.plot(WS, TWto(WS),'b')
plt.plot(WS, TW_cruise(WS),'r')
plt.plot(WSpouso+0*WS, cons,'k')
plt.show()