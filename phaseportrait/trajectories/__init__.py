try:
    __TRAJECTORIES_IMPORTED__
except NameError:
    __TRAJECTORIES_IMPORTED__= False

if not __TRAJECTORIES_IMPORTED__:
    from .rungekutta import RungeKutta
    from .trajectory import trajectory
    
__TRAJECTORIES_IMPORTED__ = True