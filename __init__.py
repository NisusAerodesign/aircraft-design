from src.airfoil import *
from src.pre_selection_plotter import *

a = aircraft_selection(
    'My airplane',
    first_range=6000.0,
    second_range=300.0,
    LDmax=15.8,
    sfc_cruise=18.2,
    sfc_sea_level=12.0,
    wing_spain=20.7,
    wing_area=49,
)

print(a)

f, ax = a.plot_constraint_diagram(
    700, 900, 2.5, V_stall_kmph=190, imperial_units=True, V_vertical_kmph=30
)
plt.close()

a.thrust_to_weight_ratio = 0.3807
a.wing_load = 3591.0

print(a)

a.computate_geometry(0.5, 20, 5, 1.2, 0.7, 3)
print(a)
"""_summary_

"""