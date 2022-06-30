import numpy as np
from matplotlib.colors import Normalize
from matplotlib.collections import LineCollection, PolyCollection

from . import Streamlines_base

class Streamlines_Size_Gradient(Streamlines_base):
    """
    Streamlines
    --------
    Creates trajectories given a `dF` function. Using Euler integrator.
    
    Integrated in:
        -PhasePortrait2D
    """



    def __init__(
        self, dF, X, Y, spacing=2, maxLen=500, detectLoops=False, deltat=0.01, *, dF_args=None, dr=0.01, **kargs
    ):
        """
        Compute a set of streamlines given velocity function `dF`.


        Parameters
        --------

        X and Y: 1D or 2D arrays
            arrays of the grid points. The mesh spacing is assumed to be uniform in each dimension.
        spacing: int, default=2
            Sets the minimum density of streamlines, in grid points.
        maxLen: int default=500
            The maximum length of an individual streamline segment.
        detectLoops: bool default=False
            Determines whether an attempt is made to stop extending a given streamline before reaching 
            maxLen points if it forms a closed loop or reaches a velocity node.
        deltat: float default=0.01

        Key arguments:
        --------
        dF_args: dict|None default=None
            dF_args of `dF` function.

        dr: float default=0.01
            distance for loop detection.
        """

        super().__init__(dF, X, Y, spacing, maxLen, detectLoops, deltat, dF_args=dF_args, dr=dr, **kargs)

    def plot(self, ax, cmap, cnorm, arrow_width):
        for streamline in self.streamlines:
            x, y, v = streamline
            points = np.array([x, y]).T.reshape(-1 , 1, 2)
            segments = np.concatenate([points[:-1], points[1:]], axis=1)

            n = len(segments)

            D = np.sqrt(((points[1:] - points[:-1]) ** 2).sum(axis=-1))
            L = D.cumsum().reshape(n, 1) + np.random.uniform(0, 1)
            C = np.zeros((n, 3))
            C[:] = (L * 1.5) % 1

            C = cmap(((L * 1.5) % 1).ravel())

            linewidths = np.zeros(n)
            linewidths[:] = arrow_width - arrow_width*((L.reshape(n) * 1.5) % 1)
            line = LineCollection(segments, color=C, linewidth=linewidths)

            line = LineCollection(segments, color=C)
            ax.add_collection(line)