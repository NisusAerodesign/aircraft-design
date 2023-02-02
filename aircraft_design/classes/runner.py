import avlwrapper as avl

from configparser import ConfigParser
from aircraft_design.classes.errors import AircraftDesignError
from pathlib import Path
import shutil

__config_path__ = Path(__file__).parent.parent.absolute() / 'bin'

__list_bin_path__ = [file for file in __config_path__.iterdir()]

__config_file__ = ConfigParser()

__config_file__['environment'] = {
    'Executable': __config_path__/'avl',
    'PrintOutput': 'no',
    'GhostscriptExecutable': 'gs',
}

__config_file__['output'] = {
    'Totals': 'yes',
    'SurfaceForces': 'yes',
    'StripForces': 'yes',
    'ElementForces': 'yes',
    'BodyAxisDerivatives': 'yes',
    'StabilityDerivatives': 'yes',
    'HingeMoments': 'yes',
    'StripShearMoments': 'yes',
}

with open(__config_path__/'config.cfg', 'w') as config_file:
    __config_file__.write(config_file)
    
__cfg_path__ = __config_path__/'config.cfg'

class Session(avl.Session):
    def __init__(self, geometry, cases=None, name=None):
        self.config = __cfg_path__
        super().__init__(geometry, cases, name, config=self.config)

