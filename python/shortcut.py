class Shortcut(dict):
	"""docstring for Shortcut"""
	def __init__(self, keys):
		super(Shortcut, self).__init__()
		self["keys"] = keys
		self["count"] = 1
		self["ignore"] = False

	def increaseCount(self):
		self["count"] = self["count"] + 1
		print self["count"]
		