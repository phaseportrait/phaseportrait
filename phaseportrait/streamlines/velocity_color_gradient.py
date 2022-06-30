import numpy as np
from matplotlib.colors import Normalize
from matplotlib.collections import LineCollection, PatchCollection 
from matplotlib.patches import ArrowStyle, FancyArrowPatch
from mpl_toolkits.mplot3d.art3d import Line3DCollection, Patch3DCollection
from mpl_toolkits.mplot3d import proj3d

from . import Streamlines_base, Streamlines_base3D
# Adapted from Raymond Speth https://web.mit.edu/speth/Public/streamlines.py with MIT license.

class Streamlines_Velocity_Color_Gradient:
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
            
        # self.arrowstyle = 


    def _velocity_normalization(self):
        """ Returns a colour normalization function for colouring the stream lines. """
        vmax = None
        vmin = None

        for streamline in self.stream_base.streamlines:
            *_, v = streamline
            vmax = max(v + ([vmax] if vmax is not None else []))
            vmin = min(v + ([vmin] if vmin is not None else []))

        return Normalize(vmin, vmax)

    def plot(self, ax, cmap, cnorm, arrow_width):
        n_segments = 0
        for streamline in self.stream_base.streamlines:
            x, *_ = streamline
            n_segments += len(x)

        p_arrow = 50/n_segments

        for streamline in self.stream_base.streamlines:
            *coords, v = streamline
            points = np.array(coords).T.reshape(-1 , 1, 2 if self.proyection=="2d" else 3)
            segments = np.concatenate([points[:-1], points[1:]], axis=1)


            halflength = int(len(coords[0])/2)
            # extreme_distance = self._velocity(x[0], y[0], x[-1], y[-1], deltat=1)

            arrows = []
            # for j, segment in enumerate(segments):
            #     # if np.random.random() < p_arrow:
            #     if j==halflength:
            #         arrows.append(self._make_triangle(segment[0,0], segment[0,1], segment[1,0], segment[1,1], arrow_width))

            #         arrows_C = cmap(cnorm( self._velocity(segment[0,0], segment[0,1], segment[1,0], segment[1,1])))

            segment = segments[halflength]
            # arrows.append(self._make_triangle(segment[0,0], segment[0,1], segment[1,0], segment[1,1], arrow_width))
            arrows_C = cmap(cnorm(v[halflength]))
            
            segment_length = np.sqrt(np.sum(np.square(segment[1]-segment[0])))
            width = self.stream_base.Hipot/2*self.stream_base.dr
            
            class Arrow3D(FancyArrowPatch):
                def __init__(self, posA, posB, *args, **kwargs):
                    super().__init__((0,0), (0,0), *args, **kwargs)
                    self._verts3d = [[posA[i], posB[i]] for i in range(len(posA))]

                def do_3d_projection(self, renderer=None):
                    xs3d, ys3d, zs3d = self._verts3d
                    xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, self.axes.M)
                    self.set_positions((xs[0],ys[0]),(xs[1],ys[1]))
                    return np.min(zs)
            
            arrowstyle = ArrowStyle.Fancy(head_length=10, head_width=5, tail_width=0.1)


            arrows.append(Arrow3D(posA=segment[0,:], posB=segment[1,:], arrowstyle=arrowstyle, color=arrows_C))


            

            C = cmap(cnorm(v))

            if self.proyection == "2d":
                line = LineCollection(segments, color=C)
            if self.proyection == "3d":
                line = Line3DCollection(segments, color=C)
                
            ax.add_collection(line)

            if arrows:
                if self.proyection == "2d":
                    arrow_collection = PatchCollection(arrows, color=arrows_C)
                    ax.add_collection(arrow_collection)
                if self.proyection == "3d":
                    for a in arrows:
                        ax.add_artist(a)
                    # arrow_collection = Patch3DCollection(arrows, zs=[a._verts3d[2][0] for a in arrows], color=arrows_C)
                
                


    def _velocity(self, x,y, x1, y1, *, deltat=None):
        """ Given 2 points and time delta returns velocity. """

        if deltat is None:
            deltat = self.deltat
        dx = x1-x
        dy = y1-y
        modulo = np.sqrt(dx*dx + dy*dy)
        return modulo/deltat