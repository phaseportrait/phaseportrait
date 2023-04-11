# dF function
The 'dF' function is refered several times in different implementations of it. It is a function created by the user that describes the system's evolution, either in a 2D phase portrait, a 3d trajectory or the study of a 1D map.

# Kargs
Kargs can be given. They can be changed using [sliders](slider.md) method.

For example, for an harmonic oscillator, the dF function will be defined as:
```python
def dFOscillator(x, y, *, ω=1):
    return y, -ω*ω*x
```
Where `ω` is the angular frequency of the oscillator.

## General definiton
In general, dF function will be defined the following way:
```python
def dF(*args, *, **kargs) -> tuple:
```
Where:
```python
len(dF(*args, **kargs)) == len(args)
```

# Examples

### 2D Phase portrait

When plotting a 2D phase portrait, we have a function f(x,y) that describes the system. The dF function will be constructed by the expressions of the derivatives respect the x and y coordinates, such that:

```python
def dF(x,y):
  return expressionX  ,  expressionY
```
It must contain as much args as returned elements.

### 3D Trajectory

Let's say we want to see some trajectories on Lorenz's attractor. The dF function will be constructed as a function that returns each of the expressions of the system:

```py
def Lorenz(x,y,z,*, s=10, r=28, b=8/3):
  return -s*x+s*y, -x*z+r*x-y, x*y-b*z
```

### 1D Maps

Let's say we want to study the Logistic Map. The dF function will be constructed by creating a function that returns the evolution of one step in the map:

```py
def Logistic(x, *, r=1.5):
  return r*x*(1-x)
```