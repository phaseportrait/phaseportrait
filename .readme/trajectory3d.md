# Trajectory3D
> *class* phaseportrait.**Trajectory3D**(*dF, \*, Range=None, dF_args={}, n_points=10000, runge_kutta_step=0.01, runge_kutta_freq=1, \*\*kwargs*)

Gives the option to represent 3D trajectories given a [dF](dFfunction.md) function with 3 args.

| Attributes          | Methods                                                                  |
| ------------------ | ------------------------------------------------------------------------ |
| dF                 | [initial_position           ](#trajectory3dinitial_position)             |
| dF_args            | [termalize                 ](#trajectory3dtermalize)                     |
| Range              | [add_slider                 ](#trajectory3dadd_slider)                   |
| values             | [plot                       ](#trajectory3dplot)                         |
| velocity           | [compute_trajectory         ](#trajectory3dcompute_trajectory)           |
| initial_conditions | [rungekutta_time_independent](#trajectory3drungekutta_time_independent)  |
| runge_kutta_step   |                                                                          |
| runge_kutta_freq   |                                                                          |
| n_points           |                                                                          |
| Title              |                                                                          |
| xlabel             |                                                                          |
| ylabel             |                                                                          |
| zlabel             |                                                                          |
| fig                |                                                                          |
| ax                 |                                                                          |
| sliders            |                                                                          |
| lines              |                                                                          |
| termalization      |                                                                          |
| color              |                                                                          |

### **Attributes**
* **dF** ([dF](dFfunction.md) function) - computes the derivatives of given coordinates.

* **dF_args** (dict) - dictionary with parameters for `dF` function.

* **Range** (Optional[list, float]) - see [defining a 3D range](#defining-range).

* **lines**=False (bool) - representing with lines instead of points.

* **color** (str) - if `'t'` passed, trajectories are colored depending on time. It doesn't work with `lines=True`. In other case, it paints dependong on velocities with the color scheme given.

* **termalization**=0 (int) - number of steps taken before trajectory is saved.

* **size**=0.5 (float) - point size in the plot.

* **numba**=False (bool) - compiles [dF](dFfunction.md) using numba.

* **n_points** (int) - number of points in the plot.

* **runge_kutta_spet** (float) - time step in 4th order runge-kutta algorithm.

* **runge_kutta_freq** (int) - number of points computed between saved positions.

* **Title** (str) -  title of the plot. Default value is `'Trajectory'`.
  
* **xlabel** (str) -  x axis label in the plot. Default value is `'X'`.
  
* **ylabel** (str) -  y axis label in the plot. Default value is `'Y'`.

* **zlabel** (str) -  z axis label in the plot. Default value is `'Z'`.

* **mark_start_point** (bool) - marks staring position with a bigger point size.


# Methods
## *Trajectory3D*.initial_position
> *Trajectory3D*.**initial_position**(**position*)

Parameter `position` must be a 3 element list or ndarray.


## *Trajectory3D*.termalize
> *Trajectory3D*.**termalize**(**position*)

Parameter `position` is optional. If it is not introduced, a random number between 0 and 1 will be taken for each coordinate.

## *Trajectory3D*.add_slider
> *Trajectory3D*.**add_slider**(*param_name, \*, valinit=None, valstep=0.1, valinterval=10*)

Adds a [slider](slider.md) which can change the value of a parameter in execution time.


## *Trajectory3D*.plot
> *Trajectory3D*.**plot**(*, color=None)

Takes as arguments class attributes. Color scheme can be changed introducing kwarg `color`. A list with accepted values can be found [here](https://matplotlib.org/stable/gallery/color/colormap_reference.html). 


## *Trajectory3D*.compute_trajectory
> *Trajectory3D*.**compute_trajectory**(*initial_values*)

Given an initial posotion by `initial_values` (containing 3 coordinates), the method returns a tuple with two lists: positions and difference between following positions. Returns `n_points` points.


## *Trajectory3D*.rungekutta_time_independent
> *Trajectory3D*.**rungekutta_time_independent**(*initial_values*)

Generator that given `initial_values`, returns the next point.

# Defining Range:

1. A single number. In this case the range is defined from zero to the given number in all axes.

2. A range, such `[lowerLimit , upperLimit]`. All axes will take the same limits.

3. Three ranges, such that `[[xAxisLowerLimit , xAxisUpperLimit], [yAxisLowerLimit , yAxisUpperLimit], [zAxisLowerLimit , zAxisUpperLimit]]`

All of the above can be mixed. For example, defining `[[0,20],[1,2],[-2,2]]` can be done as `[[0,20], [1,2], 2]` .