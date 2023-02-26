from aircraft_design.classes.xfoil_controler import run_xfoil
from aircraft_design.classes.runner import __config_path__



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