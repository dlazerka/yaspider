"""
Functions to create methods which implements listened class in Observer pattern.
Example:

class Foo:
	addPropertyListener = getAddListenerMethod('property')
	notifyPropertyListeners = getNotifyListenersMethod('property')

generates code like:

class Foo:
	propertyListeners = set()
	def addPropertyListener(self, listener):
		self.propertyListeners.add(listener)
	def notifyPropertyListeners(self, *pargs, **kargs):
		for listener in self.propertyListeners:
			listener(*pargs, **kargs)
"""

def getAddListenerMethod(name):

	listenersListName = '__%sListeners' % name
	functionName = 'add%sListener' % name.capitalize()

	def tmp(self, listener):
		if not hasattr(self, listenersListName):
			setattr(self, listenersListName, set())

		listenersList = getattr(self, listenersListName)
		listenersList.add(listener)

	tmp.__name__ = functionName

	return tmp


def getNotifyListenersMethod(name):

	listenersListName = '__%sListeners' % name
	functionName = 'add%sListener' % name.capitalize()

	def tmp(self, *pargs, **kargs):
		if hasattr(self, listenersListName):
			for listener in getattr(self, listenersListName):
				listener(*pargs, **kargs)

	tmp.__name__ = functionName

	return tmp
