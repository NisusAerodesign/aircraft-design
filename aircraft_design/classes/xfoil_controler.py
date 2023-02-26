import tempfile
import subprocess
import numpy as np
from pathlib import Path
from aircraft_design.classes.runner import __config_path__

def input_file(path:Path, airfoil_name:Path, Re:float, alpha_i:float, 
                alpha_f:float, alpha_step:float=0.5, n_iter:int=100):
    
    path = str(path.absolute()) if type(path) != str else path
    airfoil_name = str(airfoil_name.absolute()) if type(airfoil_name) != str else airfoil_name

    with open(f'{path}/input_file.in', 'w') as input_file:
        input_file.write(f'LOAD {airfoil_name}.dat\n')
        input_file.write(airfoil_name + '\n')
        input_file.write('PANE\n')
        input_file.write('OPER\n')
        input_file.write(f'Visc {Re}\n')
        input_file.write('PACC\n')
        input_file.write('polar_file.txt\n\n')
        input_file.write(f'ITER {n_iter}\n')
        input_file.write(f'ASeq {alpha_i} {alpha_f} {alpha_step}\n')
        input_file.write('\n\n')
        input_file.write('quit\n')

def run_xfoil(bin_path:Path, airfoil_name:Path, Re:float, alpha_i:float, 
                alpha_f:float, alpha_step:float=0.5, n_iter:int=100):
    
    bin_path = str(bin_path.absolute())

    with tempfile.TemporaryDirectory(prefix='xfoil_') as temp_dir:

        input_file(path=temp_dir, airfoil_name=airfoil_name, Re=Re, 
                   alpha_i=alpha_i, alpha_f=alpha_f, alpha_step=alpha_step, n_iter=n_iter)

        subprocess(f'./{bin_path} < {temp_dir}/input_file.in', shell=True)

if __name__ == '__main__':
    airfoil_name = 'NACA0012'
    alpha_i = 0
    alpha_f = 10
    alpha_step = 0.25
    Re = 1000000
    n_iter = 100

    bin_path = __config_path__/'xfoil'

    # subprocess.call('./aircraft_design/bin/xfoil < input_file.in', shell=True)

    # polar_data = np.loadtxt('polar_file.txt', skiprows=12)

    run_xfoil(bin_path, airfoil_name, Re, alpha_i, 
                alpha_f, alpha_step=0.5, n_iter=100)