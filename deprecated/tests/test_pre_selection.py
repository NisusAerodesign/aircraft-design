import numpy as np

from src.pre_selection_core import *

airplane_New_York_to_Biggin_Hill = aircraft_pre_select(
    first_range=5542.0,
    second_range=19.0,
    b=20,
    S=49,
    LDmax=15.8,
    sfc_cruise=18.2,
    sfc_sea_level=12.0,
)

b = aircraft_selection(
    first_range=5542.0,
    second_range=19.0,
    LDmax=15.8,
    sfc_cruise=18.2,
    sfc_sea_level=12.0,
    wing_spain=20,
    wing_area=49,
)


def test_airplane_New_York_to_Biggin_Hill_Wo():
    Wo = round(airplane_New_York_to_Biggin_Hill.W0, 2)
    assert Wo == 13982.88, f'Wo is not correct!: {Wo}!=13982.88 kg'


def test_airplane_New_York_to_Biggin_Hill_WfW0():
    Wf = round(airplane_New_York_to_Biggin_Hill.Wf, 2)
    assert Wf == 4526.72, f'WfW0 is not correct!: {Wf}!=4526.72 kg'


def test_airplane_New_York_to_Biggin_Hill_We():
    We = round(airplane_New_York_to_Biggin_Hill.We, 2)
    assert We == 7671.16, f'We is not correct!: {We}!=7671.16 kg'


def test_airplane_New_York_to_Biggin_Hill_state_vector():
    state_vector = np.round(
        airplane_New_York_to_Biggin_Hill.weight_fraction, 3
    )
    state_vector_correct = np.array(
        [0.970, 0.980, 0.767, 0.991, 0.995, 0.980, 0.999, 0.991, 0.995]
    )
    assert all(
        np.equal(state_vector, state_vector_correct)
    ), f'State Vector is not correct!: {state_vector}!={state_vector_correct}'


def test_change_mach_to_affect_v_cruise():
    plane = airplane_New_York_to_Biggin_Hill
    plane.Mach = 0.5
    assert (
        plane.v_cruise == plane.Mach * plane.sound_speed
    ), f'v_cruise is not correct!: {plane.v_cruise}!={plane.Mach*plane.sound_speed}'


def test_change_sound_speed_to_affect_v_cruise():
    plane = airplane_New_York_to_Biggin_Hill
    plane.sound_speed = 200
    assert (
        plane.v_cruise == plane.Mach * plane.sound_speed
    ), f'v_cruise is not correct!: {plane.v_cruise}!={plane.Mach*plane.sound_speed}'


def test_change_fist_range():
    plane = airplane_New_York_to_Biggin_Hill
    plane.first_range = 3048
    assert (
        round(plane._f_range, 3) == 10_000_000
    ), f'Unsuccessful conversion to feet!: {round(plane._f_range, 3)} != 1e7 ft'
