#!/usr/bin/env python3
from avlwrapper import Case, Control, Parameter

from .classes import AircraftDesignError
from .classes.runner import __config_path__, __list_bin_path__

__AVL_LINK__ = 'https://github.com/NisusAerodesign/aircraft-design/releases/download/binaries/avl'
__XFOIL_LINK__ = 'https://github.com/NisusAerodesign/aircraft-design/releases/download/binaries/xfoil'

if not __config_path__ / 'avl' in __list_bin_path__:
    import os
    import stat

    import requests

    try:
        file_avl = requests.get(__AVL_LINK__)
        file_xfoil = requests.get(__XFOIL_LINK__)

        avl_path = str(__config_path__ / 'avl')
        xfoil_path = str(__config_path__ / 'xfoil')

        open(avl_path, 'wb').write(file_avl.content)
        open(xfoil_path, 'wb').write(file_xfoil.content)

        st_avl = os.stat(avl_path)
        st_xfoil = os.stat(xfoil_path)

        os.chmod(avl_path, st_avl.st_mode | stat.S_IEXEC)
        os.chmod(xfoil_path, st_xfoil.st_mode | stat.S_IEXEC)
    except:
        raise AircraftDesignError('Binary not found!')

from .classes import (
    Aircraft,
    FunctionRunner,
    MultiSession,
    Session,
    Wing,
    run_xfoil,
    Aifoil,
)
