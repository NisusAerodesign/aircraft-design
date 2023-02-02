from logging.handlers import RotatingFileHandler
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
        **kwargs,
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
            **kwargs,
        )

        self._fuselage_FR = None   # FR = Fineness Ratio = Comprimento/Diâmetro
        self._fuselage_length = None

        self._wing_TR = None  # TR Taper Ratio
        self._wing_sweep = None
        self._dihedral_wing = None

        self._tail_AR = None
        self._tail_TR = None

    def computate_geometry(
        self,
        Wing_Taper_Ratio: float,
        Wing_Sweep: float,
        Wing_Dihedral: float,
        Tail_Aspect_Ratio: float,
        Tail_Taper_ratio: float,
        Fuselage_Fineness_ratio: float = 3.0,
    ):
        self.__param_computate__()

        self._fuselage_FR = Fuselage_Fineness_ratio   # FR = Fineness Ratio = Comprimento/Diâmetro

        self._wing_TR = Wing_Taper_Ratio  # TR Taper Ratio
        self._wing_sweep = Wing_Sweep
        self._dihedral_wing = Wing_Dihedral

        self._tail_AR = Tail_Aspect_Ratio
        self._tail_TR = Tail_Taper_ratio

        fuselage_length = Raymer.Raymer_fuselage_6_3(self._class_airplane)
        self._fuselage_length = fuselage_length(self._W0)

    def __repr__(self) -> str:
        if not all(
            [
                self._fuselage_FR,
                self._fuselage_length,
                self._wing_TR,
                self._wing_sweep,
                self._dihedral_wing,
                self._tail_AR,
                self._tail_TR,
            ]
        ):
            return super().__repr__()
        else:
            self.__param_computate__()
            repr = f'Airplane: {self._code_name}' + '\n'
            repr += len(repr) * '=' + '\n'
            repr += f'first range: {self.first_range} km' + '\n'
            repr += f'second range: {self.second_range} km' + '\n\n'

            repr += f'Wing Definiton\n===\n'
            repr += f'AR: {round(self._A,2)}' + '\n'
            repr += f'TR: {round(self._wing_TR,2)}' + '\n'
            repr += f'Dihedral: {round(self._dihedral_wing,2)}°' + '\n'
            repr += f'Sweep: {round(self._wing_sweep,2)}°' + '\n'
            repr += f'Wing area: {round(self.wing_area,2)} m²' + '\n'
            repr += f'Wing spain: {round(self.wing_span,2)} m' + '\n'
            repr += f'Chord: {round(self.wing_span/self._A,2)} m' + '\n'
            repr += f'Wing wet area: {round(self._S_wetted,2)} m²' + '\n\n'

            repr += f'Fuselage Definiton\n===\n'
            repr += f'Fineness Ratio: {round(self._fuselage_FR, 2)}' + '\n'
            repr += (
                f'Fuselage length: {round(self._fuselage_length, 2)} m' + '\n'
            )
            repr += (
                f'Fuselage Diameter: {round(self._fuselage_length/self._fuselage_FR,2)} m'
                + '\n\n'
            )

            repr += f'Tail Definiton\n===\n'
            repr += f'AR: {self._tail_AR}' + '\n'
            repr += f'TR: {self._tail_TR}' + '\n\n'

            repr += f'T/W0: {self._T_W0 :.3f}' + '\n'
            repr += f'W0/S: {self._W0_S :_.1f} N/m²' + '\n'
            repr += '+' + '-' * 16 + '+\n'
            repr += (
                '|' + 'W0  : ' + (f'{self.M_tow :_.0f} Kg').center(10) + '|\n'
            )
            repr += (
                '|'
                + 'Wf  : '
                + (f'{self.fuel_weigh :_.0f} kg').center(10)
                + '|\n'
            )
            repr += (
                '|'
                + 'We  : '
                + (f'{self.empty_weigh :_.0f} kg').center(10)
                + '|\n'
            )
            for i, Wn in enumerate(self.weight_fraction):
                repr += (
                    '|' + f'W{i+1}W{i}: ' + (f'{Wn:.5f}').center(10) + '|\n'
                )
            repr += '+' + '-' * 16 + '+\n'
            return repr
