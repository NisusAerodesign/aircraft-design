from typing import Any, List, Tuple

import numpy as np
from scipy.optimize import fsolve

class aircraft_selection:
    def __init__(
        self,
        first_range: float,  # km
        second_range: float,  # km
        LDmax: float,  #
        sfc_cruise: float,  # g/(kN.S)
        sfc_sea_level: float,  # g/(kN.S)
        b: float,  # m
        S: float,  # m2
        payload: float = 1500.0,  # Kg
        crew: float = 3.0,  # Number of people
        person_avg: float = 95.0,  # Kg
        loiter_time: float = 20.0,  # min
        h_cruise: float = 11_000,  # m
        h_celling: float = 15_000,  # m
        Mach: float = 0.8,  #
        class_airplane='JetTransport',
    ) -> None:

        self._f_range = first_range * 1000  # m
        self._s_range = second_range * 1000 # m

        self.LDmax = LDmax   # dimensionless

        self._sfc_cruise = sfc_cruise * 1e-6 # kg/(N.s)
        self._sfc_sea_level = sfc_sea_level * 1e-6 # kg/(N.s)

        self._b = b # m
        self._S = S # m2

        self._payload = payload # kg
        self.crew = crew
        self._person_avg = person_avg # kg

        self._loiter_time = loiter_time * 60   # seg

        self._h_cruise = h_cruise # m
        self._h_celling = h_celling # m

        self._mach = Mach
        self._sound_speed = 340 # m/s
        self._v_cruise = self._mach * self._sound_speed   # m/s

        self.class_airplane = class_airplane
    
    # ======< parameter treatment >======
    @property
    def v():
        ...