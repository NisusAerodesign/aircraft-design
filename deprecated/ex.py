#%% Librarys
import matplotlib.pyplot as plt
import numpy as np
import src.Aircraft_Classes as ac
import avlwrapper as avl

from src.builder import config_file
from pathlib import Path

#%% Paths
PATH_CASE = Path('avlCases')
PATH_DATA = Path('data')
PATH_AIRF = Path('airfoils').absolute()

#%% Constantes
Rsp = 287.15
gamma = 1.4
T0 = 288.15
LA = -0.0065
rho0 = 1.225
g = 9.81

#%% Functions generic


def T(H: float) -> float:
    return T0 + LA * H


def rho(H: float) -> float:
    return rho0 * (T(H) / T0) ** (-g / LA / Rsp - 1)


def soundSpeed(H: float) -> float:
    return np.sqrt(gamma * Rsp * T(H))


#%% Functions geometry
def root_chord(chord: float, taper_ratio: float) -> float:
    return 2 * chord * taper_ratio / (1 + taper_ratio)


def tip_chord(chord: float, taper_ratio: float) -> float:
    return 2 * chord / (1 + taper_ratio)


def transition_chord(
    chord: float, taper_ratio: float, transition_point: float
) -> float:
    Ct = 2 * chord / (1 + taper_ratio)
    Cr = 2 * chord * taper_ratio / (1 + taper_ratio)
    return Cr * (1 - transition_point) + Ct * transition_point


#%% Head
config_file()
cfg_path = Path('src', './config.cfg')
my_config = avl.Configuration(cfg_path)

airfoil_wing = Path(PATH_AIRF, 'SC(2)-0614.dat')
airfoil_empennage = Path(PATH_AIRF, 'SD7032-NEG.dat')
elevator = avl.Control(name='elevator', gain=1, x_hinge=0.75, duplicate_sign=1)
flap_fowler = avl.Control(name='flap', gain=1, x_hinge=0.7, duplicate_sign=1)

b = 21.55
sweep = 28
dx = (b / 4) * np.tan(sweep * np.pi / 180)
Ctr = transition_chord(2.4, 2, 0.5)
Cr = root_chord(2.4, 2)
Ct = tip_chord(2.4, 2)
Cmean = 2.4
print(root_chord(2.4, 2), tip_chord(2.4, 2))
#%% Aeronave em decolagem e Pouso
flap = ac.wing(
    airfoil=airfoil_wing,
    wingspan=b * 0.5,
    mean_chord=(Cr + Ctr) / 2 * 1.43,
    taper_ratio=Cr / Ctr,
    sweep_angle=28.0,
    x_position=9.70,
    control=[flap_fowler],
    name='wing_fowler_flap',
)

wingFlap = ac.wing(
    airfoil=airfoil_wing,
    wingspan=b * 0.5,
    mean_chord=(Ctr + Ct) / 2,
    taper_ratio=Ctr / Ct,
    sweep_angle=28.0,
    x_position=dx + 9.70,
    y_position=b / 4,
    name='wing',
)


#%% Aeronave em cruzeiro

wing = ac.wing(
    airfoil=airfoil_wing,
    wingspan=b,
    mean_chord=(Cr + Ct) / 2,
    taper_ratio=Cr / Ct,
    sweep_angle=28.0,
    x_position=9.70,
    y_position=0,
    name='wing',
)

#%% Empenagens

empennage = ac.wing(
    airfoil=airfoil_empennage,
    wingspan=9.982,
    mean_chord=1.15,
    taper_ratio=2.0,
    sweep_angle=25.0,
    x_position=19.61,
    z_position=6.1,
    control=[elevator],
    name='empennage_H',
)

#%% Plot
fig, aux = flap.plot()
fig, aux = wingFlap.plot(fig, aux)
fig, aux = empennage.plot(fig, aux)
plt.show()

# fig, aux = wing.plot()
# fig, aux = empennage.plot(fig, aux)
# plt.show()


#%% Geometry
f = flap.surface
wf = wingFlap.surface
w = wing.surface
e = empennage.surface
aircraft_deco = avl.Geometry(
    name='aircraft_deco',
    reference_area=wingFlap.reference_area + flap.reference_area,
    reference_chord=Cmean,
    reference_span=b,
    reference_point=avl.Point(x=0, y=0, z=0),
    mach=0,
    z_symmetry=avl.Symmetry.symmetric,
    z_symmetry_plane=0.916 * 1.1,
    surfaces=[f, wf, e],
)

aircraft_cruz = avl.Geometry(
    name='aircraft_cruz',
    reference_area=wing.reference_area,
    reference_chord=wing.c,
    reference_span=wing.b,
    reference_point=avl.Point(x=0, y=0, z=0),
    mach=0,
    surfaces=[w, e],
)
#%% Constantes
W = 18_000 * 9.81
Sref = 51.52
Clmax = 2.243
Clfunc = lambda rho, v: W / (0.5 * rho * Sref * v**2)


# Cruzeiro

rhoCru = rho(11_000)
vCru = 0.8 * soundSpeed(11_000)
ClCru = Clfunc(rho=rhoCru, v=vCru)

paramCru = {
    'CL': ClCru,
    'velocity': vCru,
    'density': rhoCru,
    'Ixx': 51.492,
    'Iyy': 173.410,
    'Izz': 132.225,
    'mass': 18000 * 0.97 * 0.985,
    'X_cg': 12.04,
    'Z_cg': 0.348,
}

# Rolagem Decolagem
vstall = np.sqrt(W / (0.5 * rho0 * Sref * Clmax))
vRD = 1.1 * vstall
ClRD = Clfunc(rho=rho0, v=vRD)
paramRD = {
    'alpha': 3,
    'velocity': vRD,
    'CL': ClRD,
    'Ixx': 51.492,
    'Iyy': 173.410,
    'Izz': 132.225,
    'mass': 18000,
    'X_cg': 12.04,
    'Z_cg': 0.348,
}
#%% Análises cruzeiro
trim_param = avl.Parameter(name='elevator', setting='Cm', value=0.0)
trim_param2 = avl.Parameter(name='alpha', setting='CL', value=ClCru)
trim_case = avl.Case(
    name='trimmed', elevator=trim_param, alpha=trim_param2, **paramCru
)

session = avl.Session(
    geometry=aircraft_cruz, cases=[trim_case], config=my_config
)
savePath = Path(PATH_CASE, aircraft_cruz.name)
session.export_run_files(savePath)
results = session.run_all_cases()
# print(f"Elevator ={results['trimmed']['Totals']}")
# %% Análises Rolagem da decolagem
trim_param = avl.Parameter(name='elevator', setting='Cm', value=0.0)
deco_param = avl.Parameter(name='flap', setting='CL', value=ClRD)

case = avl.Case(
    name='trimdeco',
    flap_fowler=deco_param,
    elevator=trim_param,
    **paramRD,
)

session = avl.Session(geometry=aircraft_deco, cases=[case], config=my_config)
savePath = Path(PATH_CASE, aircraft_deco.name)
session.export_run_files(savePath)
results = session.run_all_cases()
# %%
