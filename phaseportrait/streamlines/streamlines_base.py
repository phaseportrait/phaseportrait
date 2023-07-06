import numpy as np
from scipy import integrate
# Adapted from Raymond Speth https://web.mit.edu/speth/Public/streamlines.py with MIT license.

class Streamlines_base:
    """
    Streamlines
    --------
    Creates trajectories given a `dF` function. Using Scipy.integrate.odeint integrator.
    
    Integrated in:
    - PhasePortrait2D
    - PhasePorrtait3D
    """

    def __init__(self, odeint_method="scipy") -> None:
        if odeint_method == "scipy":
            self._integration_method = self._scipy_odeint
        elif odeint_method == "euler":
            self._integration_method = self._euler_odeint
        elif odeint_method == "rungekutta3":
            self._integration_method = self._runge_kutta_3rd_odeint
        else:
            raise NameError(f"Integration method {odeint_method} is not in [scipy, euler or rungekutta3]")
    
    def _makeStreamline(self, y0):
        """
        Compute a streamline extending in both directions from the given point.
        """
        
        s, svelocity, i_f = self._makeHalfStreamline(y0, 1)  # forwards
        r, rvelocity, i_b = self._makeHalfStreamline(y0, -1)  # backwards
        
        speed = self._speed(y0)
        
        if np.isnan(speed).any() or np.isinf(speed).any() or i_b==0 or i_f==0:
            return None
        
        svelocity = svelocity[:i_f]
        rvelocity_flip = np.flip(rvelocity[:i_b])
        
        speed = np.sqrt(np.sum(np.square(speed)))
        
        
        if not np.isclose(svelocity[0], speed, rtol=100).all() or not np.isclose(rvelocity[0], speed, rtol=100).all():
            return None
        
        s = s[:i_f]
        r = np.flip(r[:i_b],0)

        if not np.isclose(s[0], y0, rtol=100).all() or not np.isclose(r[0], y0, rtol=100).all():
            return None
        return np.concatenate((r, [y0], s), 0), np.concatenate((rvelocity_flip, [speed], svelocity))
    
    def _speed_2d_no_polar(self, y0, *args, **kargs):
        return np.array(self.dF(*y0, **self.dF_args))
    
    def _speed_2d_polar(self, y0, *args, **kargs):
        R, Theta = np.sqrt(np.sum(np.square(y0))), np.arctan2(y0[1], y0[0])
        dR, dTheta = self.dF(R, Theta, **self.dF_args)
        return np.array([dR*np.cos(Theta) - R*np.sin(Theta)*dTheta, dR*np.sin(Theta)+R*np.cos(Theta)*dTheta])

    def _speed_3d_no_polar(self, y0, *args, **kargs):
        return np.array(self.dF(*y0, **self.dF_args))
    
    def _speed_3d_polar(self, y0, *args, **kargs):
        R, Theta = np.sqrt(np.sum(np.square(y0))), np.arctan2(y0[1], y0[0])
        Phi  = np.arccos(y0[2]/R) 
        dR, dTheta, dPhi = self.dF(R, Theta, Phi, **self.dF_args)
        return np.array([\
            dR*np.cos(Theta)*np.sin(Phi) - R*np.sin(Theta)*np.sin(Phi)*dTheta + R*np.cos(Theta)*np.cos(Phi) * dPhi, \
            dR*np.sin(Theta)*np.sin(Phi) + R*np.cos(Theta)*np.sin(Phi)*dTheta + R*np.sin(Theta)*np.cos(Phi) * dPhi, \
            dR*np.cos(Phi) - R*np.sin(Phi)*dPhi
        ])

    def _speed(self, y0, *args, **kwargs):
        """
        Computes speed in given coordinates
        """
        ...


    def _scipy_odeint(self, coords, sign, deltat):
        return integrate.odeint(self._speed, coords, sign * np.arange(1,5)*0.2*deltat)[-1]
    
    def _euler_odeint(self, coords, sign, deltat):
        return coords + self._speed(coords) * deltat * sign
    
    def _runge_kutta_3rd_odeint(self, coords, sign, deltat):
        k1 = self._speed(coords)
        k2 = self._speed(coords + sign * deltat*1/4*k1)
        k3 = self._speed(coords + sign * deltat*(-1*k1 + 2*k2))
        return coords + sign * deltat * ((k1+k3)/6 + 2/3*k2)
    
    def _integration_method(self, coords, sign, deltat):
        """Function responsible to integrate the function the given delta time
        """
        ...

    def _makeHalfStreamline(self, y0, sign):
        """
        Compute a streamline extending in one direction from the given point. Using Euler integrator.
        """
        # Coordinates to Numpy
        coords = y0.copy()
        # coords_mask_position = np.asarray(np.rint((coords-self.range_min)/self.delta_coords), int)
        coords_mask_position = self.get_masked_coordinates(*coords)

        # Set prev_coords_mask_position to actual position so backwards trajectory can, at least, start
        prev_coords_mask_position = coords_mask_position.copy()

        # Save arrays
        s = np.zeros((int(self.maxLen / 2), self.dimension))
        # s = [[] for i in range(self.dimension)]
        svelocity = np.zeros((int(self.maxLen / 2)))

        i = 0
        persistency = 20
        _speed = self._speed(coords)

        while (self.range_min < coords).all() and (coords < self.range_max).all():
            if i >= int(self.maxLen / 2):
                break
            

            coords_mask_position = self.get_masked_coordinates(*coords)

            # If mask is False there is not trajectory there yet.
            if not self.used[tuple(coords_mask_position,)]:
                prev_coords_mask_position = coords_mask_position.copy()

                self.used[tuple(prev_coords_mask_position)] = True

           

            # deltat = np.sum(np.square(self.get_delta_coordinates(*coords))) / (4 * _speed)
            deltat = np.min(self.get_delta_coordinates(*coords)/(10*np.max(np.abs(_speed))))

            if np.isnan(deltat) or np.isinf(deltat):
                break

            coords = self._integration_method(coords, sign, deltat)

            # Save values
            s[i] = coords
            svelocity[i] = np.sqrt(np.sum(np.square(_speed)))


            # If persistency iterations in a region with previous trajectory break.
            if self.used[tuple(coords_mask_position)] and (prev_coords_mask_position!=coords_mask_position).any():
                persistency -= 1
                if persistency <= 0:
                    break
            
            i += 1
            
             # Integration
            _speed = self._speed(coords)
            if (i%8 == 0):
                if (np.isclose(0, _speed)).all() or \
                    np.isnan(_speed).any() or \
                    np.isinf(_speed).any():
                        break

        return s, svelocity, i


