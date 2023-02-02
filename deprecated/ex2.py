#%%
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

dat = Path('airfoils', 'clxalpha.dat')

alpha, cl = np.loadtxt(dat, usecols=(0, 1), skiprows=11, unpack=True)


cla = (cl[2] - cl[1]) / (alpha[2] - alpha[1])
y = lambda x: cla * x + cl[0]
ya = cl[list(alpha).index(18)]

plt.plot(alpha, cl, 'b', label='viscoso')
plt.plot(alpha, y(alpha), 'r', label='potencial')
plt.plot(18, y(18), 'ro', label=f'(18, {round(y(18),3)})')
plt.plot(18, ya, 'bo', label=f'(18, {round(ya,3)})')

plt.title(r'Curva Cl x $\alpha$ SC(2)-0614')
plt.xlabel(r'$\alpha$')
plt.ylabel(r'$C_l$')

plt.legend()
plt.grid()
plt.savefig('clxalpha', dpi=720, type='png')
plt.show()
