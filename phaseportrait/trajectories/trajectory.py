from inspect import signature

import matplotlib.pyplot as plt
import numpy as np

from ..exceptions import exceptions
from ..sliders import sliders
from ..utils import utils
from . import RungeKutta

class trajectory:
    """
    trajectory
    ----------
    Base class of trajectory classes: 
        -Trajectory2D
        
        -Trajectory3D
        
    Methods
    -------
    _prepare_plot :
        Prepares the plots.
        
    _scatter_start_point :
        Scatter all the start points.
        
    _scatter_trajectory :
        Scatter all the trajectories.
        
    _plot_lines :
        Plots the lines of all the trajectories.
        
    _create_sliders_plot :
        Creates the sliders plot.
        
    thermalize : 
        Adds thermalization steps and random initial position.
        
    initial_position :
        Adds a trajectory with the given initial position.
        
    plot : 
        Prepares the plots and computes the values. 
        Returns the axis and the figure.
        
    add_slider :
        Adds a `Slider` for the `dF` function.
        
    _calculate_values : 
        Computes the trajectories.
    """

    _name_ = 'trajectory'

    def __init__(self, dF, dimension, *, Range=None, dF_args={}, n_points=10000, runge_kutta_step=0.01, runge_kutta_freq=1, **kargs):
        """
        Creates an instance of trajectory
        
        Parameters
        ----------
        dF : callable
            A dF type function.
        dimension :
            The number of dimensions in which the trajectory is calculated.
            Must equal `dF` return lengh.
        
        Key Parameters
        -----
        Range : Union[float,list], default=None
            Range of every coordinate in the graphs.
        dF_args : dict
            If necesary, must contain the kargs for the `dF` function.
        n_points : int, default=10000    
            Number of positions to be saved for every trajectory.
        runge_kutta_step : float, default=0.1
            Step of 'time' in the Runge-Kutta method.
        runge_kutta_freq : int
            Number of times `dF` is aplied between positions saved.
        lines : bool
            Must be `True` if method _plot_lines is used.
        Titulo : str
            Title of the plot.
        color : str
            Matplotlib `Cmap`.
        size : float
            Size of the scattered points.
        thermalization : int
            Thermalization steps before points saved.
        mark_start_point : bool
            Marks the start position if True.
        """

        self._dimension = dimension
        self.dF_args = dF_args.copy()
        self.dF = dF 
        self.Range = Range

        try: 
            if kargs['numba']:
                from numba import jit
                self.dF = jit(self.dF, nopython=True)
                if not self.dF_args:
                    exceptions.dFArgsRequired()
        except KeyError:
            pass

        # Genral Runge-Kutta variables
        self.runge_kutta_step = runge_kutta_step
        self.runge_kutta_freq = runge_kutta_freq
        self.n_points = n_points
        self.trajectories = []
        
        # Plotting variables
        self.Title = kargs['Title'] if kargs.get('Title') else 'Trajectory'
        
        self.sliders = {}
        self.sliders_fig = False

        self.lines = kargs.get('lines')

        self.thermalization = kargs.get('thermalization')
        if not self.thermalization:
            self.thermalization = 0
        self.size = kargs.get('size')
        if not self.size:
            self.size = 0.5
        self.color = kargs.get('color')
        if self.color is None:
            self.color =  'viridis'
        self._mark_start_point = kargs.get('mark_start_point')

    # This functions must be overwriten on child classes:
    def _prepare_plot(self):...
    def _scatter_start_point(self, val_init):...
    def _scatter_trajectory(self, val, color, cmap):...
    def _plot_lines(self, val, val_init):...


    # General functions
    def _create_sliders_plot(self):
        if not isinstance(self.sliders_fig, plt.Figure):
            self.sliders_fig, self.sliders_ax = plt.subplots() 
            self.sliders_ax.set_visible(False)

        
    def thermalize(self, *, thermalization_steps=200):
        """
        Shortcut to:
        
        ```
        self.thermalization = thermalization_steps
        self.initial_position()
        ```
        """
        
        if self.thermalization is None:
            self.thermalization = thermalization_steps
        self.initial_position()


    def initial_position(self, *args, **kargs):
        """
        Adds a initial position for the computation.
        More than one can be added.
        
        Parameters
        ---------
        args : Union[float, list[2], list[3]], optional
        
            Initial position for the computation.
            If None, a random position is chosen.
            
        Example
        -------
        This example generates 2 circles with diferent radius. 
        ```
        def Circle(x,y,*, w=1, z=1):
            return w*y, -z*x

        circle = Trayectoria2D(Circle, n_points=1300, size=2, mark_start_position=True, Titulo='Just a circle')
        circle.initial_position(1,1)
        circle.initial_position(2,2)
        ```
        """

        flag = False
        for trajectory in self.trajectories:
            for a, b in zip(args, trajectory.initial_value):
                if a!=b:
                    flag = True
        
        if not flag and len(self.trajectories)>0:
            return
        
        self.trajectories.append(
            RungeKutta(
                self, self.dF, self._dimension, self.n_points, 
                dt=self.runge_kutta_step,
                dF_args=self.dF_args, 
                initial_values=args,
                thermalization=self.thermalization
                )
            )
 
        
    def _calculate_values(self, *args, all_initial_conditions=False, **kargs):
        for trajectory in self.trajectories:
            trajectory.compute_all(save_freq=self.runge_kutta_freq)


    def plot(self, color=None, **kargs):
        """
        Prepares the plots and computes the values.
        
        Key Arguments
        -------------
        color : str
        
            Matplotlib `Cmap`.
            
        Returns
        -------
        tuple(matplotlib Figure, matplotlib Axis)
        
        None 
            If attribute `fig` or `ax` not found.
            
        """

        self._prepare_plot()
        self.dF_args.update({name: slider.value for name, slider in self.sliders.items() if slider.value!= None})
        for trajectory in self.trajectories:
            trajectory.dF_args = self.dF_args
        
        self._calculate_values(all_initial_conditions=True)


        if self.color == 't':
            cmap = color
        else:
            cmap = self.color = color

        for trajectory in self.trajectories:
            val = trajectory.positions
            vel = trajectory.velocities
            val_init = trajectory.initial_value
            
            if self.lines:
                self._plot_lines(val, val_init)
                    
            else:
                def norma(v):
                    suma = 0
                    for i in range(self._dimension):
                        suma += np.nan_to_num(v[i]**2)
                    return np.sqrt(suma)
                if self.color == 't':
                    color = np.linspace(0,1, vel.shape[1])
                else:
                    color = norma(vel[:])
                    color /= color.max()

                self._scatter_trajectory(val, color, cmap)

            if self._mark_start_point:
                self._scatter_start_point(val_init)
                
        for fig in self.fig.values():
            if self.lines:
                fig.legend()
            fig.canvas.draw_idle()
        try:
            self.sliders_fig.canvas.draw_idle()
        except:
            pass

        try:
            return self.fig, self.ax
        except AttributeError:
            return None


    def add_slider(self, param_name, *, valinit=None, valstep=0.1, valinterval=10):
        """
        Adds a `Slider` for the `dF` function.
    
        Parameters
        ---------
        param_name : str
        
            Name of the variable. Must be in the `dF` kargs of the `Map1D.dF` function.
        
        Key Arguments
        ------------
        valinit : float, defautl=None
        
            Initial position of the Slider
            
        valinterval : Union[float,list], default=10
        
            Min and max value for the param range.
            
        valstep : float, default=0.1
        
            Separation between consecutive values in the param range.
        """ 
        self._create_sliders_plot()
        self.sliders.update({param_name: sliders.Slider(self, param_name, valinit=valinit, valstep=valstep, valinterval=valinterval)})

        self.sliders[param_name].slider.on_changed(self.sliders[param_name])
    
    
    @property
    def dF(self):
        return self._dF

    @dF.setter
    def dF(self, func):
        if not callable(func):
            raise exceptions.dFNotCallable(func)
        try:
            sig = signature(func)
        except ValueError:
            pass
        else:
            if len(sig.parameters)<self._dimension + len(self.dF_args):
                raise exceptions.dFInvalid(sig, self.dF_args)
        self._dF = func


    @property
    def Range(self):
        return self._Range

    @Range.setter
    def Range(self, value):
        if value == None:
            self._Range = None
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
