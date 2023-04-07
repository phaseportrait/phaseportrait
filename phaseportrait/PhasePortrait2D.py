from inspect import signature

import matplotlib.cm as mplcm
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np

from .exceptions import exceptions
from .nullclines import Nullcline2D
from .sliders import sliders
from .streamlines import Streamlines_Velocity_Color_Gradient
from .utils import manager, utils


class PhasePortrait2D:
    """
Makes a phase portrait of a 2D system.

Examples
-------
```python
from phaseportrait import PhasePortrait2D

def dF(r, θ, *, μ=0.5,η=0):
    return μ*r*(1 - r*r), 1+η*θ


example = PhasePortrait2D(dF, [-3, 3], Density=2, Polar=True, Title='Limit cycle')
example.add_slider('μ', valinit=0.5)
example.add_slider('η', valinit=0.0)
example.add_nullclines()
example.plot()
``` 
* [Click here to see more examples.](phaseportrait2d_examples.md)

![image](../../imgs/doc_examples/pp2d_example.png)

Defining Range
-------

1. A single number. In this case the range is defined from zero to the given number in both axes.

2. A range, such `[lowerLimit , upperLimit]`.  Both axes will take the same limits.

3. Two ranges, such that `[[xAxisLowerLimit , xAxisUpperLimit], [yAxisLowerLimit , yAxisUpperLimit]]`

Methods
-------    
* draw_plot: Draws the streamplot. Is internaly used by method `plot`.
    
* add_function:  Adds a function to the `dF` plot.

* add_slider: Adds a `Slider` for the `dF` function.

* plot: Prepares the plots and computes the values. Returns the axis and the figure.
    """
    _name_ = 'PhasePortrait2D'
    def __init__(self, dF, Range, *, MeshDim=30, dF_args={}, Density = 1, Polar = False, Title = 'Phase Portrait', xlabel = 'X', ylabel = r"$\dot{X}$", 
                 color='rainbow', xScale='linear', yScale='linear', maxLen=500, odeint_method="scipy", **kargs):
        """PhasePortrait2D

        Args:
            dF (callable): A dF type function.
            Range ([x_range, y_range]): Ranges of the axis in the main plot.
            MeshDim (int, optional): Number of elements in the arrows grid. Defaults to 30.
            dF_args (dict, optional): If necesary, must contain the kargs for the `dF` function. Defaults to {}.
            Density (int, optional): [Deprecated] Number of elements in the arrows grid plot. Defaults to 1.
            Polar (bool, optional): Whether to use polar coordinates or not. Defaults to False.
            Title (str, optional): title of the plot. Defaults to 'Phase Portrait'.
            xlabel (str, optional): x label of the plot. Defaults to 'X'.
            ylabel (regexp, optional): y label of the plot. Defaults to r"$\dot{X}$".
            color (str, optional): Matplotlib `Cmap`. Defaults to 'rainbow'.
            xScale (str, optional): x axis scale. Can be `linear`, `log`, `symlog`, `logit`. Defaults to 'linear'.
            yScale (str, optional): y axis scale. Can be `linear`, `log`, `symlog`, `logit`. Defaults to 'linear'.
            maxLen (int, optional): Max integrations per line of streamlines. Defaults to 500.
            odeint_method (str, optional): Selects integration method, by default uses scipy.odeint. `euler` and `rungekutta3` are also available. Defaults to "scipy".
        """        

        self.sliders = {}
        self.nullclines = []
        
        self.dF_args = dF_args.copy()                    # dF function's args
        self.dF = dF                                     # Function containing system's equations
            

        self.MeshDim  = MeshDim
        self.Density = Density                           # Controls concentration of nearby trajectories
        self.Polar = Polar                               # If dF expression given in polar coord. mark as True
        self.Title = Title                               # Title of the plot
        self.xlabel = xlabel                             # Title on X axis
        self.ylabel = ylabel                             # Title on Y axis

        self.xScale = xScale                             # x axis scale
        self.yScale = yScale                             # x axis scale 
        
        self.Range = Range                               # Range of graphical representation

        self.streamplot_callback = Streamlines_Velocity_Color_Gradient

        # Variables for plotting
        self.fig = kargs.get('fig', None)
        if self.fig:
            self.ax = self.fig.gca()
        else:
            self.fig, self.ax = plt.subplots()
            
        self.color = color
        self.grid = True
        
        self.streamplot_args = {"maxLen": maxLen, "odeint_method": odeint_method}
        
        self.manager = manager.Manager(self)
  

    def _create_arrays(self):
        # If scale is log and min range value is 0 or negative the plots is not correct
        _Range = self.Range.copy().astype(np.float64)
        for i, (scale, Range) in enumerate(zip([self.xScale, self.yScale], self.Range)):
            if scale == 'log':
                for j in range(len(Range)):
                    if Range[j]<=0:
                        _Range[i,j] = abs(max(Range))/100 if j==0 else abs(max(Range))
        self._Range = _Range

        for i, (_P, scale, Range) in enumerate(zip(["_X", "_Y"],[self.xScale, self.yScale], self.Range)):
            if scale == 'linear':
                setattr(self, _P, np.linspace(Range[0], Range[1], self.MeshDim))
            if scale == 'log':
                setattr(self, _P, np.logspace(np.log10(Range[0]), np.log10(Range[1]), self.MeshDim))
            if scale == 'symlog':
                setattr(self, _P, np.linspace(Range[0], Range[1], self.MeshDim))

        self._X, self._Y = np.meshgrid(self._X, self._Y)

        # self._X, self._Y = np.meshgrid(np.linspace(*self.Range[0,:], self.MeshDim), np.linspace(*self.Range[1,:], self.MeshDim))

        if self.Polar:   
            self._R, self._Theta = (self._X**2 + self._Y**2)**0.5, np.arctan2(self._Y, self._X)


    def plot(self, *, color=None, grid=None):
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
        if grid is not None:
            self.grid = grid
            
        self.stream = self.draw_plot(color=self.color, grid=grid)
        
        if hasattr(self, "colorbar_ax"):
            cb = plt.colorbar(mplcm.ScalarMappable(
                    norm=self.stream._velocity_normalization(), 
                    cmap=self.color),
                ax=self.ax,
                cax=self.colorbar_ax)
            
            self.colorbar_ax = cb.ax
            
        self.fig.canvas.draw_idle()

        return self.fig, self.ax 
    
    def colorbar(self, toggle=True):
        """
        Adds a colorbar for speed.
        
        Parameters
        -------
        toggle: bool, default=True
            If `True` colorbar is visible.
        """
        if (not hasattr(self, "colorbar_ax")) and toggle:
            self.colorbar_ax = None
        else:
            if hasattr(self, "colorbar_ax"):
                self.colorbar_ax.remove()
                del(self.colorbar_ax)

    def draw_plot(self, *, color=None, grid=None):
        """
        Draws the streamplot. Is internaly used by method `plot`.
        
        Returns
        -------
        matplotlib.Streamplot
        
        Key Arguments
        -------------
        color : str, default='viridis'
            Matplotlib `Cmap`.
        grid : bool, default=True
            Show grid lines.
        """
        self.dF_args.update({name: slider.value for name, slider in self.sliders.items() if slider.value!= None})

        # Re-create arrays in case Range or scale is changed
        self._create_arrays()

        try:
            for nullcline in self.nullclines:
                nullcline.plot()
        except AttributeError:
            pass

        if color is not None:
            self.color = color


        stream = self.streamplot_callback(self.dF, self._X, self._Y, 
            dF_args=self.dF_args, polar=self.Polar, **self.streamplot_args)

        try:
            norm = stream._velocity_normalization()
        except AttributeError:
            norm = None
        cmap = plt.get_cmap(self.color)
                
        stream.plot(self.ax, cmap, norm, arrowsize=self.streamplot_args.get('arrow_width', 1))

        
        self.ax.set_xlim(self.Range[0,:])
        self.ax.set_ylim(self.Range[1,:])

        self.ax.set_title(f'{self.Title}')
        self.ax.set_xlabel(f'{self.xlabel}')
        self.ax.set_ylabel(f'{self.ylabel}')
        self.ax.set_xscale(self.xScale)
        self.ax.set_yscale(self.yScale)
        self.ax.grid(grid if grid is not None else self.grid)
        
        return stream



    def add_nullclines(self, *, precision=0.01, xprecision=None, yprecision=None, offset=0, density=50, xRange=None, yRange=None, dF_args=None, xcolor='r', ycolor='g', bgcolor='w', alpha=0):
        self.nullclines.append(Nullcline2D(self, self.dF,
                                          precision=precision, xprecision=xprecision, yprecision=yprecision, offset=offset, density=density, 
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
        
        # TODO: when a slider is created it should create and append an axis to the figure. For easier cleaning
        for s in self.sliders.copy():
            if s not in sig.parameters:
                raise exceptions.dF_argsInvalid(self.dF_args)

        self._dF = func

    @property
    def Range(self):
        return self._Range


    @Range.setter
    def Range(self, value):
        self._Range = np.array(utils.construct_interval(value, dim=2))
        self._create_arrays()

    @property
    def dF_args(self):
        return self._dF_args

    @dF_args.setter
    def dF_args(self, value):
        if value:
            if not isinstance(value, dict):
                raise exceptions.dF_argsInvalid(value)
        self._dF_args = value
