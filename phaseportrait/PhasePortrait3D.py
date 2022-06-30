from inspect import signature

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np

from .exceptions import exceptions
from .sliders import sliders
from .streamlines import Streamlines_Velocity_Color_Gradient
from .utils import manager, utils


class PhasePortrait3D:
    """
    PhasePortrait3D
    ----------------
    Makes a phase portrait of a 3D system.
    
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
    _name_ = 'PhasePortrait3D'
    def __init__(self, dF, Range, *, MeshDim=6, dF_args={}, Density = 1, Polar = False, Title = 'Phase Portrait', xlabel = 'X', ylabel = 'Y', zlabel='Z', color='rainbow', xScale='linear', yScale='linear', zScale='linear', **kargs):
        """
        PhasePortrait3D
        ---------------
        
        Parameters
        ----------
        dF : callable
            A dF type function.
        Range : [x_range, y_range, z_range]
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
        ylabel : str, default='Y' 
            y label of the plot.
        zlabel : str, default='Z' 
            z label of the plot.
        color : str, default='rainbow'
            Matplotlib `Cmap`.
        xScale : str, default='linear'
            x axis scale. Can be `linear`, `log`, `symlog`, `logit`.
        yScale : str, default='linear'
            y axis scale. Can be `linear`, `log`, `symlog`, `logit`.
        zScale : str, default='linear'
            z axis scale. Can be `linear`, `log`, `symlog`, `logit`.
        """
        self.sliders = {}
        self.nullclines = []
        
        self.dF_args = dF_args.copy()                    # dF function's args
        self.dF = dF                                     # Function containing system's equations
        self.Range = Range                               # Range of graphical representation
        

        self.MeshDim  = MeshDim
        self.Density = Density                           # Controls concentration of nearby trajectories
        self.Polar = Polar                               # If dF expression given in polar coord. mark as True
        self.Title = Title                               # Title of the plot
        self.xlabel = xlabel                             # Title on X axis
        self.ylabel = ylabel                             # Title on Y axis
        self.zlabel = zlabel
        
        self.xScale = xScale                             # x axis scale
        self.yScale = yScale                             # x axis scale
        self.zScale = zScale

        self.streamplot_callback = Streamlines_Velocity_Color_Gradient           # TODO: enable different plot options

        self._create_arrays()

        # Variables for plotting
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(projection='3d')
        self.color = color
        self.grid = True
        
        self.streamplot_args = {}
        for k in kargs:
            if k in ['maxLen', 'detectLoops', 'dr', 'deltat']:
                self.streamplot_args.update({k: kargs[k]})

        
        self.manager = manager.Manager(self)
  

    def _create_arrays(self):
        # If scale is log and min range value is 0 or negative the plots is not correct
        _Range = self.Range.copy()
        for i, (scale, Range) in enumerate(zip([self.xScale, self.yScale, self.zScale], self.Range)):
            if scale == 'log':
                for j in range(len(Range)):
                    for k in range(len(Range)):
                        if Range[j, k]<=0:
                            _Range[i,j,k] = abs(max(Range))/100 if j==0 else abs(max(Range))
        self.Range = _Range

        self._X, self._Y, self._Z = np.meshgrid(*[np.linspace(*(self.Range[i][:]), self.MeshDim) for i in range(3)])

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
        
        self.draw_plot(color=self.color, grid=grid)
        self.fig.canvas.draw_idle()

        return self.fig, self.ax 
        

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

        self._create_arrays()

        try:
            for nullcline in self.nullclines:
                nullcline.plot()
        except AttributeError:
            pass

        if color is not None:
            self.color = color
        
        # if self.Polar:
        #     self._PolarTransformation()
        # else:
        #     self._dX, self._dY = self.dF(self._X, self._Y, **self.dF_args)
        
        # if utils.is_number(self._dX):
        #     self._dX = self._X.copy() * 0 + self._dX
        # if utils.is_number(self._dY):
        #     self._dY = self._Y.copy() * 0 + self._dY



        stream = self.streamplot_callback(self.dF, self._X, self._Y, self._Z, 
            spacing=(0, 0), 
            dF_args=self.dF_args, polar=self.Polar, **self.streamplot_args)

        try:
            norm = stream._velocity_normalization()
        except AttributeError:
            norm = None
        cmap = plt.get_cmap(self.color)
                
        stream.plot(self.ax, cmap, norm, arrow_width=self.streamplot_args.get('arrow_width', (self.Range[0][1]-self.Range[0][0])/ (2*self.Density*self.MeshDim)))

        
        self.ax.set_xlim(self.Range[0])
        self.ax.set_ylim(self.Range[1])
        self.ax.set_zlim(self.Range[2])
        # self.ax.set_aspect(abs(self.Range[0,1]-self.Range[0,0])/abs(self.Range[1,1]-self.Range[1,0]))

        self.ax.set_title(f'{self.Title}')
        self.ax.set_xlabel(f'{self.xlabel}')
        self.ax.set_ylabel(f'{self.ylabel}')
        self.ax.set_zlabel(f'{self.zlabel}')
        self.ax.set_xscale(self.xScale)
        self.ax.set_yscale(self.yScale)
        self.ax.set_zscale(self.zScale)
        self.ax.grid(grid if grid is not None else self.grid)
        
        return stream


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
        # TODO: ckeck if correct
        if not hasattr(self, "_dR") or not hasattr(self, "_dTheta") or not hasattr(self, "_dPhi"):
            self._R, self._Theta = np.sqrt(self._X**2 + self._Y**2 + self._Z**2), np.arctan2(self._Y, self._X)
            self._Phi = np.arccos(self._Z / self._R)
        
        self._dR, self._dTheta, self._dPhi = self.dF(self._R, self._Theta, self._Phi **self.dF_args)
        self._dX, self._dY, self._dZ = \
            self._dR*np.cos(self._Theta)*np.sin(self._Phi) - self._R*np.sin(self._Theta)*np.sin(self._Phi)*self._dTheta + self._R*np.cos(self._Theta)*np.cos(self._Phi) * self._dPhi, \
            self._dR*np.sin(self._Theta)*np.sin(self._Phi) + self._R*np.cos(self._Theta)*np.sin(self._Phi)*self._dTheta + self._R*np.sin(self._Theta)*np.cos(self._Phi)*self._dPhi, \
            self._dR*np.cos(self._Phi) - self._R*np.sin(self._Phi)*self._dPhi
        


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
        if len(value)==3:
            if np.array([len(value[i])==2 for i in range(3)]).all():
                self._Range = value
                return
        self._Range = np.array(utils.construct_interval(value, dim=3))

    @property
    def dF_args(self):
        return self._dF_args

    @dF_args.setter
    def dF_args(self, value):
        if value:
            if not isinstance(value, dict):
                raise exceptions.dF_argsInvalid(value)
        self._dF_args = value