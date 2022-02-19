import matplotlib
import numpy as np
import random
from matplotlib import pyplot as plt
import threading

from .maps import Map
from .sliders import Slider


class Map1D():
    """
    Map1D
    --------
    Class dedicated to 1 dimensional maps `x(t+1) = f(x)`.
    
    Methods
    -------
    plot_over_variable : 
        Creates every `map` instance.
            
    plot_trajectory : 
        Creates a `map` instance and computes it's positions.
        Returns : `plt.Figure` , `plt.Axis`
        
    add_function : 
        Adds a function to the `dF` plot.
    
    add_slider :
        Adds a `Slider` for the `dF` function.

    plot :
        Prepares the plots and computes the values. 
        Returns the axis and the figure.
    """
    
    _name_ = 'Map1D'

    def __init__(self, dF, x_range, y_range, n_points, *, composition_grade=1, dF_args={}, Title='1D Map', xlabel=r'Control parameter', ylabel=r'$X_{n+1}$', **kargs):
        """
        Map1D
        --------
        
        Parameters
        ----------
        dF : callable
            A dF type function.
        Range : [x_range, y_range]
            Ranges of the axis in the main plot.
        n_points : int
            Maximum number of points
        
        Key Arguments
        -----
        dF_args : dict
            If necesary, must contain the kargs for the `dF` function.
        composition_grade : int
            Number of times `dF` is applied between positions saved.
        Title : str
            Title of the plot.
        xlabel : str
            x label of the plot.
        ylabel : str
            y label of the plot.
        color : str
            Matplotlib `Cmap`.
        size : float
            Size of the scattered points.
        thermalization : int
            Thermalization steps before points saved.
        """
        
        self.dF_args = dF_args.copy()
        self.dF = dF
        self.Range = np.array([x_range, y_range])
        self.n_points = n_points
        self.dimension = 1

        self.composition_grade = composition_grade

        self.Title = Title
        self.xlabel = xlabel
        self.ylabel = ylabel

        self.fig, self.ax = plt.subplots()
        self.color = kargs.get('color')
        if not self.color:
            self.color = 'inferno'

        self.maps = {}

        self.sliders = {}
        
        self.functions = []
        
        self._trajectory = None

        self.size = kargs.get('size')
        if self.size is None:
            self.size = 1
        self.thermalization = kargs.get('thermalization')
        
        self._initial_x = random.uniform(*self.Range[1])

        self._prepare_plot()

    def _thread_compute_date(self, params):
        dF_args = self.dF_args.copy()
        for p in params:
            dF_args.update({self._param_name: p})
            self.maps.update({p: Map.instance_and_compute_all(self, self.dF, self.dimension,
                             self.n_points, dF_args, self._initial_x, thermalization=self.thermalization,
                             limit_cycle_check=self._limit_cycle_check_first, delta=self._delta_cycle_check, save_freq=self.composition_grade)})

    def _compute_data(self):
        self._range = np.arange(
            self._valinterval[0], self._valinterval[1], self._valstep)

        threads_list = []
        for th in range(8):
            params = self._range[th::8]
            t = threading.Thread(target=self._thread_compute_date, args=(params,))
            t.start()
            threads_list.append(t)

        for t in threads_list:
            t.join()


    def plot_over_variable(self, param_name, valinterval, valstep, *, initial_x=None, limit_cycle_check_first=50, delta_cycle_check=0.0001):
        """
        plot_over_variable : 
        Creates every `map` instance.
    
        Parameters
        ---------
        param_name : str
            Name of the variable. Must be in the `dF` kargs.
        valinterval : list
            Min and max value for the param range.
        valstep : float
            Separation between consecutive values in the param range.
            
        Key Arguments
        ------------
        initial_x : float
            Initial x position of every data series.
        limit_cycle_check_first : int
            Number of points saved before checking for repeated elemets.
        delta_cycle_check : float
            Diference between two positions to be considerated identical.
        """
        
        self._param_name = param_name
        self._valinterval = valinterval
        
        if initial_x is None:
            initial_x = self._initial_x
        self._initial_x = initial_x

        self._valstep = valstep
        self._limit_cycle_check_first = limit_cycle_check_first
        self._delta_cycle_check = delta_cycle_check

    def _prepare_plot(self):
        self.ax.set_title(f'{self.Title}')
        self._cmap = self.color
        self._colores_norm = plt.Normalize(
            vmin=self.Range[1][0], vmax=self.Range[1][1])
        self.ax.set_xlim(*self.Range[0])
        self.ax.set_ylim(*self.Range[1])
        try:
            self.__done
            
            self.ax.grid()
            
        except AttributeError:
            self.__done = None
            
            self.ax.set_xlabel(self.xlabel)
            self.ax.set_ylabel(self.ylabel)
            self.fig.colorbar(matplotlib.cm.ScalarMappable(
                norm=self._colores_norm, cmap=self._cmap), label=r'$X_{n}$')
            
        
        
    def update_dF_args(self):
        """
        Updates the internal dF_args attributes to match the sliders.
        """
        self.dF_args.update({name: slider.value for name, slider in self.sliders.items() if slider.value!= None})
        

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
        for func in self.functions:
            func.plot()

        self.update_dF_args()
        self._prepare_plot()
        self._compute_data()

        if color is not None:
            self._cmap = color

        for i in self._range:
            values = self.maps[i].positions
            color = values[0, 0:-2]
            range_x = np.zeros(len(color)) + i
            self.ax.scatter(
                range_x, values[0, 1:-1],
                s=self.size, c=color, cmap=self._cmap, norm=self._colores_norm
            )
            
        return self.fig, self.ax
    

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
        self.sliders.update({param_name: Slider(
            self, param_name, valinit=valinit, valstep=valstep, valinterval=valinterval)})

        self.fig.subplots_adjust(bottom=0.25)

        self.sliders[param_name].slider.on_changed(self.sliders[param_name])
        

    def _prepare_plot_trajectory(self):
        if self._trajectory is None:
            self._trajectory = plt.subplots()
        self._trajectory[1].cla()
        self._trajectory[1].set_title(f'{self.Title}: {self.xlabel}={self._param_name}')
        self._trajectory[1].set_ylim(*self.Range[1])
        self._trajectory[1].set_xlabel('t')
        self._trajectory[1].set_ylabel(r'$X_{n}$')
        self._trajectory[1].grid()

        
    def plot_trajectory(self, n_points, *, dF_args=None, initial_x=None, color='b', save_freq=1, thermalization=0):
        """
        Creates a `map` instance and computes it's positions.
        
        Returns : `plt.Figure` , `plt.Axis`
        
        Parameters
        ----------
        n_points : int
            Number of points to be calculated.
            
        Key Arguments
        -----
        dF_args : dict
            If necesary, must contain the kargs for the `dF` function. By default takes the dF_args of the `Map1D` instance.
        initial_x : float
            Initial position of the trajectory.
        color : str
            String  matplotlib color identifier.
        save_freq : int
            Number of times `dF` is aplied before a position is saved.
        thermalization : int
            Thermalization steps before points saved.
        """
        try:
            if self._param_name:
                pass
        except AttributeError:
            print('Method plot_over_variable must be executed before.')
            return
        
        if dF_args is None:
            dF_args = self.dF_args
        if initial_x is None:
            initial_x = self._initial_x
    
        self._prepare_plot_trajectory()
        s_map = Map.instance_and_compute_all(None, self.dF, self.dimension, n_points, dF_args=dF_args, initial_values=initial_x, save_freq=save_freq, thermalization=thermalization)
        self._trajectory[1].plot(s_map.positions[0], '.-', color=color)
        return self._trajectory
