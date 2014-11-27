import pythoncom, pyHook 
import json
import os 
from eventHelper import printEvent
from shortcut import Shortcut

class Main(object):  
	APP_WHITE_LIST = json.load(open("whitelist.json"))
	def __init__(self, saveDir): 
		self.shortcutPrefix = json.load(open("prefix.json"))
		self.app = ''
		self.keys = []
		self.appShortcuts = {}
		self.saveDir = saveDir
		self.loadAll() 

	def loadAll(self):
		[ self.appShortcuts.update({f.split(".json")[0]: json.load(open(os.path.join(self.saveDir,f)))}) \
			for f in os.listdir(self.saveDir) ]
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
		if key in self.keys:
			return True 
		if key in self.shortcutPrefix: 
			self.keys.append(key) 
			return True 
		if len(self.keys) == 0:
			return True

		self.keys.append(key) 
		self.save() 
		#printEvent(event)
		return True

	def save(self):  
		if ('Lshift' in self.keys or 'Rshift' in self.keys) and len(self.keys)==2:
			self.reset()	
		 	return True 

		if self.app not in self.appShortcuts:
			self.appShortcuts[self.app] = {} 

		shortcutName = " + ".join(self.keys) 
		if shortcutName in self.appShortcuts[self.app]:
			shortcut = self.appShortcuts[self.app][shortcutName]
			shortcut["count"] = shortcut["count"] + 1 
		else:   
			self.appShortcuts[self.app][shortcutName] = {"keys": self.keys, "count": 1, "ignore": False}
 
		file_path = os.path.join(self.saveDir, self.app + ".json") 
		json.dump(self.appShortcuts[self.app], open(file_path, 'w+'))
		self.reset()
		return True 
  
	def reset(self):
		self.keys = []
		return True 

	def recordShortcuts(self): 
		hm = pyHook.HookManager()
		hm.KeyDown = self.OnKeyboardEvent
		hm.HookKeyboard()
		pythoncom.PumpMessages()

main = Main("C:\\cygwin64\\home\\I311682\\github\\shortcuts\\shortcuts")
main.recordShortcuts()