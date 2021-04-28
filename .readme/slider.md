# Sliders
> *class* phaseportrait.sliders.**Slider**(*portrait, param_name, valinit=None, valstep=0.1, valinterval=[]*)

### **This class is not pretended to be used by the user. It is controlled by the other objects automatically.**

Adds a slider which can change the value of a parameter in [dF](dFfunction.md) during execution time.

# add_slider
> *method* .**add_slider**(*param_name, \*, valinit=None, valstep=0.1, valinterval=10*)

Adds a slider which can change the value of a parameter in execution time.

**Args**:
* param_name : string type. It takes the name of the parameter on which the slider will be defined. Must be the same as the one appearing as karg in the `dF` function.

**\*\*kargs**:

* valinit: initial value of *param_name* variable. Default value is 0.5 .

* valstep : slider's step value. Default value is 0.1 .

* valinterval : slider's range. Default value is `[-10, 10]` .

