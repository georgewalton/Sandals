from contextlib import contextmanager
import threading

try: # python 3
	import tkinter
	from tkinter import messagebox
	from tkinter import filedialog
	from tkinter import simpledialog
	from tkinter import scrolledtext
	from tkinter import Scrollbar
	
	from tkinter import N
	from tkinter import NE
	from tkinter import E
	from tkinter import SE
	from tkinter import S
	from tkinter import SW
	from tkinter import W
	from tkinter import NW
	
	from tkinter import CENTER
	from tkinter import BOTTOM
	from tkinter import LEFT
	from tkinter import RIGHT
	from tkinter import TOP
	from tkinter import NONE
	
	from tkinter import NORMAL
	from tkinter import ACTIVE
	from tkinter import DISABLED
	
	from tkinter import FLAT
	from tkinter import RAISED
	from tkinter import SUNKEN
	from tkinter import GROOVE
	from tkinter import RIDGE
	
	from tkinter import TRUE
	from tkinter import FALSE
	
except ImportError: # python 2
	import Tkinter as tkinter
	import tkMessageBox as messagebox
	import tkFileDialog as filedialog
	import tkSimpleDialog as simpledialog
	import ScrolledText as scrolledtext
	from Tkinter import Scrollbar
	
	from Tkinter import N
	from Tkinter import NE
	from Tkinter import E
	from Tkinter import SE
	from Tkinter import S
	from Tkinter import SW
	from Tkinter import W
	from Tkinter import NW
	
	from Tkinter import CENTER
	from Tkinter import BOTTOM
	from Tkinter import LEFT
	from Tkinter import RIGHT
	from Tkinter import TOP
	from Tkinter import NONE
	
	from Tkinter import NORMAL
	from Tkinter import ACTIVE
	from Tkinter import DISABLED
	
	from Tkinter import FLAT
	from Tkinter import RAISED
	from Tkinter import SUNKEN
	from Tkinter import GROOVE
	from Tkinter import RIDGE
	
	from Tkinter import TRUE
	from Tkinter import FALSE
	
_root = None
_pack_side = None
_events = []
_radioVariable = None

class AutoScrollbar(Scrollbar):
    # a scrollbar that hides itself if it's not needed.  only
    # works if you use the grid geometry manager.
    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            # grid_remove is currently missing from Tkinter!
            self.tk.call("grid", "remove", self)
        else:
            self.grid()
        Scrollbar.set(self, lo, hi)
    def pack(self, **kw):
        raise TclError("cannot use pack with this widget")
    def place(self, **kw):
        raise TclError("cannot use place with this widget")
		
class window(tkinter.Tk):
	def __init__(self, title="Window", **kw):
		tkinter.Tk.__init__(self)
		self.title(title)
		self.kw = kw
		
	def __enter__(self):
		global _root, _pack_side

		# create scroll bar
		self.vscrollbar = AutoScrollbar(self)
		self.vscrollbar.grid(row=0, column=1, sticky=N+S)

		# create canvas
		self.canvas = tkinter.Canvas(self,
						yscrollcommand=self.vscrollbar.set, bd=5)
		self.canvas.grid(row=0, column=0, sticky=N+S+E+W)

		# configure scroll bar for canvas
		self.vscrollbar.config(command=self.canvas.yview)

		# make the canvas expandable
		self.grid_rowconfigure(0, weight=1)
		self.grid_columnconfigure(0, weight=1)

		# create frame in canvas
		self.frame = tkinter.Frame(self.canvas)
		self.frame.columnconfigure(0, weight=1)
		self.frame.columnconfigure(1, weight=1)
		

		_pack_side = TOP
		_root = self.frame
		return self # was _root for some reason
		
	def __exit__(self, type, value, traceback):
		global _root, _pack_side
		
		# puts tkinter widget onto canvas
		self.canvas.create_window(0, 0, anchor=NW, window=self.frame, width = int(self.canvas.config()['width'][4])-int(self.vscrollbar.config()['width'][4]))

		# deal with canvas being resized
		def resize_canvas(event):
			self.canvas.create_window(0, 0, anchor=NW, window=self.frame, width = int(event.width)-int(self.vscrollbar.config()['width'][4]))
		self.canvas.bind("<Configure>", resize_canvas)

		# updates geometry management
		self.frame.update_idletasks()

		# set canvas scroll region to all of the canvas
		self.canvas.config(scrollregion=self.canvas.bbox("all"))

		# set minimum window width
		self.update()
		self.minsize(self.winfo_width(), 0)
		self.config(**self.kw)
		
		self.frame.update()
		
		# start mainloop
		self.mainloop()
		
		# window closed...
		
		_pack_side = None
		
		# stop all ongoing _events
		[event.set() for event in _events]
		
class slot(tkinter.Frame):
	def __init__(self, **kw):
		self.kw = kw
		
	def __enter__(self):
		global _root, _pack_side
		self._root_old = _root
		self._pack_side_old = _pack_side
		tkinter.Frame.__init__(self, self._root_old, **self.kw)
		self.pack( side=self._pack_side_old, fill=tkinter.X)
		_root = self
		
	def __exit__(self, type, value, traceback):
		global _root, _pack_side
		_root = self._root_old
		_pack_side = self._pack_side_old
		
