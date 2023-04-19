[![PyPI Downloads](https://img.shields.io/pypi/dm/phaseportrait.svg?label=downloads)](https://pypi.org/project/phaseportrait/)
[![PyPI Version](https://img.shields.io/pypi/v/phaseportrait?)](https://pypi.org/project/phaseportrait/)

![Commit activity](https://img.shields.io/github/commit-activity/m/phaseportrait/phaseportrait)
[![License](https://img.shields.io/pypi/l/phaseportrait)](LICENSE)
[![Build](https://img.shields.io/github/actions/workflow/status/phaseportrait/phaseportrait/ci.yml)](https://github.com/phaseportrait/phaseportrait/actions)

[![Python Version](https://img.shields.io/pypi/pyversions/phaseportrait)](https://pypi.org/project/phaseportrait/)
[![Wheel](https://img.shields.io/pypi/wheel/phaseportrait)](https://pypi.org/project/phaseportrait/)

<br></br>

<div align="center">

<a href="https://phaseportrait.github.io/">
<img src="https://github.com/phaseportrait/phaseportrait/raw/master/docs/img/duckduck.png" width=40%>
</img>
</a>
<a href="https://github.com/phaseportrait/phaseportrait-gui">
<img src="https://github.com/phaseportrait/phaseportrait/raw/master/docs/img/duckduck_son.png" width=30%>
</a>

<br></br>

<a href="https://phaseportrait.github.io/">
<img src=https://img.shields.io/github/deployments/phaseportrait/phaseportrait/github-pages?label=Documentation>
</a>

</div>

<br></br>

```py
from matplotlib import pyplot
import numpy

import phaseportrait

def pendulum(θ, dθ):
    return dθ, - numpy.sin(θ)

SimplePendulum = phaseportrait.PhasePortrait2D(pendulum, [-9, 9], Title='Simple pendulum', xlabel=r"$\Theta$", ylabel=r"$\dot{\Theta}$")
SimplePendulum.plot()
```

<div align="center">
<a href="https://phaseportrait.github.io/reference/legacy/phaseportrait2d_examples/">
<img src="https://github.com/phaseportrait/phaseportrait/raw/master/docs/imgs/index/pendulum_example.png" width=49.45%><img src="https://github.com/phaseportrait/phaseportrait/raw/master/docs/imgs/index/damped_pendulum_example.png" width=50%>
</a>

<a href="https://phaseportrait.github.io/reference/legacy/phaseportrait3d/">
<img src="https://github.com/phaseportrait/phaseportrait/raw/master/docs/imgs/pp3d_examples/example.png">
</a>


<a href="https://phaseportrait.github.io/reference/legacy/trajectories_examples/">
<img src="https://github.com/phaseportrait/phaseportrait/raw/master/docs/imgs/trj_examples/Figure_7.png">
</a>





<a href="https://phaseportrait.github.io/reference/legacy/mapsandcobweb_examples/">
<img src="https://github.com/phaseportrait/phaseportrait/raw/master/docs/imgs/index/map_example_code.png">
</a>.

</div>


# Documentation

To check out [*phaseportrait*'s documentation](https://phaseportrait.github.io/), view some examples and read more about it, check our website or try our [Graphical User Interface](https://github.com/phaseportrait/phaseportrait-gui)!



# Installation
**Installing via pip:**

Phaseportrait releases are available as wheel packages for macOS, Windows and Linux on PyPI. Install it using pip:
```
$ pip install phaseportrait
```

**Installing from source:**

Open a terminal on desired route and type the following:
```
$ git clone https://github.com/phaseportrait/phaseportrait
```
**Manual installation**

Visit [phase-portrait](https://github.com/phaseportrait/phaseportrait) webpage on GitHub. Click on green button saying *Code*, and download it in zip format.
Save and unzip on desired directory.


# What's this?
The idea behind this project was to create a simple way to make phase portraits in 2D and 3D in Python, as we couldn't find something similar on the internet, so we got down to work. (Update: found [jmoy/plotdf](https://github.com/jmoy/plotdf), offers similar 2D phase plots but it is very limited).

Eventually, we did some work on bifurcations, 1D maps and chaos in 3D trayectories.

This idea came while taking a course in non linear dynamics and chaos, during the 3rd year of physics degree, brought by our desire of visualizing things and programming.



We want to state that we are self-taught into making this kind of stuff, and we've tried to make things as *professionally* as possible, any comments about improving our work are welcome!

<!-- ## **Disclaimer:**

**Today's date (July 2021), we've decided to cease our work on this project (for the moment, as we have to move on other things). Therefore, this is the 'final' version of the project, there are no more features incoming. We've tried to leave the code documentated and with good organisation in case someone wants to carry on with some idea! Cheers** -->

# Authors

- Víctor Loras Herrero (vhloras@gmail.com)
- Unai Lería Fortea (unaileria@gmail.com)


# Contributing
This proyect is open-source, everyone can download, use and contribute. To do that, several options are offered:

* Fork the project, add a new feature / improve the existing ones and pull a request via GitHub.
* Contact us on our emails:
    * [vhloras@gmail.com](mailto:vhloras@gmail.com)
    * [unaileria@gmail.com](mailto:unaileria@gmail.com)
