import matplotlib.pyplot as plt

from .trajectories import trajectory
 

class Trajectory3D(trajectory):
    """
    Computes a trajectory on a 3D system.
    """
    _name_ = 'Trajectory3D'
    def __init__(self, dF, *, Range=None, dF_args={}, n_points=10000, runge_kutta_step=0.01, runge_kutta_freq=1, **kargs):

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


    def _plot_lines(self, val, val_init):
        self.ax['3d'].plot3D(*val[:,1:], label=f"({','.join(tuple(map(str, val_init)))})")
        self.ax['X'].plot(val[1,1:], val[2,1:], label=f"({','.join(tuple(map(str, val_init)))})")
        self.ax['Y'].plot(val[0,1:], val[2,1:], label=f"({','.join(tuple(map(str, val_init)))})")
        self.ax['Z'].plot(val[0,1:], val[1,1:], label=f"({','.join(tuple(map(str, val_init)))})")


    def _scatter_start_point(self, val_init):
        self.ax['3d'].scatter3D(*val_init, s=self.size+1, c=[0])
        self.ax['X'].scatter(val_init[1], val_init[2], s=self.size+1, c=[0])
        self.ax['Y'].scatter(val_init[0], val_init[2], s=self.size+1, c=[0])
        self.ax['Z'].scatter(val_init[0], val_init[1], s=self.size+1, c=[0])


    def _scatter_trajectory(self, val, color, cmap):
        self.ax['3d'].scatter3D(*val, s=self.size, c=color, cmap=cmap)
        self.ax['X'].scatter(val[1,:], val[2,:], s=self.size, c=color, cmap=cmap)
        self.ax['Y'].scatter(val[0,:], val[2,:], s=self.size, c=color, cmap=cmap)
        self.ax['Z'].scatter(val[0,:], val[1,:], s=self.size, c=color, cmap=cmap)


    def _prepare_plot(self):
        self.ax['3d'].set_title(f'{self.Title}')
        if self.Range is not None:
            self.ax['3d'].set_xlim(self.Range[0,:])
            self.ax['3d'].set_ylim(self.Range[1,:])
            self.ax['3d'].set_zlim(self.Range[2,:])
        self.ax['3d'].set_xlabel(f'{self.xlabel}')
        self.ax['3d'].set_ylabel(f'{self.ylabel}')
        self.ax['3d'].set_zlabel(f'{self.zlabel}')
        self.ax['3d'].grid()

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
            self.ax[coord].grid()