import numpy as np
from matplotlib.colors import Normalize
from matplotlib.collections import LineCollection, PolyCollection

# Adapted from Raymond Speth https://web.mit.edu/speth/Public/streamlines.py with MIT license.

class Streamlines_base3D:
    """
    Streamlines
    --------
    Creates trajectories given a `dF` function. Using Euler integrator.
    
    Integrated in:
        -PhasePortrait3D
    """



    def __init__(
        self, dF, X, Y, Z, spacing=2, maxLen=2500, detectLoops=False, deltat=0.01, *, dF_args=None, polar=False, dr=1, density=1
    ):
        """
        Compute a set of streamlines given velocity function `dF`.


        Parameters
        --------

        X, Y and Z: 1D or 2D arrays
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

        # PP = 0.99999999
        PP = 1

        self.density = int(abs(density))

        xa = np.asanyarray(X)
        ya = np.asanyarray(Y)
        za = np.asanyarray(Z)
        self.x = xa if xa.ndim == 1 else xa[0,:,0]
        self.y = ya if ya.ndim == 1 else ya[:,0,0]
        self.z = za if za.ndim == 1 else za[0,0,:]
        self.dx = PP*(self.x[-1] - self.x[0]) / (self.x.size - 1) / self.density # assume a regular grid
        self.dy = PP*(self.y[-1] - self.y[0]) / (self.y.size - 1) / self.density # assume a regular grid
        self.dz = PP*(self.z[-1] - self.z[0]) / (self.z.size - 1) / self.density # assume a regular grid
        
        self.dr = dr #(self.x[1]-self.x[0])/self.x.shape[0] * dr/100
        self.Hipot = np.sqrt(np.square(self.dx) + np.square(self.dy) + np.square(self.dz))

        self.polar = polar

        # marker for which regions have contours
        self.used = np.zeros((X.shape[0]*self.density, X.shape[1]*self.density, X.shape[2]*self.density), dtype=bool)
        self.used[0] = True
        self.used[-1] = True
        self.used[:, 0] = True
        self.used[:, -1] = True
        self.used[:,:, 0] = True
        self.used[:,:, -1] = True

        # Make the streamlines
        self.streamlines = []

        i = 0
        while not self.used.all():
            nz = np.transpose(np.logical_not(self.used).nonzero())
            # Make a streamline starting at the first unrepresented grid point
            choose = np.random.randint(nz.shape[0])


            x = nz[choose][0]*self.dx + self.x[0]
            y = nz[choose][1]*self.dy + self.y[0]
            z = nz[choose][2]*self.dz + self.z[0]
            self.streamlines.append(
                self._makeStreamline(x, y, z)
            )
            # self.streamlines.append(
            #     self._makeStreamline(self.x[nz[0][0]], self.y[nz[0][1]])
            # )

            # import matplotlib.pyplot as plt
            # fig, ax = plt.subplots()
            # ax.plot(self.streamlines[0][0])
            # ax.plot(self.streamlines[0][1])
            # ax.plot(self.streamlines[0][2])
            # plt.show()
            # plt.close(fig)
            # i+=1
            # if i==40:
            #     break

    def _makeStreamline(self, x0, y0, z0):
        """
        Compute a streamline extending in both directions from the given point. Using Euler integrator.
        """

        sx, sy, sz, svelocity = self._makeHalfStreamline(x0, y0, z0, 1)  # forwards
        rx, ry, rz, rvelocity = self._makeHalfStreamline(x0, y0, z0, -1)  # backwards

        rx.reverse()
        ry.reverse()
        rz.reverse()
        rvelocity.reverse()

        u, v, w = self._speed(x0, y0, z0)

        return rx + [x0] + sx, ry + [y0] + sy, rz + [z0] + sz,  rvelocity + [np.sqrt(u*u + v*v + w*w)] + svelocity
    

    def _speed(self, x, y, z):
        if not self.polar:
            u, v, w = self.dF(x,y,z, **self.dF_args)
        else: # TODO: complete
            R, Theta = np.sqrt(x*x + y*y + z*z), np.arctan2(y, x)
            Phi  = np.arccos(z/R) 
            dR, dTheta, dPhi = self.dF(R, Theta, Phi, **self.dF_args)
            u, v, w = \
                dR*np.cos(Theta)*np.sin(Phi) - R*np.sin(Theta)*np.sin(Phi)*dTheta + R*np.cos(Theta)*np.cos(Phi) * dPhi, \
                dR*np.sin(Theta)*np.sin(Phi) + R*np.cos(Theta)*np.sin(Phi)*dTheta + R*np.sin(Theta)*np.cos(Phi) * dPhi, \
                dR*np.cos(Phi) - R*np.sin(Phi)*dPhi
        return u, v, w

    def _makeHalfStreamline(self, x0, y0, z0, sign):
        """
        Compute a streamline extending in one direction from the given point. Using Euler integrator.
        """

        xmin = self.x[0]
        xmax = self.x[-1]
        ymin = self.y[0]
        ymax = self.y[-1]
        zmin = self.z[0]
        zmax = self.z[-1]

        sx = []
        sy = []
        sz = []
        svelocity = []

        x = x0
        y = y0
        z = z0
        i = 0

        prev_xi = None
        prev_yj = None
        prev_zk = None

        x_clip = lambda x: x%self.used.shape[0]
        y_clip = lambda y: y%self.used.shape[1]
        z_clip = lambda z: z%self.used.shape[2]

        persistency = 20

        while xmin < x < xmax and ymin < y < ymax and zmin < z < zmax:
            xi = (x - self.x[0]) / self.dx
            yj = (y - self.y[0]) / self.dy
            zk = (z - self.z[0]) / self.dz

            xi, yj, zk = int(np.rint(xi)), int(np.rint(yj)), int(np.rint(zk))

            if i%10==0:
                if self.detectLoops and self._detectLoop(sx, sy, sz):
                    break

            if not self.used[xi, yj, zk]:
                prev_xi = xi
                prev_yj = yj
                prev_zk = zk

                # self.used[
                #     x_clip(prev_xi - self.spacing[0]): x_clip(prev_xi + self.spacing[0]+1),
                #     y_clip(prev_yj - self.spacing[1]): y_clip(prev_yj + self.spacing[1]+1)
                #     ] = True
                self.used[prev_xi, prev_yj, prev_zk] = True

            if i > self.maxLen / 2:
                break

            u, v, w = self._speed(x, y, z)

            x += sign * self.deltat * u
            y += sign * self.deltat * v
            z += sign * self.deltat * w
            _speed = np.sqrt(u*u + v*v + w*w)

            sx.append(x)
            sy.append(y)
            sz.append(z)
            svelocity.append(_speed)
            if _speed==0:
                break

            i += 1

            if self.used[xi, yj, zk] and (prev_xi!=xi or prev_yj!=yj or prev_zk!=zk):
                persistency -= 1
                if persistency <= 0:
                    break

                # self.used[
                #     x_clip(prev_xi): x_clip(prev_xi + self.spacing[0]+1),
                #     y_clip(prev_yj): y_clip(prev_yj + self.spacing[1]+1)
                #     ] = True

        return sx, sy, sz, svelocity

    def _detectLoop(self, xVals, yVals, zVals):
        """ Detect closed loops and nodes in a streamline. """
        x = xVals[-1]
        y = yVals[-1]
        z = zVals[-1]
        
        D = np.array(
            [np.sqrt(np.square(x - xj) + np.square(y - yj) + np.square(z - zj)) for xj, yj, zj in zip(xVals[:-1], yVals[:-1], zVals[:-1])]
        )
        return (D < (self.dr/100*self.Hipot)).any()