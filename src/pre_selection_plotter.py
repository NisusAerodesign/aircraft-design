from cProfile import label
from src.pre_selection import *
import matplotlib.pyplot as plt


class aircraft_selection(aircraft_selection_core):
    def plot_restriction_diagram(
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
        CL_land_per_CL_max: float = 1.0,  # CL_max_land/CL_max to fix land CL
        CL_takeoff_per_CL_max: float = 1.0,  # CL_max_takeoff/CL_max to fix takeoff CL
        imperial_units: bool = False,
        n_points: int = 1000,
    ):
        (
            WS_stall,
            WS_land,
            TW_to,
            TW_cruise,
            TW_ceiling,
        ) = self.restriction_diagram(
            Range_takeoff,
            Range_land,
            CL_max,
            rho_sea,
            sigma_land,
            sigma_takeoff,
            TcruiseT0,
            V_stall_kmph,
            V_vertical_kmph,
            CL_stall_per_CL_max,
            CL_land_per_CL_max,
            CL_takeoff_per_CL_max,
            imperial_units,
        )
        # test_crosses = np.linspace(0, 10*max(WS_land, WS_stall), n_points)
        # WS_takeoff_crosses_cruise = np.argwhere(
        #     np.diff(np.sign(TW_to(test_crosses) - TW_cruise(test_crosses)))
        # ).flatten()

        bigger_ws = max(
            WS_land,
            WS_stall,
        )

        smaller_ws = min(
            WS_land,
            WS_stall,
        )

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
        index, = np.where(TW_to_fill == TW_to_fill_min)
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
        ax.legend()
        ax.set_xlabel(r'W/S [N/m²]')
        ax.set_ylabel(r'T/W')

        return f, ax
