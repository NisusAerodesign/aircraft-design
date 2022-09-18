import matplotlib.pyplot as plt
from src.pre_selection import *

a = aircraft_pre_select(
    first_range=5542.0,
    second_range=19.0,
    LDmax=15.8,
    sfc_cruise=18.2,
    sfc_sea_level=12.0,
)

WSpouso, TWto, TW_cruise = a.__restriction_diagram__(10_000)
WS = np.linspace(10, 200)
cons = np.linspace(0,10)
plt.plot(WS, TWto(WS),'b')
plt.plot(WS, TW_cruise(WS),'r')
plt.plot(WSpouso+0*WS, cons,'k')
plt.show()