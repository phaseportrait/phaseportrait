
# trajectory
> *class* phaseportrait.trajectories.**trajectory**(*dF, dimension, \*, Range=None, dF_args={}, n_points=10000, runge_kutta_step=0.01, runge_kutta_freq=1, \*\*karg*)

Parent class for trajectories. Represents trajectories given a [dF](dFfunction.md) function with N args.

Class inheriting must have the following methods:

>   def _prepare_plot(self): ...

Prepares the plots: axis titles, graph title, grid, etc.
    
>   def _plot_lines(self, val, val_init): ...

Plots a line of points given in a tuple of positions `val` and an initial position `val_init`, both N-dimensional.

>   def _scatter_start_point(self, val_init): ...

Marks starting position `val_init` (N-dimensional) in the several plots created. 
    
>   def _scatter_trajectory(self, val, color, cmap): ...

Plots with points `val` (N-dimensional list) according to `color` (N-dimensional) with `cmap` color map.

# Example (from Trajectories2D):
```py
def _plot_lines(self, val, val_init):
        self.ax['Z'].plot(val[0,1:], val[1,1:], label=f"({','.join(tuple(map(str, val_init)))})")


def _scatter_start_point(self, val_init):
    self.ax['Z'].scatter(val_init[0], val_init[1], s=self.size+1, c=[0])


def _scatter_trajectory(self, val, color, cmap):
    self.ax['Z'].scatter(val[0,:], val[1,:], s=self.size, c=color, cmap=cmap)


def _prepare_plot(self):
    for coord, r0, r1, x_label, y_label in [
        ('Z', 0, 1, self.xlabel, self.ylabel),
    ]:

        self.ax[coord].set_title(f'{self.Titulo}')
        if self.Range is not None:
            self.ax[coord].set_xlim(self.Range[r0,:])
            self.ax[coord].set_ylim(self.Range[r1,:])
        self.ax[coord].set_xlabel(f'{x_label}')
        self.ax[coord].set_ylabel(f'{y_label}')
        self.ax[coord].grid()
```
