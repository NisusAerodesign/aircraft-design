#%%
import numpy as np
from scipy.optimize import fsolve

#%%
def mission_estimation(
    f_range: float,
    s_range: float,
    LDmax: float,
    sfc_cruize: float,
    sfc_sea_level: float,
    payload: float = 1500.0,
    crew: float = 3.0,
    person_avg: float = 95.0,
    loiter_time: float = 20.0,
    Mach: float = 0.8,
    class_airplane='JetTransport',
):

    #%% Conversion
    ft = 3.28084
    lb = 2.20462262
    a = 340 * ft   # ft/s
    f_range *= 1000 * ft   # ft
    s_range *= 1000 * ft   # ft

    V = Mach * a   # ft/s

    sfc_cruize /= 3600
    sfc_sea_level /= 3600

    loiter_time *= 60
    time_cruize = f_range / V   # s
    time_second_range = s_range / V   # s

    def Raymer_We(category: str) -> any:
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

    print(f'Alcance adotado: {round( (f_range+s_range)/(1000*3.28084), 2)} km')

    We = Raymer_We(class_airplane)
    ##  W1/W0 -> Warmup and Take Off
    W1W0 = Raymer_Wf('WuTo')
    print(f'WarmUp TakeOff    -> {W1W0}')

    ## W2/W1 -> Climb
    W2W1 = Raymer_Wf('Climb-Ac')
    W2W1 = W2W1(Mach)
    print(f'Climb             -> {W2W1}')

    ## W3/W2 -> Cruise
    W3W2f = Raymer_Wf('Cruise')
    W3W2 = lambda x: W3W2f(x, sfc_cruize, LDmax * 0.866, V)
    print(f'Cruise1           -> {W3W2(f_range)}')

    ## W4/W3 -> Loiter 1
    W4W3f = Raymer_Wf('Loiter')
    W4W3 = lambda x: W4W3f(x, sfc_sea_level, LDmax)
    print(f'Loiter1           -> {W4W3(loiter_time)}')

    ## W5/W4 -> Tentativa de Pouso
    W5W4 = Raymer_Wf('Landing')
    print(f'Attempt to Land   -> {W5W4}')

    ## W6/W5 -> Climb
    W6W5 = W2W1
    print(f'Climb             -> {W6W5}')

    ## W7/W6 -> Cruseiro 2 - tempo
    W7W6 = Raymer_Wf('Loiter')
    W7W6 = W7W6(time_second_range, sfc_cruize, LDmax * 0.866)
    print(f'Cruise2           -> {W7W6}')

    ## W8/W7 -> Loiter
    W8W7 = W4W3
    print(f'Landing           -> {W8W7(loiter_time)}')

    ## W9/W8 -> Landing
    W9W8 = Raymer_Wf('Landing')
    print(f'Final Landing     -> {W9W8}')

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
    print(f'Wf/W0             -> {WfW0(f_range, loiter_time)}')

    ## Carga Paga
    Wpl = (payload) * lb
    print(f'Carga Paga        -> {Wpl/lb}')

    ## Tripulacao
    Wcrew = (crew * person_avg) * lb
    print(f'Tripulação        -> {Wcrew/lb}')

    ## Calculo dos Pesos
    W0 = fsolve(
        lambda W0: W0 * (1 - WfW0(f_range, loiter_time) - We(W0))
        - Wpl
        - Wcrew,
        60000,
    )
    W0 = W0[0]
    print(f'Mtow:                         {round(W0/lb, 2)} kg')
    print(
        f'Qde de Combustível:           {round(WfW0(f_range,loiter_time)*W0/lb, 2)} kg'
    )
    print(f'Peso Vazio:                   {round(We(W0)*W0/lb, 2)} kg')
    print(f'Carga Paga + Tripulacao:      {round((Wpl+Wcrew)/lb, 2)} kg')

    return (
        W0 / lb,
        np.array(
            [
                W1W0,
                W2W1,
                W3W2(f_range),
                W4W3(loiter_time),
                W5W4,
                W6W5,
                W7W6,
                W8W7(loiter_time),
                W9W8,
            ]
        ),
        WfW0(f_range, loiter_time),
        We(W0),
    )


def return_fuel_mass(airplane_mass: tuple, W0=None, Wd=None):
    wo, vect, wfwo, wewo = airplane_mass
    if W0 != None:
        wo = W0
    if Wd != None:
        wd = Wd

    wd = wewo * wo
    acum = wo
    wtot = [acum - wd]
    for val in vect:
        acum *= val
        wtot.append(acum - wd)

    return np.array(wtot)
