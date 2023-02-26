import matplotlib.pyplot as plt
from aircraft_design import Wing, Aircraft
from pathlib import Path

def test_dimentions_geometry_taper():
    wing = Wing('aircraft_design/basic_airfoils/S1223.dat', 2.3, 0.5, 2, 0.5, sweep_angle=0, align='TE', name='wing')
    tail = Wing('aircraft_design/basic_airfoils/SD7032-NEG.dat', 1, 0.5, x_position=1.1, z_position=0.25, name='tail')
    airplane = Aircraft(0, 0.5, 2.3, [wing, tail])
    airplane_geom = airplane.geometry('airplane')
    x_pos_real = airplane_geom.surfaces[0].sections[1].leading_edge_point.x
    assert x_pos_real == 0.0, 'Posicionamento da sessão de transição!'


def test_dimentions_geometry_taper_and_sweep():
    wing = Wing('aircraft_design/basic_airfoils/S1223.dat', 2.3, 0.5, 2, 0.5, sweep_angle=45, align='TE', name='wing')
    tail = Wing('aircraft_design/basic_airfoils/SD7032-NEG.dat', 1, 0.5, x_position=1.1, z_position=0.25, name='tail')
    airplane = Aircraft(0, 0.5, 2.3, [wing, tail])
    airplane_geom = airplane.geometry('airplane')
    x_pos_real = airplane_geom.surfaces[0].sections[1].leading_edge_point.x
    assert round(x_pos_real,3) == 0.575, 'Posicionamento da sessão de transição!'