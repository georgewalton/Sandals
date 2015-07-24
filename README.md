# Sandals
A TkInter wrapper for python inspired by the GUI library Shoes for Ruby.

This is intended to make it easier to create simple GUI interfaces quickly. All these classes inheret from their TkInter counterparts so you can use them just as you would their original TkInter counterparts if need be.

To use this library I'd reccommend simply adding this to the top of your script;
```python
from sandals import *
```
How to create windows
--

Context managers are used to create windows, stacks (columns) and flows (rows).

For example, this is how a context manager is used to make a window;

<table>
<tr>
<td align="center">
<b>CODE</b>
</td>
<td align="center">
<b>GUI</b>
</td>
<tr>
<td>
<pre lang="python">
from sandals import *

with window("My window"):
  label("Hello world")
</pre>
</td>
<td>
<img src="https://raw.githubusercontent.com/georgewalton/Sandals/master/example%20images/helloworld.png"
alt="Manipulating buttons example">
</td>
</tr>
</table>

The way stacks and flows work was intended to be the same as with the Ruby library Shoes, but it's not quite there yet.
Info on how they're meant to work can be found on the Ruby Shoes website: http://shoesrb.com/

As mentioned below, the library needs to be ideally be rewritten to use TkInter grids, rather than just packing elements in different ways, which is something I'm working on at the moment.
The @button and other GUI decorators
--

Adding the decorator 
```python 
@button 
```
to a function adds a button that triggers that function. The button is located in whatever context manager the function is defined in.


For example, this code will create a window with a button, which when clicked will create a popup;

<table>
<tr>
<td align="center">
<b>CODE</b>
</td>
<td align="center">
<b>GUI</b>
</td>
<tr>
<td valign="top">
<pre lang="python">
from sandals import *

with window():

  @button("Create a popup box")
  def makePopupBox():
    showInfo(message = "You clicked the button")
</pre>
</td>
<td>
<img src="https://raw.githubusercontent.com/georgewalton/Sandals/master/example%20images/buttonexample.png"
alt="Button example">
</td>
</tr>
</table>

Checkboxes, radio buttons, spin boxes, scale bars, and option menus can all be applied as decorators in a similar way. They are also located in whatever context manager (window, stack or flow) the function is defined in.
For example, here is a simple implementation of a check box to change a boolean; 

```python
@checkBox("Is the oven on?", checked = True)
def ovenOn(checked):
	theOvenIsOn = checked
```

And here is a simple example of how to implement an options menu;

```python
label("How's the oven?")
@optionMenu("clean", "dirty", "broken")
def ovenState(option):
	print "The oven is", option
```

All these decorators can also be used as classes where this is more convenient.
Manipulating buttons
---
Because these decorators inherit from their TkInter classes, they can be used as normal (i.e. not as decorators) and then configured using e.g. ```my_button.config(**kwargs)```.

Buttons can be altered even when created as a decorator, as they are added as a function attribute of the function they are applied to, so can be accessed via e.g.  ```my_function.button```.

All the TkInter adjectives used to modify buttons - such as ```DISABLE``` and  ```NORMAL``` which describe the state of a disabled and enabled button respectively - are imported as well.

Here is an example where this method is used to disable a button created using a decorator;

<table>
<tr>
<td align="center">
<b>CODE</b>
</td>
<td align="center">
<b>GUI</b>
</td>
<tr>
<td valign="top">
<pre lang="python">
from sandals import *

with window():

	@button("This button does nothing")
	def doNothing():
		pass
		
	@button("Disable button")
	def disableButton():
		doNothing.button.config(state = DISABLED)
</pre>
</td>
<td>
<img src="https://raw.githubusercontent.com/georgewalton/Sandals/master/example%20images/manipulatingbuttonsexample.png"
alt="Manipulating buttons example">
</td>
</tr>
</table>

The @repeat and @loop decorators
---
Two new decorators are included which you might not necessarily associate with a GUI library;
The ``@repeat`` and ``@loop`` decorators.

These create a thread that repeats or loops the function the decorator is applied to. Once the context the decorated function is defined in is destroyed (e.g. closing a window) then that thread is stopped and the function will stop repeating or looping. As an example, here is a function that repeats once a minute;

```python
@repeat(60)
def clock():
	print "A minute has passed"
```

The repeat and loop decorators are inspired by similar methods in Shoes, which turn out to be more useful than you might expect when designing a GUI.

Changing and reading text in GUI elements
--

How the text in labels and other GUI elements is changed to try and make them easier to work with.

A slightly more complex example that demonstrates this;

<table>
<tr>
<td align="center">
<b>CODE</b>
</td>
<td align="center">
<b>GUI</b>
</td>
<tr>
<td>
<pre lang="python">
from sandals import *
with window("This is a window"):
    label("This is a label",
    font = "Verdana 24 bold underline")
    with stack(padx=10):
        myLabel = label("This text changes")
        @button("Change the above text",
            font = "Veranda 12 italic")
        def change_that_text():
            myLabel.text = "OMG it changed"
        with flow(pady=10):
            edit = editBox("edit me")
            @button("<-read edit box")
            def read_edit_box():
                showInfo(message
				= "Edit box says: "
				+ edit.text)
</pre>
</td>
<td>
<img src="https://raw.githubusercontent.com/georgewalton/Sandals/master/example%20images/simpleexample.png"
alt="Simple example">
</td>
</tr>
</table>
Complete example
--

`example.py` has a more complete example of how to use the different methods, context managers, etc. which should look like this;

<table>
<tr>
<td align="center">
<b>GUI</b>
</td>
</tr>
<tr>
<td>
<img src="https://raw.githubusercontent.com/georgewalton/Sandals/master/example%20images/example.png"
alt="Complex example">
</td>
</tr>
</table>

which is a bit of a mess.

Todo
--
Ideally this library should be rewritten at some point to use TkInter grids, instead of just packing GUI elements. I'm trying to re-write it this way at the moment.

3rd-party content
--

This library uses the AutoScrollbar class by Fredrik Lundh for the autohiding scrollbars;

http://effbot.org/zone/tkinter-autoscrollbar.htm
