from configparser import ConfigParser
from pathlib import Path


def config_file():
    avl_path = Path.home() / '.local/bin/avl'

    config = ConfigParser()

    config['environment'] = {
        'Executable': avl_path.absolute(),
        'PrintOutput': 'no',
        'GhostscriptExecutable': 'gs',
    }

    config['output'] = {
        'Totals': 'yes',
        'SurfaceForces': 'yes',
        'StripForces': 'yes',
        'ElementForces': 'yes',
        'BodyAxisDerivatives': 'yes',
        'StabilityDerivatives': 'yes',
        'HingeMoments': 'yes',
        'StripShearMoments': 'yes',
    }

    with open('config.cfg', 'w') as config_file:
        config.write(config_file)
