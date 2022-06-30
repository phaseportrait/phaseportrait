try:
    __NULLCLINES_IMPORTED__
except NameError:
    __NULLCLINES_IMPORTED__= False

if not __NULLCLINES_IMPORTED__:
    from .nullclines import Nullcline2D
    
__NULLCLINES_IMPORTED__ = True