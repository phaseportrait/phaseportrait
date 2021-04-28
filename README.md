# What's this?
The idea behind this project was to create a simple way to make phase portraits in 2D and 3D, as we couldn't find something similar on the internet, so we got down to work.

This idea came while taking a course in non linear dynamics and chaos, during the 3rd year of physics degree, brought by our desire of visualizing things and programming.

We want to state that we are self-taught into making this kind of stuff, and we've tried to make things as *professionally* as possible, any comments about improving our work are welcome!

At first, this project was made up in spanish. The spanish version can be found [here](https://github.com/Loracio/retrato-de-fases).
## Authors

- Víctor Loras Herrero (vhloras@gmail.com)
- Unai Lería Fortea (unaileria@gmail.com)

## Contributing
The [code](#files) is open, everyone can download it and use it. You can also contribute if you wish. To do that, several options are offered:

* Fork the project, add a new feature / improve the existing ones and pull a request via GitHub.
* Contact us on our emails (shown above).

# Installation
## Installation via pip:
> $ pip install phaseportrait

## Installation via git:
Open a terminal on desired route and type the following
> $ git clone https://github.com/Loracio/phase-portrait

## Manual installation
Visit [phase-portrait](https://github.com/Loracio/phase-portrait) webpage on GitHub. Click on green button saying *Code*, and download it in zip format.
Save and unzip on desired directory.

# Examples of use
- ### [examples.ipynb](examples/examples.ipynb):
Examples showing how to use *PhasePortrait2D* class.

- ### [sliderExamples.py](examples/sliderExamples.py) :
Examples using the *slider* feature from *PhasePortrait2D* class.

- ### [TrajectoryExamples.py](examples/TrajectoryExamples.py):
Contains examples of 2D and 3D trajectories with and without sliders.

# Instructions
Using *phaseportrait* is easy, it has to be firstly imported, which can be done this way:
```python
import phaseportrait
from phaseportrait import *
```
This will let us use the following classes:
- [PhasePortrait2D](.readme/phaseportrait2d.md)
- [Trajectory3D](.readme/trajectory3d.md)

Both of them share their first arg: a function that computes the derivative of given coordinates in a point.

# [dF function](.readme/dFfunction.md)
```python
def dF(x,y):
  return expressionX  ,  expressionY
```

Extra variables can also be passed in dictionary form. For example, we can pass `ω` parameter for an harmonic oscillator with default value 1 the following way:
```python
def dFOscillator(x, y, *, ω=1):
    return y, -ω*ω*x
```

# [PhasePortrait2D](.readme/phaseportrait2d.md)
> *class* phaseportrait.**PhasePortrait2D**(*dF, Range, \*, MeshDim=10, dF_args={}, Density=1, Polar=False, \*\*kargs*)

Gives the option to represent a 2D phase portrait given a [dF](.readme/dFfunction.md) function with 2 args.

# [Trajectory2D](.readme/trajectory2d.md)
> *class* phaseportrait.**Trajectory2D**(*dF, \*, Range=None, dF_args={}, n_points=10000, runge_kutta_step=0.01, runge_kutta_freq=1, \*\*kargs*)

Gives the option to represent 2D trajectories given a [dF](.readme/dFfunction.md) function with 3 args.

# [Trajectory3D](.readme/trajectory3d.md)
> *class* phaseportrait.**Trajectory3D**(*dF, \*, Range=None, dF_args={}, n_points=10000, runge_kutta_step=0.01, runge_kutta_freq=1, \*\*kargs*)

Gives the option to represent 3D trajectories given a [dF](.readme/dFfunction.md) function with 3 args.