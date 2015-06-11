# Sandals
A TkInter wrapper for python inspired by the GUI library Shoes for Ruby.

Not a complete library by any means but just a way to test out a few ideas.
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
The @button decorator
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

The way stacks and flows work was intended to be the same as with the Ruby library Shoes, but it's not quite there yet.
Info on how they're meant to work can be found on the Ruby Shoes website: http://shoesrb.com/
Changing and reading text in GUI elements
--

How the text in labels and other GUI elements is changed to try and make them easier to work with.

A slightly more complex example;

```python
from sandals import *

with window("This is a window"):

	label("This is a label", font = "Verdana 24 bold underline")
	
	with stack(padx=10):
		myLabelText = "This text changes"
		myLabel = label(myLabelText)
		
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

example.py has a more complete example of how to use the different methods, context managers, etc.

3rd-party content
--

This library uses the AutoScrollbar class by Fredrik Lundh for the autohiding scrollbars;

http://effbot.org/zone/tkinter-autoscrollbar.htm
