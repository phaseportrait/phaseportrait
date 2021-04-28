import numpy as np

from .exceptions import *
from .utils import utils
from matplotlib.widgets import Slider as matplot_slider

class Slider():
    def __init__(self, portrait, param_name, valinit=None, valstep=0.1, valinterval=[]):
        self.portrait = portrait
        self.param_name = param_name
        self.value = valinit
        
        valinterval = utils.construct_interval_1d(valinterval)
        valinterval = np.array(valinterval)
 
        if 'Trajectory' in self.portrait._name_: 
            self.ax = self.portrait.sliders_fig.add_axes([0.25, 0.88 - 0.05*len(self.portrait.sliders), 0.4, 0.05])

        if 'PhasePortrait' in self.portrait._name_:
            self.ax = self.portrait.fig.add_axes([0.25, 0.015 + 0.05*len(self.portrait.sliders), 0.4, 0.03])

        
        aux = {'valinit':valinit} if isinstance(self.value, (int, float)) else {}
        self.slider = matplot_slider(self.ax, self.param_name, *valinterval, valstep=valstep, **aux)

    def __call__(self, value):
        try:
            self.portrait.ax.cla()
        except:
            for ax in self.portrait.ax.values():
                ax.cla()
        self.value = value
        self.portrait.plot()
