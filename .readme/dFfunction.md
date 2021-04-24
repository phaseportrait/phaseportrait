# dF function
This function is thought to compute the derivatives of given coordinates:
```python
def dF(x,y):
  return expressionX  ,  expressionY
```
It must contain as much args as returned elements.

## kwargs
Kwargs can be given. They can be changed using [sliders](slider.md) method.

For an harmonic oscillator, the dF function will be defined as:
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