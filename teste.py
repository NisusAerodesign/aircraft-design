from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from aircraft_design import Aircraft, Case, Control, Parameter, Session, Wing

if __name__ == '__main__':
    ...
    # wing = Wing(
    #     Path() / 'aircraft_design/basic_airfoils/S1223.dat',
    #     name='wing',
    #     wingspan=2.3,
    #     mean_chord=0.455,
    #     alpha_angle=1,
    #     taper_ratio=1.84375,
    #     transition_point=0.28,
    #     x_position=0.152,
    #     align=1,
    #     dihedral=3,
    # )

    # htail = Wing(
    #     Path() / 'aircraft_design/basic_airfoils/SD7032-NEG.dat',
    #     name='htail',
    #     wingspan=1.0,
    #     mean_chord=0.25,
    #     taper_ratio=1,
    #     x_position=1.45,
    #     z_position=0.445,
    # )

    # aircraft = Aircraft(
    #     0,
    #     reference_chord=0.455,
    #     reference_span=2.3,
    #     surfaces_list=[wing, htail],
    # )

    # aircraft.plot()
    # plt.show()

    # decolagem = Case(name='Decolagem', alpha=0)
    # session = Session(
    #     geometry=aircraft.geometry('aircraft'), cases=[decolagem]
    # )
    # results = session.run_all_cases()

    # surfaces = results[1]['StripForces']
    # for surface in surfaces:
    #     y_pos = surfaces[surface]['Yle']
    #     cl_pos = surfaces[surface]['cl']

    #     plt.plot(y_pos, cl_pos, 'x', label=surface)

    # plt.grid()
    # plt.legend()
    # plt.show()
