import Tkinter
import ctypes
top = Tkinter.Tk()

class ept(object):
	"""docstring for ept"""
	def __init__(self, title):
		super(ept, self).__init__() 
		self.title = Tkinter.Label(top, text=title)
		self.title.pack()  
		self.quit_btn = Tkinter.Button(top, text='QUIT', command=self.quit, bg='blue', fg='white')
		self.quit_btn.pack(fill=Tkinter.X, expand=1)
		Tkinter.mainloop()
 
	def quit(self): 
		print "quit"
		ctypes.windll.user32.PostQuitMessage(0)
		top.quit() 
		 
if __name__ == '__main__': 
	ept(1, "test")
 
 