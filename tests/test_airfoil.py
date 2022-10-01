#%% Library
from src.airfoil import *

#%% testes
A = []
for air in airfoils:
    A.append(area(air,title=air.name))
# %%
