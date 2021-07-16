
# Trajectory
> *class* phaseportrait.trajectories.**trajectory**(*dF, dimension, \*, Range=None, dF_args={}, n_points=10000, runge_kutta_step=0.01, runge_kutta_freq=1, \*\*karg*)

**This class is not meant to be used by the user.**

Parent class for [trajectory2d](trajectory2d.md) and [trajectory3d](trajectory3d.md). Represents trajectories given a [dF](dFfunction.md) function with N args.

Class inheriting must have the following methods:

* **def _prepare_plot(self): ...**

    Prepares the plots: axis titles, graph title, grid, etc.
    
* **def _plot_lines(self, val, val_init): ...**

    Plots a line of points given in a tuple of positions `val` and an initial position `val_init`, both N-dimensional.

* **def _scatter_start_point(self, val_init): ...**

    Marks starting position `val_init` (N-dimensional) in the several plots created. 
    
* **def _scatter_trajectory(self, val, color, cmap): ...**

    Plots with points `val` (N-dimensional list) according to `color` (N-dimensional) with `cmap` color map.

# Methods

### *trajectory*.thermalize
> *trajectory*.**thermalize**(*\*, thermalization_steps=200*)

Sets the thermalization steps if given and executes self.initial_position method.

**Returns**

* None

### *trajectory*.initial_position
> *trajectory*.**initial_position**()

Adds a initial position for the computation.
More than one can be added.

**Parameters**

* args : Union[float, list[2], list[3]], optional

    Initial position for the computation.
    If None, a random position is chosen.

**Returns**

* None

### *trajectory*.plot
> *trajectory*.**plot**()

Prepares the plots and computes the values.

**Key Arguments**

* color : str

    Matplotlib `Cmap`. If given `'t'` value, color follows the temporal evolution of the trajectory.  

**Returns**

* tuple(matplotlib Figure, matplotlib Axis)

* None (if attribute `fig` or `ax` is not found)

### *trajectory*.add_slider
> *trajectory*.**add_slider**(*param_name, \*, valinit=None, valstep=0.1, valinterval=10*)

Adds a slider which can change the value of a parameter in execution time.

**Parameters**

* param_name : str

    The string key of the variable. Must be the same as the key in the `dF` function.

**Key Arguments**

* valinit : float, default=None

    Initial value of the parameter.
    
* valinterval : Union[float, list], default=0.1

    The range of values the slider of the parameter will cover.
    
* valstep : float, default=10

    Precision in the slider.

**Returns**

* None

# Examples

This class is implemented in other classes, check out:

* [Trajectory2D](trajectory2d.md)
* [Trajectory3D](trajectory3d.md)