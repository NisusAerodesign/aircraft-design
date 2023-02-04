#!/usr/bin/env python3
from aircraft_design.classes.runner import __config_path__, __list_bin_path__
from aircraft_design.classes import AircraftDesignError
from pathlib import Path
from shutil import copy


if not __config_path__ / 'avl' in __list_bin_path__:
    try:
        file = input('Input path to binary AVL file: ')
        file = Path(file).absolute()
        copy(str(file), str(__config_path__ / 'avl'))
    except:
        raise AircraftDesignError('Binary not found!')

from aircraft_design.classes import Aircraft, Wing
