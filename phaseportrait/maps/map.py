import numpy as np

from ..generators_base import _Generator_


class Map(_Generator_):
    """
    This class is an implementation of \_Generator\_ for maps generators.
    """
    def __init__(self, portrait, dF, dimension, max_values, *, dF_args=None, initial_values=None, thermalization=0, **kargs):
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
            
        dF_args : dict
            If necesary, must contain the kargs for the `dF` funcion. By default, None.
            
        initial_values : float, list, optional
            Initial set of conditions, by default None.
            If None, random initial conditions are aplied in the interval [0,1) for each coordinate.
            
        thermalization : int, optional
            Thermalization steps before data is saved, by default None. 
            If None, thermalization steps are set to 0.
        """
        super().__init__(portrait, dF, dimension, max_values, dF_args=dF_args,
                         initial_values=initial_values, thermalization=thermalization, **kargs)

        self.positions = self._create_values_array()

    @classmethod
    def _instance_and_compute_all(cls, tup):
        instance = cls(tup[0], tup[1], tup[2], tup[3], dF_args=tup[4], initial_values=tup[5], thermalization=tup[6])
 
        max_index = instance.compute_all(limit_cycle_check=tup[7], delta=tup[8])
        if max_index is not None:
            instance.positions = instance.positions[:,0:max_index-1]
        return instance
    @classmethod
    def instance_and_compute_all(cls, portrait, dF, dimension, max_values, dF_args, initial_values, save_freq, thermalization, **kargs):
        """Creates an instance of phase-portrait.maps.Map. 
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
            
        max_values : int
            Max number of values saved.
        
        dF_args : dict
            If necesary, must contain the kargs for the `dF` funcion. By default, None.
        
        initial_values : float, list, optional
            Initial set of conditions, by default None.
            If None, random initial conditions are aplied in the interval [0,1) for each coordinat
        
        save_freq : int, optional, by default 1
            Number of values computed before saving them.
            
        thermalization : int, optional
            Thermalization steps before data is saved, by default None. 
            If None, thermalization steps are set to 0.

        limit_cycle_check : int, bool, optional, by default False
            Whenever to check it there os a limit cycle in the data.
            
        delta : float, optional, by default 0.01
            If `limit_cycle_check==True` is the distance between data elements to be considerated equal.

        Returns
        -------
        phase-portrait.maps.Map
            The instance with all the data requested
        """

        instance = cls(portrait, dF, dimension, max_values, dF_args=dF_args,
                       initial_values=initial_values, save_freq=save_freq, thermalization=thermalization, **kargs)

        max_index = instance.compute_all(**kargs)
        if max_index is not None:
            instance.positions = instance.positions[:,0:max_index-1]
        return instance

    def _next(self): 
        """
        Generates from `self.position` its following value.
        """
        self.position[0] = self.dF(*(self.position), **self.dF_args)

    def save(self, i):
        """
        Saves `self.position` in the attribute `self.positions`.

        Parameters
        ----------
        i : int
            Index in which the data is saved.
        """
        try:
            self.positions[:, i] = self.position
        except IndexError:
            np.concatenate(self.positions, self._create_values_array(), axis=1)
            self.max_values *= 2
            self.save(i)

    def clear_values(self):
        """
        Clears the data arrays `self.positions`.
        """
        self.positions[:, 1:] = 0
        
    def _check_limit_cycle(self, delta):
        """Checks if there is a limit cycle in the data.

        Parameters
        ----------
        delta : float
            Difference between data values to be considerated equal.

        Returns
        -------
        bool
            Whenever data reached a limit cylce.
        """
        for i in self.positions[0,0:-2]:
            if np.linalg.norm(i - self.position)<delta:
                return True
        return False    