from imp import reload
from typing import Any, List, Tuple

from scipy.optimize import fsolve

from src.raymer_tables import *


class aircraft_selection_core:
    @staticmethod
    def __kwargs_treatment__(possible_args: dict, **kwargs):
        for arg in kwargs:
            assert (
                arg in possible_args
            ), f'ERROR: unrecognized argument ({arg})'

        for arg in possible_args:
            if not arg in kwargs:
                kwargs[arg] = possible_args[arg]

        return kwargs

    __CLASS_POSSIBLE_ARGS__ = {
        'payload': 1500.0,  # Kg
        'crew': 3.0,  # Number of people
        'person_avg': 95.0,  # Kg
        'loiter_time': 20.0,  # min
        'h_cruise': 11_000,  # m
        'h_celling': 15_000,  # m
        'Mach': 0.8,  #
        'class_airplane': 'JetTransport',
    }

    def __init__(
        self,
        code_name: str,
        first_range: float,  # km
        second_range: float,  # km
        LDmax: float,  #
        sfc_cruise: float,  # g/(kN.S)
        sfc_sea_level: float,  # g/(kN.S)
        wing_spain: float,  # m
        wing_area: float,  # m2
        **kwargs,
    ) -> None:
        kwargs = self.__kwargs_treatment__(
            self.__CLASS_POSSIBLE_ARGS__, **kwargs
        )

        payload = kwargs['payload']
        crew = kwargs['crew']
        person_avg = kwargs['person_avg']
        loiter_time = kwargs['loiter_time']
        h_cruise = kwargs['h_cruise']
        h_celling = kwargs['h_celling']
        Mach = kwargs['Mach']
        class_airplane = kwargs['class_airplane']

        self._code_name = code_name.upper()

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

        self.__update_parameters__ = [
            self.__reload_sound_speed__,
            self.__reload_v_cruise__,
            self.__reload_S_wett__,
            self.__reload_AR__,
            self.__reload_SI_mass_props__,
        ]
        # === Need to computate ===
        self._sound_speed = 0   # m/s
        self._v_cruise = 0   # m/s
        self._W0 = 0
        self._We = 0
        self._Wf = 0
        self._weight_fraction = 0

        self._S_wetted = 0   # m2
        self._A = 0

    # ======< parameter treatment: Getters >======
    @property
    def code_name(self) -> float:
        return self._code_name

    @property
    def first_range(self) -> float:
        return self._f_range / 1000   # km

    @property
    def second_range(self) -> float:
        return self._s_range / 1000   # km

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
        return self._crew

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
    def sound_speed(self) -> float:   #
        self.__param_computate__()
        return self._sound_speed   # m/s

    @property
    def v_cruise(self) -> float:   #
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

    # ======< parameter treatment: Setters >======
    @code_name.setter
    def code_name(self, codename: str):
        self._code_name = codename.upper()

    @wing_span.setter
    def wing_span(self, meters: float):
        self._b = meters   # m
        self.__add_to_update__(self.__reload_AR__)
        self.__add_to_update__(self.__reload_S_wett__)

    @wing_area.setter
    def wing_area(self, meters2: float):
        self._S = meters2   # m2
        self.__add_to_update__(self.__reload_AR__)

    @h_cruise.setter
    def h_cruise(self, meters: float):
        self._h_cruise = meters  # m
        self.__add_to_update__(self.__reload_sound_speed__)

    @h_celling.setter
    def h_celling(self, meters: float):
        self._h_celling = meters   # m

    @first_range.setter
    def first_range(self, kilometers: float):
        self._f_range = kilometers * 1000   # km
        self.__add_to_update__(self.__reload_SI_mass_props__)

    @second_range.setter
    def second_range(self, kilometers: float):
        self.second_range = kilometers * 1000   # km
        self.__add_to_update__(self.__reload_SI_mass_props__)

    @LD_max.setter
    def LD_max(self, Value: float):
        self._LDmax = Value   # dimensionless
        self.__add_to_update__(self.__reload_S_wett__)
        self.__add_to_update__(self.__reload_SI_mass_props__)

    @sfc_cruise.setter
    def sfc_cruise(self, g_per_kN_s: float):
        self._sfc_cruise = g_per_kN_s * 1e-6   # kg/(N.s)
        self.__add_to_update__(self.__reload_SI_mass_props__)

    @sfc_sea_level.setter
    def sfc_sea_level(self, g_per_kN_s: float):
        self._sfc_sea_level = g_per_kN_s * 1e6   # kg/(N.s)
        self.__add_to_update__(self.__reload_SI_mass_props__)

    @payload.setter
    def payload(self, kilogram: float):
        self._payload = kilogram   # kg
        self.__add_to_update__(self.__reload_SI_mass_props__)

    @crew.setter
    def crew(self, n_crew: float):
        self._crew = n_crew
        self.__add_to_update__(self.__reload_SI_mass_props__)

    @person_avg_weigh.setter
    def person_avg_weigh(self, kilogram: float):
        self._person_avg = kilogram   # kg
        self.__add_to_update__(self.__reload_SI_mass_props__)

    @loiter_time.setter
    def loiter_time(self, minutes: float):
        self._loiter_time = minutes * 60   # min
        self.__add_to_update__(self.__reload_SI_mass_props__)

    @Mach.setter
    def Mach(self, mach: float):
        self._mach = mach
        self.__add_to_update__(self.__reload_v_cruise__)
        self.__add_to_update__(self.__reload_SI_mass_props__)

    @class_airplane.setter
    def class_airplane(self, airplane_class: str):
        self._class_airplane = airplane_class
        self.__add_to_update__(self.__reload_SI_mass_props__)

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
        return 340  # (gamma * R * T) ** 0.5

    # ======< Calculation >======
    def __SI_mass_props__(
        self,
        We: callable,
        first_step: float = 20_000.0,
    ) -> Tuple[float, float, float, np.array]:
        # first_step *= unit.lb

        time_second_range = self._s_range / self._v_cruise   # s

        # Raymer.Raymer_We(self._class_airplane)
        ##  W1/W0 -> Warmup and Take Off
        W1W0 = Raymer.Raymer_Wf('WuTo')

        ## W2/W1 -> Climb
        W2W1 = Raymer.Raymer_Wf('Climb-Ac')
        W2W1 = W2W1(self._mach)

        ## W3/W2 -> Cruise
        W3W2f = Raymer.Raymer_Wf('Cruise')
        W3W2 = lambda range: W3W2f(
            range, self._sfc_cruise, self._LDmax * 0.866, self._v_cruise
        )

        ## W4/W3 -> Loiter 1
        W4W3f = Raymer.Raymer_Wf('Loiter')
        W4W3 = lambda time: W4W3f(time, self._sfc_sea_level, self._LDmax)

        ## W5/W4 -> Tentativa de Pouso
        W5W4 = Raymer.Raymer_Wf('Landing')

        ## W6/W5 -> Climb
        W6W5 = W2W1

        ## W7/W6 -> Cruseiro 2 - tempo
        W7W6 = Raymer.Raymer_Wf('Loiter')
        W7W6 = W7W6(time_second_range, self._sfc_cruise, self._LDmax * 0.866)

        ## W8/W7 -> Loiter
        W8W7 = W4W3

        ## W9/W8 -> Landing
        W9W8 = Raymer.Raymer_Wf('Landing')

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

    def constraint_diagram(
        self,
        Range_takeoff: float,
        Range_land: float,
        CL_max: float,  # depends if it has flaps
        imperial_units: bool = False,
        **kwargs,
    ):
        self.__param_computate__()

        possible_args = {
            'rho_sea': 1.225,  # kg/m^3,
            'sigma_land': 0.9,  # ratio of rho_air/rho_sea_level,
            'sigma_takeoff': 0.9,  # ratio of rho_air/rho_sea_level,
            'TcruiseT0': 0.3,  # avg Tcruise/T0,
            'V_stall_kmph': 113,
            'V_vertical_kmph': 36,  # km/h,
            'CL_stall_per_CL_max': 1,
            'CL_land_per_CL_max': 1,
            'CL_takeoff_per_CL_max': 1,
        }

        kwargs = self.__kwargs_treatment__(possible_args, **kwargs)
        rho_sea = kwargs['rho_sea']
        sigma_land = kwargs['sigma_land']
        sigma_takeoff = kwargs['sigma_takeoff']
        TcruiseT0 = kwargs['TcruiseT0']
        V_stall_kmph = kwargs['V_stall_kmph']
        V_vertical_kmph = kwargs['V_vertical_kmph']
        CL_stall_per_CL_max = kwargs['CL_stall_per_CL_max']
        CL_land_per_CL_max = kwargs['CL_land_per_CL_max']
        CL_takeoff_per_CL_max = kwargs['CL_takeoff_per_CL_max']

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

        if imperial_units:
            lbf_ft2 = 47.880172   # N/m^2

            WS_stall = WS_stall / lbf_ft2
            WS_land = WS_land / lbf_ft2
            TW_to_r = lambda WS_imperial: TW_to(WS_imperial * lbf_ft2)
            TW_cruise_r = lambda WS_imperial: TW_cruise(WS_imperial * lbf_ft2)
            TW_ceiling_r = lambda WS_imperial: TW_ceiling(
                WS_imperial * lbf_ft2
            )
        else:
            TW_to_r = lambda WS_SI: TW_to(WS_SI)
            TW_cruise_r = lambda WS_SI: TW_cruise(WS_SI)
            TW_ceiling_r = lambda WS_SI: TW_ceiling(WS_SI)
        return (
            WS_stall,
            WS_land,
            TW_to_r,
            TW_cruise_r,
            TW_ceiling_r,
        )

    # ======< Reload Function >======
    def __reload_sound_speed__(self):
        # Update sound speed
        self._sound_speed = self.__sound_speed_calculator__(
            self.__T_per_h__(self._h_cruise)
        )

    def __reload_S_wett__(self):
        # S_wett
        A_wetted = (self._LDmax / 15.5) ** 2   # Verify Raymer
        self._S_wetted = self._b**2 / A_wetted

    def __reload_v_cruise__(self):
        # Update v cruise
        self._v_cruise = self._mach * self._sound_speed

    def __reload_AR__(self):
        # Update aspect ratio
        self._A = self._b**2 / self._S

    def __reload_SI_mass_props__(self):
        W0, Wf, We, n = self.__SI_mass_props__(
            Raymer.Raymer_We(self._class_airplane)
        )
        self._W0, self._Wf, self._We, self._weight_fraction = (
            W0,
            Wf,
            We,
            n,
        )

    def __add_to_update__(self, param: callable):
        if param not in self.__update_parameters__:
            self.__update_parameters__.append(param)

    def __param_computate__(self):
        while len(self.__update_parameters__) > 0:
            self.__update_parameters__[0]()
            self.__update_parameters__.pop(0)

    # === OVERLOAD ===
    def __repr__(self) -> str:
        self.__param_computate__()

        repr = f'Airplane: {self._code_name}' + '\n'
        repr += len(repr) * '=' + '\n'
        repr += f'first range: {self.first_range} km' + '\n'
        repr += f'second range: {self.second_range} km' + '\n\n'
        repr += f'AR: {round(self._A,2)}' + '\n'
        repr += f'Wing area: {round(self.wing_area,2)} m²' + '\n'
        repr += f'Wing wet area: {round(self._S_wetted,2)} m²' + '\n'
        repr += f'Wing spain: {round(self.wing_span,2)} m' + '\n'
        repr += '+' + '-' * 16 + '+\n'
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
