from typing import Any, List, Tuple

import numpy as np
from scipy.optimize import fsolve


class unit:
    lb: float = 1 / 0.45359237   # lb/kg
    ft: float = 1 / 0.30480000   # ft/m
    lbf: float = 1 / 4.44822162   # lbf/N
    hp: float = 1 / 745.69987200   # hp/W
    slug_per_ft3: float = 1 / 515.2381961366   # (slug/ft3)/(kg/m3)

    kg: float = 0.45359237   # kg/lb
    m: float = 0.30480000   # m/ft
    N: float = 4.44822162   # N/lbf
    W: float = 745.69987200   # W/hp
    kg_per_m3: float = 515.2381961366   # (kg/m3)/(slug/ft3)
    g: float = 9.806650010448807   # m/s


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
        self._crew = crew
        self._person_avg = person_avg   # kg

        self._loiter_time = loiter_time * 60   # seg

        self._h_cruise = h_cruise   # m
        self._h_celling = h_celling   # m

        self._mach = Mach

        self._class_airplane = class_airplane

        self.__has_modified__ = True

        # === Need to computate ===
        self._sound_speed = 0   # m/s
        self._v_cruise = 0   # m/s
        self._W0 = 0
        self._We = 0
        self._Wf = 0
        self._weight_fraction = 0

        self._S_wetted = 0   # m2

        # === Optional PARAMS ===
        self._T_W0 = None
        self._W0_S = None

    # ======< parameter treatment: Getters >======
    @property
    def first_range(self) -> float:
        self.__param_computate__()
        return self._f_range / 1000   # km

    @property
    def second_range(self) -> float:
        self.__param_computate__()
        return self.second_range / 1000   # km

    @property
    def LD_max(self) -> float:
        self.__param_computate__()
        return self._LDmax   # dimensionless

    @property
    def sfc_cruise(self) -> float:
        self.__param_computate__()
        return self._sfc_cruise * 1e6   # g/(kN.s)

    @property
    def sfc_sea_level(self) -> float:
        self.__param_computate__()
        return self._sfc_sea_level * 1e6   # g/(kN.s)

    @property
    def wing_span(self) -> float:
        self.__param_computate__()
        return self._b   # m

    @property
    def wing_area(self) -> float:
        self.__param_computate__()
        return self._S   # m2

    @property
    def payload(self) -> float:
        self.__param_computate__()
        return self._payload   # kg

    @property
    def crew(self) -> float:
        self.__param_computate__()
        return self._crew

    @property
    def person_avg_weigh(self) -> float:
        self.__param_computate__()
        return self._person_avg   # kg

    @property
    def loiter_time(self) -> float:
        self.__param_computate__()
        return self._loiter_time / 60   # min

    @property
    def h_cruise(self) -> float:
        self.__param_computate__()
        return self._h_cruise  # m

    @property
    def h_celling(self) -> float:
        self.__param_computate__()
        return self._h_celling   # m

    @property
    def Mach(self) -> float:
        self.__param_computate__()
        return self._mach

    @property
    def class_airplane(self) -> float:
        self.__param_computate__()
        return self._class_airplane

    @property
    def sound_speed(self) -> float:
        self.__param_computate__()
        return self._sound_speed   # m/s

    @property
    def v_cruise(self) -> float:
        self.__param_computate__()
        return self._v_cruise   # m/s

    @property
    def M_tow(self) -> float:
        self.__param_computate__()
        return self._W0

    @property
    def empty_weigh(self) -> float:
        self.__param_computate__()
        return self._We

    @property
    def fuel_weigh(self) -> float:
        self.__param_computate__()
        return self._Wf

    @property
    def weight_fraction(self) -> float:
        self.__param_computate__()
        return self._weight_fraction

    @property
    def wing_load(self) -> float:
        self.__param_computate__()
        assert self._W0_S, "ERROR: you didn't set a wing load value!"
        return self._W0_S

    @property
    def thrust_to_weight_ratio(self) -> float:
        self.__param_computate__()
        assert self._T_W0, "ERROR: you didn't set a thrust to weight ratio!"
        return self._T_W0

    # ======< parameter treatment: Setters >======
    @first_range.setter
    def first_range(self, kilometers: float):
        self._f_range = kilometers * 1000   # km
        self.__has_modified__ = True

    @second_range.setter
    def second_range(self, kilometers: float):
        self.second_range = kilometers * 1000   # km
        self.__has_modified__ = True

    @LD_max.setter
    def LD_max(self, Value: float):
        self._LDmax = Value   # dimensionless
        self.__has_modified__ = True

    @sfc_cruise.setter
    def sfc_cruise(self, g_per_kN_s: float):
        self._sfc_cruise = g_per_kN_s * 1e-6   # kg/(N.s)
        self.__has_modified__ = True

    @sfc_sea_level.setter
    def sfc_sea_level(self, g_per_kN_s: float):
        self._sfc_sea_level = g_per_kN_s * 1e6   # kg/(N.s)
        self.__has_modified__ = True

    @wing_span.setter
    def wing_span(self, meters: float):
        self._b = meters   # m
        self.__has_modified__ = True

    @wing_area.setter
    def wing_area(self, meters2: float):
        self._S = meters2   # m2
        self.__has_modified__ = True

    @payload.setter
    def payload(self, kilogram: float):
        self._payload = kilogram   # kg
        self.__has_modified__ = True

    @crew.setter
    def crew(self, n_crew: float):
        self._crew = n_crew
        self.__has_modified__ = True

    @person_avg_weigh.setter
    def person_avg_weigh(self, kilogram: float):
        self._person_avg = kilogram   # kg
        self.__has_modified__ = True

    @loiter_time.setter
    def loiter_time(self, minutes: float):
        self._loiter_time = minutes * 60   # min
        self.__has_modified__ = True

    @h_cruise.setter
    def h_cruise(self, meters: float):
        self._h_cruise = meters  # m
        self.__has_modified__ = True

    @h_celling.setter
    def h_celling(self, meters: float):
        self._h_celling = meters   # m
        self.__has_modified__ = True

    @Mach.setter
    def Mach(self, mach: float):
        self._mach = mach
        self.__has_modified__ = True

    @class_airplane.setter
    def class_airplane(self, airplane_class: str):
        self._class_airplane = airplane_class
        self.__has_modified__ = True

    @wing_load.setter
    def wing_load(self, W0_S: float):
        self._W0_S = W0_S
        self.__has_modified__ = True

    @thrust_to_weight_ratio.setter
    def thrust_to_weight_ratio(self, T_W0: float):
        self._T_W0 = T_W0
        self.__has_modified__ = True

    # ======< Static method Functions >======
    @staticmethod
    def __rho_per_h__(
        h_meters: float,  # m
        T0=288.15,  # °K
        rho0: float = 1.225,  # kg/m^3
        g: float = 9.80665,  # m/s^2
        Lambda: float = -0.0065,  # °K/m
        R: float = 287.15,  # J/(kg °K)
    ):
        T = T0 + Lambda * h_meters   # °K
        rho = rho0 * (T / T0) ** (-g / (Lambda * R) - 1)
        return rho

    @staticmethod
    def __T_per_h__(
        h_meters: float,  # m
        T0=288.15,  # °K
        Lambda: float = -0.0065,  # °K/m
    ):
        return T0 + Lambda * h_meters

    @staticmethod
    def __sound_speed_calculator__(
        T: float,  # °K
        gamma=1.4,  # Dimensionless
        R=287.15,  # J/(kg °K)
    ):
        return (gamma * R * T) ** 0.5

    @staticmethod
    def Raymer_We(category: str) -> callable:
        coefs = {
            'Sail': [0.86, -0.05],
            'Sailpowerd': [0.91, -0.05],
            'HBmetal': [1.19, -0.09],
            'HBcomp': [0.99, -0.09],
            'GAsingle': [2.36, -0.18],
            'GAtwin': [1.51, -0.10],
            'Agricultural': [0.74, -0.03],
            '2TurboP': [0.96, -0.05],
            'FlyBoat': [1.09, -0.05],
            'JetTrainer': [1.59, -0.10],
            'JetFighter': [2.34, -0.13],
            'MilitaryCargo': [0.93, -0.07],
            'JetTransport': [1.02, -0.06],
        }
        A, C = coefs[category]
        wewo = lambda wo: A * ((wo * unit.lb) ** (C))
        return wewo

    @staticmethod
    def Raymer_Wf(fase: str) -> any:
        coef = {
            'WuTo': 0.97,
            'Climb': 0.985,
            'Climb-Ac': lambda M: (1.0065 - 0.0325 * M)
            if M < 1
            else (0.991 - 0.007 * M - 0.01 * M**2),
            'Landing': 0.995,
            'Cruise': lambda R, SFC, LD, V: np.exp(
                -R * SFC * unit.g / (V * LD)
            ),
            'Loiter': lambda E, SFC, LD: np.exp(-E * SFC * unit.g / LD),
        }
        wf = coef[fase]
        return wf

    # ======< Calculation >======
    def __SI_mass_props__(
        self,
        first_step: float = 20_000.0,
    ) -> Tuple[float, float, float, np.array]:
        # first_step *= unit.lb

        time_second_range = self._s_range / self._v_cruise   # s

        We = self.Raymer_We(self._class_airplane)
        ##  W1/W0 -> Warmup and Take Off
        W1W0 = self.Raymer_Wf('WuTo')

        ## W2/W1 -> Climb
        W2W1 = self.Raymer_Wf('Climb-Ac')
        W2W1 = W2W1(self._mach)

        ## W3/W2 -> Cruise
        W3W2f = self.Raymer_Wf('Cruise')
        W3W2 = lambda range: W3W2f(
            range, self._sfc_cruise, self._LDmax * 0.866, self._v_cruise
        )

        ## W4/W3 -> Loiter 1
        W4W3f = self.Raymer_Wf('Loiter')
        W4W3 = lambda time: W4W3f(time, self._sfc_sea_level, self._LDmax)

        ## W5/W4 -> Tentativa de Pouso
        W5W4 = self.Raymer_Wf('Landing')

        ## W6/W5 -> Climb
        W6W5 = W2W1

        ## W7/W6 -> Cruseiro 2 - tempo
        W7W6 = self.Raymer_Wf('Loiter')
        W7W6 = W7W6(time_second_range, self._sfc_cruise, self._LDmax * 0.866)

        ## W8/W7 -> Loiter
        W8W7 = W4W3

        ## W9/W8 -> Landing
        W9W8 = self.Raymer_Wf('Landing')

        ## Fracao de Combustivel
        WfW0 = lambda range, loiter_time: 1.06 * (
            1
            - W1W0
            * W2W1
            * W3W2(range)
            * W4W3(loiter_time)
            * W5W4
            * W6W5
            * W7W6
            * W8W7(loiter_time)
            * W9W8
        )

        ## Carga Paga
        Wpl = self._payload

        ## Tripulacao
        Wcrew = self._crew * self._person_avg

        ## Calculo dos Pesos
        W0 = fsolve(
            lambda W0: W0
            * (1 - WfW0(self._f_range, self._loiter_time) - We(W0))
            - Wpl
            - Wcrew,
            first_step,
        )
        W0 = W0[0]

        return (
            W0,  # * unit.kg,
            WfW0(self._f_range, self._loiter_time) * W0,  # * unit.kg,
            We(W0) * W0,  # * unit.kg,
            np.array(
                [
                    W1W0,
                    W2W1,
                    W3W2(self._f_range),
                    W4W3(self._loiter_time),
                    W5W4,
                    W6W5,
                    W7W6,
                    W8W7(self._loiter_time),
                    W9W8,
                ]
            ),
        )

    # ======< Reload Function >======
    def __param_computate__(self):

        if self.__has_modified__:
            # Update sound speed
            self._sound_speed = self.__sound_speed_calculator__(
                self.__T_per_h__(self._h_cruise)
            )

            # S_wett
            A_wetted = (self._LDmax / 15.5) ** 2
            self._S_wetted = self._b**2 / A_wetted

            # Update v cruise
            self._v_cruise = self._mach * self._sound_speed

            # Update mass props
            W0, Wf, We, n = self.__SI_mass_props__()
            self._W0, self._Wf, self._We, self._weight_fraction = W0, Wf, We, n

            # Veriry if exists W0/S and T/W0 to make better estimation
            if self._T_W0 != None and self._W0_S != None:
                ...
            # Stop correction loop
            self.__has_modified__ = False
        else:
            pass

    def restriction_diagram(
        self,
        Range_takeoff: float,
        Range_land: float,
        CL_max: float,  # depends if it has flaps
        rho_sea: float = 1.225,  # kg/m^3
        sigma_land: float = 0.9,  # ratio of rho_air/rho_sea_level
        sigma_takeoff: float = 0.9,  # ratio of rho_air/rho_sea_level
        TcruiseT0: float = 0.3,  # avg Tcruise/T0
        V_stall_kmph: float = 113,  # FAR 23 km/h -> just for comercial planes
        V_vertical_kmph: float = 2,  # km/h
        CL_stall_per_CL_max: float = 1,  # CL_max_stall/CL_max to fix CL in stall
        CL_land_per_CL_max: float = 1,  # CL_max_land/CL_max to fix land CL
        CL_takeoff_per_CL_max: float = 1,  # CL_max_takeoff/CL_max to fix takeoff CL
    ):
        self.__param_computate__()

        v_vertical = V_vertical_kmph / 3.6
        v_stall = V_stall_kmph / 3.6

        rho_sea_level = rho_sea   # kg/m^3
        rho_cruise = rho_sea * (
            self.__rho_per_h__(self._h_cruise) / self.__rho_per_h__(0)
        )

        CD_min = 0.003 * self._S_wetted / self._S   # CL_max/self.LDmax

        # V_stall condition
        CL_max_stall = CL_max * CL_stall_per_CL_max
        WstallW0 = np.prod(self._weight_fraction[:2])
        WS_stall = (
            0.5 * rho_sea_level * (v_stall**2) * CL_max_stall * WstallW0
        )   # <= que este valor

        # land distance condition
        CL_max_land = CL_max * CL_land_per_CL_max
        WlW0 = np.prod(self._weight_fraction[:4])

        WS_land = (
            unit.N
            * (unit.ft**3)  # = (N/lbf)*(ft^3/m^3)
            * (2 / 3)
            * Range_land
            * sigma_land
            * CL_max_land
            / (79.4 * WlW0)
        )   # <= este valor

        # takeoff distance condition
        CL_max_to = CL_max * CL_takeoff_per_CL_max
        WtoW0 = self._weight_fraction[0]

        def TW_to(WS):   # >= este valor, WS [N/m^2]
            WSc = WS * WtoW0 * (unit.lbf / (unit.ft**2))
            A = 20 * WSc
            B = sigma_takeoff * CL_max_to
            C = Range_takeoff * unit.ft - 69.6 * np.sqrt(
                WSc / (sigma_takeoff * CL_max_to)
            )
            return A / (B * C)

        # V_cruise condition
        q = 0.5 * rho_cruise * (self._v_cruise**2)   # N/m^2
        K = 1 / (np.pi * self._b**2 / self._S)   # dimensionless

        WcruiseW0 = np.prod(self._weight_fraction[:2])

        def TW_cruise(WS):   # >= este valor
            WSc = WS * WcruiseW0 * (unit.lbf / (unit.ft**2))
            q_imperial = q * unit.lbf / (unit.ft**2)
            A = q_imperial * CD_min / (WSc)
            B = (K * WSc) / (q_imperial)
            return (A + B) * WcruiseW0 / TcruiseT0

        # Service Ceiling condition
        rho_celling = (
            rho_sea
            * self.__rho_per_h__(self._h_celling)
            / self.__rho_per_h__(0)
        )
        WcellingW0 = np.prod(self._weight_fraction[:2])

        def TW_ceiling(WS):   # >= este valor
            WSc = (
                WS * WcruiseW0 * (unit.lbf / (unit.ft**2))
            )   # N/m^2 to lbf/ft^2
            v_v = v_vertical * unit.ft   # m/s to ft/s
            rho_cell = rho_celling * unit.slug_per_ft3   # kg/m^3 to slug/ft^3

            A = np.sqrt(K / (3 * CD_min))
            B = v_v / np.sqrt(2 * WSc * A / rho_cell)
            C = 4 * np.sqrt(K * CD_min / 3)
            return (B + C) / WcellingW0

        return WS_stall, WS_land, TW_to, TW_cruise, TW_ceiling

    # ======< Variables Overload >======

    def __repr__(self) -> str:
        repr = '+' + '-' * 16 + '+\n'
        repr += '|' + 'W0  : ' + (f'{self.M_tow :_.0f} Kg').center(10) + '|\n'
        repr += (
            '|' + 'Wf  : ' + (f'{self.fuel_weigh :_.0f} kg').center(10) + '|\n'
        )
        repr += (
            '|'
            + 'We  : '
            + (f'{self.empty_weigh :_.0f} kg').center(10)
            + '|\n'
        )
        for i, Wn in enumerate(self.weight_fraction):
            repr += '|' + f'W{i+1}W{i}: ' + (f'{Wn:.5f}').center(10) + '|\n'
        repr += '+' + '-' * 16 + '+\n'
        return repr
