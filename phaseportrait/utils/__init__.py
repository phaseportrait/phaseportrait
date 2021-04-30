try:
    __PHASE_UTILS_IMPORTED__
except NameError:
    __PHASE_UTILS_IMPORTED__= False

if not __PHASE_UTILS_IMPORTED__:
    from . import utils

__PHASE_UTILS_IMPORTED__ = True