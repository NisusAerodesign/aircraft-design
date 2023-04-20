import pickle
from pathlib import Path

from numpy import loadtxt, array
from aircraft_design import run_xfoil

"""
WIP - TUDO AINDA
"""
__AIRFOIL_CLASS_VERSION__ = '0.0.0'

class __BaseAirfoil__:
    def __init__(self, name: str, x_points: array, y_points: array, delta_alpha:float = 0.01, delta_Re:float=1000):
        assert (
            x_points.shape == y_points.shape,
            'x_points do not match with y_points!',
        )
        assert (
            len(x_points.shape) == 1,
            'X or y points have a shape different from (n,).',
        )

        self.x_points = x_points
        self.y_points = y_points
        self.name = name
        self.__delta_alpha = delta_alpha
        self.__delta_Re = delta_Re

        self.__simulation_tree = {'version': __AIRFOIL_CLASS_VERSION__, 'Re': {}}

class Airfoil(__BaseAirfoil__):
    
    @property
    def version(self)->str:
        return self.__simulation_tree['version']

    def __found_re(self, Re:float):
        if Re in self.__simulation_tree['Re'].keys():
            return self.__simulation_tree['Re'][Re]

        Re_list = self.__simulation_tree['Re'].keys()
        tam_list = len(Re_list)
        for i, Re_val in (Re_list):
            if Re < Re_val:
                if i == 0:
                    return None
                elif i == (tam_list-1):
                    return None
                elif Re_val - Re_list[i-1] <= self.__delta_Re:
                    return (Re_list[i], Re_list[i-1])
        return None

    def simulate(self, Re:float)->array:
        assert(self.version == __AIRFOIL_CLASS_VERSION__, "Versions don't match!")
    
        if value := self.__found_re(Re) != None:
            ...