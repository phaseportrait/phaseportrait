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

        self.fig, self.ax = plt.subplots()
        self.sliders = {}
        self.sliders_fig = False



    def _prepare_plot(self, min_value, max_value):

        self.ax.set_title(self.Title)
        self.ax.set_xlabel(self.xlabel)
        self.ax.set_ylabel(self.ylabel)

        if self.yrange==[]:
            self.ax.set_ylim(bottom= 1.10*min_value,top=1.10*max_value)
        else:
            self.ax.set_ylim(self.yrange)

        self.ax.grid()
    


    def plot(self, *args, **kargs):

        bisector = np.linspace(self.xrange[0], self.xrange[1], self.n_points)
        func_result = self.dF(bisector, **self.dF_args)

        self._prepare_plot(np.min(func_result), np.max(func_result))

        self.ax.plot(bisector, func_result, 'b')
        self.ax.plot(bisector, bisector, "k:", color='grey')

        x, y = self.initial_position, self.dF(self.initial_position, **self.dF_args)
        self.ax.plot([x, x], [0, y], 'k:')
        self.ax.scatter(x , 0, color='green')

        for _ in range(self.max_steps):

            self.ax.plot([x, y], [y, y], 'k:')
            self.ax.plot([y, y], [y, self.dF(y, **self.dF_args)], 'k:')
            x, y = y, self.dF(y, **self.dF_args)

            if y>self.xrange[1] or y<self.xrange[0]:
                print(f'Warning: cobweb plot got out of range and could not compute {self.max_steps} steps.')
                break


        self.fig.canvas.draw_idle()



    def add_slider(self, param_name, *, valinit=None, valstep=0.1, valinterval=10):
        """
        Adds a slider on an existing plot
        """
        self.sliders.update({param_name: sliders.Slider(self, param_name, valinit=valinit, valstep=valstep, valinterval=valinterval)})

        self.fig.subplots_adjust(bottom=0.25)

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
