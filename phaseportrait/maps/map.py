from random import random

import numpy as np

from ..exceptions import exceptions
from ..generators_base import _Generator_
from ..utils import utils


class Map(_Generator_):
    def __init__(self, portrait, dF, dimension, max_values, *, dF_args=None, initial_values=None, thermalization=0, **kargs):
        super().__init__(portrait, dF, dimension, max_values, dF_args=dF_args,
                         initial_values=initial_values, thermalization=thermalization, **kargs)

        self.positions = self._create_values_array()

    @classmethod
    def instance_and_compute_all(cls, portrait, dF, dimension, max_values, dF_args, initial_values, save_freq=1, thermalization=0, **kargs):
        '''
        Creates a RungeKutta instance and computes `max_values` pairs of position and velocity every `save_freq`.
        If `thermalization` is given it saves the pairs from that point forward.
        '''

        instance = cls(portrait, dF, dimension, max_values, dF_args=dF_args,
                       initial_values=initial_values, save_freq=save_freq, thermalization=thermalization, **kargs)

        max_index = instance.compute_all(**kargs)
        if max_index is not None:
            instance.positions = instance.positions[:,0:max_index-1]
        return instance

    def _next(self): 
        self.position[0] = self.dF(*(self.position), **self.dF_args)

    def save(self, i):
        try:
            self.positions[:, i] = self.position
        except IndexError:
            np.concatenate(self.positions, self._create_values_array(), axis=1)
            self.max_values *= 2
            self.save(i)

    def clear_values(self):
        self.positions[:, 1:] = 0
        
    def _check_limit_cycle(self, delta):
        for i in self.positions[0,0:-2]:
            if np.linalg.norm(i - self.position)<delta:
                return True
        return False    