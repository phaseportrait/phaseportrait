from phaseportrait import Cobweb, Map1D
from matplotlib import pyplot as plt

"""
Example 1: Logistic map cobweb plot and bifurcation diagram
"""

def Logistic(x, *, r=1.5):
    return r*x*(1-x)

# Create an instance of Map1D
Logistic_Map = Map1D(Logistic, [2,3.9], [0,1], 5000, thermalization=50, size=0.05)

# We want to plot for r in the range 0 < r <4. Every 0.005.
Logistic_Map.plot_over_variable('r', [0,4], 0.0005)

# Plot.
f, ax = Logistic_Map.plot()

# Cobweb plot and time series.
LogisticCobweb = Cobweb(Logistic, 0.2, [0,1], dF_args={'r':1.5}, yrange=[0,1])
LogisticCobweb.add_slider('r', valinit=1.5, valinterval=[0,4])
LogisticCobweb.initial_position_slider(valstep=0.01)
LogisticCobweb.plot()

# Show the plots.
plt.show()


"""
Example 2: Cubic map cobweb plot and bifurcation diagram
"""

def CubicMap(x, *, r=0.9):
        return r * x ** 3 + x * (1 - r)

CubicCobweb = Cobweb(CubicMap, 0.2, [-1,1], dF_args={'r':0.9}, Title='Cubic Map cobweb plot')
CubicCobweb.add_slider('r', valinit=1.5, valinterval=[0,4])
CubicCobweb.initial_position_slider(valstep=0.01)
CubicCobweb.plot()

Cubic_Map =  Map1D(CubicMap, [1,4], [-1,1], 1000, dF_args={'r':1}, thermalization=100, size=0.1, Title='Cubic Map')
Cubic_Map.plot_over_variable('r', [0,4], 0.0005)
Cubic_Map.plot()

plt.show()


"""
Example 3: Singer map cobweb plot and bifurcation diagram
"""

def SingerMap(x, *, r=0.9):
    return r * (7.86 * x - 23.31 * x ** 2 + 28.75 * x ** 3 - 13.3 * x ** 4)

SingerCobweb = Cobweb(SingerMap, 0.4, [0,1], dF_args={'r':0.9}, Title='Singer Map cobweb plot')
SingerCobweb.add_slider('r', valinit=0.5, valinterval=[0,1])
SingerCobweb.initial_position_slider(valstep=0.01)
SingerCobweb.plot()

Singer_Map =  Map1D(SingerMap, [0.9,1.075], [0,1], 1000, dF_args={'r':1}, thermalization=500, size=0.1, Title= 'Singer Map')
Singer_Map.plot_over_variable('r', [0.9,1.075], 0.0001)
Singer_Map.plot()

plt.show()

"""
Example 4: Logistic² map cobweb plot and bifurcation diagram
"""

def Logistic2(x, *, r=1.5):
        return Logistic(Logistic(x, r=r), r=r)

Logistic2Cobweb = Cobweb(Logistic2, 0.2, [0,1], dF_args={'r':1.5}, yrange=[0,1])
Logistic2Cobweb.add_slider('r', valinit=1.5, valinterval=[0,4])
Logistic2Cobweb.initial_position_slider(valstep=0.01)
Logistic2Cobweb.plot()

Logistic2_Map =  Map1D(Logistic2, [2.5,4], [0,1], 2000, dF_args={'r':1.5}, thermalization=500, size=0.05)
Logistic2_Map.plot_over_variable('r', [2.5, 3.98], 0.0005)
Logistic2_Map.plot()

plt.show()