import matplotlib.pyplot as plt

from src.airfoil import *
from src.pre_selection import *

def plot_areas(airfoil: Path, airfoil_name, colour, ax, xatk=0.1, xfug=0.7):
    fs, fi = airfoil_points(airfoil)
    print(
        f'Área do aerofólio {airfoil_name} = {round(airfoil_area(airfoil), 5)} m²'
    )

    x = np.linspace(0, 1, 1_000)
    xarea = np.linspace(xatk, xfug, 1_000)

    Atot = airfoil_area(airfoil, initial_point=0, final_point=1)
    Aliq = airfoil_area(airfoil, initial_point=xatk, final_point=xfug)
    ax.plot(
        x, fs(x), f'{colour}--', alpha=0.6)
    ax.plot(x, fi(x), f'{colour}--', alpha=0.6)
    ax.fill_between(
        xarea,
        fs(xarea),
        fi(xarea),
        color=colour,
        alpha=0.3,
        label=f'{round(100*Aliq/Atot, 2)}% = {round(Aliq*10000,2)} cm²',
    )
    ax.set_title(f'{airfoil_name}')
    ax.legend()
    ax.axis('equal')
    #ax.sharex(ax3)
    ax.grid()

fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(5, 1, sharex=True)
plot_areas(Path() / 'data/SC(2)-0714.dat', 'SC(2)-0714', 'b', ax3)
plot_areas(Path() / 'data/WHITCOMB INTEGRAL.dat', 'WHITCOMB INTEGRAL', 'y', ax5)
plot_areas(Path() / 'data/SC(2)-0614.dat', 'SC(2)-0614', 'c', ax4)
plot_areas(Path() / 'data/KC-135 Winglet.dat', 'KC-135 Winglet', 'g', ax2)
plot_areas(Path() / 'data/LOCKHEED-GEORGIA.dat', 'LOCKHEED-GEORGIA', 'r', ax1)
plt.close()

al_a, cl_a, cd_a, ld_a = load_xfoil_data(Path()/'data/LOCKHEED-GEORGIA_CL_CD_42M_RE.txt')
al_b, cl_b, cd_b, ld_b = load_xfoil_data(Path()/'data/KC-135 Winglet_CL_CD_42M_RE.txt')
al_c, cl_c, cd_c, ld_c = load_xfoil_data(Path()/'data/SC(2)-0714_CL_CD_42M_RE.txt')
al_d, cl_d, cd_d, ld_d = load_xfoil_data(Path()/'data/SC(2)-0614_CL_CD_42M_RE.txt')
al_e, cl_e, cd_e, ld_e = load_xfoil_data(Path()/'data/WHITCOMB INTEGRAL_CL_CD_42M_RE.txt')

plt.plot(al_a, cl_a,'r', label = 'LOCKHEED-GEORGIA')
plt.plot(al_b, cl_b,'g', label = 'KC-135 Winglet')
plt.plot(al_c, cl_c,'b', label = 'SC(2)-0714')
plt.plot(al_d, cl_d,'c', label = 'SC(2)-0614')
plt.plot(al_e, cl_e,'y', label = 'WHITCOMB INTEGRAL')
plt.grid()
plt.legend()
plt.xlim([0,30])
plt.ylim([0,2.75])
plt.ylabel('Cl')
plt.xlabel(r'alpha')
plt.title('Comparação do Cl para Re = 42.000.000')
plt.close()

plt.plot(al_a, ld_a,'r', label = 'LOCKHEED-GEORGIA')
plt.plot(al_b, ld_b,'g', label = 'KC-135 Winglet')
plt.plot(al_c, ld_c,'b', label = 'SC(2)-0714')
plt.plot(al_d, ld_d,'c', label = 'SC(2)-0614')
plt.plot(al_e, ld_e,'y', label = 'WHITCOMB INTEGRAL')
plt.grid()
plt.legend()
plt.xlim([0,30])
plt.ylim([0,185])
plt.ylabel('L/D')
plt.xlabel(r'alpha')
plt.title('Comparação do L/D para Re = 42.000.000')
plt.show()