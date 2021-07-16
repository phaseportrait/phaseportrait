import numpy as np
from matplotlib.colors import to_hex

class Nullcline2D():
    """
    Nullcline2D
    --------
    Class dedicated to 2 dimensions phase portraits. 
    Useful where it is necessary to plot nulclines in a plot.
    
    Integrated via method `add_nullclines` in:
        -PhasePortrait2D 
    
    Methods
    -------
    plot : 
        Plots the nullclines.
        Returns : x and y contourns.
    """
    
    def __init__(self, portrait, funcion, *, precision=0.01, xprecision=None, yprecision=None, offset=0, density=50, xRange=None, yRange=None, dF_args=None, xcolor='r', ycolor='b', bgcolor='w', alpha=0, polar=False):
        """Creates an instance of Nullcline2D

        Parameters
        ----------
        portrait : 
            The class that uses Nullcline2D
        funcion : callable
            A `dF` type funcion.
        precision : float, optional
            The minimum diferencie from `offset` to be considerated a nullcline, by default 0.01
        xprecision : float, optional
            For a different precision value only in the x axis, by default `precision`
        yprecision : float, optional
            For a different precision value only in the y axis, by default `precision`
        offset : float, optional
            If you want, for instance, a twoclide, by default 0
        density : int, optional
            Number of inner divisions on the x axis and y axis, by default 50
        xRange : Union[float,list], optional
            The range in which the nullclines are calculated, by default `portrait.Range[0]`
        yRange : Union[float,list], optional
            The range in which the nullclines are calculated, by default `portrait.Range[1]`
        dF_args : dict, optional
            If necesary, must contain the kargs for the `dF` funcion, by default None
        xcolor : str, optional
            X nullcline color, by default 'r'
        ycolor : str, optional
            Y nullcline color], by default 'b'
        bgcolor : str, optional
            Background color, by default 'w'
        alpha : int, optional
            Opacity of the background, by default 0
        polar : bool, optional
            If the dF funcion requires polar coordinates, by default False
        """                         
        self.portrait = portrait
        self.funcion = funcion
        self.precision = precision
        self.xprecision = xprecision if xprecision is not None else precision
        self.yprecision = yprecision if yprecision is not None else precision
        self.offset = offset
        self.xcolor = to_hex(xcolor)
        self.ycolor = to_hex(ycolor)
        self.bgcolor = bgcolor
        self.density = density
        self.xRange = xRange if xRange is not None else self.portrait.Range[0,:]
        self.yRange = yRange if yRange is not None else self.portrait.Range[1,:]
        self.alpha = alpha
        self.polar = polar
        
        try:
            self.dF_args = dF_args if dF_args is not None else self.portrait.dF_args
        except:
            self.dF_args = {}
            
    def update_dF_args(self):
        self.dF_args = self.portrait.dF_args.copy()
           
    def plot(self, *, axis=None):
        """Plots the nullclines in the given axis

        Parameters
        ----------
        axis : matplotlib.Axis, optional
            The axis in which the nullclines will be represented, by default `portrait.ax`

        Returns
        -------
        [matplotlib.contour.QuadContourSet,matplotlib.contour.QuadContourSet]
            X and Y contours.
        """
        
        
        self.update_dF_args()
        
        if axis is None:
            axis = self.portrait.ax
        
        _x = np.linspace(*self.xRange, self.density)
        _y = np.linspace(*self.yRange, self.density)
        
        _xdF = np.zeros([self.density, self.density])
        _ydF = np.zeros([self.density, self.density])
        
        
        if self.polar:
            for i,xx in enumerate(_x):
                for j,yy in enumerate(_y):
                    _r, _t = (xx**2 + yy**2)**0.5, np.arctan2(yy, xx)
                    _dr, _dt = self.funcion(_r,_t, **self.dF_args)
                    _xdF[j,i], _ydF[j,i] = _dr*np.cos(_t) - _r*np.sin(_t)*_dt, _dr*np.sin(_t) + _r*np.cos(_t)*_dt       
        else:
            for i,xx in enumerate(_x):
                for j,yy in enumerate(_y):
                    _xdF[j,i], _ydF[j,i] = self.funcion(xx,yy, **self.dF_args)
        
        xct = axis.contourf(_x, _y,_xdF, levels=[-self.xprecision + self.offset, self.xprecision + self.offset], colors=[self.xcolor], extend='neither')
        yct = axis.contourf(_x, _y,_ydF, levels=[-self.yprecision + self.offset, self.yprecision + self.offset], colors=[self.ycolor], extend='neither')
        
        xct.cmap.set_over(self.bgcolor, alpha=self.alpha)
        yct.cmap.set_over(self.bgcolor, alpha=self.alpha)
        xct.cmap.set_under(self.bgcolor, alpha=self.alpha)
        yct.cmap.set_under(self.bgcolor, alpha=self.alpha)
    
        return xct, yct