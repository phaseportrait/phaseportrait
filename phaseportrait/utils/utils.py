from ..exceptions import exceptions

def is_number(x):
    return isinstance(x, (float,int))

def is_range(U):
    return isinstance(U, (list,tuple))

def construct_interval_1d(var):
    try:
        if is_number(var):
            return sorted([-var, var])
        if is_range(var):
             return var
    except Exception as e:
        raise exceptions.RangoInvalid(f"{var} as 1D range gave the following error: "+str(e))

def construct_interval_2d(var, *, depth=0):
    try:
        if is_number(var):
            if depth == 0:
                return [sorted([0, var])]*2
            elif depth == 1:
                return sorted([-var, var])
        if is_range(var):
            if depth == 0:
                return [construct_interval_2d(i, depth=depth+1) for i in var]
            if depth == 1:
                return var
    except Exception as e:
        raise exceptions.RangoInvalid(f"{var} as 2D range gave the following error: "+str(e))

def construct_interval_3d(var, *, depth=0):
    try:
        if is_number(var):
            if depth == 0:
                return [sorted([0, var])]*3
            elif depth == 1:
                return sorted([-var, var])
        elif is_range(var):
            if depth==0:
                return [construct_interval_3d(i, depth=depth+1) for i in var]
            if depth==1:
                return var
    except Exception as e:
        raise exceptions.RangoInvalid(f"{var} as 3D range gave the following error: "+str(e))


def construct_interval(var, *, dim=None, depth=0):
    if not dim:
        dim = len(var) 

    if dim==1:
        inter = construct_interval_1d(var)
    elif dim==2:
        inter = construct_interval_2d(var, depth=depth)
    elif dim==3:
        inter = construct_interval_3d(var, depth=depth)
    while len(inter)<dim:
        inter.append(inter[-1])
    return inter