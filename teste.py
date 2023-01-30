from pathlib import Path
from builder import config_file
import avlwrapper as avl
import numpy as np

config_file()

cfg_path = Path('./config.cfg')
my_config = avl.Configuration(cfg_path)

# Definições da asa
b_wing = 1.9   # m
C_wing = 0.4   # m
taper_ratio = 2   # Croot/Ctip
d_transition = 0.5   # Ponto de transição da corda

Ct_wing = 2 * C_wing / (1 + taper_ratio)
Cr_wing = 2 * C_wing * taper_ratio / (1 + taper_ratio)

b_2_wing = b_wing / 2
xwing = 0

inc = 0   # graus

# Estabilisador horizontal
b_elevator = 1.0
d_elevator = 1.2
C_elevator = 0.25
h_elevator = 0.3

Ct_elevator = 2 * C_elevator / (1 + taper_ratio)
Cr_elevator = 2 * C_elevator * taper_ratio / (1 + taper_ratio)

b_2_elevator = b_elevator / 2

# condições
h_efeito_solo = 0.17   # m


"""Construção da geometria"""
airfoil_wing = avl.FileAirfoil('airfoils/NP2022.dat')
airfoil_Tail = avl.FileAirfoil('airfoils/SD7032-NEG.dat')

wing_root = avl.Point(xwing, y=0, z=0)
wing_tr = avl.Point(xwing, y=d_transition * b_2_wing, z=0)
wing_tip = avl.Point(xwing, y=b_2_wing, z=0)


root_section = avl.Section(
    leading_edge_point=wing_root,
    chord=Cr_wing,
    airfoil=airfoil_wing,
    angle=inc,
)
tr_section = avl.Section(
    leading_edge_point=wing_tr, chord=Cr_wing, airfoil=airfoil_wing, angle=inc
)
tip_section = avl.Section(
    leading_edge_point=wing_tip, chord=Ct_wing, airfoil=airfoil_wing, angle=inc
)

wing = avl.Surface(
    name='wing',
    n_chordwise=10,
    chord_spacing=avl.Spacing.cosine,
    n_spanwise=25,
    span_spacing=avl.Spacing.neg_sine,
    y_duplicate=0.0,
    sections=[root_section, tr_section, tip_section],
)

elevator = avl.Control(name='elevator', gain=1, x_hinge=0.6, duplicate_sign=1)
elevator_root = avl.Point(d_elevator, 0, h_elevator)
elevator_tip = avl.Point(x=d_elevator, y=b_2_elevator, z=h_elevator)

root_section = avl.Section(
    leading_edge_point=elevator_root,
    chord=Cr_elevator,
    airfoil=airfoil_Tail,
    controls=[elevator],
)
tip_section = avl.Section(
    leading_edge_point=elevator_tip,
    chord=Ct_elevator,
    airfoil=airfoil_Tail,
    controls=[elevator],
)

horizontal_tail = avl.Surface(
    name='horizontal_tail',
    n_chordwise=10,
    chord_spacing=avl.Spacing.cosine,
    n_spanwise=15,
    span_spacing=avl.Spacing.cosine,
    y_duplicate=0.0,
    sections=[root_section, tip_section],
)

ref_pnt = avl.Point(x=0, y=0, z=0)

aircraft = avl.Geometry(
    name='aircraft',
    reference_area=b_wing * C_wing,
    reference_chord=C_wing,
    reference_span=b_wing,
    reference_point=ref_pnt,
    mach=0,
    z_symmetry=avl.Symmetry.symmetric,
    z_symmetry_plane=-h_efeito_solo,
    surfaces=[wing, horizontal_tail],
)

trim_param = avl.Parameter(name='elevator', setting='Cm', value=0.0)
decolagem = avl.Case(name='Decolagem', alpha=0, elevator=trim_param)

session = avl.Session(geometry=aircraft, cases=[decolagem], config=my_config)
results = session.run_all_cases()
print(results)
# session.show_geometry()
# if 'gs_bin' in session.config.settings:
#     img = session.save_geometry_plot(file_format='png')[0]
#     #avl.show_image(img)
# else:
#     session.show_geometry()