class Streamlines_base2D(Streamlines_base):
    """
    Streamlines2D
    --------
    Creates trajectories given a `dF` function. Using Euler integrator.
    
    Integrated in:
        -PhasePortrait2D
    """


    def __init__(
        self, dF, X, Y, maxLen=500, deltat=0.01, *, dF_args=None, polar=False, density=1, odeint_method="scipy"
    ):
        """
        Compute a set of streamlines given velocity function `dF`.

        Args:
            dF (callable) : A dF type funcion. Computes the derivatives of given coordinates.
            X (list, list[list]) : Arrays of the grid points. The mesh spacing is assumed to be uniform in each dimension.
            Y (list, list[list]) : Arrays of the grid points. The mesh spacing is assumed to be uniform in each dimension.
            maxLen (int, default=500) : The maximum length of an individual streamline segment.
            polar (bool, default=false) : Whether to use polar coordinates or not.
            density (int, default=1) : Density of mask grid. Used for making the stream lines not collide.
            odeint_method (str, default="scipy") : Selects integration method, by default uses scipy.odeint. `euler` and `rungekutta3` are also available.
            dF_args (dict|None, default=None) : dF_args of `dF` function.
        """
        super().__init__(odeint_method=odeint_method)

        self.dimension = 2
        self.dF = dF
        self.dF_args = dF_args if dF_args is not None else  {}

        self.maxLen = maxLen
        self.deltat = deltat

        self.density = int(abs(density))

        xa = np.asanyarray(X)
        ya = np.asanyarray(Y)
        if np.isnan(xa).any() or np.isnan(ya).any():
            raise Exception("Invalid range. Chech limits and scales.")
        self.x = xa if xa.ndim == 1 else xa[0]
        self.y = ya if ya.ndim == 1 else ya[:, 0]
        
        self.polar = polar
        self._speed = self._speed_2d_no_polar if not polar else self._speed_2d_polar

        # marker for which regions have contours. +1 outside the plot at the far side of every axis. 
        self.used = np.zeros((1 + X.shape[0]*self.density, 1 + X.shape[1]*self.density), dtype=bool)
        self.used[0] = True
        self.used[-1] = True
        self.used[:, 0] = True
        self.used[:, -1] = True

        self.range_min = np.array((self.x[0], self.y[0]))
        self.range_max = np.array((self.x[-1], self.y[-1]))

        self.streamlines = []

        while not self.used.all():
            nz = np.transpose(np.logical_not(self.used).nonzero())
            # Make a streamline starting at the first unrepresented grid point
            # choose = np.random.randint(nz.shape[0])
            choose = 0

            x_ind = nz[choose][0]
            x = self.x[x_ind-1] + 0.5 * (self.x[x_ind]-self.x[x_ind-1])
            y_ind = nz[choose][1]
            y = self.y[y_ind-1] + 0.5 * (self.y[y_ind]-self.y[y_ind-1])


            # x = nz[choose][0]*self.dx + self.x[0]
            # y = nz[choose][1]*self.dy + self.y[0]
            self.streamlines.append(
                self._makeStreamline(np.array([x, y]))
            )

    def get_masked_coordinates(self, x, y):
        """
        Returns index of position in masked coordinates
        """
        x_ind = np.searchsorted(self.x, x)
        y_ind = np.searchsorted(self.y, y)
        return np.array([x_ind, y_ind])

    def get_delta_coordinates(self, x, y):
        """
        Returns closest delta coordinates of grid
        """
        x_mask, y_mask = self.get_masked_coordinates(x, y)
        return np.array([
            self.x[x_mask] - self.x[x_mask-1], 
            self.y[y_mask] - self.y[y_mask-1]])

    @property
    def Range(self):
        return ((self.x[0], self.x[-1]), (self.y[0], self.y[-1])) 


