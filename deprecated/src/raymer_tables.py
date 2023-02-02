from http.cookies import CookieError

import numpy as np


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


class Raymer:
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
    def Raymer_AR_4_1(
        category: str,
    ):
        coefs = {
            'JetTrainer': [4.737, -0.979],
            'JetFighter(dogfighter)': [5.416, -0.622],
            'JetFighter(other)': [4.110, -0.622],
            'MilitaryCargo': [5.570, -1.075],
            'JetTransport': [13.697, 1.882],
            # 7 to 10 this perform nearly good
        }

        a, C = coefs[category]
        round_dot_5 = lambda v: round(v * 2) / 2
        return lambda Mach: round_dot_5(a * (Mach**C))

    @staticmethod
    def Raymer_We_6_1(
        catergory: str,
        A: float,
        T_W0: float,
        W0_S: float,
        M: float,
        Kvs: float = 1.04,
    ) -> callable:
        coefs = {
            'JetTrainer': [0, 4.28, -0.1, 0.1, 0.2, -0.24, 0.11],
            'JetFighter': [-0.02, 2.16, -0.10, 0.2, 0.04, -0.1, 0.08],
            'MilitaryCargo': [0.07, 1.71, -0.1, 0.1, 0.06, -0.1, 0.05],
            'JetTransport': [0.32, 0.66, -0.13, 0.3, 0.06, -0.05, 0.05],
        }
        a, b, C1, C2, C3, C4, C5 = coefs[catergory]

        def We_W0(W0):
            P1 = b * ((W0 * unit.lb) ** C1) * (A**C2) * (T_W0**C3)
            P2 = ((W0_S * unit.lb / (unit.ft**2)) ** C4) * (M**C5)
            return (a + P1 * P2) * Kvs

        return We_W0

    @staticmethod
    def Raymer_fuselage_6_3(category: str):
        coefs = {
            'JetTrainer': [0.333, 0.41],
            'JetFighter': [0.389, 0.39],
            'MilitaryCargo': [0.104, 0.50],
            'JetTransport': [0.287, 0.43],
        }

        a, C = coefs[category]
        return lambda W0: a * (W0**C)

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
