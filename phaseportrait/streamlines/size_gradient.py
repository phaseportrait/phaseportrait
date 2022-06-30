import numpy as np
from matplotlib.colors import Normalize
from matplotlib.collections import LineCollection, PolyCollection
from mpl_toolkits.mplot3d.art3d import Line3DCollection

from . import Streamlines_base, Streamlines_base3D

class Streamlines_Size_Gradient(Streamlines_base):
    """
    Streamlines
    --------
    Creates trajectories given a `dF` function. Using Euler integrator.
    
    Integrated in:
        -PhasePortrait2D
    """



    def __init__(
        self, dF, X, Y, *Z, spacing=2, maxLen=500, detectLoops=False, deltat=0.01, dF_args=None, dr=0.01, **kargs
    ):
        """
        Compute a set of streamlines given velocity function `dF`.


        Parameters
        --------

        X and Y: 1D or 2D arrays
            arrays of the grid points. The mesh spacing is assumed to be uniform in each dimension.
        
        Key arguments:
        --------
        spacing: int, default=2
            Sets the minimum density of streamlines, in grid points.
        maxLen: int default=500
            The maximum length of an individual streamline segment.
        detectLoops: bool default=False
            Determines whether an attempt is made to stop extending a given streamline before reaching 
            maxLen points if it forms a closed loop or reaches a velocity node.
        deltat: float default=0.01
            delta time for Euler integrator
        dF_args: dict|None default=None
            dF_args of `dF` function.
        dr: float default=0.01
            distance for loop detection.
        """

        if not Z:
            self.proyection="2d"
            self.stream_base = Streamlines_base(dF, X, Y, spacing, maxLen, detectLoops, deltat, dF_args=dF_args, dr=dr, **kargs)
        else:
            self.proyection="3d"
            self.stream_base = Streamlines_base3D(dF, X, Y, Z[0], spacing, maxLen, detectLoops, deltat, dF_args=dF_args, dr=dr, **kargs)
            

    def plot(self, ax, cmap, cnorm, arrow_width):
        for streamline in self.stream_base.streamlines:
            *x, v = streamline
            points = np.array(x).T.reshape(-1 , 1, len(x))
            segments = np.concatenate([points[:-1], points[1:]], axis=1)

            n = len(segments)

            D = np.sqrt(((points[1:] - points[:-1]) ** 2).sum(axis=-1))
            L = D.cumsum().reshape(n, 1) + np.random.uniform(0, 1)
            C = np.zeros((n, 3))
            C[:] = (L * 1.5) % 1

            C = cmap(((L * 1.5) % 1).ravel())

            linewidths = np.zeros(n)
            linewidths[:] = arrow_width - arrow_width*((L.reshape(n) * 1.5) % 1)
            # line = LineCollection(segments, color=C, linewidth=linewidths)
            
            if self.proyection == "2d":
                line = LineCollection(segments, color=C, linewidths=linewidths)
            if self.proyection == "3d":
                line = Line3DCollection(segments, color=C, linewidths=linewidths)

            # line = LineCollection(segments, color=C)
            ax.add_collection(line)