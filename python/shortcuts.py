import pythoncom, pyHook 
import json
import os 

class Shortcut(object):  
	APP_WHITE_LIST = json.load(open("whitelist.json", "r"))
	def __init__(self, saveDir): 
		self.shortcutPrefix = ('Lcontrol', 'Rcontrol', 'Lshift', 'Rshift', 'Lmenu', 'Rmenu')
		self.app = ''
		self.shortcut = []
		self.shortcutDict = {}
		self.saveDir = saveDir
		self.loadAll()
		print self.APP_WHITE_LIST

	def loadAll(self):
		[ self.shortcutDict.update({f.split(".json")[0]: json.load(open(os.path.join(self.saveDir,f)))}) for f in os.listdir(self.saveDir) ]
		return True


	def OnKeyboardEvent(self, event):
		windowName = event.WindowName.split(" - ")[-1]
		if windowName not in self.APP_WHITE_LIST:
			print windowName
			return True 


		if self.app == '' or self.app != None and self.app != windowName:
			self.reset()
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
		self.save() 
		#self.printEvent(event)
		return True

	def save(self):  
		if ('Lshift' in self.shortcut or 'Rshift' in self.shortcut) and len(self.shortcut)==2:
			self.reset()	
		 	return True 

		if self.app not in self.shortcutDict:
			self.shortcutDict[self.app] = {} 

		shortcutString = " + ".join(self.shortcut) 
		if shortcutString in self.shortcutDict:
			return True 

		self.shortcutDict[self.app][shortcutString] = self.shortcut
		file_path = os.path.join(self.saveDir, self.app + ".json")   
		json.dump(self.shortcutDict[self.app], open(file_path, 'w+'))
		self.reset()
		return True

	def reset(self):
		self.shortcut = []
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
		print( '-----------------------------------------')
		return True

	def recordShortcuts(self): 
		hm = pyHook.HookManager()
		hm.KeyDown = self.OnKeyboardEvent
		hm.HookKeyboard()
		pythoncom.PumpMessages()

shortcut = Shortcut("C:\\cygwin64\\home\\I311682\\github\\shortcuts\\shortcuts")
shortcut.recordShortcuts()