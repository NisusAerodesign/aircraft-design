#%% Librarys
import matplotlib.pyplot as plt
from pathlib import Path

from src.airfoil import *
from src.pre_selection import *

#%% plot areas
airfoil_path = [
    Path() / 'data/SC(2)-0714.dat',
    Path() / 'data/WHITCOMB INTEGRAL.dat',
    Path() / 'data/SC(2)-0614.dat',
    Path() / 'data/KC-135 Winglet.dat',
    Path() / 'data/LOCKHEED-GEORGIA.dat',
]
airfoil_name = [
    'SC(2)-0714',
    'WHITCOMB INTEGRAL',
    'SC(2)-0614',
    'KC-135 Winglet',
    'LOCKHEED-GEORGIA',
]
plot_airfoil(airfoil_path, airfoil_name)

al_a, cl_a, cd_a, ld_a = load_xfoil_data(
    Path() / 'data/LOCKHEED-GEORGIA_CL_CD_42M_RE.txt'
)
al_b, cl_b, cd_b, ld_b = load_xfoil_data(
    Path() / 'data/KC-135 Winglet_CL_CD_42M_RE.txt'
)
al_c, cl_c, cd_c, ld_c = load_xfoil_data(
    Path() / 'data/SC(2)-0714_CL_CD_42M_RE.txt'
)
al_d, cl_d, cd_d, ld_d = load_xfoil_data(
    Path() / 'data/SC(2)-0614_CL_CD_42M_RE.txt'
)
al_e, cl_e, cd_e, ld_e = load_xfoil_data(
    Path() / 'data/WHITCOMB INTEGRAL_CL_CD_42M_RE.txt'
)

plt.plot(al_a, cl_a, 'r', label='LOCKHEED-GEORGIA')
plt.plot(al_b, cl_b, 'g', label='KC-135 Winglet')
plt.plot(al_c, cl_c, 'b', label='SC(2)-0714')
plt.plot(al_d, cl_d, 'c', label='SC(2)-0614')
plt.plot(al_e, cl_e, 'y', label='WHITCOMB INTEGRAL')
plt.grid()
plt.legend()
plt.xlim([0, 30])
plt.ylim([0, 2.75])
plt.ylabel('Cl')
plt.xlabel(r'alpha')
plt.title('Comparação do Cl para Re = 42.000.000')
plt.close()

plt.plot(al_a, ld_a, 'r', label='LOCKHEED-GEORGIA')
plt.plot(al_b, ld_b, 'g', label='KC-135 Winglet')
plt.plot(al_c, ld_c, 'b', label='SC(2)-0714')
plt.plot(al_d, ld_d, 'c', label='SC(2)-0614')
plt.plot(al_e, ld_e, 'y', label='WHITCOMB INTEGRAL')
plt.grid()
plt.legend()
plt.xlim([0, 30])
plt.ylim([0, 185])
plt.ylabel('L/D')
plt.xlabel(r'alpha')
plt.title('Comparação do L/D para Re = 42.000.000')
plt.show()
#%% test wing volume
PATH_DATA = Path() / 'data'
airfoil = list(PATH_DATA.glob('*.dat'))
airfoil = sorted(airfoil, key=lambda x: x.name)
print([i.name for i in airfoil])
for air in airfoil[:-1]:
    area, k = airfoil_area(
        air, chord=2.458, initial_point=0.1, final_point=0.7
    )
    print(f'___{air.name}___')
    print(f'Area\t: {area} m²')
    print(f'k\t: {k}')
    print(f'Volume\t: {area*20} m³')
    volume = wing_volume(wingarea=49.16, mean_chord=2.458, k=k)
    print('\n')
# %%
