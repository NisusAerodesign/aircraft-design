#!/usr/bin/env python3
from aircraft_design.classes.aircraft import Aircraft
from aircraft_design.classes.errors import AircraftDesignError
from aircraft_design.classes.runner import (
    FunctionRunner,
    MultiSession,
    Session,
)
from aircraft_design.classes.wing import Wing
from aircraft_design.classes.xfoil_controler import run_xfoil
from aircraft_design.classes.airfoil import Airfoil