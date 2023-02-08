from aircraft_design import Wing, Aircraft, Session
from avlwrapper import Parameter, Case
from pathlib import Path

airfoil_a = Path('basic_airfoils/E423.dat')
airfoil_b= Path('basic_airfoils/SD7032-NEG.dat')
def test_just_create_wing():
    main_wing = Wing(airfoil=airfoil_a, wingspan=1.8, mean_chord=0.5).surface
    return True

def test_just_create_aircraft():
    main_wing = Wing(airfoil=airfoil_a, wingspan=1.8, mean_chord=0.5).surface
    main_eh = Wing(airfoil=airfoil_b, wingspan=0.8, mean_chord=0.24).surface

    my_plane = Aircraft(
        mach=0,
        ground_effect=0,
        reference_chord=0.5,
        reference_span=1.8,
        surfaces_list=[main_eh, main_wing]
    )
    return True

def test_run_simple_session():
    main_wing = Wing(airfoil=airfoil_a, wingspan=1.8, mean_chord=0.5)
    main_eh = Wing(airfoil=airfoil_b, wingspan=0.8, mean_chord=0.24)

    aircraft = Aircraft(
        mach=0,
        ground_effect=0,
        reference_chord=0.5,
        reference_span=1.8,
        surfaces_list=[main_eh, main_wing]
    ).geometry('my_plane')

    trim_param = Parameter(name='elevator', setting='Cm', value=0.0)
    decolagem = Case(name='Decolagem', alpha=0, elevator=trim_param)

    session = Session(geometry=aircraft, cases=[decolagem])
    results = session.run_all_cases()
    return True