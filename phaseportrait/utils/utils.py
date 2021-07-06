from ..exceptions import exceptions

def is_number(x):
    """Checks if `x` is a number

    Parameters
    ----------
    x : 
        The object.

    Returns
    -------
    bool
        Whether is a number or not.
    """
    
    return isinstance(x, (float,int))

def is_range(U):
    """Checks if `x` is a list or a tuple

    Parameters
    ----------
    U :
        The object.

    Returns
    -------
    bool
        Whether is a collection of elements or not.
    """
    return isinstance(U, (list,tuple))

def construct_interval_1d(var):
    """Creates an 1d interval from a variable
    
    Parameters
    ----------
    var : float, list
        Element from which a 1d interval is created
        It supports:
        * number
        * [number, number]

    Returns
    -------
    list
        1d interval: []
        

    Raises
    ------
    exceptions.RangoInvalid
        If the parameter given is not a number nor a list or tuple.
    """
    try:
        if is_number(var):
            if var !=0:
                return sorted([-var, var])
            raise Exception('0 is not a valid range.')
        if is_range(var):
             return var
    except Exception as e:
        raise exceptions.InvalidRange(f"{var} as 1D range gave the following error: "+str(e))

def construct_interval_2d(var):
    """Creates an 2d interval from a variable

    Parameters
    ----------
    var : float, list
        Element from which a 1d interval is created
        It supports:
        * number
        * [number, number]
        * [[number, number], number]
        * [[number, number],[number, number]]
        
        And all the permutations.

    Returns
    -------
    list
        2d interval: [[],[]]

    Raises
    ------
    exceptions.RangoInvalid
        If the parameter given is not a number nor a list or tuple.
    """
    try:
        [a,b],[c,d] = var
    except Exception:
        try:
            b,d = var
            if is_range(b) or is_range(d):
                [a,b],[c,d] = construct_interval_1d(b), construct_interval_1d(d)
            else:
                a = c = b
                b = d
        except Exception:
            try:
                a = var
                if a !=0:
                    b = d = a
                    a = c = 0
                else:
                    raise Exception
            except Exception as e:    
                raise exceptions.InvalidRange(f"{var} is not a valid 2D range.")
    a1 = [a,b]
    a2 = [c,d]
    a1.sort()
    a2.sort()
    return [a1, a2]

def construct_interval_3d(var, *, depth=0):
    """Creates an 3d interval from a variable

    Parameters
    ----------
    var : float, list
        Element from which a 1d interval is created
        It supports:
        * number
        * [number, number, number]
        * [[number, number], number, number]
        * [[number, number], [number, number], number]
        * [[number, number],[number, number], [number, number]]
        
        And all the permutations.

    Returns
    -------
    list
        3d interval: [[],[],[]]

    Raises
    ------
    exceptions.RangoInvalid
        If the parameter given is not a number nor a list or tuple.
    """
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
        raise exceptions.InvalidRange(f"{var} as 3D range gave the following error: "+str(e))


def construct_interval(var, *, dim=None, depth=0):
    """Construct intervals from `var` for `dim` dimensions.

    Parameters
    ----------
    var : 
        Element from which a 1d interval is created
    dim : int, optional
        Dimension of the requested interval, by default None
    depth : int, optional
        Used for `dim==3` by default 0

    Returns
    -------
    list
        `dim` dimensional interval.
    """
    if not dim:
        dim = len(var) 

    if dim==1:
        inter = construct_interval_1d(var)
    elif dim==2:
        inter = construct_interval_2d(var)
    elif dim==3:
        inter = construct_interval_3d(var, depth=depth)
    while len(inter)<dim:
        inter.append(inter[-1])
    return inter