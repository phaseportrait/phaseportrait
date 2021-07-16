from phaseportrait import Trajectory2D, Trajectory3D
from matplotlib import pyplot as plt
import numpy as np

"""
IMPORTANT:

For each example, 3 or 4 plots will be created. In order to prevent your PC from hyperventillating, be sure that your programming environment doesn't plot all
of a sudden every example. If that happens, mark as False all examples except the one you want to visualize.
"""

if True:
    """
    Example 0: 2D trajectory. It can throw overflow error.
    """

    def dF(x,y,*, w=1, z=1):
        return w*np.sin(y*y*y), -z*np.exp(x*x)

    example = Trajectory2D(dF, n_points=1300, size=2, mark_start_position=True, Title='Just an example')
    example.initial_position(1,1)
    example.add_slider('w', valinterval=[-1,5])
    example.add_slider('z', valinterval=[-1,5])
    example.plot()
    plt.show()
    
if True:
    """
    Example 1: Nearby IC on Lorenz attractor
    """

    def Lorenz(x,y,z,*, s=10, r=28, b=8/3):
        return -s*x+s*y, -x*z+r*x-y, x*y-b*z

    a = Trajectory3D(Lorenz, lines=True, n_points=1300, size=3, mark_start_position=True, Title='Nearby IC on Lorenz attractor')
    a.initial_position(10,10,10)
    a.initial_position(10,10,10.0001)
    a.add_slider('r', valinterval=[24,30])
    a.plot()
    plt.show()


if True:
    """
    Example 2: Lorenz attractor. Printing a trajectory, using numba
    """

    def Lorenz(x,y,z,*, s=10, r=28, b=8/3):
        return -s*x+s*y, -x*z+r*x-y, x*y-b*z

    b = Trajectory3D(Lorenz, dF_args={'s':10, 'r':28, 'b':8/3}, n_points=4000, numba=True, color='t', size=2, Title='Lorenz attractor')
    b.initial_position(10,10,10)
    b.plot()
    plt.show()



if True:
    """
    Example 3: Rossler attractor
    """
    
    def Rossler(x,y,z,*, s=10, r=28, b=8/3):
        return -(y+z), s*y+x, b+z*(x-r)
    
    c = Trajectory3D(Rossler, Range=[20, 20,[0,40]], dF_args={'s':0.2, 'r':5.7, 'b':0.2}, n_points=20000, numba=True, thermalization=2000, size=4, Title= 'Rossler attractor')
    c.add_slider('r', valinit=5.7, valinterval=[0,10])
    c.thermalize()
    c.plot()
    plt.show()

if True:
    """
    Example 4: Halvorsen attractor
    """

    def Halvorsen(x,y,z, *, s=1.4):
        delta = (3*s+15)
        return -s*x+2*y-4*z-y**2+delta , -s*y+2*z-4*x-z**2+delta, -s*z+2*x-4*y-x**2+delta

    d = Trajectory3D(Halvorsen, dF_args={'s':1.4}, n_points=10000, thermalization=0, numba=True, size=2, mark_start_point=True, Title='Halvorsen attractor')
    d.initial_position(0,5,10)
    d.plot()
    plt.show()


if True:
    """
    Example 5: Thomas attractor
    """

    def Thomas(x,y,z,*, s=0.208186):
      return -s*x+np.sin(y), -s*y+np.sin(z), -s*z+np.sin(x)
    
    e = Trajectory3D(Thomas, dF_args={'s':0.208186}, n_points=30000, size=1, numba=True, thermalization=2000, Title='Thomas attractor')
    e.thermalize()
    e.plot()
    plt.show()

if True:
    """
    Example 6: Four-Wings attractor
    """
    def Four_wings(x,y,z,*, a=0.2, b=0.01, c=-0.4):
      return a*x+y*z, b*x+c*y-x*z, -z - x*y
    
    f = Trajectory3D(Four_wings,  n_points=10000, runge_kutta_freq=5, size=2, thermalization=2000, Title='Four-Wings attractor')
    f.add_slider('a', valinit=0.21, valinterval=[0.1,0.3], valstep=0.005)
    f.add_slider('b', valinit=0.01, valinterval=[0,0.3], valstep=0.005)
    f.add_slider('c', valinit=-0.4, valinterval=[-1,0], valstep=0.005)
    f.thermalize()
    f.plot()
    plt.show()

if True:
    """
    Example 7: Aizawa attractor
    """
    def Aizawa(x,y,z,*, a=0.95, b=0.7, c=0.6, d=3.5, e=0.25, f=0.1):
        return (z-b)*x - d*y, d*x + (z-b)*y, c + a*z - z*z*z/3 - (x*x + y*y) * (1 + e*z) + f*z*x*x*x

    g = Trajectory3D(Aizawa, n_points=10000, size=1, thermalization=2000, Title='Aizawa attractor')
    g.thermalize()
    g.add_slider('a', valinit=0.95, valinterval=[0,1], valstep=0.005)
    g.add_slider('b', valinit=0.7, valinterval=[0,1], valstep=0.005)
    g.add_slider('c', valinit=0.6, valinterval=[0,1], valstep=0.005)
    g.add_slider('d', valinit=3.5, valinterval=[0,4], valstep=0.05)
    g.add_slider('e', valinit=0.24, valinterval=[0,1], valstep=0.005)
    g.add_slider('f', valinit=0.1, valinterval=[0,1], valstep=0.005)
    g.plot()
    plt.show()


if True:
    """
    Example 8: Sprott attractor
    """

    def Sprott(x, y, z, *, a=2.07, b=1.79):
        return y + a*x*y + x*z, 1 - b*x*x + y*z, x - x*x - y*y

    h = Trajectory3D(Sprott, dF_args={'a':2.07, 'b':1.79}, n_points=10000, numba=True, size=1, thermalization=2000, Title='Sprott attractor')
    h.thermalize()
    h.add_slider('a', valinit=2.07, valinterval=[0,5])
    h.add_slider('b', valinit=1.79, valinterval= [0,5])
    h.plot()
    plt.show()