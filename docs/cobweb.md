# Cobweb
> *class* phaseportrait.**Cobweb**(*dF, initial_position, xrange, \*, dF_args={None}, yrange=[], max_steps=100, n_points=100, \*\*kargs)*)

A class used to represent a Cobweb plot and a time series to study the convergence of a 1D map `x(t+1) = f(x)`.

| Parameters| Methods                                   |
| --------- | ----------------------------------------- |
| dF        | [plot](#cobwebplot)                  |
| initial_position| [add_slider](#cobwebadd_slider)                 |
| xrange | [initial_position_slider](#cobwebinitial_position_slider)|
| dF_args   |                                           |
| yrange    |                                           |
| max_steps    |                                           |
| n_points |                                           |
| Title  |                                           |
| xlabel  |                                           |
| ylabel |                                           |


### **Parameters**

* **dF** : callable

    A dF type funcion.
    
* **initial_position** : float

    Initial x of the iteration.
    
* **xrange** : list

    Range of the x axis in the main plot.
    
### **Key Arguments**

* **dF_args** : dict

    If necesary, must contain the kargs for the `dF` funcion.
    
* **yrange** : list

    Range of the y axis in the main plot
    
* **max_steps** : int

    Maximun number of poits to be represented.
    
* **n_points** : int

    Number of points in the bisector. 
    
* **Title** : str

    Title of the plot.
    
* **xlabel** : str

    x label of the plot.
    
* **ylabel** : str

    y label of the plot.
    
# Methods
## *Cobweb*.plot
> *Cobweb*.**plot**(\*args, \*\*kargs)

Creates two figures, one containing the Cobweb plot and other with the time series.

**Returns**

* tuple(matplotlib Figure (Cobweb plot), matplotlib Axis (Cobweb plot), matplotlib Figure (Time series), matplotlib Axis (Time series))

## *Cobweb*.add_slider
> *Cobweb*.**add_slider**(param_name, \*, valinit=None, valstep=0.1, valinterval=10)

Adds a slider which can change the value of a parameter in execution time.

**Parameters**

* param_name : str
    The string key of the variable. Must be the same as the key in the `dF` function.

**Key Arguments**

* valinit : float

    Initial value of the parameter.
    
* valinterval : Union[float, list]

    The range of values the slider of the parameter will cover.
    
* valstep : float

    Precision in the slider.

**Returns**

* None

## *Cobweb*.initial_position_slider
> *Cobweb*.**initial_position_slider**(\*, valinit=None, valstep=0.05, valinterval=None)

Adds a slider for changing initial value on a cobweb plot.

**Key Arguments**

* valinit : numeric, optional

    Initial position. Default value is the same as initial position given when initializing Cobweb object.

* valinterval : Union[float, list]

    The range of values the slider of the parameter will cover.

* valstep : float

    Precision in the slider.

**Returns**

* None
