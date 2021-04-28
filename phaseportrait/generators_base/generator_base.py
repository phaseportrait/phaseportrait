from random import random

import numpy as np

from ..exceptions import *
from ..utils import utils


class _Generator_():
    def __init__(self, portrait, dF, dimension, max_values, *, dF_args=None, initial_values=None, thermalization=0):
        self.portrait = portrait
        self.dF = dF
        self.dimension = dimension
        self.max_values = max_values
        self.thermalization = thermalization

        self.dF_args = dF_args

        if initial_values is None or len(initial_values) < self.dimension:
            aux = [random() for i in range(dimension)]
            self.initial_value = np.array(aux)
        else:
            self.initial_value = np.array(tuple(map(float, initial_values)))

        self.position = self.initial_value.copy()
        

    # Methods that must be overwritten

    def _next(self):
        '''Genera a partir de `self.position` el siguiente valor de `self.position`'''
        ...

    def save(self, index):
        '''Guarda `self.position` de la manera conveniente para el tipo de representación'''
        ...

    def clear_values(self):
        '''Borra las listas que guardan la información guardada por `self.save`'''
        ...

    # General methods
    def compute_all(self, *, save_freq=1):
        '''
        Computes `RungeKutta.max_values` and saves them. If `save_freq` is given it saves them every that amount.
        If not, it saves them every `RungeKutta.save_freq` times, 1 by default.
        '''
        for i in range(self.thermalization):
            self._next()

        self.Nnext(self.max_values, save_freq=save_freq)

    def _create_values_array(self, *, max_values: int = None):
        if max_values is not None:
            self.max_values = max_values
        return np.zeros([self.dimension, self.max_values])

    def Nnext(self, number, *, save_freq=1):
        '''
        Computes next `number` pairs of position and velocity values and saves them. If `save_freq` is given it saves the save_freq'th pair each time.
        '''
        for i in range(number):
            self.next(save_freq=save_freq, index=i)

    def next(self, *, save_freq=1, index=1):
        '''
        Computes next pair of position and velocity values and saves it. If `save_freq` is given it saves the save_freq'th next.
        '''
        if save_freq:
            self.save_freq = save_freq

        for j in range(self.save_freq):
            self._next()
        self.save(index)