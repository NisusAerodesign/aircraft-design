#%% Library
from pathlib import Path

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
) -> float:

    fsup, finf = airfoil_points(airfoil_path)

    x = np.linspace(initial_point, final_point)
    ysup = fsup(x)
    yinf = finf(x)

    area = trapz(chord * yinf, chord * x) - trapz(chord * ysup, chord * x)

    return abs(area)


#%% Import data
def load_xfoil_data(Data: Path):

    alpha, Cl, Cd, *_ = np.loadtxt(Data, skiprows=11, unpack=True)
    LD = np.array([cl / cd for cl, cd in zip(Cl, Cd)])

    return alpha, Cl, Cd, LD
