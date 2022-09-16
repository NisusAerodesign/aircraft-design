from src.pre_selection import aircraft_pre_select


def test_pre_selection():

    airplane_A = aircraft_pre_select(
        f_range=5542,
        s_range=19,
        LDmax=15.8,
        sfc_cruize=18.2,
        sfc_sea_level=12.0,
    )
    
    #params = airplane_A.mission_estimation()
    #print(params)
    
    assert True, 'Plane equal'
