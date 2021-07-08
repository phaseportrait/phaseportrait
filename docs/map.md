# Map
> *class* phaseportrait.maps.**Map**(*portrait, dF, dimension, max_values, \*, dt=0.1, dF_args=None, initial_values=None, thermalization=0*)

**This class is used internally in Map1D. It is not intended to be used by the user.**

This class is an implementation of [\_Generator\_](generator.md) for maps generators.


### **Parameters**

* **portrait** : 

    Class that uses the Map objects.

* **dF** : callable

    A dF type funcion.
    
* **dimension** : int
            
    Number of dimensions in which it calculates the next values. Must equal the amount of outputs the `dF`
    funcion gives.

* **max_values** : int
    
    Max number of values saved.

### **Key Arguments**

* **dF_args** : dict

    If necesary, must contain the kargs for the `dF` funcion. By default, None.
    
* **initial_values** : float, list, optional
    
    Initial set of conditions, by default None.
    If None, random initial conditions are aplied in the interval [0,1) for each coordinate.

* **thermalization** : int, optional

    Thermalization steps before data is saved, by default None. 
    If None, thermalization steps are set to 0.
        
    
# Overwritten methods
### *map*._\_next_
> *map*.**\_next**()

Generates from `self.position` its following value. Explicitly:

```py
def _next(self):
    self.position[0] = self.dF(*(self.position), **self.dF_args)
```

**Returns**

* None

### *map*._save_
> *map*.**save**(i)

Saves `self.position` in the attribute `self.positions`.

**Parameters**

* i : int

    Index in which the data is saved.

Explicitly:

```py
def save(self, i):
    try:
        self.positions[:, i] = self.position
    except IndexError:
        np.concatenate(self.positions, self._create_values_array(), axis=1)
        self.max_values *= 2
        self.save(i)
```

**Returns**

* None

### *map*._clear_values_
> *map*.**clear_values**()

Clears the data arrays `self.positions`.

**Returns**

* None

### *map*._check_limit_cycle
> *map*.**\_check_limit_cycle**()

**Parameters**

* delta : float

    Difference between data values to be considerated equal.

**Returns**

* bool

    Whenever data reached a limit cylce.


# Methods

### *map*.instance_and_compute_all
> *map*.**instance_and_compute_all**(portrait, dF, dimension, dF_args, initial_values, max_values, save_freq=1, dt=0.1, thermalization=0)

Creates an instance of phase-portrait.trajectories.Map. Computes all the data requested and returns the instance.

**Parameters**

* portrait : 

    Class that uses the Map objects.

* dF : callable

    A dF type funcion.
    
* dimension : int
            
    Number of dimensions in which it calculates the next values. Must equal the amount of outputs the `dF`
    funcion gives.

* max_values : int
    
    Max number of values saved.

* dF_args : dict

    If necesary, must contain the kargs for the `dF` funcion. By default, None.

* initial_values : float, list, optional
    
    Initial set of conditions, by default None.
    If None, random initial conditions are aplied in the interval [0,1) for each coordinat

* save_freq : int, optional, by default 1

    Number of values computed before saving them.

* thermalization : int, optional

    Thermalization steps before data is saved, by default None. 
    If None, thermalization steps are set to 0.

* limit_cycle_check : int, bool, optional, by default False

    Whenever to check it there os a limit cycle in the data.
            
* delta : float, optional, by default 0.01

    If `limit_cycle_check==True` is the distance between data elements to be considerated equal.


**Returns**

* phase-portrait.trajectories.Map

# Examples

This class is implemented in other classes, check out:

* [Map1D](map1d.md)