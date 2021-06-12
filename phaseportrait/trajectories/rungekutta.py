import numpy as np

from ..generators_base import _Generator_

class RungeKutta(_Generator_):
    def __init__(self, portrait, dF, dimension, max_values, *, dt=0.1, dF_args=None, initial_values=None, thermalization=0):
        super().__init__(portrait, dF, dimension, max_values, dF_args=dF_args,
                         initial_values=initial_values, thermalization=thermalization)

        self.dt = dt
        self.positions = self._create_values_array()
        self.velocities = self._create_values_array()

    @classmethod
    def instance_and_compute_all(cls, portrait, dF, dimension, dF_args, initial_values, max_values, save_freq=1, dt=0.1, thermalization=0):
        '''
        Creates a RungeKutta instance and computes `max_values` pairs of position and velocity every `save_freq`.
        If `thermalization` is given it saves the pairs from that point forward.
        '''

        instance = cls(portrait, dF, dimension, dt=dt, dF_args=dF_args, initial_values=initial_values, thermalization=thermalization)

        instance.compute_all()
        return instance
    

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