import matplotlib.pyplot as plt
from src.pre_selection import *
from src.airfoil import *

airfoil = Path() / 'data/LOCKHEED-GEORGIA.dat'


def plot_areas(airfoil: Path, airfoil_name, colour, xatk=0.1, xfug=0.7):
    fs, fi = airfoil_points(airfoil)
    print(
        f'Área do aerofólio SC(2)-0714 = {round(airfoil_area(airfoil), 5)} m²'
    )

    x = np.linspace(0, 1, 1_000)
    xarea = np.linspace(xatk, xfug, 1_000)

    Atot = airfoil_area(airfoil, initial_point=0, final_point=1)
    Aliq = airfoil_area(airfoil, initial_point=xatk, final_point=xfug)
    plt.plot(x, fs(x), f'{colour}--')
    plt.plot(x, fi(x), f'{colour}--')
    plt.fill_between(
        xarea,
        fs(xarea),
        fi(xarea),
        color=colour,
        alpha=0.3,
        label=f'{airfoil_name}: {round(100*Aliq/Atot, 2)}% de área ocupada sendo área liquida de {round(Aliq*10000,2)} cm²',
    )


plot_areas(Path() / 'data/LOCKHEED-GEORGIA.dat', 'LOCKHEED-GEORGIA', 'r')
plot_areas(Path() / 'data/KC-135 Winglet.dat', 'KC-135 Winglet', 'g')
plot_areas(Path() / 'data/SC(2)-0714.dat', 'SC(2)-0714', 'b')

plt.legend()
plt.axis('equal')
plt.grid()
plt.title(
    f'comparação dos aerofólios'
)
plt.show()
