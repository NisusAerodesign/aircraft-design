from select import KQ_FILTER_AIO
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
        wing_spain: float,  # m
        wing_area: float,  # m2
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
        self._s_range = second_range * 1000   # m

        self._LDmax = LDmax   # dimensionless

        self._sfc_cruise = sfc_cruise * 1e-6   # kg/(N.s)
        self._sfc_sea_level = sfc_sea_level * 1e-6   # kg/(N.s)

        self._b = wing_spain   # m
        self._S = wing_area   # m2

        self._payload = payload   # kg
        self.crew = crew
        self._person_avg = person_avg   # kg

        self._loiter_time = loiter_time * 60   # seg

        self._h_cruise = h_cruise   # m
        self._h_celling = h_celling   # m

        self._mach = Mach

        self._class_airplane = class_airplane

        # === Need to computate ===
        self._sound_speed = 0   # m/s
        self._v_cruise = 0   # m/s
        self._W0 = 0
        self._We = 0
        self._Wf = 0
        self._weight_fraction = 0

        self.__param_computate__()

    # ======< parameter treatment: Getters >======
    @property
    def first_range(self) -> float:
        return self._f_range / 1000   # km

    @property
    def second_range(self) -> float:
        return self.second_range / 1000   # km

    @property
    def LD_max(self) -> float:
        return self._LDmax   # dimensionless

    @property
    def sfc_cruise(self) -> float:
        return self._sfc_cruise * 1e6   # g/(kN.s)

    @property
    def sfc_sea_level(self) -> float:
        return self._sfc_sea_level * 1e6   # g/(kN.s)

    @property
    def wing_span(self) -> float:
        return self._b   # m

    @property
    def wing_area(self) -> float:
        return self._S   # m2

    @property
    def payload(self) -> float:
        return self._payload   # kg

    @property
    def crew(self) -> float:
        return self.crew

    @property
    def person_avg_weigh(self) -> float:
        return self._person_avg   # kg

    @property
    def loiter_time(self) -> float:
        return self._loiter_time / 60   # min

    @property
    def h_cruise(self) -> float:
        return self._h_cruise  # m

    @property
    def h_celling(self) -> float:
        return self._h_celling   # m

    @property
    def Mach(self) -> float:
        return self._mach

    @property
    def class_airplane(self) -> float:
        return self._class_airplane
    
    @property
    def sound_speed(self) -> float:
        return self._sound_speed   # m/s

    @property
    def v_cruise(self) -> float:
        return self._v_cruise   # m/s

    @property
    def M_tow(self) -> float:
        return self._W0

    @property
    def empty_weigh(self) -> float:
        return self._We

    @property
    def fuel_weigh(self) -> float:
        return self._Wf

    @property
    def weight_fraction(self) -> float:
        return self._weight_fraction

    # ======< parameter treatment: Setters >======
    @first_range.setter
    def first_range(self, kilometers: float):
        self._f_range = kilometers * 1000   # km
        self.__param_computate__()

    @second_range.setter
    def second_range(self, kilometers: float):
        self.second_range = kilometers * 1000   # km
        self.__param_computate__()

    @LD_max.setter
    def LD_max(self, Value: float):
        self._LDmax = Value   # dimensionless
        self.__param_computate__()

    @sfc_cruise.setter
    def sfc_cruise(self, g_per_kN_s: float):
        self._sfc_cruise = g_per_kN_s * 1e-6   # kg/(N.s)
        self.__param_computate__()

    @sfc_sea_level.setter
    def sfc_sea_level(self, g_per_kN_s: float):
        self._sfc_sea_level = g_per_kN_s * 1e6   # kg/(N.s)
        self.__param_computate__()

    @wing_span.setter
    def wing_span(self, meters: float):
        self._b = meters   # m
        self.__param_computate__()

    @wing_area.setter
    def wing_area(self, meters2: float):
        self._S = meters2   # m2
        self.__param_computate__()

    @payload.setter
    def payload(self, kilogram: float):
        self._payload = kilogram   # kg
        self.__param_computate__()

    @crew.setter
    def crew(self, n_crew: float):
        self.crew = n_crew
        self.__param_computate__()

    @person_avg_weigh.setter
    def person_avg_weigh(self, kilogram: float):
        self._person_avg = kilogram   # kg
        self.__param_computate__()

    @loiter_time.setter
    def loiter_time(self, minutes: float):
        self._loiter_time = minutes * 60   # min
        self.__param_computate__()

    @h_cruise.setter
    def h_cruise(self, meters: float):
        self._h_cruise = meters  # m
        self.__param_computate__()

    @h_celling.setter
    def h_celling(self, meters: float):
        self._h_celling = meters   # m
        self.__param_computate__()

    @Mach.setter
    def Mach(self, mach: float):
        self._mach = mach
        self.__param_computate__()

    @class_airplane.setter
    def class_airplane(self, airplane_class:str):
        self._class_airplane = airplane_class
        self.__param_computate__()

    # ======< Functions >======
    
    
    
    def __param_computate__(self):
        ...
