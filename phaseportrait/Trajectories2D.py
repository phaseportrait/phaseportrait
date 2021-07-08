import matplotlib.pyplot as plt

from .trajectories import trajectory


class Trajectory2D(trajectory):
    """
    Trajectory2D
    ----------
    Class dedicated to compute and represent trajectories in 2D.
        
    Methods
    -------
    thermalize : 
        Adds thermalization steps and random initial position.
        
    initial_position :
        Adds a trajectory with the given initial position.
        
    plot : 
        Prepares the plots and computes the values. 
        Returns the axis and the figure.
        
    add_slider :
        Adds a `Slider` for the `dF` function.
        
    _prepare_plot :
        Prepares the plots.
        
    _scatter_start_point :
        Scatter all the start points.
        
    _scatter_trajectory :
        Scatter all the trajectories.
        
    _plot_lines :
        Plots the lines of all the trajectories.
        
    _create_sliders_plot :
        Creates the sliders plot.
    """ 

    _name_ = 'Trajectory2D'

    def __init__(self, dF, *, Range=None, dF_args={}, n_points=10000, runge_kutta_step=0.01, runge_kutta_freq=1, **kargs):
        """
        Creates an instance of Trjaectoy2D

        Parameters
        ----------
        dF : callable
            A `dF` type function.
            
        Key Parameters
        -------------
        Range : list, optional
            Ranges if the axis in the main plot, by default None
        dF_args : dict, optional
            If necesary, must contain the kargs for the `dF` function, by default {}
        n_points : int, optional
            Maximum number of points to be calculated and represented, by default 10000
        runge_kutta_step : float, optional
            Step of 'time' in the Runge-Kutta method, by default 0.01
        runge_kutta_freq : int, optional
            Number of times `dF` is aplied between positions saved, by default 1
        xlabel : str, optional
            x label of the plot, by default 'X'
        ylabel : str, optional
            y label of the plot, by default 'Y'
        """
        
        super().__init__(dF, 2, Range=Range, dF_args=dF_args, n_points=n_points, runge_kutta_step=runge_kutta_step, runge_kutta_freq=runge_kutta_freq, **kargs)

        # Variables for plots
        self.xlabel = kargs['xlabel'] if kargs.get('xlabel') else 'X'
        self.ylabel = kargs['ylabel'] if kargs.get('ylabel') else 'Y'


        figZ, axZ= plt.subplots()

        self.fig = {
            'Z': figZ,
        }
        self.ax = {
            'Z': axZ,
        }


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

            self.ax[coord].set_title(f'{self.Title}')
            if self.Range is not None:
                self.ax[coord].set_xlim(self.Range[r0,:])
                self.ax[coord].set_ylim(self.Range[r1,:])
            self.ax[coord].set_xlabel(f'{x_label}')
            self.ax[coord].set_ylabel(f'{y_label}')
            self.ax[coord].grid()