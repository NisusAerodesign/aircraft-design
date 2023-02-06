#!/usr/bin/env python3
from .classes.runner import __config_path__, __list_bin_path__
from .classes import AircraftDesignError
from pathlib import Path
from shutil import copy


if not __config_path__ / 'avl' in __list_bin_path__:
    try:
        file = input('Input path to binary AVL file: ')
        file = Path(file).absolute()
        copy(str(file), str(__config_path__ / 'avl'))
    except:
        raise AircraftDesignError('Binary not found!')

from .classes import Aircraft, Wing, Session, MultiSession
