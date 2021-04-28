import numpy as np

from ..exceptions import *
from ..utils import utils
from random import random

class RungeKutta():
    def __init__(self, portrait, dF, dimension, max_values, *, dt=0.1, dF_args=None, initial_values=None, thermalization=0):
        self.portrait = portrait
        self.dF = dF
        self.dimension = dimension
        self.dt = dt
        self.max_values=max_values
        self.thermalization=thermalization
        
        self.dF_args = dF_args
        
        if initial_values is None or len(initial_values)<self.dimension:
            aux = [random() for i in range(dimension)]
            self.initial_value = np.array(aux)
        else:
            self.initial_value = np.array(tuple(map(float,initial_values)))
        
        self.position = self.initial_value.copy()
        self.positions = self._create_values_array()
        self.velocities = self._create_values_array()
            
 
    @classmethod
    def instance_and_compute_all(cls, portrait, dF, dimension, dF_args, initial_values, max_values, save_freq=1, dt=0.1, thermalization=0):
        '''
        Creates a RungeKutta instance and computes `max_values` pairs of position and velocity every `save_freq`.
        If `thermalization` is given it saves the pairs from that point forward.
        '''
        
        instance = cls(portrait, dF, dimension, dt=dt, dF_args=dF_args, initial_values=initial_values)
        instance.max_values = max_values
        instance.save_freq = save_freq
        instance.thermalization = thermalization
        
        instance.positions = instance._create_values_array()
        instance.velocities = instance._create_values_array()
        
        instance.compute_all()
        return instance
        
    
    def compute_all(self, *, save_freq=1):
        '''
        Computes `RungeKutta.max_values` and saves them. If `save_freq` is given it saves them every that amount.
        If not, it saves them every `RungeKutta.save_freq` times, 1 by default.
        '''
        for  i in range(self.thermalization):
            self._next()

        self.Nnext(self.max_values, save_freq=save_freq)

    
    def _create_values_array(self, *, max_values: int=None):
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
    

    def _next(self):
        k1 = np.array(self.dF(*(self.position), **self.dF_args))
        k2 = np.array(self.dF(*(self.position+0.5*k1*self.dt), **self.dF_args))
        k3 = np.array(self.dF(*(self.position+0.5*k2*self.dt), **self.dF_args))
        k4 = np.array(self.dF(*(self.position+k3*self.dt), **self.dF_args))
        self.velocity = 1/6*(k1+2*k2+2*k3+k4)
        self.position += self.velocity*self.dt
    
    
    def save(self, i):
        try:
            self.positions[:, i] = self.position
            self.velocities[:, i] = self.velocity
        except IndexError:
            np.concatenate(self.positions, self._create_values_array(), axis=1)
            np.concatenate(self.velocities, self._create_values_array(), axis=1)
            self.max_values += 2000
            self.save(i)
        
        
    def clear_values(self):
        self.positions[:,1:] = 0
        self.velocity[:,1:] = 0