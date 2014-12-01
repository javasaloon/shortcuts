import pythoncom, pyHook 
import json
import os 
from eventHelper import printEvent
from shortcut import Shortcut
from show import ept

class Main(object):  
	with open("whitelist.json") as f: 
		APP_WHITE_LIST = json.load(f)

	def __init__(self, saveDir): 
		with open("prefix.json") as f:
			self.shortcutPrefix = json.load(f) 
		self.app = ''
		self.keys = []
		self.saveDir = saveDir 
		self.appShortcuts = { f.split(".json")[0]: self.getJson(f) for f in os.listdir(self.saveDir) }  
		self.ept = ept("ept")
		 
	def getJson(self, fileName):
		with open(os.path.join(self.saveDir, fileName)) as f:
			return json.load(f) 

	def OnKeyboardEvent(self, event):
		windowName = event.WindowName.split(" - ")[-1]
		if windowName not in self.APP_WHITE_LIST:
			print unicode(windowName)
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
			shortcut["count"] += 1 
		else:   
			self.appShortcuts[self.app][shortcutName] = {"keys": self.keys, "count": 1, "ignore": False}
 
		file_path = os.path.join(self.saveDir, self.app + ".json") 
		with open(file_path, 'w') as f:
			json.dump(self.appShortcuts[self.app], f)
		
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