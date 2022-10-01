#%% Library
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
from scipy.integrate import trapz
from scipy.interpolate import interp1d

#%% import data 
PATH_DATA = Path().absolute().parent / 'data'

airfoils = list(PATH_DATA.glob('*.dat'))
airfoils = sorted(airfoils, key=lambda x:x.name)

#%% functions
def area(air:str, title:str = None)-> float:
    
    x, y = np.loadtxt(air, skiprows=1, unpack=True)
    org = list(x).index(0)

    area = trapz(y[org:], x[org:]) - trapz(y[:org], x[:org])
    print(f'Area = {round(area,3)} [m²]')

    plt.plot(x,y, 'r', label = f'Area = {area} [m²]')
    plt.axis('equal')
    
    if not title == None:
        plt.title(title)
    plt.grid()
    plt.show()

    return area

# %%
