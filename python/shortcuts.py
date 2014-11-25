import pythoncom, pyHook 

class Shortcut(object):
	"""docstring for shortcut"""
	def __init__(self): 
		self.shortcutPrefix = ('Lcontrol', 'Rcontrol', 'Lshift', 'Rshift', 'Lmenu', 'Rmenu')
		self.app = ''
		self.shortcut = []

	def OnKeyboardEvent(self, event): 
		windowName = event.WindowName.split(" - ")[-1]
		if self.app == '' or self.app != None and self.app != windowName:
			self.shortcut = []
			self.app = windowName

		key = event.Key
		if key in self.shortcut:
			return True 
		if key in self.shortcutPrefix: 
			self.shortcut.append(key) 
			return True 
		if len(self.shortcut) == 0:
			return True

		self.shortcut.append(key) 
		print(self.app + ": " + " + ".join(self.shortcut)) 
		self.shortcut = []
		#self.printEvent(event)
		return True

	def printEvent(self, event):
		print('MessageName:', event.MessageName) 
		print('Message:',event.Message)
		print('Time:', event.Time)
		print('Window:',event.Window)
		print('WindowName:',event.WindowName)
		print('Ascii:', event.Ascii, chr(event.Ascii))
		print('Key:', event.Key)
		print( 'KeyID:', event.KeyID)
		print( 'ScanCode:', event.ScanCode)
		print( 'Extended:', event.Extended)
		print( 'Injected:', event.Injected)
		print( 'Alt', event.Alt)
		print( 'Transition', event.Transition)
		print( '---')
		return True

	def recordShortcuts(self): 
		hm = pyHook.HookManager()
		hm.KeyDown = self.OnKeyboardEvent
		hm.HookKeyboard()
		pythoncom.PumpMessages()

shortcut = Shortcut()
shortcut.recordShortcuts()