import numpy as np

from ..generators_base import _Generator_

class RungeKutta(_Generator_):
    """
    This class is an implementation of \_Generator\_ for a Runge-Kutta 4th order data generator.
    """
    def __init__(self, portrait, dF, dimension, max_values, *, dt=0.1, dF_args=None, initial_values=None, thermalization=0):
        """
        Parameters
        ----------
        portrait : 
            Class that uses the RungeKutta objects.
            
        dF : callable
            A dF type funcion.
            
        dimension : int
            Number of dimensions in which it calculates the next values. Must equal the amount of outputs the `dF`
            funcion gives.
    
        max_values : int
            Max number of values saved.
            
        dt : double, optional, by default 0.1
            Time interval used in the Runge-Kutta 4th order method.
            
        dF_args :  dict
            If necesary, must contain the kargs for the `dF` funcion. By default, None.
            
        initial_values : float, list, optional
            Initial set of conditions, by default None.
            If None, random initial conditions are aplied in the interval [0,1) for each coordinate.
            
        thermalization : int, optional
            Thermalization steps before data is saved, by default None. 
            If None, thermalization steps are set to 0.
        """
        super().__init__(portrait, dF, dimension, max_values, dF_args=dF_args,
                         initial_values=initial_values, thermalization=thermalization)

        self.dt = dt
        self.positions = self._create_values_array()
        self.velocities = self._create_values_array()

    @classmethod
    def instance_and_compute_all(cls, portrait, dF, dimension, dF_args, initial_values, max_values, save_freq=1, dt=0.1, thermalization=0):
        """Creates an instance of phase-portrait.trajectories.RungeKutta. 
        Computes all the data requested and returns the instance.

        Parameters
        ----------
        portrait : 
            Class that uses the RungeKutta objects.
        
        dF : callable
            A dF type funcion.
        
        dimension : int
            Number of dimensions in which it calculates the next values. Must equal the amount of outputs the `dF`
            funcion gives.
        
        dF_args : dict
            If necesary, must contain the kargs for the `dF` funcion. By default, None.
        
        initial_values : float, list, optional
            Initial set of conditions, by default None.
            If None, random initial conditions are aplied in the interval [0,1) for each coordinat
        
        max_values : int
            Max number of values saved.
        
        save_freq : int, optional, by default 1
            Number of values computed before saving them.
            
        dt : float, optional, by default 0.1
            Time interval used in the Runge-Kutta 4th order method.
        
        thermalization : int, optional
            Thermalization steps before data is saved, by default None. 
            If None, thermalization steps are set to 0.

        Returns
        -------
        phase-portrait.trajectories.RungeKutta
            The instance with all the data requested
        """
        instance = cls(portrait, dF, dimension, dt=dt, dF_args=dF_args, initial_values=initial_values, thermalization=thermalization)

        instance.compute_all()
        return instance
    

    def _next(self):
        """
        Generates from `self.position` its following value via the Runge-Kutta 4th order method.
        """
        k1 = np.array(self.dF(*(self.position), **self.dF_args))
        k2 = np.array(self.dF(*(self.position+0.5*k1*self.dt), **self.dF_args))
        k3 = np.array(self.dF(*(self.position+0.5*k2*self.dt), **self.dF_args))
        k4 = np.array(self.dF(*(self.position+k3*self.dt), **self.dF_args))
        self.velocity = 1/6*(k1+2*k2+2*k3+k4)
        self.position += self.velocity*self.dt
    
    
    def save(self, i):
        """
        Saves `self.position` in the attribute `self.positions`, and `self.velocity` in `self.velocities`.

        Parameters
        ----------
        i : int
            Index in which the data is saved.
        """
        try:
            self.positions[:, i] = self.position
            self.velocities[:, i] = self.velocity
        except IndexError:
            np.concatenate(self.positions, self._create_values_array(), axis=1)
            np.concatenate(self.velocities, self._create_values_array(), axis=1)
            self.max_values += 2000
            self.save(i)
        
        
    def clear_values(self):
        """
        Clears the data arrays `self.positions` and `self.velocities`.
        """
        self.positions[:,1:] = 0
        self.velocity[:,1:] = 0