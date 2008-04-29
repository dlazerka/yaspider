class Config(object):
	def __init__(self, homedir):
		self.homedir = homedir
		
	def __str__(self):
		return "%s: homedir=\"%s\"" % (self.__repr__(), self.homedir)
			
