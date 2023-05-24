import matplotlib.pyplot as plt

import phaseportrait
from phaseportrait.streamlines import *


def dF(x,y,z):
    return -x, -y, -z

p1 = phaseportrait.PhasePortrait3D(dF, [-3, 3])
p1.plot()
plt.show()



def dF(x,y,z, *, w=1):
    return -y, x, -z + w


p2 = phaseportrait.PhasePortrait3D(dF, [-3, 3], MeshDim=8, maxLen=2500, deltat=0.05)

p2.add_slider('w')

p2.plot(color='viridis', grid=False)
plt.show()
