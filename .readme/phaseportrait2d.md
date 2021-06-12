# PhasePortrait2D
> *class* phaseportrait.**PhasePortrait2D**(*dF, Range, \*, MeshDim=10, dF_args={}, Density=1, Polar=False, \*\*kargs*)

Gives the option to represent a 2D phase portrait given a [dF](dFfunction.md) function with 2 args.

| Attributes | Methods                                   |
| --------- | ----------------------------------------- |
| dF        | [add_slider](#phaseportrait2dadd_slider)  |
| Range     | [plot](#phaseportrait2dplot)              |
| dF_args   |                                           |
| Density   |                                           |
| Polar     |                                           |
| L         |                                           |
| Title     |                                           |
| xlabel    |                                           |
| ylabel    |                                           |
| color     |                                           |
| sliders   |                                           |
| fig       |                                           |
| ax        |                                           |

### **Attributes**
* **dF** ([dF](dFfunction.md) function) - computes the derivatives of given coordinates.

* **dF_args** (dict) - dictionary with parameters for `dF` function.
  
* **Range** (Optional[list, float]) - see [defining a 2D range](#defining-range).
  
* **Polar** (bool) - boolean with default value `False`. It must be passed when `dF` function computes polar coordinates.
  
* **Density** (float) - controls closeness of nearby trajectories. Default value is 1. Changing this value affects considerably computing time.

* **MeshDim** (int) -  in order to calculate the phase portrait, a mesh is created, which depends on the given range. The side of the mesh is calculated by multiplying *MeshDim* value by the length of given *Range*. Default value is 10.
  
* **Title** (str) -  title of the plot. Default value is `'Phase Portrait'`.
  
* **xlabel** (str) -  x axis label in the plot. Default value is `'X'`.
  
* **ylabel** (str) -  y axis label in the plot. Default value is `r"$\dot{X}$"`.



# Methods
## *PhasePortrait2D*.plot
> *PhasePortrait2D*.**plot**(*, color=None)

Takes as arguments class attributes. Color scheme can be changed introducing kwarg `color`. A list with accepted values can be found [here](https://matplotlib.org/stable/gallery/color/colormap_reference.html). 


## *PhasePortrait2D*.add_slider
> *PhasePortrait2D*.**add_slider**(*param_name, \*, valinit=None, valstep=0.1, valinterval=10*)

Adds a [slider](slider.md) which can change the value of a parameter in execution time.

# Defining Range:
1. A single number. In this case the range is defined from zero to the given number in both axes.

2. A range, such `[lowerLimit , upperLimit]`. Both axes will take the same limits.

3. Two ranges, such that `[[xAxisLowerLimit , xAxisUpperLimit], [yAxisLowerLimit , yAxisUpperLimit]]`