
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

*Aquí me he quedao*