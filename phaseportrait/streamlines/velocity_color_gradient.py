import numpy as np
import matplotlib
from matplotlib.colors import Normalize
from matplotlib.collections import LineCollection, PatchCollection 
from matplotlib.patches import ArrowStyle, FancyArrowPatch
from mpl_toolkits.mplot3d.art3d import Line3DCollection, Patch3DCollection
from mpl_toolkits.mplot3d import proj3d

from .streamlines_base import Streamlines_base, Streamlines_base2D, Streamlines_base3D

class Arrow3D(FancyArrowPatch):
    """
    3D FancyArrowPatch proyection
    """
    def __init__(self, posA, posB, *args, **kwargs):
        super().__init__((0,0), (0,0), *args, **kwargs)
        self._verts3d = [[posA[i], posB[i]] for i in range(len(posA))]

    def do_3d_projection(self, renderer=None):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, self.axes.M)
        self.set_positions((xs[0],ys[0]),(xs[1],ys[1]))
        return np.min(zs)

    # Matplotlib rises error if renderer is not present. If it is, warning is raised. PepeSad
    # def do_3d_projection(self):
    #     xs3d, ys3d, zs3d = self._verts3d
    #     xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, self.axes.M)
    #     self.set_positions((xs[0],ys[0]),(xs[1],ys[1]))
    #     return np.min(zs)


class Streamlines_Velocity_Color_Gradient:
    """
    Streamlines
    --------
    Creates trajectories given a `dF` function. Using Euler integrator.
    
    Integrated in:
    - PhasePortrait2D
    """



    def __init__(
        self, dF, X, Y, *Z, maxLen=500, dF_args=None, **kargs
    ):
        """
        Compute a set of streamlines given velocity function `dF`.

        Args:
            X (list, list[list]): arrays of the grid points. The mesh spacing is assumed to be uniform in each dimension.
            Y (list, list[list]): arrays of the grid points. The mesh spacing is assumed to be uniform in each dimension.
            maxLen (int default=500): The maximum length of an individual streamline segment.
            dF_args (dict|None default=None) : dF_args of `dF` function.
        """
        if not Z:
            self.proyection="2d"
            self.stream_base = Streamlines_base2D(dF, X, Y, maxLen, dF_args=dF_args, **kargs)
        else:
            self.proyection="3d"
            self.stream_base = Streamlines_base3D(dF, X, Y, Z[0], maxLen, dF_args=dF_args, **kargs)


    def _velocity_normalization(self):
        """ Returns a colour normalization function for colouring the stream lines. """
        vmax = None
        vmin = None

        for streamline in self.stream_base.streamlines:
            *_, v = streamline
            vmax = max(v + ([vmax] if vmax is not None else []))
            vmin = min(v + ([vmin] if vmin is not None else []))

        return Normalize(vmin, vmax)

    def plot(self, ax, cmap, cnorm, *, linewidth=None, arrowsize=1, arrowstyle='-|>'):
        # n_segments = 0
        # for streamline in self.stream_base.streamlines:
        #     x, *_ = streamline
        #     n_segments += len(x)



        if self.proyection == "2d":
            LineClass = LineCollection
            ArrowClass = FancyArrowPatch
        if self.proyection == "3d":
            LineClass = Line3DCollection
            ArrowClass = Arrow3D

        if linewidth is None:
            linewidth = matplotlib.rcParams['lines.linewidth']

        line_kw = {}
        arrow_kw = dict(arrowstyle=arrowstyle, mutation_scale=10 * arrowsize)

        for streamline in self.stream_base.streamlines:
            *coords, v = streamline
            points = np.array(coords).T.reshape(-1 , 1, 2 if self.proyection=="2d" else 3)
            segments = np.concatenate([points[:-1], points[1:]], axis=1)

            s = np.sqrt(np.sum(np.square(points), 2))
            s = np.cumsum(s)
            n = np.searchsorted(s, s[-1] / 2.)

            arrows = []
           
            arrows_C = cmap(cnorm(v[n]))

            arrow_tail = points[n][0]
            arrow_head = np.mean(points[n:n + 2], 0)[0]

            arrows.append(ArrowClass(arrow_tail, arrow_head, color=arrows_C, **arrow_kw))

            C = cmap(cnorm(v))

            line = LineClass(segments, color=C, **line_kw)
            ax.add_collection(line)

            for a in arrows:
                ax.add_patch(a)
            # if arrows:
            #     if self.proyection == "2d":
            #         arrow_collection = PatchCollection(arrows, color=arrows_C)
            #         ax.add_collection(arrow_collection)
            #     if self.proyection == "3d":
            #         for a in arrows:
            #             ax.add_patch(a)
                    # arrow_collection = Patch3DCollection(arrows, zs=[a._verts3d[2][0] for a in arrows], color=arrows_C)