class stack(slot):
	def __init__(self, **kw):
		slot.__init__(self, **kw)
	def __enter__(self):
		global _pack_side
		slot.__enter__(self)
		_pack_side = TOP
		return _root
		
class flow(slot):
	def __init__(self, **kw):
		slot.__init__(self, **kw)
	def __enter__(self):
		global _pack_side
		slot.__enter__(self)
		_pack_side = LEFT
		return _root
		
class button(tkinter.Button, object):
	def __init__(self, text="", **kw):
		self.kw   = kw
		self.textvariable = tkinter.StringVar()
		self.textvariable.set(self.kw['text'] if 'text' in self.kw else text)
		if 'text' in self.kw:
			del self.kw['text']
		tkinter.Button.__init__(self, _root, textvariable = self.textvariable, **kw)
		self.pack( side = _pack_side )
		
	def __call__(self, func):
		func.button = self
		self.config(command = lambda: func())
		return func
		
	@property
	def text(self):
		return self.textvariable.get()
	
	@text.setter
	def text(self, text):
		self.textvariable.set(text)
		
class label(tkinter.Label, object):
	def __init__(self, text="", **kw):
		self.kw   = kw
		self.textvariable = tkinter.StringVar()
		self.textvariable.set(self.kw['text'] if 'text' in self.kw else text)
		if 'text' in self.kw:
			del self.kw['text']
		tkinter.Label.__init__(self, _root, textvariable=self.textvariable, **kw)
		self.pack( side=_pack_side )
		
	@property
	def text(self):
		return self.textvariable.get()
	
	@text.setter
	def text(self, text):
		self.textvariable.set(text)
		
class message(tkinter.Message, object):
	def __init__(self, text="", **kw):
		self.kw = kw
		self.textvariable = tkinter.StringVar()
		self.textvariable.set(self.kw['text'] if 'text' in self.kw else text)
		if 'text' in self.kw:
			del self.kw['text']
		tkinter.Message.__init__(self, _root, textvariable=self.textvariable, anchor=NW, **kw)
		self.pack( side=_pack_side )
		
	@property
	def text(self):
		return self.textvariable.get()
	
	@text.setter
	def text(self, text):
		self.textvariable.set(text)
		
class repeat(threading.Thread):
	def __init__(self, interval=1):
		global _events
		threading.Thread.__init__(self)
		self.interval = interval
		self.stopped = threading.Event()
		_events.append(self.stopped)
		
	def __call__(self, func):
		self.func = func
		self.start()
		return func
		
	def run(self):
		while not self.stopped.wait(self.interval):
			self.func()
			
class loop(threading.Thread):
	def __init__(self):
		global _events
		threading.Thread.__init__(self)
		self.stopped = threading.Event()
		_events.append(self.stopped)
		
	def __call__(self, func):
		self.func = func
		self.start()
		return func
		
	def run(self):
		while not self.stopped.isSet():
			self.func()
			
class editBox(tkinter.Entry, object):
	def __init__(self, text="", *args, **kwargs):
		self.textvariable = tkinter.StringVar()
		self.textvariable.set(text)
		tkinter.Entry.__init__(self, _root, textvariable=self.textvariable, **kwargs)
		self.pack(side=_pack_side)
	
	@property
	def text(self):
		return self.textvariable.get()
	
	@text.setter
	def text(self, text):
		self.textvariable.set(text)
		
def showInfo(title = "Info", message = "", **kw):
	messagebox.showinfo(title, message, **kw)
	
def showWarning(title = "Warning", message = "", **kw):
	messagebox.showwarning(title, message, **kw)
	
def showError(title = "Error", message = "", **kw):
	messagebox.showerror(title, message, **kw)
	
def askYesNo(title = "Question", message = "", **kw):
	return messagebox.askyesno(title, message, **kw)
	
def askOkCancel(title = "Question", message = "", **kw):
	return messagebox.askokcancel(title, message, **kw)
	
def askRetryCancel(title = "Retry?", message = "", **kw):
	return messagebox.askretrycancel(title, message, **kw)
	
def askYesNoCancel(title = "Retry?", message = "", **kw): # returns None on cancel
	return messagebox.askyesnocancel(title, message, **kw)
	
def askOpenFilename(**kw):
	return filedialog.askopenfilename(**kw)
	
def askSaveAsFilename(**kw):
	return filedialog.asksaveasfilename(**kw)
	
def askOpenFilenames(**kw):
	return filedialog.askopenfilenames(**kw)

@contextmanager
def askOpenFile(**kw):
	file = filedialog.askopenfile(**kw)
	try:
		yield file
	finally:
		file.close()

@contextmanager
def askOpenFiles(**kw):
	files = filedialog.askopenfiles(**kw)
	try:
		yield files
	finally:
		for file in files:
			file.close()

@contextmanager
def askSaveAsFile(**kw):
	file = filedialog.asksaveasfile(**kw)
	try:
		yield file
	finally:
		file.close()
	
def askDirectory(**kw):
	return filedialog.askdirectory(**kw)
	
