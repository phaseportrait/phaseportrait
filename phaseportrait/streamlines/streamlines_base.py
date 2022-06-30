import numpy as np

# Adapted from Raymond Speth https://web.mit.edu/speth/Public/streamlines.py with MIT license.

class Streamlines_base:
    """
    Streamlines
    --------
    Creates trajectories given a `dF` function. Using Euler integrator.
    
    Integrated in:
        -PhasePortrait2D
    """


    def __init__(
        self, dF, X, Y, spacing=2, maxLen=2500, detectLoops=False, deltat=0.01, *, dF_args=None, polar=False, dr=1, density=1
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
        polar: bool default=false

        Key arguments:
        --------
        dF_args: dict|None default=None
            dF_args of `dF` function.

        dr: float default=1
            distance for loop detection in % of X and Y grid distance.
        """

        self.dF = dF
        self.dF_args = dF_args if dF_args is not None else  {}

        self.spacing = spacing
        self.detectLoops = detectLoops
        self.maxLen = maxLen
        self.deltat = deltat

        # TODO: convert floats to indexes can cause index error: out of range. A smaller delta usually solves it.
        # PP = 0.99999999
        PP = 1

        self.density = int(abs(density))

        xa = np.asanyarray(X)
        ya = np.asanyarray(Y)
        self.x = xa if xa.ndim == 1 else xa[0]
        self.y = ya if ya.ndim == 1 else ya[:, 0]
        self.dx = PP*(self.x[-1] - self.x[0]) / (self.x.size - 1) / self.density
        self.dy = PP*(self.y[-1] - self.y[0]) / (self.y.size - 1) / self.density
        self.dr = (self.x[1]-self.x[0])/self.x.shape[0] * dr/100

        self.polar = polar

        # marker for which regions have contours
        self.used = np.zeros((X.shape[0]*self.density, X.shape[1]*self.density), dtype=bool)
        self.used[0] = True
        self.used[-1] = True
        self.used[:, 0] = True
        self.used[:, -1] = True


        self.streamlines = []

        while not self.used.all():
            nz = np.transpose(np.logical_not(self.used).nonzero())
            # Make a streamline starting at the first unrepresented grid point
            choose = np.random.randint(nz.shape[0])


            x = nz[choose][0]*self.dx + self.x[0]
            y = nz[choose][1]*self.dy + self.y[0]
            self.streamlines.append(
                self._makeStreamline(x, y)
            )


    def _makeStreamline(self, x0, y0):
        """
        Compute a streamline extending in both directions from the given point. Using Euler integrator.
        """

        sx, sy, svelocity = self._makeHalfStreamline(x0, y0, 1)  # forwards
        rx, ry, rvelocity = self._makeHalfStreamline(x0, y0, -1)  # backwards

        rx.reverse()
        ry.reverse()
        rvelocity.reverse()

        u, v = self._speed(x0, y0)

        return rx + [x0] + sx, ry + [y0] + sy, rvelocity + [np.sqrt(u*u + v*v)] + svelocity

    def _speed(self, x, y):
        """
        Computes speed in given coordinates
        """
        if not self.polar:
            u, v = self.dF(x,y, **self.dF_args)
        else:
            R, Theta = np.sqrt(x**2 + y**2), np.arctan2(y, x)
            dR, dTheta = self.dF(R, Theta, **self.dF_args)
            u, v = dR*np.cos(Theta) - R*np.sin(Theta)*dTheta, dR*np.sin(Theta)+R*np.cos(Theta)*dTheta
        return u, v

    def _makeHalfStreamline(self, x0, y0, sign):
        """
        Compute a streamline extending in one direction from the given point. Using Euler integrator.
        """

        xmin = self.x[0]
        xmax = self.x[-1]
        ymin = self.y[0]
        ymax = self.y[-1]

        sx = []
        sy = []
        svelocity = []

        x = x0
        y = y0
        i = 0

        prev_xi = None
        prev_yj = None

        x_clip = lambda x: x%self.used.shape[0]
        y_clip = lambda y: y%self.used.shape[1]

        persistency = 20

        while xmin < x < xmax and ymin < y < ymax:
            xi = (x - self.x[0]) / self.dx
            yj = (y - self.y[0]) / self.dy

            xi, yj = int(np.rint(xi)), int(np.rint(yj))

            if i%10==0:
                if self.detectLoops and self._detectLoop(sx, sy):
                    break

            if not self.used[xi, yj]:
                prev_xi = xi
                prev_yj = yj

                # TODO: Check if necessary.
                # self.used[
                #     x_clip(prev_xi - self.spacing[0]): x_clip(prev_xi + self.spacing[0]+1),
                #     y_clip(prev_yj - self.spacing[1]): y_clip(prev_yj + self.spacing[1]+1)
                #     ] = True
                self.used[prev_xi, prev_yj] = True

            if i > self.maxLen / 2:
                break

            u, v = self._speed(x, y)

            x += sign * self.deltat * u
            y += sign * self.deltat * v
            _speed = np.hypot(u,v)

            sx.append(x)
            sy.append(y)
            svelocity.append(_speed)
            if _speed==0:
                break

            i += 1

            if self.used[xi, yj] and (prev_xi!=xi or prev_yj!=yj):
                persistency -= 1
                if persistency <= 0:
                    break

        return sx, sy, svelocity

    def _detectLoop(self, xVals, yVals):
        """ Detect closed loops and nodes in a streamline. """
        x = xVals[-1]
        y = yVals[-1]
        D = np.array(
            [np.hypot(x - xj, y - yj) for xj, yj in zip(xVals[:-1], yVals[:-1])]
        )
        return (D < (self.dr/100*np.hypot(self.dx, self.dy))).any()