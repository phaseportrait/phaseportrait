import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import LineCollection
from matplotlib.colors import Colormap, Normalize
from mpl_toolkits.mplot3d.art3d import Line3DCollection, Patch3DCollection

from .trajectories import trajectory


class Trajectory3D(trajectory):
    """
    Trajectory3D
    ----------
    Class dedicated to compute and represent trajectories in 2D.
        
    Methods
    -------    
    * thermalize : Adds thermalization steps and random initial position. 
    * initial_position : Adds a trajectory with the given initial position. 
    * plot : Prepares the plots and computes the values.  Returns the axis and the figure. 
    * add_slider : Adds a `Slider` for the `dF` function. 
    * _prepare_plot : Prepares the plots. 
    * _scatter_start_point : Scatter all the start points. 
    * _scatter_trajectory : Scatter all the trajectories. 
    * _plot_lines : Plots the lines of all the trajectories. 
    * _create_sliders_plot : Creates the sliders plot.
    """ 
    _name_ = 'Trajectory3D'

    def __init__(self, dF, *, Range=None, dF_args={}, n_points=10000, runge_kutta_step=0.01, runge_kutta_freq=1, **kargs):
        """
        Creates an instance of Trajectory3D

        Args:
            dF (callable) :A `dF` type function.
            Range (list, optional) :Ranges of the axis in the main plot, by default None
            dF_args (dict, optional) :If necesary, must contain the kargs for the `dF` function, by default {}
            n_points (int, optional) :Maximum number of points to be calculated and represented, by default 10000
            runge_kutta_step (float, optional) :Step of 'time' in the Runge-Kutta method, by default 0.01
            runge_kutta_freq (int, optional) :Number of times `dF` is aplied between positions saved, by default 1
            xlabel (str, optional) :x label of the plot, by default 'X'
            ylabel (str, optional) :y label of the plot, by default 'Y'
            zlabel (str, optional) :z label of the plot, by default 'Z'
        """

        super().__init__(dF, 3, Range=Range, dF_args=dF_args, n_points=n_points, runge_kutta_step=runge_kutta_step, runge_kutta_freq=runge_kutta_freq, **kargs)

        self.xlabel = kargs['xlabel'] if kargs.get('xlabel') else 'X'
        self.ylabel = kargs['ylabel'] if kargs.get('ylabel') else 'Y'
        self.zlabel = kargs['zlabel'] if kargs.get('zlabel') else 'Z'


        # Variables for plots
        figX, axX= plt.subplots()
        figY, axY= plt.subplots()
        figZ, axZ= plt.subplots()
        fig3d = plt.figure()
        ax3d = fig3d.add_subplot(projection='3d')

        self.fig = {
            'X': figX,
            'Y': figY,
            'Z': figZ,
            '3d': fig3d
        }
        self.ax = {
            'X': axX,
            'Y': axY,
            'Z': axZ,
            '3d': ax3d
        }


    def _plot_lines(self, val, vel, val_init, *, color=None, cnorm=None):
        val_ = val.T.reshape(-1, 1, 3)
        segments = np.concatenate([val_[:-1], val_[1:]], axis=1)

        if color is None:
            vel_ = np.sqrt(np.sum(np.square(vel), axis=0))
            if cnorm is None:
                cnorm = Normalize(vel_.min(), vel_.max())
            C = plt.get_cmap(self.color)(cnorm(vel_))
        else:
            C = color
        line3d = Line3DCollection(segments, linewidth=self.size, color=C)
        linex = LineCollection(segments[:,:,(1,2)], linewidth=self.size, color=C)
        liney = LineCollection(segments[:,:,(0,2)], linewidth=self.size, color=C)
        linez = LineCollection(segments[:,:,(0,1)], linewidth=self.size, color=C)

        

        self.ax['3d'].add_collection(line3d)
        self.ax['X'].add_collection(linex)
        self.ax['Y'].add_collection(liney)
        self.ax['Z'].add_collection(linez)


        if isinstance(C, list): 
            C = C[0]
        self.ax['3d'].plot(*[[val_init[i],val[i,0]] for i in range(3)], '-', linewidth=self.size, color=C)
        self.ax['X'].plot([val_init[1],val[1,0]], [val_init[2], val[2,0]], '-', linewidth=self.size, color=C, zorder=-1)
        self.ax['Y'].plot([val_init[0],val[0,0]], [val_init[2], val[2,0]], '-', linewidth=self.size, color=C, zorder=-1)
        self.ax['Z'].plot([val_init[0],val[0,0]], [val_init[1], val[1,0]], '-', linewidth=self.size, color=C, zorder=-1)
        self._update_3d_lims()

    def _update_3d_lims(self):
        self.ax['3d'].set_xlim(self.ax['Y'].get_xlim())
        self.ax['3d'].set_ylim(self.ax['Z'].get_xlim())
        self.ax['3d'].set_zlim(self.ax['X'].get_ylim())


    def _scatter_start_point(self, val_init):
        label = f"({','.join(tuple(map(str, val_init)))})"
        self.ax['3d'].scatter3D(*val_init, s=self.size*2, label=label)
        self.ax['X'].scatter(val_init[1], val_init[2], s=self.size*2, label=label)
        self.ax['Y'].scatter(val_init[0], val_init[2], s=self.size*2, label=label)
        self.ax['Z'].scatter(val_init[0], val_init[1], s=self.size*2, label=label)


    def _scatter_trajectory(self, val, color, cmap):
        self.ax['3d'].scatter3D(*val, s=self.size, c=color, cmap=cmap)
        self.ax['X'].scatter(val[1,:], val[2,:], s=self.size, c=color, cmap=cmap)
        self.ax['Y'].scatter(val[0,:], val[2,:], s=self.size, c=color, cmap=cmap)
        self.ax['Z'].scatter(val[0,:], val[1,:], s=self.size, c=color, cmap=cmap)
        self._update_3d_lims()


    def _prepare_plot(self, grid=False):
        self.ax['3d'].set_title(f'{self.Title}')
        if self.Range is not None:
            self.ax['3d'].set_xlim(self.Range[0,:])
            self.ax['3d'].set_ylim(self.Range[1,:])
            self.ax['3d'].set_zlim(self.Range[2,:])
        self.ax['3d'].set_xlabel(f'{self.xlabel}')
        self.ax['3d'].set_ylabel(f'{self.ylabel}')
        self.ax['3d'].set_zlabel(f'{self.zlabel}')
        self.ax['3d'].grid(grid)

        for coord, r0, r1, title, x_label, y_label in [
            ('X', 1, 2, 'YZ', self.ylabel, self.zlabel),
            ('Y', 0, 2, 'XZ', self.xlabel, self.zlabel),
            ('Z', 0, 1, 'XY', self.xlabel, self.ylabel),
        ]:

            self.ax[coord].set_title(f'{self.Title}: {title}')
            if self.Range is not None:
                self.ax[coord].set_xlim(self.Range[r0,:])
                self.ax[coord].set_ylim(self.Range[r1,:])
            self.ax[coord].set_xlabel(f'{x_label}')
            self.ax[coord].set_ylabel(f'{y_label}')
            self.ax[coord].grid(grid)