def askInteger(title, prompt, **kw):
	return simpledialog.askinteger(title, prompt, **kw)
	
def askFloat(title, prompt, **kw):
	return simpledialog.askfloat(title, prompt, **kw)
	
def askString(title, prompt, **kw):
	return simpledialog.askstring(title, prompt, **kw)
	
class scrolledText(scrolledtext.ScrolledText, object):
	def __init__(self, text = "", bg='white', height=10, expand=True, editable=True, **kw):
		global _root, _pack_side
		scrolledtext.ScrolledText.__init__(self, _root, bg=bg, height=height, **kw)
		self.insert(tkinter.END, text)
		if not editable:
			self.config(state=DISABLED)
		self.pack(fill=tkinter.BOTH, side=_pack_side, expand=expand)
		
	@property
	def editable(self):
		return self.state==NORMAL
	
	@editable.setter
	def editable(self, editable):
		if editable:
			self.config(state=NORMAL)
		else:
			self.config(state=DISABLED)
	
class checkBox(tkinter.Checkbutton, object):
	def __init__(self, text="", checked=False, *args, **kwargs):
		self.textvariable = tkinter.StringVar()
		self.textvariable.set(text)
		self._checked = tkinter.BooleanVar()
		self._checked.set(checked)
		tkinter.Checkbutton.__init__(self, _root, textvariable=self.textvariable, variable=self._checked, **kwargs)
		self.pack(side=_pack_side)
		
	def __call__(self, func):
		self.config(command = lambda: func(self.checked))
		return func
	
	@property
	def text(self):
		return self.textvariable.get()
	
	@text.setter
	def text(self, text):
		self.textvariable.set(text)
		
	@property
	def checked(self):
		return self._checked.get()
	
	@checked.setter
	def checked(self, text):
		self._checked.set(text)
		
		
class radioButton(tkinter.Radiobutton, object):
	def __init__(self, value, text="", variable=None, checked=False, *args, **kwargs):
		global _radioVariable
		self.textvariable = tkinter.StringVar()
		self.textvariable.set(text)
		if variable is None:
			variable = _radioVariable
		self.variable = variable
		tkinter.Radiobutton.__init__(self, _root, textvariable=self.textvariable, variable=self.variable, value=value, **kwargs)
		self.pack(side=_pack_side)
		
	def __call__(self, func):
		self.config(command = lambda: func(self.variable.get()))
		return func
	
	@property
	def text(self):
		return self.textvariable.get()
	
	@text.setter
	def text(self, text):
		self.textvariable.set(text)
		
class radioSet(object):
	def __enter__(self):
		global _radioVariable
		self.IntVar = tkinter.IntVar()
		_radioVariable = self.IntVar
		return self
		
	def __exit__(self, type, value, traceback):
		pass
		
	@property
	def number(self):
		return self.IntVar.get()
	
	@number.setter
	def number(self, n):
		self.IntVar.set(n)
		
class spinBox(tkinter.Spinbox, object):
	def __init__(self, **kw):
		tkinter.Spinbox.__init__(self, _root, **kw)
		self.pack(side=_pack_side)
		
	def __call__(self, func):
		self.config(command = lambda: func(self.get()))
		return func
		
	@property
	def value(self):
		return self.get()
		
class scaleBar(tkinter.Scale, object):
	def __init__(self, range=None, enabled=True, **kw):
		tkinter.Scale.__init__(self, _root, **kw)
		self.pack(side=_pack_side)
		self._enabled = enabled
		
	def __call__(self, func):
		self.config(command = func)
		return func
		
	@property
	def value(self):
		return self.get()
		
	@value.setter
	def value(self, value):
		if not self.enabled:
			self.config(state=NORMAL)
		self.set(value)
		if not self.enabled:
			self.config(state=DISABLED)
		
	@property
	def enabled(self):
		return self._enabled
	
	@enabled.setter
	def enabled(self, enabled):
		self._enabled = enabled
		if enabled:
			self.config(state=NORMAL)
		else:
			self.config(state=DISABLED)
			
class optionMenu(tkinter.OptionMenu, object):
	def __init__(self, *values, **kw):
		self.values = values
		self.kw = kw
		self.StringVar = tkinter.StringVar()
		tkinter.OptionMenu.__init__(self, _root, self.StringVar, *values, **kw)
		self.pack(side=_pack_side)
		
	def __call__(self, func):
		self.StringVar = tkinter.StringVar()
		tkinter.OptionMenu.__init__(self, _root, self.StringVar, *self.values, command = func, **self.kw)
		self.pack(side=_pack_side)
		return func
		
	@property
	def option(self):
		return self.StringVar.get()
	
	@option.setter
	def option(self, option):
		self.StringVar.set(option)
	
class listBox(tkinter.Listbox, object):
	def __init__(self, **kw):
		values = kw['values']
		if 'values' in kw:
			del kw['values']
		tkinter.Listbox.__init__(self, _root, **kw)
		self.pack(side=_pack_side)
		for item in values:
			self.insert(tkinter.END, item)
			
	@property
	def selection(self):
		return self.curselection()[0]
