# Instructions
Using *phaseportrait* is easy, it has to be firstly imported, which can be done this way:

```python
from phaseportrait import *
```

This will let us use the following classes:

- [PhasePortrait2D](phaseportrait2d.md)

- [Trajectory3D](trajectory3d.md)

Both of them share their first arg: a function that computes the derivative of given coordinates in a point.

# [dF function](dFfunction.md)
```python
def dF(x,y):
  return expressionX  ,  expressionY
```

Extra variables can also be passed in dictionary form. For example, we can pass `ω` parameter for an harmonic oscillator with default value 1 the following way:
```python
def dFOscillator(x, y, *, ω=1):
    return y, -ω*ω*x
```

# [PhasePortrait2D](phaseportrait2d.md)
> *class* phaseportrait.**PhasePortrait2D**(*dF, Range, \*, MeshDim=10, dF_args={}, Density=1, Polar=False, \*\*kargs*)

Gives the option to represent a 2D phase portrait given a [dF](dFfunction.md) function with 2 args.

# [Trajectory2D](trajectory2d.md)
> *class* phaseportrait.**Trajectory2D**(*dF, \*, Range=None, dF_args={}, n_points=10000, runge_kutta_step=0.01, runge_kutta_freq=1, \*\*kargs*)

Gives the option to represent 2D trajectories given a [dF](dFfunction.md) function with 3 args.

# [Trajectory3D](trajectory3d.md)
> *class* phaseportrait.**Trajectory3D**(*dF, \*, Range=None, dF_args={}, n_points=10000, runge_kutta_step=0.01, runge_kutta_freq=1, \*\*kargs*)

Gives the option to represent 3D trajectories given a [dF](dFfunction.md) function with 3 args. 
