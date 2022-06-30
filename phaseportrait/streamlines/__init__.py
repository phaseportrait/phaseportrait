try:
    __STREAMLINES_IMPORTED__
except NameError:
    __STREAMLINES_IMPORTED__= False

if not __STREAMLINES_IMPORTED__:
    from .streamlines_base import Streamlines_base
    from .streamlines_base3d import Streamlines_base3D
    from .velocity_color_gradient import Streamlines_Velocity_Color_Gradient
    from .size_gradient import Streamlines_Size_Gradient
    
__STREAMLINES_IMPORTED__ = True