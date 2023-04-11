# Sliders
> *class* phaseportrait.sliders.**Slider**(*portrait, param_name, valinit=None, valstep=0.1, valinterval=[]*)

**This class is not pretended to be used by the user. It is handled by the other objects automatically.**

Adds a slider which can change the value of a parameter in [dF](dFfunction.md) during execution time.

Integrated via method `add_slider` in:
* Map1D

* Cobweb

* PhasePortrait2D

* Trajectory2D

* Trajectory3D

### **Parameters**

* portrait : 

    Class that uses the Slider.
    
* param_name : str

    Name of the parameter to slide over.
    
* valinit : float

    Initial value of the parameter in the slider.
    
* valsetp : float, default=0.1

    Precision of the slider.
    
* valinterval : Union[float, list]

    Parameter range in the slider. Default value is `[-10, 10]` 

# Methods

### *Slider*.\_\_call\_\_

> *method* **\_\_call\_\_**(*value*)

Updates internal dF_args and replots the graphs.

**Arguments**

* value : float

    New value for the parameter of the slider

**Returns**

* None

# Examples

Slider is implemented in several classes via *add_slider* method (tipically), check out:

* [Cobweb](cobweb.md)
* [Map1D](map1d.md)
* [PhasePortrait2D](phaseportrait2d.md)
* [Trajectory2D](trajectory2d.md)
* [Trajectory3D](trajectory3d.md)