from inspect import signature

from .exceptions import exceptions
from .sliders import sliders
from .utils import utils, manager

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt

import numpy as np

from .nullclines import Nullcline2D

class PhasePortrait2D:
    """
    PhasePortrait2D
    ----------------
    Makes a phase portrait of a 2D system.
    
    Methods
    -------    
    draw_plot : 
        Draws the streamplot. Is internaly used by method `plot`.
        
    add_function : 
        Adds a function to the `dF` plot.
    
    add_slider :
        Adds a `Slider` for the `dF` function.

    plot :
        Prepares the plots and computes the values. 
        Returns the axis and the figure.
    """
    _name_ = 'PhasePortrait2D'
    def __init__(self, dF, Range, *, MeshDim=30, dF_args={}, Density = 1, Polar = False, Title = 'Phase Portrait', xlabel = 'X', ylabel = r"$\dot{X}$", color='rainbow'):
        """
        PhasePortrait2D
        ---------------
        
        Parameters
        ----------
        dF : callable
            A dF type function.
        Range : [x_range, y_range]
            Ranges of the axis in the main plot.
            
        Key Arguments
        -------------
        MeshDim : int, default=30
            Number of elements in the arrows grid.
        dF_args : dict
            If necesary, must contain the kargs for the `dF` function.
        Density : float, default=1
            Number of elements in the arrows grid plot.
        Polar : bool, default=False
            Whether to use polar coordinates or not.
        Title : str, default='Phase Portrait' 
        xlabel : str, default='X'
            x label of the plot.
        ylabel : str, default='$\dot{X}$' 
            y label of the plot.
        color : str, default='rainbow'
            Matplotlib `Cmap`.
        """
        self.dF_args = dF_args.copy()                    # dF function's args
        self.dF = dF                                     # Function containing system's equations
        self.Range = Range                               # Range of graphical representation
        

        self.MeshDim  = MeshDim
        self.Density = Density                                           # Controls concentration of nearby trajectories
        self.Polar = Polar                                               # If dF expression given in polar coord. mark as True
        self.Title = Title                                               # Title of the plot
        self.xlabel = xlabel                                             # Title on X axis
        self.ylabel = ylabel                                             # Title on Y axis

        self._create_arrays()

        # Variables for plotting
        self.fig, self.ax = plt.subplots()
        self.color = color
        self.sliders = {}
        self.nullclines = []
        
        self.manager = manager.Manager(self)



    def _create_arrays(self):
        self._X, self._Y = np.meshgrid(np.linspace(*self.Range[0,:], self.MeshDim), np.linspace(*self.Range[1,:], self.MeshDim))

        if self.Polar:   
            self._R, self._Theta = (self._X**2 + self._Y**2)**0.5, np.arctan2(self._Y, self._X)


    def plot(self, *, color=None):
        """
        Prepares the plots and computes the values.
        
        Returns
        -------
        tuple(matplotlib Figure, matplotlib Axis)
        
        Key Arguments
        -------------
        color : str
            Matplotlib `Cmap`.
        """
        if color is not None:
            self.color = color
        
        self.draw_plot(color=self.color)
        self.fig.canvas.draw_idle()

        return self.fig, self.ax 
        

    def draw_plot(self, *, color=None):
        """
        Draws the streamplot. Is internaly used by method `plot`.
        
        Returns
        -------
        matplotlib.Streamplot
        
        Key Arguments
        -------------
        color : str
            Matplotlib `Cmap`.
        """
        self.dF_args.update({name: slider.value for name, slider in self.sliders.items() if slider.value!= None})

        self._create_arrays()

        try:
            for nullcline in self.nullclines:
                nullcline.plot()
        except AttributeError:
            pass

        if color is not None:
            self.color = color
        
        if self.Polar:
            self._PolarTransformation()
        else:
            self._dX, self._dY = self.dF(self._X, self._Y, **self.dF_args)
        
        if utils.is_number(self._dX):
            self._dX = self._X.copy() * 0 + self._dX
        if utils.is_number(self._dY):
            self._dY = self._Y.copy() * 0 + self._dY
            
        colors = (self._dX**2+self._dY**2)**(0.5)
        colors_norm = mcolors.Normalize(vmin=colors.min(), vmax=colors.max())
        stream = self.ax.streamplot(self._X, self._Y, self._dX, self._dY, color=colors, cmap=self.color, norm=colors_norm, linewidth=1, density= self.Density)
        self.ax.set_xlim(self.Range[0,:])
        self.ax.set_ylim(self.Range[1,:])
        x0,x1 = self.ax.get_xlim()
        y0,y1 = self.ax.get_ylim()
        self.ax.set_aspect(abs(x1-x0)/abs(y1-y0))
        self.ax.set_title(f'{self.Title}')
        self.ax.set_xlabel(f'{self.xlabel}')
        self.ax.set_ylabel(f'{self.ylabel}')
        self.ax.grid()
        
        return stream

    def add_nullclines(self, *, precision=0.01, offset=0, density=50, xRange=None, yRange=None, dF_args=None, xcolor='r', ycolor='g', bgcolor='w', alpha=0):
        self.nullclines.append(Nullcline2D(self, self.dF, 
                                          precision=precision, offset=offset, density=density, 
                                          xRange=xRange, yRange=yRange, dF_args=dF_args, 
                                          xcolor=xcolor, ycolor=ycolor, bgcolor=bgcolor, alpha=alpha, polar=self.Polar))


    def add_slider(self, param_name, *, valinit=None, valstep=0.1, valinterval=10):
        """
        Adds a slider which can change the value of a parameter in execution time.

        Parameters
        ----------
        param_name : str
            It takes the name of the parameter on which the slider will be defined. Must be the same as the one appearing as karg in the `dF` function.

        valinit : numeric, optional
            Initial value of *param_name* variable. Default value is 0.5.

        valstep : numeric, optional
            Slider step value. Default value is 0.1.

        valinterval : numeric or list, optional
            Slider range. Default value is [-10, 10].
        """
        
        self.sliders.update({param_name: sliders.Slider(self, param_name, valinit=valinit, valstep=valstep, valinterval=valinterval)})

        self.fig.subplots_adjust(bottom=0.25)

        self.sliders[param_name].slider.on_changed(self.sliders[param_name])
    
    def _PolarTransformation(self):
        """
        Computes the expression of the velocity field if coordinates are given in polar representation.
        """
        if not hasattr(self, "_dR") or not hasattr(self, "_dTheta"):
            self._R, self._Theta = (self._X**2 + self._Y**2)**0.5, np.arctan2(self._Y, self._X)
        
        self._dR, self._dTheta = self.dF(self._R, self._Theta, **self.dF_args)
        self._dX, self._dY = self._dR*np.cos(self._Theta) - self._R*np.sin(self._Theta)*self._dTheta, self._dR*np.sin(self._Theta)+self._R*np.cos(self._Theta)*self._dTheta
        


    @property
    def dF(self):
        return self._dF

    @dF.setter
    def dF(self, func):
        if not callable(func):
            raise exceptions.dFNotCallable(func)
        sig = signature(func)
        if len(sig.parameters)<2 + len(self.dF_args):
            raise exceptions.dFInvalid(sig, self.dF_args)
        self._dF = func

    @property
    def Range(self):
        return self._Range


    @Range.setter
    def Range(self, value):
        self._Range = np.array(utils.construct_interval(value, dim=2))

    @property
    def dF_args(self):
        return self._dF_args

    @dF_args.setter
    def dF_args(self, value):
        if value:
            if not isinstance(value, dict):
                raise exceptions.dF_argsInvalid(value)
        self._dF_args = value