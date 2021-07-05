from random import random

import numpy as np

from ..exceptions import *
from ..utils import utils


class _Generator_():
    """
    _Generator_
    -----------
    Base class of the generators classes:
        -Map
        
        -RungeKutta
    
    Methods
    -------
    Nnext :
        Computes next `number` pairs of position and velocity values and saves them.
    compute_all :
        Computes `RungeKutta.max_values` and saves them.
    next :
        Computes the next usable pair of values and saves them.
    save :
        Saves `self.position` in a convenient way for the representation.
    clear_values :
        Erases the values saved by method `save`.
    _next :
        Computes the next pair of values.
    _create_values_array : 
        Creates the arrays in which the values will be saved.
    _check_limit_cycle :
        Optional, checks if a there is repeated elements saved.
    """
    def __init__(self, portrait, dF, dimension, max_values, *, dF_args=None, initial_values=None, thermalization=None, **kargs):
        """Creates an instance of _Generator_

        Parameters
        ----------
        portrait : 
            Class that uses the _Generator_ class. 
        dF : callable
            A `dF` type function.
        dimension : int
            Number of dimensions in which it calculates the next values.
        max_values : int
            Max number of values saved
        dF_args : dict, optional
            If necesary, must contain the kargs for the `dF` function, by default None
        initial_values : float, list, optional
            Initial set of conditions, by default None
        thermalization : int, optional
            Thermalization steps before points saved, by default None
        """

        self.portrait = portrait
        self.dF = dF
        self.dimension = dimension
        self.max_values = max_values
        self.thermalization = thermalization if thermalization is not None else 0

        self.dF_args = dF_args
        if utils.is_number(initial_values):
            initial_values = [initial_values]

        if initial_values is None or len(initial_values) < self.dimension:
            aux = [random() for i in range(dimension)]
            self.initial_value = np.array(aux)
        else:
            self.initial_value = np.array(tuple(map(float, initial_values)))

        self.position = self.initial_value.copy()
        

    # Methods to be overwritten by child classes

    def _next(self):
        """Generates from `self.position` its following value"""
        ...

    def save(self, index):
        """Saves `self.position` in a convenient way for the type of representation"""
        ...

    def clear_values(self):
        """Clears list containing information in `self.save`"""
        ...
        
    def _check_limit_cycle(self, _delta):
        """(Optional) Checks if the trajectory is on a limit cycle"""
        return False
     

    # General methods
    def compute_all(self, *, save_freq=1, limit_cycle_check=False, delta=0.01):
        """
        Computes `_Generator_.max_values` and saves them.

        Parameters
        ----------
        save_freq : int, optional
            Number of values computed before saving them, by default 1
        limit_cycle_check : int, optional
            Number of points before checking for limit cycles, by default False
        delta : float, optional
            Diference between two values to be considerated equal, by default 0.01

        Returns
        -------
        int
            Number of points calculated.
        """

        for i in range(self.thermalization):
            self._next()

        return self.Nnext(self.max_values, save_freq=save_freq, limit_cycle_check=limit_cycle_check, delta=delta)

    def _create_values_array(self, *, max_values: int = None):
        """
        Creates an array for storaging the values

        Parameters
        ----------
        max_values : int, optional
            Max size of the arrays, by default None

        Returns
        -------
        Numpy.ndarray
            Empty array with size `dimension*max_values`
        """

        if max_values is not None:
            self.max_values = max_values
        return np.zeros([self.dimension, self.max_values])

    def Nnext(self, number, *, save_freq=1, limit_cycle_check=False, delta=0.001):
        """
        Computes next `number` pairs of position and velocity values and saves them.

        Parameters
        ----------
        number : int
            Number of pairs of values saved.
        delta : float, optional
            Difference between numbers to be considerated equal. Only if `limit_cycle_check=True`.
        save_freq : int, optional
            Number of values computed before saving them, by default 1
        limit_cycle_check : bool, optional
            Whenever to look for limit cycles, by default False

        Returns
        -------
        int, optional
            Only if limit_cycle_check is `True`. It returns the number of points calculated.
        """

        if save_freq is not None:
            self.save_freq = save_freq
        
        if limit_cycle_check is False:
            for i in range(number):
                self.next(index=i)
            return
        
        for i in range(limit_cycle_check):
            self.next(index=i)
        if self._check_limit_cycle(delta):
            return i
        for j in range(number-limit_cycle_check):
            self.next(index=i + j)

    def next(self, *, index=1):
        """
        Computes the next usable pair of values and saves them.

        Parameters
        ----------
        index : int, optional
            Where to save the pair of values, by default 1
        """

        for j in range(self.save_freq):
            self._next()
        self.save(index)