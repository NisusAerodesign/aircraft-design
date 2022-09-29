from os import stat
import re
from typing import Any, List, Tuple

import numpy as np
from scipy.optimize import fsolve


class unit:
    lb: float = 1 / 0.45359237   # lb/kg
    ft: float = 1 / 0.30480000   # ft/m
    lbf: float = 1 / 4.44822162   # lbf/N
    hp: float = 1 / 745.69987200   # hp/W

    kg: float = 0.45359237   # kg/lb
    m: float = 0.30480000   # m/ft
    N: float = 4.44822162   # N/lbf
    W: float = 745.69987200   # W/hp


class aircraft_pre_select:
    def __init__(
        self,
        first_range: float,  # km
        second_range: float,  # km
        LDmax: float,  #
        sfc_cruise: float,  # g/(kN.S)
        sfc_sea_level: float,  # g/(kN.S)
        b:float,  # m
        S:float, # m2
        payload: float = 1500.0,  # Kg
        crew: float = 3.0,  # Number of people
        person_avg: float = 95.0,  # Kg
        loiter_time: float = 20.0,  # min
        h_cruise:float = 11, # km
        h_celling:float = 14, # km
        Mach: float = 0.8,  #
        class_airplane='JetTransport',
    ) -> None:

        self._f_range = first_range * 1000 * unit.ft   # fts
        self._s_range = second_range * 1000 * unit.ft   # fts

        self.LDmax = LDmax   # dimensionless

        self._sfc_cruise = (
            sfc_cruise * 1e-6 * unit.lb / unit.lbf
        )   # lb/(lbf.s)
        self._sfc_sea_level = (
            sfc_sea_level * 1e-6 * unit.lb / unit.lbf
        )   # lb/(lbf.s)
        
        self._b = b*unit.ft
        self._S = S*unit.ft**2

        self._payload = payload * unit.lb   # lb
        self.crew = crew
        self._person_avg = person_avg * unit.lb   # lb

        self._loiter_time = loiter_time * 60   # seg
        
        self._h_cruise = h_cruise*1000*unit.ft # fts
        self._h_celling = h_celling*1000*unit.ft # fts

        self._mach = Mach
        self._sound_speed = 340 * unit.ft   # ft/s
        self._v_cruise = self._mach * self._sound_speed   # ft/s

        self.class_airplane = class_airplane

    # ======< parameter treatment >======
    @property
    def first_range(self) -> float:
        return self._f_range * 1000 * unit.m

    @property
    def second_range(self) -> float:
        return self._s_range * 1000 * unit.m

    @property
    def sfc_cruise(self) -> float:
        return self._sfc_cruise * 1e6 * unit.kg / unit.N   # g/(kN.S)

    @property
    def sfc_sea_level(self) -> float:
        return self._sfc_sea_level * 1e6 * unit.kg / unit.N   # g/(kN.S)

    @property
    def b(self) -> float:
        return self._b * unit.m
    
    @property
    def S(self) ->float:
        return self._S * unit.m
    
    @property
    def chord(self) -> float:
        return self._S/self._b * unit.m
    
    @property
    def _chord_imperial(self) -> float:
        return self._S/self._b
    
    @property
    def _S_wetted(self) -> float:
        A_wetted = (self.LDmax/15.5)**2
        return self._b**2 / A_wetted
    
    @property
    def payload(self) -> float:
        return self._payload * unit.kg

    @property
    def person_avg(self) -> float:
        return self._person_avg * unit.kg

    @property
    def loiter_time(self) -> float:
        self._loiter_time / 60

    @property
    def Mach(self) -> float:
        return self._mach

    @property
    def sound_speed(self) -> float:
        return self._sound_speed * unit.m   # m/s

    @property
    def v_cruise(self) -> float:
        return self._v_cruise * unit.m   # m/s

    @property
    def W0(self) -> float:
        resp, _, _, _ = self.__SI_mass_props__()
        return resp

    @property
    def Wf(self) -> float:
        _, resp, _, _ = self.__SI_mass_props__()
        return resp

    @property
    def We(self) -> float:
        _, _, resp, _ = self.__SI_mass_props__()
        return resp

    @property
    def weight_fraction(self) -> np.array:
        _, _, _, resp = self.__SI_mass_props__()
        return resp

    @property
    def __imperial_mass_props__(self) -> Tuple[float, float, float, list]:
        w0_kg, wf_kg, we_kg, wf = self.__SI_mass_props__()
        return w0_kg * unit.lb, wf_kg * unit.lb, we_kg * unit.lb, wf

    @first_range.setter
    def first_range(self, kilometers: float) -> None:
        self._f_range = kilometers * 1000 * unit.ft

    @second_range.setter
    def second_range(self, kilometers: float) -> None:
        self._s_range = kilometers * 1000 * unit.ft

    @sfc_cruise.setter
    def sfc_cruise(self, sfc_SI_unit: float) -> None:
        self._sfc_cruise = sfc_SI_unit * 1e-6 * unit.lb / unit.lbf

    @sfc_sea_level.setter
    def sfc_sea_level(self, sfc_SI_unit: float) -> None:
        self._sfc_sea_level = sfc_SI_unit * 1e-6 * unit.lb / unit.lbf
    
    @payload.setter
    def payload(self, mass_kg: float) -> None:
        self._payload = mass_kg * unit.lb

    @person_avg.setter
    def person_avg(self, mass_kg: float) -> None:
        self._person_avg = mass_kg * unit.lb

    @loiter_time.setter
    def loiter_time(self, time_minutes: float) -> None:
        self._loiter_time = time_minutes * 60

    @Mach.setter
    def Mach(self, mach_number: float) -> None:
        self._mach = mach_number
        self._v_cruise = self._mach * self._sound_speed

    @sound_speed.setter
    def sound_speed(self, speed_SI: float) -> None:
        self._sound_speed = speed_SI * unit.ft   # ft/s
        self._v_cruise = self._mach * self._sound_speed

    # ======< Climatic props >======
    @staticmethod
    def __rho_h_imperial__(H_feets:float):
        h_m = H_feets*unit.m
        T0 = 288.15 # °K
        T = T0 - 0.0065*h_m # °K
        rho = 1.225*(T/T0)**(-9.80665/(-0.0065*287.15) - 1)
        return rho*unit.lb/(unit.ft**3)
    
    # ======< Raymer functions definition >======
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
        wewo = lambda wo: A * (wo ** (C))
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
            'Cruise': lambda R, SFC, LD, V: np.exp(-R * SFC / (V * LD)),
            'Loiter': lambda E, SFC, LD: np.exp(-E * SFC / LD),
        }
        wf = coef[fase]
        return wf

    @staticmethod
    def Raymer_T_W0(category: str) -> callable:
        coef = {
            'JetTrainer': [0.488, 0.728],
            'JetFighterDogfigther': [0.648, 0.594],
            'JetTrainerOther': [0.514, 0.141],
            'MilitaryCargo': [0.244, 0.341],
            'JetTransport': [0.267, 0.363],
            'Sailpowerd': [0.043, 0.0],
            'HBmetal': [0.005, 0.57],
            'HBcomp': [0.004, 0.57],
            'GAsingle': [0.025, 0.22],
            'GAtwin': [0.036, 0.32],
            'Agricultural': [0.009, 0.50],
            '2TurboP': [0.013, 0.5],
            'FlyBoat': [0.030, 0.23],
        }
        a, C = coef[category]

        return lambda x: a * (x**C)

    # ======< Estimation >======
    def __SI_mass_props__(
        self, first_step: float = 27_000.0
    ) -> Tuple[float, float, float, np.array]:
        first_step *= unit.lb

        time_second_range = self._s_range / self._v_cruise   # s

        We = self.Raymer_We(self.class_airplane)
        ##  W1/W0 -> Warmup and Take Off
        W1W0 = self.Raymer_Wf('WuTo')

        ## W2/W1 -> Climb
        W2W1 = self.Raymer_Wf('Climb-Ac')
        W2W1 = W2W1(self._mach)

        ## W3/W2 -> Cruise
        W3W2f = self.Raymer_Wf('Cruise')
        W3W2 = lambda x: W3W2f(
            x, self._sfc_cruise, self.LDmax * 0.866, self._v_cruise
        )

        ## W4/W3 -> Loiter 1
        W4W3f = self.Raymer_Wf('Loiter')
        W4W3 = lambda x: W4W3f(x, self._sfc_sea_level, self.LDmax)

        ## W5/W4 -> Tentativa de Pouso
        W5W4 = self.Raymer_Wf('Landing')

        ## W6/W5 -> Climb
        W6W5 = W2W1

        ## W7/W6 -> Cruseiro 2 - tempo
        W7W6 = self.Raymer_Wf('Loiter')
        W7W6 = W7W6(time_second_range, self._sfc_cruise, self.LDmax * 0.866)

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
        Wcrew = self.crew * self._person_avg

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
            W0 * unit.kg,
            WfW0(self._f_range, self._loiter_time) * W0 * unit.kg,
            We(W0) * W0 * unit.kg,
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

    def __restriction_diagram__(
        self,
        Sl: float,
        V_vertical_kmph: float = 2,
        sigma_land: float = 0.9,
        sigma_takeoff: float = 0.9,
        CL_max: float = 2.3,
        V_stall_kmph: float = 260,
        TcruiseT0: float = 0.4,
        rho_sea: float = 1.225,
    ):
        v_vertical = V_vertical_kmph * unit.ft / 3.6
        v_stall = V_stall_kmph * unit.ft / 3.6

        rho_sea_level = rho_sea*0.0019403203   # slug/ft3
        rho_cruise = self.__rho_h_imperial__(self._h_cruise) / 32.174
    
        CD_min = 0.003*self._S_wetted/self._S   # CL_max/self.LDmax
        # V_stall condition
        WstallW0 = np.prod(self.weight_fraction[:2])
        WS_stall = (
            0.5 * rho_sea_level * (v_stall**2) * CL_max * WstallW0
        )   # <= que este valor

        # land distance condition
        CL_max_land = CL_max / (1.3**2)   # Norma de aviação
        WlW0 = np.prod(self.weight_fraction[:4])

        WS_land = (
            (2 / 3) * Sl * sigma_land * CL_max_land / (79.4 * WlW0)
        )   # <= este valor

        # takeoff distance condition
        CL_max_to = CL_max / (1.1**2)
        WtoW0 = self.weight_fraction[0]

        def TW_to(WS):   # >= este valor
            WSc = WS * WtoW0
            A = 20 * WSc
            B = sigma_takeoff * CL_max_to
            C = Sl - 69.6 * np.sqrt(WSc / (sigma_takeoff * CL_max_to))
            return A / (B * C)

        # V_cruise condition
        q = 0.5 * rho_cruise * (self._v_cruise**2)
        K = 1/(np.pi*self._b**2/self._S)

        WcruiseW0 = np.prod(self.weight_fraction[:2])

        def TW_cruise(WS):   # >= este valor
            WSc = WS * WcruiseW0
            A = q * CD_min / (WSc)
            B = (K * WSc) / q  
            return (A + B) * WcruiseW0/TcruiseT0

        # Service Ceiling condition
        rho_celling = self.__rho_h_imperial__(self._h_celling)
        WcellingW0 = np.prod(self.weight_fraction[:2])
        
        def TW_ceiling(WS):   # >= este valor
            WSc = WS * WcruiseW0
            A = np.sqrt(K / (3 * CD_min))
            B = v_vertical / np.sqrt(2 * WSc * A / rho_celling)
            C = 4 * np.sqrt(K * CD_min / 3)
            return (B + C)/WcellingW0

        return WS_stall, WS_land, TW_to, TW_cruise, TW_ceiling

    # ======< Variables Overload >======

    def __repr__(self) -> str:
        values = self.__SI_mass_props__()
        repr = '+' + '-' * 16 + '+\n'
        repr += '|' + 'W0  : ' + (f'{values[0] :_.0f} Kg').center(10) + '|\n'
        repr += '|' + 'Wf  : ' + (f'{values[1] :_.0f} kg').center(10) + '|\n'
        repr += '|' + 'We  : ' + (f'{values[2] :_.0f} kg').center(10) + '|\n'
        for i, Wn in enumerate(values[3]):
            repr += '|' + f'W{i+1}W{i}: ' + (f'{Wn:.5f}').center(10) + '|\n'
        repr += '+' + '-' * 16 + '+\n'
        return repr
