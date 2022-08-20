# Streamlines_base2D
*class* phaseportrait.streamlines.**Streamlines_base2D**(*dF, X, Y, maxLen=500, deltat=0.01, *, dF_args=None, polar=False, density=1, scypi_odeint=False, \*\*kargs*)

Compute a set of streamlines given velocity function `dF`.


### **Parameters**

* **dF** : callable

    A dF type funcion. Computes the derivatives of given coordinates.
  
* **X and Y** : 1D or 2D arrays

    Arrays of the grid points. The mesh spacing is assumed to be uniform in each dimension.

* **maxLen** : int, default=500

    The maximum length of an individual streamline segment.

* **polar** : bool, default=false

    Whether to use polar coordinates or not.

* **density** : int, default=1

    Density of mask grid. Used for making the stream lines not collide.

* **scypi_odeint** : bool, default=False

    Use scipy.odeint for integration. If `False` Runge-Kutta 3rd order is used.

### **Key Arguments**
        --------
        dF_args: dict|None, default=None
            dF_args of `dF` function.

# Streamlines_baseD3
*class* phaseportrait.streamlines.**Streamlines_baseD3**(*dF, X, Y, Z, maxLen=500, deltat=0.01, *, dF_args=None, polar=False, density=1, scypi_odeint=False, \*\*kargs*)

Compute a set of streamlines given velocity function `dF`.


### **Parameters**

* **dF** : callable

    A dF type funcion. Computes the derivatives of given coordinates.
  
* **X, Y and Z** : 1D or 2D arrays

    Arrays of the grid points. The mesh spacing is assumed to be uniform in each dimension.

* **maxLen** : int, default=500

    The maximum length of an individual streamline segment.

* **polar** : bool, default=false

    Whether to use polar coordinates or not.

* **density** : int, default=1

    Density of mask grid. Used for making the stream lines not collide.

* **scypi_odeint** : bool, default=False

    Use scipy.odeint for integration. If `False` Runge-Kutta 3rd order is used.

### **Key Arguments**
        --------
        dF_args: dict|None, default=None
            dF_args of `dF` function.

