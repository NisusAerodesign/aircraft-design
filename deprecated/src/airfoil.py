#%% Library
from pathlib import Path
from typing import List, Tuple

import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import trapz
from scipy.interpolate import interp1d


#%% functions
def airfoil_points(airfoil_path: Path) -> float:

    x, y = np.loadtxt(airfoil_path, skiprows=1, unpack=True)
    org = list(x).index(0)
    fsup = interp1d(x[org:], y[org:])
    finf = interp1d(x[: org + 1], y[: org + 1])
    return fsup, finf


def airfoil_area(
    airfoil_path: Path,
    chord: float = 1.0,
    initial_point: float = 0.0,
    final_point: float = 1.0,
) -> tuple:

    fsup, finf = airfoil_points(airfoil_path)

    x = np.linspace(initial_point, final_point)
    ysup = fsup(x)
    yinf = finf(x)

    area = trapz(chord * yinf, chord * x) - trapz(chord * ysup, chord * x)
    k = abs(area) / (chord**2)

    return abs(area), k


def wing_volume(
    wingarea: float, mean_chord: float, k: float, Lambda: float = 0.5
) -> float:

    root_chord = (
        mean_chord * (1 + Lambda) / (2 / 3 * (1 + Lambda + Lambda**2))
    )
    tip_chord = Lambda * root_chord
    volume = k * wingarea * mean_chord

    print(f'Voluem da asa\t: {volume} m³')
    print(f'Corda na raiz\t: {root_chord} m')
    print(f'Corda na ponta\t: {tip_chord} m')
    return abs(volume)


#%% Import data
def load_xfoil_data(Data: Path):

    alpha, Cl, Cd, _, Cm, *_ = np.loadtxt(Data, skiprows=11, unpack=True)

    return alpha, Cl, Cd, Cm


# %%
def plot_areas(airfoil: Path, airfoil_name, colour, ax, xatk=0.1, xfug=0.7):
    fs, fi = airfoil_points(airfoil)

    x = np.linspace(0, 1, 1_000)
    xarea = np.linspace(xatk, xfug, 1_000)

    Atot, _ = airfoil_area(airfoil, initial_point=0, final_point=1)
    Aliq, _ = airfoil_area(airfoil, initial_point=xatk, final_point=xfug)
    ax.plot(x, fs(x), f'{colour}--', alpha=0.6)
    ax.plot(x, fi(x), f'{colour}--', alpha=0.6)
    ax.fill_between(
        xarea,
        fs(xarea),
        fi(xarea),
        color=colour,
        alpha=0.3,
        label=f'{airfoil_name}: {round(100*Aliq/Atot, 2)}% = {round(Aliq*10000,2)} cm²',
    )

    ax.set_title(f'{airfoil_name}')
    # ax.legend()
    ax.axis('equal')
    ax.grid()


def plot_airfoil(
    airfoil_path: List[Path],
    airfoil_name: List[str],
    initial_point: float = 0.0,
    final_point: float = 1.0,
    Colors: List[str] = None,
    bbox_to_anchor: Tuple[float] = (0.85, 0.05),
    maxH=0.08,
    proportion=(5, 6),
):
    plt.rcParams['figure.figsize'] = proportion
    fig, axes = plt.subplots(len(airfoil_path), 1)  # , sharex=True)

    for i, ax in enumerate(axes):
        if Colors != None:
            plot_areas(
                airfoil_path[i],
                airfoil_name[i],
                Colors[i],
                ax,
                xatk=initial_point,
                xfug=final_point,
            )
        else:
            plot_areas(
                airfoil_path[i],
                airfoil_name[i],
                'k',
                ax,
                xatk=initial_point,
                xfug=final_point,
            )
        ax.set_xlim([0, 1])
        ax.set_ylim([-maxH, maxH])
        ax.set_xticklabels([])
    axes[-1].set_xticklabels([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
    fig.subplots_adjust(
        left=0.125, bottom=0.1, right=0.9, top=0.9, wspace=0.4, hspace=0.4
    )
    fig.legend(bbox_to_anchor=bbox_to_anchor)

    return fig, axes
