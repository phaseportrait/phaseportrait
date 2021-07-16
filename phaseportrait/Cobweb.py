from inspect import signature

import matplotlib.pyplot as plt
import numpy as np

from .sliders import sliders
from .exceptions import exceptions
from .utils import utils


class Cobweb:
    """
    A class used to represent a Cobweb plot and a time series to study the convergence of a map.

    Attributes
    ----------
    dF : function
        Map function, which returns value given a point and some parameters.
    initial_position : numeric
        Initial position for iterating the map.
    xrange : numeric or list
        Range of representation on x axis.
    dF_args : dict, optional
        Dictionary with parameters for `dF` function.
    yrange : numeric or list, optional
        Range of representation on y axis.
    max_steps : int, optional
        Number of iterations of the map.
    n_points : int, optional
        Number of points to plot the map.
    xlabel : str, optional
        x axis label in the plot. Default value is `r'$X_{n}$'`
    ylabel : str, optional
        y axis label in the plot. Default value is `r'$X_{n+1}$'`
    Title : str, optional
        title of the plot. Default value is `'Cobweb plot'`.

    Methods
    -------
    plot():
        Creates two figures, one containing the Cobweb plot and other with the time series.

    add_slider(param_name, valinit=None, valstep=0.1, valinterval=10):
        Adds a slider which can change the value of a parameter in execution time.

    initial_position_slider(valinit=None, valstep=0.05, valinterval=None):
        Adds a slider for changing initial value on a cobweb plot
    """
    _name_ = 'Cobweb'
    def __init__(self, dF, initial_position, xrange, *, dF_args={}, yrange=[], max_steps=100, n_points=10000, **kargs):
        
        self.dF = dF
        self.dF_args = dF_args.copy()
        self.initial_position = initial_position 
        self.xrange = xrange

        self.yrange = yrange
        self.max_steps = max_steps
        self.n_points = n_points

        self.Title = kargs['Title'] if kargs.get('Title') else 'Cobweb plot'
        self.xlabel = kargs['xlabel'] if kargs.get('xlabel') else r'$X_n$'
        self.ylabel = kargs['ylabel'] if kargs.get('ylabel') else r'$X_{n+1}$'

        figCobweb, axCobweb = plt.subplots()
        figTimeSeries, axTimeSeries = plt.subplots()

        self.fig = {
            'Cobweb': figCobweb,
            'TimeSeries': figTimeSeries
        }
        self.ax = {
            'Cobweb': axCobweb,
            'TimeSeries': axTimeSeries
        }

        self.sliders = {}
        self.sliders_fig = False



    def _prepare_plot(self, min_value, max_value):
        """
        Internally used method. Sets titles and axis for Cobweb and Time Series plots.

        Parameters
        ----------
        min_value: numeric
            Minimum value of the function in the interval.

        max_value: numeric
            Maximum value of the function in the interval.
        """
        self.ax['Cobweb'].set_title(self.Title)
        self.ax['Cobweb'].set_xlabel(self.xlabel)
        self.ax['Cobweb'].set_ylabel(self.ylabel)

        if self.yrange==[]:
            self.ax['Cobweb'].set_ylim(bottom= 1.10*min_value,top=1.10*max_value)
        else:
            self.ax['Cobweb'].set_ylim(self.yrange)

        self.ax['Cobweb'].grid()

        self.ax['TimeSeries'].set_title('Time Series')
        self.ax['TimeSeries'].set_ylabel(r'$x_t$')
        self.ax['TimeSeries'].set_xlabel('t')
        self.ax['TimeSeries'].set_ylim(self.xrange)
        self.ax['TimeSeries'].grid()


    def plot(self, *args, **kargs):
        """
        Prepares the plots, compute the values and plots them.
        
        Returns
        -------
        tuple(matplotlib Figure (Cobweb plot), matplotlib Axis (Cobweb plot), matplotlib Figure (Time series), matplotlib Axis (Time series))
        """
        bisector = np.linspace(self.xrange[0], self.xrange[1], self.n_points)
        func_result = self.dF(bisector, **self.dF_args)

        xTimeSeries = []
        yTimeSeries = []

        self._prepare_plot(np.min(func_result), np.max(func_result))

        self.ax['Cobweb'].plot(bisector, func_result, 'b')
        self.ax['Cobweb'].plot(bisector, bisector, ":", color='grey')

        x, y = self.initial_position, self.dF(self.initial_position, **self.dF_args)
        self.ax['Cobweb'].plot([x, x], [0, y], ':')
        self.ax['Cobweb'].scatter(x , 0, color='green')

        xTimeSeries.append(0)
        yTimeSeries.append(x)

        for i in range(self.max_steps):

            self.ax['Cobweb'].plot([x, y], [y, y], 'k:')
            self.ax['Cobweb'].plot([y, y], [y, self.dF(y, **self.dF_args)], 'k:')

            x, y = y, self.dF(y, **self.dF_args)

            xTimeSeries.append(i)
            yTimeSeries.append(x)

            if y>self.xrange[1] or y<self.xrange[0]:
                print(f'Warning: cobweb plot got out of range and could not compute {self.max_steps} steps.')
                break
        
        self.ax['TimeSeries'].scatter(xTimeSeries , yTimeSeries, color='black', s=10)
        self.ax['TimeSeries'].plot(xTimeSeries , yTimeSeries, ':', color='grey')

        self.fig['Cobweb'].canvas.draw_idle()
        self.fig['TimeSeries'].canvas.draw_idle()

        return self.fig['Cobweb'], self.ax['TimeSeries'], self.fig['TimeSeries'], self.ax['TimeSeries']

    def _create_sliders_plot(self):
        """
        Internally used method. Checks if there is already a sliders plot. If not, it creates it.
        """
        if not isinstance(self.sliders_fig, plt.Figure):
            self.sliders_fig, self.sliders_ax = plt.subplots() 
            self.sliders_ax.set_visible(False)
            

    def add_slider(self, param_name, *, valinit=None, valstep=0.1, valinterval=10):
        """
        Adds a slider on an existing plot.
        
        Parameters
        ----------
        param_name : str
            The string key of the variable. Must be the same as the key in the `dF` function.
        
        Key Arguments
        -------------
        valinit : float
            Initial value of the parameter.
        valinterval : Union[float, list]
            The range of values the slider of the parameter will cover.
        valstep : float
            Precision in the slider.
        """
        self._create_sliders_plot()

        self.sliders.update({param_name: sliders.Slider(self, param_name, valinit=valinit, valstep=valstep, valinterval=valinterval)})

        self.sliders[param_name].slider.on_changed(self.sliders[param_name])


    def update_dF_args(self):
        """
        Internally used method. It is used for setting the new values of dF_args and also for initial position.

        It is meant to be called on `call` method in Slider class.
        """
        for name, slider in self.sliders.items():
            if slider.value!= None and name!=r'$x_0$':
                self.dF_args[name] = slider.value 

        if self.sliders.get(r'$x_0$'):
            self.initial_position = self.sliders[r'$x_0$'].value

    def initial_position_slider(self, *, valinit=None, valstep=0.05, valinterval=None):
        """
        Adds a slider for changing initial value on a cobweb plot.
        
        Key Arguments
        -------------
        valinit : numeric, optional
            Initial position. Default value is the same as initial position given when initializing Cobweb object.
        valinterval : Union[float, list]
            The range of values the slider of the parameter will cover.
        valstep : float
            Precision in the slider.
        """
        if valinit is None:
            valinit = self.initial_position

        if valinterval is None:
            valinterval = list(self.xrange)
        
        self.add_slider(r'$x_0$', valinit=valinit, valstep=valstep, valinterval=valinterval)

    
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
        self._dF = func

    @property
    def xrange(self):
        return self._xrange

    @xrange.setter
    def xrange(self, value):
        if value == None:
            self._xrange = None
            return
        self._xrange = np.array(utils.construct_interval(value, dim=1))

    @property
    def yrange(self):
        return self._yrange

    @yrange.setter
    def yrange(self, value):
        if value == []:
            self._yrange = []
            return
        self._yrange = np.array(utils.construct_interval(value, dim=1))

    @property
    def dF_args(self):
        return self._dF_args

    @dF_args.setter
    def dF_args(self, value):
        if value:
            if not isinstance(value, dict):
                raise exceptions.dF_argsInvalid(value)
        self._dF_args = value
