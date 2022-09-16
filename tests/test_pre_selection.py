import numpy as np
from src.pre_selection import *

airplane_New_York_to_Biggin_Hill = aircraft_pre_select(
    first_range=5542.0,
    second_range=19.0,
    LDmax=15.8,
    sfc_cruize=18.2,
    sfc_sea_level=12.0,
)

(
    Wo,
    Wf,
    We,
    state_vector,
) = airplane_New_York_to_Biggin_Hill.mission_estimation()

Wo, We, Wf, state_vector = (
    np.round(Wo, 2),
    np.round(We, 2),
    np.round(Wf, 3),
    np.round(state_vector, 3),
)


def test_airplane_New_York_to_Biggin_Hill_Wo():
    assert Wo == 13982.88, f'Wo is not correct!: {Wo}!=13982.88 kg'


def test_airplane_New_York_to_Biggin_Hill_WfW0():
    assert Wf == 4526.72, f'WfW0 is not correct!: {Wf}!=4526.72 kg'


def test_airplane_New_York_to_Biggin_Hill_We():
    assert We == 7671.16, f'We is not correct!: {We}!=7671.16 kg'


def test_airplane_New_York_to_Biggin_Hill_state_vector():
    state_vector_correct = np.array(
        [0.970, 0.980, 0.767, 0.991, 0.995, 0.980, 0.999, 0.991, 0.995]
    )
    assert all(
        np.equal(state_vector, state_vector_correct)
    ), f'State Vector is not correct!: {state_vector}!={state_vector_correct}'


def test_change_mach_to_affect_v_cruize():
    plane = airplane_New_York_to_Biggin_Hill
    plane.Mach = 0.5
    assert (
        plane.v_cruize == plane.Mach * plane.sound_speed
    ), f'v_cruize is not correct!: {plane.v_cruize}!={plane.Mach*plane.sound_speed}'


def test_change_sound_speed_to_affect_v_cruize():
    plane = airplane_New_York_to_Biggin_Hill
    plane.sound_speed = 200
    assert (
        plane.v_cruize == plane.Mach * plane.sound_speed
    ), f'v_cruize is not correct!: {plane.v_cruize}!={plane.Mach*plane.sound_speed}'


def test_change_fist_range():
    plane = airplane_New_York_to_Biggin_Hill
    plane.first_range = 3048
    assert (
        round(plane._f_range, 3) == 10_000_000
    ), f'Unsuccessful conversion to feet!: {round(plane._f_range, 3)} != 1e7 ft'
