from src.pre_selection_CD import *


class aircraft_selection_geometry(aircraft_selection_TW):
    def __init__(
        self,
        code_name: str,
        first_range: float,
        second_range: float,
        LDmax: float,
        sfc_cruise: float,
        sfc_sea_level: float,
        wing_spain: float,
        wing_area: float,
        **kwargs
    ) -> None:

        super().__init__(
            code_name,
            first_range,
            second_range,
            LDmax,
            sfc_cruise,
            sfc_sea_level,
            wing_spain,
            wing_area,
            **kwargs
        )

        self._fuselage_FR = None   # FR = Fineness Ratio = Comprimento/Diâmetro

        self._wing_TR = None  # TR Taper Ratio
        self._wing_sweep = None
        self._dihedral_wing = None

        self._tail_AR = None
        self._tail_TR = None

    def computate_geometry(
        self,
        Fuselage_Fineness_ratio: float,
        Wing_Taper_Ratio: float,
        Wing_Sweep: float,
        Wing_Dihedral: float,
        Tail_Aspect_Ratio: float,
        Tail_Taper_ratio: float,
    ):
        self._fuselage_FR = Fuselage_Fineness_ratio   # FR = Fineness Ratio = Comprimento/Diâmetro

        self._wing_TR = Wing_Taper_Ratio  # TR Taper Ratio
        self._wing_sweep = Wing_Sweep
        self._dihedral_wing = Wing_Dihedral

        self._tail_AR = Tail_Aspect_Ratio
        self._tail_TR = Tail_Taper_ratio

