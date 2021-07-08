# \_Generator\_
> *class* phaseportrait.generator_base.**\_Generator\_**(*dF, initial_position, xrange, \*, dF_args={None}, yrange=[], max_steps=100, n_points=100, \*\*kargs*)

**This class is used internally in Maps and Trajectories. It is not intended to be used by the user.**

A class used to generate and save data.


### **Parameters**

* **portrait** : 

    Class that uses the \_Generator\_ objects.

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
        
    
# Methods to be overwritten
### *\_Generator\_*._\_next_
> *\_Generator\_*.**\_next**()

Generates from `self.position` its following value

**Returns**

* None

### *\_Generator\_*._save_
> *\_Generator\_*.**save**()

Saves `self.position` in a convenient way for the type of representation.

**Returns**

* None

### *\_Generator\_*._clear_values_
> *\_Generator\_*.**clear_values**()

Clears the data arrays.

**Returns**

* None

### *\_Generator\_*._\_check_limit_cycle_
> *\_Generator\_*.**\_check_limit_cycle**(_delta)

(Optional) Checks if the trajectory is on a limit cycle.

**Returns**

* False
* int, number of saved points


# Methods

### *\_Generator\_*.compute_all
> *\_Generator\_*.**compute_all**(\*, save_freq=1, limit_cycle_check=False, delta=0.01)

Computes `_Generator_.max_values` and saves them.


**Key Arguments**

* save_freq : int, optional, by default 1

    Number of values computed before saving them.

* limit_cycle_check : int, optional, by default False

    Number of points before checking for limit cycles.

* delta : float, optional, by default 0.01

    Diference between two values to be considerated equal. 

**Returns**

* Numpy.ndarray

    Saved data with size: [`_Generator_.dimension`, `_Generator_.max_values`]

### *\_Generator\_*.\_create_values_array
> *\_Generator\_*.**\_create_values_array**(\*, max_values: int = None)

Creates an array for storaging the values.

**Key Arguments**

* max_values : int, optional, by default None

    Max size of the arrays.


**Returns**

* Numpy.ndarray

    Empty array with size `dimension*max_values`


### *\_Generator\_*.Nnext
> *\_Generator\_*.**Nnext**(number, \*, save_freq=1, limit_cycle_check=False, delta=0.001)

Computes next `number` pairs of position and velocity values and saves them.

**Parameters**

* number : int

    Number of pairs of values saved.

**Key Arguments**

* delta : float, optional

    Difference between numbers to be considerated equal. Only if `limit_cycle_check=True`.

* save_freq : int, optional, by default 1

    Number of values computed before saving them.

* limit_cycle_check : bool, optional, by default False

    Whenever to look for limit cycles.

**Returns**

* int, optional

    Only if limit_cycle_check is `True`. It returns the number of points calculated.


### *\_Generator\_*.next
> *\_Generator\_*.**next**(\*, index=1)

Computes the next usable pair of values and saves them.


**Parameters**

* index : int, optional, by default 1

    Where to save the pair of values.

**Returns**

* None


# Examples

This class is implemented in other classes, such as:

* [Map](map.md)
* [RungeKutta](rungekutta.md)

