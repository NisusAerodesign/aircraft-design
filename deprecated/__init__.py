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

lam_esc = np.arccos(0.7 / 0.8) * 180 / np.pi

print(f'Alpha = {lam_esc : .2f}°')
f, ax, al, alc4 = a.wing_super_view(lam_esc, 'l')
plt.close()
print(f'Λ_LE = {al:.2f}°, Λ_C/4 = {alc4:.2f}°')

mach = lambda M, alpha: M * np.cos(alpha * np.pi / 180)
lambda_LE = np.linspace(0, 90)
plt.plot(lambda_LE, mach(0.8, lambda_LE))
plt.plot([al], [mach(0.8, al)], 'x', label='configuração escolhida')
plt.plot([30], [mach(0.8, 30)], 'x', label='configuração 30°')
plt.plot([20], [mach(0.8, 20)], 'x', label='configuração 20°')
plt.xlabel('graus')
plt.ylabel('Mach aparente')
plt.title('Comportamento do Mach aparente para Mach de referência de 0,8')
plt.grid()
plt.legend()
plt.show()
"""_summary_

"""
