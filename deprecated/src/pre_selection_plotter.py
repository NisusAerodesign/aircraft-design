from cProfile import label
from dataclasses import dataclass
from turtle import color
from typing import Optional

import matplotlib.pyplot as plt

from src.pre_selection_geometry import *


@dataclass
class Plane:
    name: str
    W0: float
    Wing_area: float
    thrust: float   # to all engines
    imperial_units: bool = False
    color: Optional[str] = None

    def WS(self):
        return self.W0 / self.Wing_area

    def TW(self):
        if self.imperial_units:
            return self.thrust / self.W0
        else:
            return self.thrust / (self.W0 * unit.g)


@dataclass
class Engine:
    name: str
    thrust: float   # to single engine
    number_of_engines: int
    imperial_units: bool = False
    linestyle: Optional[str] = None
    color: Optional[str] = None


class aircraft_selection(aircraft_selection_geometry):
    def plot_constraint_diagram(
        self,
        Range_takeoff: float,
        Range_land: float,
        CL_max: float,  # depends if it has flaps
        imperial_units: bool = False,
        n_points: int = 1000,  # Resolution of the curve
        bbox_to_anchor: Tuple[float] = (1.0, 1.0),
        **kwargs,
    ):
        self.__param_computate__()

        (
            WS_stall,
            WS_land,
            TW_to,
            TW_cruise,
            TW_ceiling,
        ) = self.constraint_diagram(
            Range_takeoff, Range_land, CL_max, imperial_units, **kwargs
        )
        # test_crosses = np.linspace(0, 10*max(WS_land, WS_stall), n_points)
        # WS_takeoff_crosses_cruise = np.argwhere(
        #     np.diff(np.sign(TW_to(test_crosses) - TW_cruise(test_crosses)))
        # ).flatten()

        bigger_ws = max(WS_land, WS_stall)

        smaller_ws = min(WS_land, WS_stall)

        # Plot:
        WS_vector = np.linspace(0.6 * smaller_ws, 1.1 * bigger_ws, n_points)

        # Max and min values
        max_to, min_to = max(TW_to(WS_vector)), min(TW_to(WS_vector))
        max_cruise, min_cruise = max(TW_cruise(WS_vector)), min(
            TW_cruise(WS_vector)
        )
        max_ceiling, min_ceiling = max(TW_ceiling(WS_vector)), min(
            TW_ceiling(WS_vector)
        )

        min_tw = 0.8 * min(min_to, min_cruise, min_ceiling)
        max_tw = 1.1 * max(max_to, max_cruise, max_ceiling)

        # Fill between curves
        WS_to_fill = np.linspace(WS_vector[0], smaller_ws, n_points)
        TW_to_fill = np.max(
            [TW_to(WS_to_fill), TW_cruise(WS_to_fill), TW_ceiling(WS_to_fill)],
            axis=0,
        )

        TW_to_fill_min = min(TW_to_fill)
        (index,) = np.where(TW_to_fill == TW_to_fill_min)
        WS_to_fill_min = WS_to_fill[index]
        # plots
        f, ax = plt.subplots()
        ax.fill_between(
            WS_to_fill,
            TW_to_fill,
            max_tw,
            interpolate=True,
            alpha=0.3,
            hatch='//',
            label='zone of interest',
            color='blue',
        )
        ax.plot([WS_land, WS_land], [min_tw, max_tw], 'r', label='Land')
        ax.plot(WS_vector, TW_to(WS_vector), 'g', label='Takeoff')
        ax.plot(WS_vector, TW_cruise(WS_vector), 'b', label='Cruise')
        ax.plot(WS_vector, TW_ceiling(WS_vector), 'y', label='Ceiling')
        ax.plot([WS_stall, WS_stall], [min_tw, max_tw], 'c', label='Stall')
        ax.plot(WS_to_fill_min, TW_to_fill_min, 'kx', label='Optimal point')

        ax.set_xlim([WS_vector[0], WS_vector[-1]])
        ax.set_ylim([min_tw, max_tw])

        ax.grid()

        f.legend(bbox_to_anchor=bbox_to_anchor)
        f.suptitle('Constraint diagram')

        if imperial_units:
            ax.set_xlabel(r'W0/S [lb/ft²]')
        else:
            ax.set_xlabel(r'W0/S [N/m²]')
        ax.set_ylabel(r'T/W0')

        return f, ax

    def plot_select_engine(
        self,
        Range_takeoff: float,
        Range_land: float,
        CL_max: float,  # depends if it has flaps
        Engines: List[Engine],
        Planes: Optional[List[Plane]] = None,
        imperial_units: bool = False,
        n_points: int = 1000,  # Resolution of the curve
        bbox_to_anchor: Tuple[float] = (1.0, 1.0),
        **kwargs,
    ):
        self.__param_computate__()

        (
            WS_stall,
            WS_land,
            TW_to,
            TW_cruise,
            TW_ceiling,
        ) = self.constraint_diagram(
            Range_takeoff,
            Range_land,
            CL_max,
            imperial_units,
            **kwargs,
        )
        v = 0.6 * min(WS_land, WS_stall)
        smaller_ws = min(WS_land, WS_stall)
        bigger_ws = max(WS_land, WS_stall)
        WS_to_fill = np.linspace(v, smaller_ws, n_points)
        TW_to_fill = np.max(
            [TW_to(WS_to_fill), TW_cruise(WS_to_fill), TW_ceiling(WS_to_fill)],
            axis=0,
        )

        WS_vector = np.linspace(0.6 * smaller_ws, 1.1 * bigger_ws, n_points)

        max_to = max(TW_to(WS_vector))
        max_cruise = max(TW_cruise(WS_vector))
        max_ceiling = max(TW_ceiling(WS_vector))

        max_tw = 1.1 * max(max_to, max_cruise, max_ceiling)

        f, ax = plt.subplots()

        ax.fill_between(
            WS_to_fill,
            TW_to_fill,
            max_tw,
            interpolate=True,
            alpha=0.1,
            label='zone of interest',
            color='blue',
        )
        # Plot engines
        for engine in Engines:
            assert (
                engine.imperial_units == imperial_units
            ), 'Error: you cannot mix imperial and SI units!'
            if engine.imperial_units:
                TW = (engine.thrust * unit.N * engine.number_of_engines) / (
                    self._W0 * unit.g
                )
                ax.plot(
                    [WS_to_fill[0], WS_to_fill[-1]],
                    [TW, TW],
                    color=engine.color,
                    linestyle=engine.linestyle,
                    label=f'{engine.name} with {engine.number_of_engines} engines',
                )
            else:
                TW = (
                    engine.thrust
                    * engine.number_of_engines
                    / self._W0
                    * unit.g
                )
                ax.plot(
                    [WS_to_fill[0], WS_to_fill[-1]],
                    [TW, TW],
                    color=engine.color,
                    linestyle=engine.linestyle,
                    label=f'{engine.name} with {engine.number_of_engines} engines',
                )
        if not Planes == None:
            for plane in Planes:
                assert (
                    plane.imperial_units == imperial_units
                ), 'Error: you cannot mix imperial and SI units!'
                if plane.imperial_units:
                    ax.plot(
                        [plane.WS()],
                        [plane.TW()],
                        'x',
                        color=plane.color,
                        label=f'{plane.name}',
                    )
        ax.set_ylabel('T/W0')
        if imperial_units:
            ax.set_xlabel('W0/S [lb/ft²]')
        else:
            ax.set_xlabel('W0/S [N/m²]')

        ax.grid()
        f.suptitle('Engine comparison')
        f.legend(bbox_to_anchor=bbox_to_anchor)
        f.tight_layout()
        return f, ax

    def wing_super_view(self, alpha_atk_deg: float = None, align='c'):
        # C is Center
        # T is Trailing edge
        # L is Leading edge
        assert all(
            [
                self._fuselage_FR,
                self._fuselage_length,
                self._wing_TR,
                self._wing_sweep,
                self._dihedral_wing,
                self._tail_AR,
                self._tail_TR,
            ]
        ), 'Error: Aircraft geometry is not defined!'

        if alpha_atk_deg == None:
            alpha_atk_deg = self._wing_sweep

        cm = self._S / self._b
        cr = 2 * cm / (self._wing_TR + 1)
        ct = self._wing_TR * cr

        b_2 = self._b / 2

        al = alpha_atk_deg * np.pi / 180
        if align.lower() == 'l':
            ctc = b_2 * np.tan(al)
        elif align.lower() == 'c':
            ctc = b_2 * np.tan(al) + (cr - ct) / 2
        elif align.lower() == 't':
            ctc = b_2 * np.tan(al) + (cr - ct)
        else:
            assert (
                True
            ), f'Error align parameter ({align.lower()}) not recognized!'

        CR = np.linspace(0, cr)
        CT = np.linspace(ctc, ctc + ct)

        al = (180 / np.pi) * np.arctan(ctc / b_2)
        alc4 = (180 / np.pi) * np.arctan((ctc + ct / 4 - cr / 4) / b_2)

        plt.rcParams['figure.figsize'] = (6, 12)
        f, ax = plt.subplots()
        f.subplots_adjust(
            left=0.105,
            bottom=0.067,
            right=0.967,
            top=0.933,
            wspace=0.0,
            hspace=0.2,
        )
        ax.plot(CR, 0 * CR, 'k')
        ax.plot(CT, b_2 + 0 * CT, 'k')
        ax.plot(CT, -b_2 + 0 * CT, 'k')
        ax.plot([0, CT[0]], [0, b_2], 'k')
        ax.plot([0, CT[0]], [0, -b_2], 'k')
        ax.plot([cr, CT[-1]], [0, b_2], 'k')
        ax.plot([cr, CT[-1]], [0, -b_2], 'k')
        ax.plot([cr / 4, ctc + ct / 4], [0, b_2], 'k--')
        ax.plot([cr / 4, ctc + ct / 4], [0, -b_2], 'k--')
        ax.axis('equal')
        ax.set_xlabel('meters')
        ax.set_ylabel('meters')
        ax.set_title(
            f'Wing configuration \n Λ_LE = {al:.2f}°, Λ_C/4 = {alc4:.2f}°'
        )

        return f, ax, al, alc4