class Streamlines_base3D(Streamlines_base):
    """
    Streamlines
    --------
    Creates trajectories given a `dF` function. Using Euler integrator.
    
    Integrated in:
        -PhasePortrait3D
    """


    def __init__(
        self, dF, X, Y, Z, maxLen=2500, *, dF_args=None, polar=False, density=1, odeint_method="scipy"
    ):
        """
        Compute a set of streamlines given velocity function `dF`.

        Args:
            X (list, list[list]): arrays of the grid points. The mesh spacing is assumed to be uniform in each dimension.
            Y (list, list[list]): arrays of the grid points. The mesh spacing is assumed to be uniform in each dimension.
            Z (list, list[list]): arrays of the grid points. The mesh spacing is assumed to be uniform in each dimension.
            maxLen (int default=500) : The maximum length of an individual streamline segment.
            polar (bool default=false) : Whether to use polar coordinates or not.
            density (int, default=1) : Density of mask grid. Used for making the stream lines not collide.
            odeint_method (str, default="scipy") : Selects integration method, by default uses scipy.odeint. `euler` and `rungekutta3` are also available.
            dF_args (dict|None default=None) : dF_args of `dF` function.
        """
        super().__init__(odeint_method=odeint_method)
        self.dF = dF
        self.dF_args = dF_args if dF_args is not None else  {}

        self.maxLen = maxLen

        self.dimension = 3

        self.density = int(abs(density))

        xa = np.asanyarray(X)
        ya = np.asanyarray(Y)
        za = np.asanyarray(Z)
        self.x = xa if xa.ndim == 1 else xa[0,:,0]
        self.y = ya if ya.ndim == 1 else ya[:,0,0]
        self.z = za if za.ndim == 1 else za[0,0,:]

        self.polar = polar
        self._speed = self._speed_3d_no_polar if not polar else self._speed_3d_polar

        # marker for which regions have contours. +1 outside the plot at the far side of every axis. 
        self.used = np.zeros((1 + X.shape[0]*self.density, 1 + X.shape[1]*self.density, 1 + X.shape[2]*self.density), dtype=bool)
        self.used[0] = True
        self.used[-1] = True
        self.used[:, 0] = True
        self.used[:, -1] = True
        self.used[:,:, 0] = True
        self.used[:,:, -1] = True


        self.range_min = np.array((self.x[0], self.y[0], self.z[0]))
        self.range_max = np.array((self.x[-1], self.y[-1], self.z[-1]))

        # Make the streamlines
        self.streamlines = []

        while not self.used.all():
            nz = np.transpose(np.logical_not(self.used).nonzero())
            # Make a streamline starting at the first unrepresented grid point
            # choose = np.random.randint(nz.shape[0])
            choose = 0

            x_ind = nz[choose][0]
            x = self.x[x_ind-1] + 0.5 * (self.x[x_ind]-self.x[x_ind-1])
            y_ind = nz[choose][1]
            y = self.y[y_ind-1] + 0.5 * (self.y[y_ind]-self.y[y_ind-1])
            z_ind = nz[choose][2]
            z = self.z[z_ind-1] + 0.5 * (self.z[z_ind]-self.z[z_ind-1])
            self.streamlines.append(
                self._makeStreamline(np.array([x, y, z]))
            )

    
    def get_masked_coordinates(self, x, y, z):
        """
        Returns index of position in masked coordinates
        """
        x_ind = np.searchsorted(self.x, x)
        y_ind = np.searchsorted(self.y, y)
        z_ind = np.searchsorted(self.z, z)
        return np.array([x_ind, y_ind, z_ind])

    def get_delta_coordinates(self, x, y, z):
        """
        Returns closest delta coordinates of grid
        """
        x_mask, y_mask, z_mask = self.get_masked_coordinates(x, y, z)
        return np.array([
            self.x[x_mask] - self.x[x_mask-1], 
            self.y[y_mask] - self.y[y_mask-1], 
            self.z[z_mask] - self.z[z_mask-1]])

    @property
    def Range(self):
        return ((self.x[0], self.x[-1]), (self.y[0], self.y[-1]), (self.z[0], self.z[-1])) 