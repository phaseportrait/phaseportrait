from inspect import signature

import matplotlib.pyplot as plt
import numpy as np

from .sliders import sliders
from .exceptions import exceptions
from .utils import utils


class Cobweb:

    _name_ = 'Cobweb'
    def __init__(self, dF, initial_position, xrange, *, dF_args={None}, yrange=[], max_steps=100, n_points=10000, **kargs):
        
        self.dF = dF
        self.dF_args = dF_args
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

        bisector = np.linspace(self.xrange[0], self.xrange[1], self.n_points)
        func_result = self.dF(bisector, **self.dF_args)

        self._prepare_plot(np.min(func_result), np.max(func_result))

        self.ax['Cobweb'].plot(bisector, func_result, 'b')
        self.ax['Cobweb'].plot(bisector, bisector, "k:", color='grey')

        x, y = self.initial_position, self.dF(self.initial_position, **self.dF_args)
        self.ax['Cobweb'].plot([x, x], [0, y], 'k:')
        self.ax['Cobweb'].scatter(x , 0, color='green')

        self.ax['TimeSeries'].scatter(0 , x, color='black', s=5.5)

        for i in range(self.max_steps):

            self.ax['Cobweb'].plot([x, y], [y, y], 'k:')
            self.ax['Cobweb'].plot([y, y], [y, self.dF(y, **self.dF_args)], 'k:')
            x, y = y, self.dF(y, **self.dF_args)
            self.ax['TimeSeries'].scatter(i , x, color='black', s=5.5)

            if y>self.xrange[1] or y<self.xrange[0]:
                print(f'Warning: cobweb plot got out of range and could not compute {self.max_steps} steps.')
                break


        self.fig['Cobweb'].canvas.draw_idle()
        self.fig['TimeSeries'].canvas.draw_idle()


    def _create_sliders_plot(self):
        if not isinstance(self.sliders_fig, plt.Figure):
            self.sliders_fig, self.sliders_ax = plt.subplots() 
            self.sliders_ax.set_visible(False)
            

    def add_slider(self, param_name, *, valinit=None, valstep=0.1, valinterval=10):
        """
        Adds a slider which can change the value of a parameter in execution time.

        Args:

            param_name : string type. It takes the name of the parameter on which the slider will be defined. Must be the same as the one appearing as karg in the `dF` function.

        **kargs:

            valinit: initial value of *param_name* variable. Default value is 0.5 .

            valstep : slider step value. Default value is 0.1 .

            valinterval : slider range. Default value is [-10, 10] .
        """
        self._create_sliders_plot()

        self.sliders.update({param_name: sliders.Slider(self, param_name, valinit=valinit, valstep=valstep, valinterval=valinterval)})

        self.sliders[param_name].slider.on_changed(self.sliders[param_name])


    def update_dF_args(self):
        for name, slider in self.sliders.items():
            if slider.value!= None and name!=r'$x_0$':
                self.dF_args[name] = slider.value 

        if self.sliders.get(r'$x_0$'):
            self.initial_position = self.sliders[r'$x_0$'].value

    def initial_position_slider(self, *, valinit=None, valstep=0.05, valinterval=None):
        """
        Adds a slider for changing initial value on a cobweb plot
        """
        if valinit is None:
            valinit = self.initial_position

        if valinterval is None:
            valinterval = list(self.xrange)
        
        self.add_slider(r'$x_0$', valinit=valinit, valstep=valstep, valinterval=valinterval)

    # Funciones para asegurarse que los parametros introducidos son válidos
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
