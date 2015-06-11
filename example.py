from sandals import *

with window("This is a window"):

	label("This is a label", font = "Verdana 24 bold underline")
	
	with flow():
		with stack(padx=10):
			my_label_text = "This text changes"
			my_label = label(my_label_text)

			@button("Change the above text", font = "Veranda 12 italic")
			def change_that_text():
				if (askYesNo(message = "Change that text?")):
					my_label.text = "OMG it changed"
			button("(Also changes that text)", command = change_that_text)
			
			with flow():
				
				label("Look, this label counts upwards:")

				counting_label = label("0")
					
				@repeat(1)
				def update_label():
					new_number = int(counting_label.text) + 1
					counting_label.text = str(new_number)
		
		with stack(padx=10):
			message("Below is a combination of a stack and two flows, forming a grid", width=140, borderwidth=1, relief=tkinter.SUNKEN)
			
			@button("Yes / no / cancel")
			def yes_no_cancel():
				response = askYesNoCancel(message = "What do?")
				if response is True:
					showInfo(message = "You pressed yes")
				elif response is False:
					showWarning(message = "You pressed no")
				elif response is None:
					showError(message = "You pressed cancel")
		
	with flow():
		edit = editBox("edit me")
		
		@button("<-read edit box")
		def read_edit_box():
			showInfo(message = "Edit box says: " + edit.text)
		
	
	
	with stack(padx=2, pady=2, borderwidth=1, relief=tkinter.SUNKEN):
	
		label("Browse dialogs", font = "Verdana 10 underline")
		
		with stack(borderwidth=1, relief=tkinter.SUNKEN):
			file_label = label("No file or directory picked", font = "Verdana 12 bold")
	
		with flow():
			@button("Pick file")
			def pick_file():
				with askOpenFile() as file:
					file_label.text = file.name
			
			@button("Pick directory", padx = 10)
			def pick_file():
				file_label.text = askDirectory()
	
	with flow():
		@button("Enter integer")
		def enter_integer():
			integer = askInteger("Integer", "Write an integer in the box")
			integer_label.text = str(integer)
			
		integer_label = label("No integer entered yet")
	
	with stack(padx=2, pady=2, borderwidth=1, relief=tkinter.SUNKEN):
	
		label("Scrolled text", font = "Verdana 10 underline")
	
		scrollText = scrolledText("\n".join(["line "+str(i) for i in range(1,20)]), width=50, height=0)

		@checkBox("Scrolled text is editable?", checked = True, font = "Verdana 10 bold")
		def check(checked):
			scrollText.editable = checked
			
	with stack(padx=2, pady=2, borderwidth=1, relief=tkinter.SUNKEN):
	
		label("Radio buttons", font = "Verdana 10 underline")
		
		@button("What number is it?")
		def show_number():
			if (set.number == 0):
				showInfo(message = "No radio button selected")
			else:
				showInfo(message = "The selected radio button is: " + str(set.number))
			
		with flow():
		 
			with stack():
			
				with radioSet() as set:
					@radioButton(1, "one")
					@radioButton(2, "two")
					@radioButton(3, "three")
					def val(value):
						radio_label.text = "Radio button: " + str(value)
					
			with stack():
							
				radio_label = label("No radio button checked")
				
				
						
	with flow():
		label("This is a spin box:")
		@spinBox(values=(1, 2, 4, 8))
		def spin(value):
			spin_label.text = str(value)
		spin_label = label("1")
		
	with flow():
		label("These are scale bars:")
		@scaleBar(from_=0, to=100)
		def scale(value):
			scale_bar_2.value = 100-int(value)
		scale_bar_2 = scaleBar(from_=0, to=100, enabled=False)
		
	with flow():
		label("This is an options menu:")
		@optionMenu("one", "two", "three")
		def opt(option):
			print(option)
			
	label("This is a list box")
	list_box = listBox(height=4, values=["one", "two", "three", "four"])
	@button("list")
	def read_list():
		print(list_box.selection)