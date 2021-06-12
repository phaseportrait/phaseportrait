try:
    __SLIDERS_IMPORTED__
except NameError:
    __SLIDERS_IMPORTED__= False

if not __SLIDERS_IMPORTED__:
    from .sliders import Slider
    
__SLIDERS_IMPORTED__ = True