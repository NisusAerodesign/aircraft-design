#!/usr/bin/env python3
from pathlib import Path

import avlwrapper as avl
import matplotlib.pyplot as plt
import numpy as np

from aircraft_design.classes import AircraftDesignError


def __correct_angle_sweep__(
    align: str, b: float, sweep: float, ct: float, tr: float
) -> float:
    if align == 'C':
        return sweep + (180 / np.pi) * np.arctan(ct * (tr - 1) / b)
    elif align == 'TE':
        return sweep + (180 / np.pi) * np.arctan(2 * ct * (tr - 1) / b)
    elif align == 'LE':
        return sweep
    else:
        raise AircraftDesignError(f'Align {align} not recognize')


"""ESTRUTURAÇÃO DA ASA"""


class Wing:
    def __init__(
        self,
        airfoil: Path | str,
        name: str,
        wingspan: float,
        mean_chord: float,
        taper_ratio: float = 1.0,
        transition_point: float = 0.0,
        alpha_angle: float = 0.0,
        sweep_angle: float = 0.0,
        x_position: float = 0.0,
        y_position: float = 0.0,
        z_position: float = 0.0,
        dihedral: float = 0.0,
        align: float = 0.0,
        control: list = [None],
        panel_chordwise: int = 10,
        panel_spanwise: int = 25,
    ):
        self.airfoil = Path(airfoil) if type(airfoil) == str else airfoil
        self.b = wingspan
        self.c = mean_chord
        self.tr = taper_ratio
        self.tp = transition_point
        self.alpha = alpha_angle
        self.sweep = sweep_angle
        self.xp = x_position
        self.yp = y_position
        self.zp = z_position
        self.dihedral = dihedral
        self.name = name
        self.__align = align
        self.control = control
        self.panel_chordwise = panel_chordwise
        self.panel_spanwise = panel_spanwise

        self.cr = 2 * self.c * self.tr / (1 + self.tr)
        self.ct = 2 * self.c / (1 + self.tr)

        self.__delta_ct = lambda b, Delta: b / 2 * np.sin(np.radians(Delta))

        if align > 1 or align < 0:
            raise AircraftDesignError(f'Align {align} not recognize')
        else:
            self.__dif = (self.cr - self.ct) * self.__align

    @property
    def align(self) -> float:
        return self.__align

    @align.setter
    def align(self, percent: float):
        if percent > 1 or percent < 0:
            raise AircraftDesignError(f'Align {percent} not recognize')
        else:
            self.__align = percent
            self.__dif = (self.cr - self.ct) * self.__align

    @property
    def surface(self) -> avl.Surface:
        return self.__mount_wing__()

    @property
    def reference_area(self) -> float:
        return self.c * self.b

    def __mount_wing__(self) -> avl.Surface:
        airfoil_path = str(self.airfoil.absolute())

        d_sweep_tra = 0.5 * self.tp * self.b * np.tan(self.sweep * np.pi / 180)
        d_sweep_tip = 0.5 * self.b * np.tan(self.sweep * np.pi / 180)

        pto_wrt = avl.Point(self.xp, self.yp, self.zp)   # root
        pto_wtp = avl.Point(
            self.xp + d_sweep_tip + self.__dif,
            self.yp + 0.5 * self.b,
            self.zp + self.__delta_ct(self.b, self.dihedral),
        )   # tip

        root_section = avl.Section(
            leading_edge_point=pto_wrt,
            chord=self.cr,
            airfoil=avl.FileAirfoil(airfoil_path),
            angle=self.alpha,
            controls=self.control,
        )

        tip_section = avl.Section(
            leading_edge_point=pto_wtp,
            chord=self.ct,
            airfoil=avl.FileAirfoil(airfoil_path),
            angle=self.alpha,
            controls=self.control,
        )

        if self.tp > 0:
            pto_wtr = avl.Point(
                self.xp + d_sweep_tra,
                self.yp + 0.5 * self.tp * self.b,
                self.zp,
            )   # transition

            transition_section = avl.Section(
                leading_edge_point=pto_wtr,
                chord=self.cr,
                airfoil=avl.FileAirfoil(airfoil_path),
                angle=self.alpha,
                controls=self.control,
            )

            sections = [root_section, transition_section, tip_section]
        else:
            sections = [root_section, tip_section]

        wing = avl.Surface(
            name=self.name,
            n_chordwise=self.panel_chordwise,
            chord_spacing=avl.Spacing.cosine,
            n_spanwise=self.panel_spanwise,
            span_spacing=avl.Spacing.neg_sine,
            y_duplicate=0.0,
            sections=sections,
        )
        return wing

    def plot(
        self,
        figure=None,
        axis=None,
        linewidth: float = 1.0,
        color: str = 'black',
    ):
        if figure == None and axis == None:
            figure = plt.figure()
            axis = figure.add_subplot(projection='3d')
        elif (figure == None) ^ (axis == None):
            assert False, 'Impossível receber apenas um parâmetro!'

        d_sweep_roo = 0.0
        d_sweep_tip = 0.5 * self.b * np.tan(self.sweep * np.pi / 180)
        d_sweep_tra = 0.5 * self.tp * self.b * np.tan(self.sweep * np.pi / 180)

        air = np.loadtxt(self.airfoil, skiprows=1)

        al = -self.alpha * np.pi / 180
        Rot = np.array([[np.cos(al), -np.sin(al)], [np.sin(al), np.cos(al)]])
        air = np.dot(Rot, air.T).T

        inc_x = np.cos(al)
        inc_z = np.sin(al)

        wing_a_x = air[:, 0]
        wing_a_z = air[:, 1]

        pos_r = self.xp
        pos_t = self.xp
        wing_x = [
            pos_t + d_sweep_tip + self.ct * wing_a_x + self.__dif,
            pos_r + d_sweep_tra + self.cr * wing_a_x,
            pos_r + d_sweep_roo + self.cr * wing_a_x,
            pos_r + d_sweep_roo + self.cr * wing_a_x,
            pos_r + d_sweep_tra + self.cr * wing_a_x,
            pos_t + d_sweep_tip + self.ct * wing_a_x + self.__dif,
        ]

        pos_r = 0
        pos_t = 0.5 * self.b
        delta_tp = self.__delta_ct(self.b, self.dihedral)
        wing_z = [
            self.ct * wing_a_z + delta_tp,
            self.cr * wing_a_z,
            self.cr * wing_a_z,
            self.cr * wing_a_z,
            self.cr * wing_a_z,
            self.ct * wing_a_z + delta_tp,
        ]

        wing_y = [
            -self.yp - pos_t + 0 * wing_a_z,
            -self.yp - self.tp * pos_t + 0 * wing_a_z,
            -self.yp + pos_r + 0 * wing_a_z,
            self.yp + pos_r + 0 * wing_a_z,
            self.yp + self.tp * pos_t + 0 * wing_a_z,
            self.yp + pos_t + 0 * wing_a_z,
        ]

        for i, _ in enumerate(wing_x):
            axis.plot(
                wing_x[i],
                wing_y[i],
                self.zp + wing_z[i],
                c=color,
                linewidth=linewidth,
            )
        # Plot das linhas bordo de atk
        axis.plot(
            [
                self.xp + d_sweep_tip + self.__dif,
                self.xp + d_sweep_tra,
                self.xp + d_sweep_roo,
            ],
            [
                -self.yp - 0.5 * self.b,
                -self.yp - 0.5 * self.tp * self.b,
                -self.yp + 0,
            ],
            [self.zp + delta_tp, self.zp, self.zp],
            c=color,
            linewidth=linewidth,
        )
        axis.plot(
            [
                self.xp + d_sweep_roo,
                self.xp + d_sweep_tra,
                self.xp + d_sweep_tip + self.__dif,
            ],
            [
                self.yp + 0,
                self.yp + 0.5 * self.tp * self.b,
                self.yp + 0.5 * self.b,
            ],
            [self.zp, self.zp, self.zp + delta_tp],
            c=color,
            linewidth=linewidth,
        )
        # Linhas de bordo de fuga
        axis.plot(
            [
                self.xp + d_sweep_tip + self.ct * inc_x + self.__dif,
                self.xp + d_sweep_tra + self.cr * inc_x,
                self.xp + d_sweep_roo + self.cr * inc_x,
            ],
            [
                -self.yp - 0.5 * self.b,
                -self.yp - 0.5 * self.tp * self.b,
                -self.yp + 0,
            ],
            [
                self.zp + self.ct * inc_z + delta_tp,
                self.zp + self.cr * inc_z,
                self.zp + self.cr * inc_z,
            ],
            c=color,
            linewidth=linewidth,
        )
        axis.plot(
            [
                self.xp + d_sweep_roo + self.cr * inc_x,
                self.xp + d_sweep_tra + self.cr * inc_x,
                self.xp + d_sweep_tip + self.ct * inc_x + self.__dif,
            ],
            [
                self.yp + 0,
                self.yp + 0.5 * self.tp * self.b,
                self.yp + 0.5 * self.b,
            ],
            [
                self.zp + self.cr * inc_z,
                self.zp + self.cr * inc_z,
                self.zp + self.ct * inc_z + delta_tp,
            ],
            c=color,
            linewidth=linewidth,
        )

        axis.axis('equal')
        return figure, axis
