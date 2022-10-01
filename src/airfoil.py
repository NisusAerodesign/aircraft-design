#%% Library
import numpy as np
from pathlib import Path
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
