from cProfile import label
import matplotlib.pyplot as plt
from src.pre_selection import *

a = aircraft_pre_select(
    first_range=6000.0,
    second_range=300.0,
    LDmax=15.8,
    sfc_cruise=18.2,
    sfc_sea_level=12.0,
)

WS_stall, WS_land, TW_to, TW_cruise, TW_ceiling = a.__restriction_diagram__(
    5_000, 36
)

WS_vector = np.linspace(10, 60)

plt.plot(WS_stall + WS_vector * 0, np.linspace(0, 2), label='WS stall')
plt.plot(WS_land + WS_vector * 0, np.linspace(0, 2), label='WS land')
plt.plot(WS_vector, TW_to(WS_vector), label='TW takeoff')
plt.plot(WS_vector, TW_cruise(WS_vector), label='TW cruise')
plt.plot(WS_vector, TW_ceiling(WS_vector), label='TW ceiling')
plt.legend()
plt.show()
