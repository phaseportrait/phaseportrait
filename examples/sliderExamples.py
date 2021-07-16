from phaseportrait import *
import matplotlib.pyplot as plt
import numpy as np

def dFDampedPendulum(theta, v):
    return v, -0.75*v-np.sin(theta)

DampedPendulum = PhasePortrait2D(dFDampedPendulum, [[-10,10],[-5, 5]], color='hola',Density=2, Title='Damped pendulum', xlabel=r"$\Theta$", ylabel=r"$\dot{\Theta}$")
# DampedPendulum.add_nullclines()
DampedPendulum.plot(color='inferno')

"""
Nullclines example
"""
def dFnull(x,y):
    return x + np.exp(-y), -y

null = PhasePortrait2D(dFnull, [[-10,10], [-5, 5]])
null.add_nullclines(precision=0.05)
null.plot()
plt.show()

"""
Example 1: sliders for 2 parameters
"""

def dFPolar(r, θ, *, μ=0.5,η=0):
    return μ*r*(1 - r*r), 1+η*θ


PolarCoordinates = PhasePortrait2D(dFPolar, [-3, 3], Polar=True, Title='Limit cicle')
PolarCoordinates.add_slider('μ', valinit=0.5)
PolarCoordinates.add_slider('η', valinit=0.0)
PolarCoordinates.add_nullclines()
PolarCoordinates.plot()

"""
Example 2: sliders for 4 parameters on the Love Affairs system
"""

def dFLoveAffairs(R, J, *, a=1, b=0, c=-1, d=1):
    return a*J + b*R, c*R + d*J


LoveAffairsPortrait = PhasePortrait2D(dFLoveAffairs, [-3, 3], Density=1.5, Title='Love Affairs', xlabel='R', ylabel='J')
LoveAffairsPortrait.add_slider('d', valinit=1)
LoveAffairsPortrait.add_slider('c', valinit=-1)
LoveAffairsPortrait.add_slider('b', valinit=0)
LoveAffairsPortrait.add_slider('a', valinit=1)
LoveAffairsPortrait.add_nullclines()

LoveAffairsPortrait.plot()

"""
Example 3: sliders for 4 parameters, showing a non-linear center
"""

def dFNonLinearCenter(x, y, *, a=1, b=1, c =1, d=1):
    return a*(y-b*y**3), -c*x-d*y**2

NonLinearCenterPortrait = PhasePortrait2D(dFNonLinearCenter, [-2,2], Density=2, Title='Non-linear center at (0,0)', xlabel='X', ylabel='Y')
NonLinearCenterPortrait.add_slider('d', valinit=1)
NonLinearCenterPortrait.add_slider('c', valinit=1)
NonLinearCenterPortrait.add_slider('b', valinit=1)
NonLinearCenterPortrait.add_slider('a', valinit=1)
NonLinearCenterPortrait.add_nullclines()

NonLinearCenterPortrait.plot()


plt.show()