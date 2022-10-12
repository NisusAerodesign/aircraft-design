from src.pre_selection_core import *


class aircraft_selection_TW(aircraft_selection_core):
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

        # === Optional PARAMS ===
        self._T_W0 = None
        self._W0_S = None

    # GETTERS
    @property
    def wing_load(self) -> float:
        assert self._W0_S, "ERROR: you didn't set a wing load value!"
        return self._W0_S

    @property
    def thrust_to_weight_ratio(self) -> float:
        assert self._T_W0, "ERROR: you didn't set a thrust to weight ratio!"
        return self._T_W0

    # SETTERS
    @wing_load.setter
    def wing_load(self, W0_S: float):
        self._W0_S = W0_S
        self.__add_to_update__(self.__reload_SI_mass_props__)

    @thrust_to_weight_ratio.setter
    def thrust_to_weight_ratio(self, T_W0: float):
        self._T_W0 = T_W0
        self.__add_to_update__(self.__reload_SI_mass_props__)

    # === RELOADS ===
    def __reload_AR__(self):
        if self._T_W0 == None and self._W0_S == None:
            super().__reload_AR__()
        else:
            AR_function = Raymer.Raymer_AR_4_1(category=self._class_airplane)
            self._A = AR_function(self._mach)
            self.wing_span = (self._A * self._S) ** 0.5

    def __reload_SI_mass_props__(self):
        if self._T_W0 == None and self._W0_S == None:
            super().__reload_SI_mass_props__()

        elif self._T_W0 != None and self._W0_S != None:
            self.__reload_AR__()
            W0, Wf, We, n = self.__SI_mass_props__(
                Raymer.Raymer_We_6_1(
                    self._class_airplane,
                    self._A,
                    self._T_W0,
                    self._W0_S,
                    self._mach,
                )
            )

            self._W0, self._Wf, self._We, self._weight_fraction = (
                W0,
                Wf,
                We,
                n,
            )

            self._S = self._W0 * unit.g / self._W0_S
        else:
            assert False, 'Error: T/W0 and W0/S is not defined!'

    # === OVERLOAD ===
    def __repr__(self) -> str:
        if self._T_W0 == None and self._W0_S == None:
            return super().__repr__()
        else:
            self.__param_computate__()
            repr = f'Airplane: {self._code_name}' + '\n'
            repr += len(repr) * '=' + '\n'
            repr += f'first range: {self.first_range} km' + '\n'
            repr += f'second range: {self.second_range} km' + '\n\n'
            repr += f'AR: {round(self._A,2)}' + '\n'
            repr += f'Wing area: {round(self.wing_area,2)} m²' + '\n'
            repr += f'Wing wet area: {round(self._S_wetted,2)} m²' + '\n'
            repr += f'Wing spain: {round(self.wing_span,2)} m' + '\n\n'
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
