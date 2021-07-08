import numpy as np

from ..exceptions import *
from ..utils import utils
from matplotlib.widgets import Slider as matplot_slider

class Slider():
    """
    Slider
    ------
    Internal class. Manages sliders.
    
    Integrated via method `add_slider` in:
        -Map1D
        
        -Cobweb
        
        -PhasePortrait2D
        
        -PhasePotrait3D
        
        -Trajectory2D
        
        -Trajectory3D
    
    Methods
    -------
    __call__ :
        Updates internal dF_args and replots the graphs.
    """
    def __init__(self, portrait, param_name, valinit=None, valstep=0.1, valinterval=[]):
        """
        Slider
        ------
        Internal class. Manages sliders.
        
        Parameters
        ----------
        portrait : 
            Class that uses the Slider.
        param_name : str
            Name of the parameter to slide over.
        valinit : float
            Initial value of the parameter in the slider.
        valsetp : float, default=0.1
            Precision of the slider.
        valinterval : Union[float, list]
            Parameter range in the slider.
        """
        
        self.portrait = portrait
        self.param_name = param_name
        self.value = valinit
        
        valinterval = utils.construct_interval_1d(valinterval)
        valinterval = np.array(valinterval)
 
        if 'Trajectory' in self.portrait._name_ or 'Cobweb' in self.portrait._name_: 
            self.ax = self.portrait.sliders_fig.add_axes([0.25, 0.88 - 0.05*len(self.portrait.sliders), 0.4, 0.05])

        if 'PhasePortrait' in self.portrait._name_ or 'Map1D' in self.portrait._name_:
            self.ax = self.portrait.fig.add_axes([0.25, 0.015 + 0.05*len(self.portrait.sliders), 0.4, 0.03])
        
        aux = {'valinit':valinit} if isinstance(self.value, (int, float)) else {}
        self.slider = matplot_slider(self.ax, self.param_name, *valinterval, valstep=valstep, **aux)

    def __call__(self, value):
        """
        Updates internal dF_args and replots the graphs.
        
        Arguments
        ---------
        value : float
            New value for the parameter of the slider
        """
        
        try:
            self.portrait.ax.cla()
        except:
            for ax in self.portrait.ax.values():
                ax.cla()
        self.value = value

        if 'Cobweb' in self.portrait._name_:
            self.portrait.update_dF_args()

        self.portrait.plot()
