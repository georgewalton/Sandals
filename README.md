# Sandals
A TkInter wrapper for python inspired by the GUI library Shoes for Ruby.

Not a fully complete library by any means but a nice way to test out a few ideas.

This is intended to make it easier to create simple GUI interfaces quickly. All these classes inheret from their TkInter counterparts so you can use them just as you would their original TkInter counterparts if need be.

To use this library I'd reccommend simply adding this to the top of your script;
```python
from sandals import *
All the examples below assume this line is at the top of the file.
```
How to create windows
--

Context managers are used to create windows, stacks (columns) and flows (rows).

For example;

```python
with window("My window"):
  label("Hello world")
```
creates a window with the text "Hello world" in it;

![Hello world](https://raw.githubusercontent.com/georgewalton/Sandals/master/example%20images/helloworld.png "Hello world")

The way stacks and flows work was intended to be the same as with the Ruby library Shoes, but it's not quite there yet.
Info on how they're meant to work can be found on the Ruby Shoes website: http://shoesrb.com/

As mentioned below, the library needs to be ideally be rewritten to use TkInter grids, rather than just packing elements in different ways.
The @button and other GUI decorators
--

Adding the decorator 
```python 
@button 
```
to a function adds a button that triggers that function.

For example;
```python
with window():

  @button("Create a popup box")
  def makePopupBox():
    showInfo(message = "You clicked the button")
```

will create a window with a button, which when clicked will create a popup;

![Button example](https://raw.githubusercontent.com/georgewalton/Sandals/master/example%20images/buttonexample.png "Button example")

Checkboxes, radio buttons, spin boxes, scale bars, and option menus can all be applied as decorators in a similar way.
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
Because these decorators inherit from their TkInter classes, they can be used as normal (i.e. not as decorators) and then altered using ```my_button.config(**kwargs)```.

Buttons can be altered even when created as a decorator, as they are added as a function attribute of the function they are applied to, e.g.  ```my_function.button```.

The TkInter adjectives used to modify buttons, such as ```DISABLE``` and  ```NORMAL``` to describe the state of a disabled and enabled button respectively, are imported as well.

Here is an example where this is used to disable a button created using a decorator;

```python
with window():
	@button("This button does nothing")
	def doNothing():
		pass

	@button("Disable button")
	def disableButton():
		doNothing.button.config(state = DISABLED)
```

which looks like;

![Simple example](https://raw.githubusercontent.com/georgewalton/Sandals/master/example%20images/manipulatingbuttonsexample.png "Simple example")
The @repeat and @loop decorators
---
Two new decorators are included which you might not necessarily associate with a GUI library - these are the @repeat and @loop decorators.

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

A slightly more complex example;

```python
with window("This is a window"):

	label("This is a label", font = "Verdana 24 bold underline")
	
	with stack(padx=10):
		myLabel = label("This text changes")
		
		@button("Change the above text", font = "Veranda 12 italic")
		def change_that_text():
			myLabel.text = "OMG it changed"
			
		with flow(pady=10):
			edit = editBox("edit me")
			
			@button("<-read edit box")
			def read_edit_box():
				showInfo(message = "Edit box says: " + edit.text)
```

looks like this;

![Simple example](https://raw.githubusercontent.com/georgewalton/Sandals/master/example%20images/simpleexample.png "Simple example")

where clicking the first button will change the text at the top of the window, and clicking the second button will create a popup displaying the text that has been entered into the edit box.

Complete example
--

`example.py` has a more complete example of how to use the different methods, context managers, etc. which should look like this;

![Example](https://raw.githubusercontent.com/georgewalton/Sandals/master/example%20images/example.png "Example")

which is a bit of a mess.

Todo
--
Ideally this library should be rewritten at some point to use TkInter grids, instead of just packing GUI elements, which is how it is implemented at the moment.

3rd-party content
--

This library uses the AutoScrollbar class by Fredrik Lundh for the autohiding scrollbars;

http://effbot.org/zone/tkinter-autoscrollbar.htm
