#!/usr/bin/env python3
from .classes.runner import __config_path__, __list_bin_path__
from .classes import AircraftDesignError
import requests
from pathlib import Path
from shutil import copy

__AVL_LINK__ = 'https://github.com/NisusAerodesign/aircraft-design/releases/download/binaries/avl'

if not __config_path__ / 'avl' in __list_bin_path__:
    try:
        file = requests.get(__AVL_LINK__)
        open(str(__config_path__ / 'avl'), 'wb').write(file.content)
        # file = input('Input path to binary AVL file: ')
        # file = Path(file).absolute()
        # copy(str(file), str(__config_path__ / 'avl'))
    except:
        raise AircraftDesignError('Binary not found!')

from .classes import Aircraft, Wing, Session, MultiSession
