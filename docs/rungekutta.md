# RungeKutta
> *class* phaseportrait.trajectories.**RungeKutta**(*portrait, dF, dimension, max_values, \*, dt=0.1, dF_args=None, initial_values=None, thermalization=0*)

**This class is used internally in Trajectories. It is not intended to be used by the user.**

This class is an implementation of [\_Generator\_](generator.md) for a Runge-Kutta 4th order data generator.


### **Parameters**

* **portrait** : 

    Class that uses the RungeKutta objects.

* **dF** : callable

    A dF type funcion.
    
* **dimension** : int
            
    Number of dimensions in which it calculates the next values. Must equal the amount of outputs the `dF`
    funcion gives.

* **max_values** : int
    
    Max number of values saved.

### **Key Arguments**

* **dt** : double, optional, by default 0.1

    Time interval used in the Runge-Kutta 4th order method.

* **dF_args** : dict

    If necesary, must contain the kargs for the `dF` funcion. By default, None.
    
* **initial_values** : float, list, optional
    
    Initial set of conditions, by default None.
    If None, random initial conditions are aplied in the interval [0,1) for each coordinate.

* **thermalization** : int, optional

    Thermalization steps before data is saved, by default None. 
    If None, thermalization steps are set to 0.
        
    
# Overwritten methods
### *\_Generator\_*._\_next_
> *\_Generator\_*.**\_next**()

Generates from `self.position` its following value via the Runge-Kutta 4th order method. Explicitly:

```py
def _next(self):
    k1 = np.array(self.dF(*(self.position), **self.dF_args))
    k2 = np.array(self.dF(*(self.position+0.5*k1*self.dt), **self.dF_args))
    k3 = np.array(self.dF(*(self.position+0.5*k2*self.dt), **self.dF_args))
    k4 = np.array(self.dF(*(self.position+k3*self.dt), **self.dF_args))
    self.velocity = 1/6*(k1+2*k2+2*k3+k4)
    self.position += self.velocity*self.dt
```

**Returns**

* None

### *\_Generator\_*._save_
> *\_Generator\_*.**save**(i)

Saves `self.position` in the attribute `self.positions`, and `self.velocity` in `self.velocities`.

**Parameters**

* **i** : int

    Index in which the data is saved.

Explicitly:

```py
def save(self, i):
    try:
        self.positions[:, i] = self.position
        self.velocities[:, i] = self.velocity
    except IndexError:
        np.concatenate(self.positions, self._create_values_array(), axis=1)
        np.concatenate(self.velocities, self._create_values_array(), axis=1)
        self.max_values += 2000
        self.save(i)
```

**Returns**

* None

### *\_Generator\_*._clear_values_
> *\_Generator\_*.**clear_values**()

Clears the data arrays `self.positions` and `self.velocities`.

**Returns**

* None

# Methods

### *\_Generator\_*.instance_and_compute_all
> *\_Generator\_*.**instance_and_compute_all**(portrait, dF, dimension, dF_args, initial_values, max_values, save_freq=1, dt=0.1, thermalization=0)

Creates an instance of phase-portrait.trajectories.RungeKutta. Computes all the data requested and returns the instance.

**Parameters**

* portrait : 

    Class that uses the RungeKutta objects.

* dF : callable

    A dF type funcion.
    
* dimension : int
            
    Number of dimensions in which it calculates the next values. Must equal the amount of outputs the `dF`
    funcion gives.

* dF_args : dict

    If necesary, must contain the kargs for the `dF` funcion. By default, None.

* initial_values : float, list, optional
    
    Initial set of conditions, by default None.
    If None, random initial conditions are aplied in the interval [0,1) for each coordinat

* max_values : int
    
    Max number of values saved.

* save_freq : int, optional, by default 1

    Number of values computed before saving them.

* dt : double, by default 0.1

    Time interval used in the Runge-Kutta 4th order method.

* thermalization : int, optional

    Thermalization steps before data is saved, by default None. 
    If None, thermalization steps are set to 0.

**Returns**

* phase-portrait.trajectories.RungeKutta

# Examples

This class is implemented in other classes, check out:

* [Trajectory](trajectory.md)