import xml.dom.minidom
import re
from StringIO import StringIO


import Listened


class ProjectCfg:
	def __init__(self, name, filePath):
		self.filePath = filePath
		self.name = name
		self.firstUrl = None
		self.localDir = None
		self.remoteDir = None
		self.regExp = None
		self.__isLoaded = False


	def load(self):
		self.cfgDom = xml.dom.minidom.parse(self.filePath)
		cfgNode = self.cfgDom.getElementsByTagName('cfg')[0]

		self.name = cfgNode.getElementsByTagName('name')[0].childNodes[0].data
		self.firstUrl = cfgNode.getElementsByTagName('firstUrl')[0].childNodes[0].data
		self.remoteDir = cfgNode.getElementsByTagName('remoteDir')[0].childNodes[0].data
		self.localDir = cfgNode.getElementsByTagName('localDir')[0].childNodes[0].data
		self.regExp = cfgNode.getElementsByTagName('regExp')[0].childNodes[0].data

		self.__isLoaded = True


	def set(self,
		name = None,
		firstUrl = None,
		localDir = None,
		remoteDir = None,
		regExp = None,
	):
		if name:
			self.name = name
		if firstUrl:
			self.firstUrl = firstUrl
		if localDir:
			self.localDir = localDir
		if regExp:
			self.regExp = regExp

		if firstUrl:
			if not remoteDir:
				self.remoteDir = re.sub('/[^/]*$', '', firstUrl)

		self.notifyListeners(
			name = name,
			firstUrl = firstUrl,
			localDir = localDir,
			remoteDir = remoteDir,
			regExp = regExp,
		)


	def save(self):
		w = StringIO()
		dom = self.cfgDom
		w.write('<?xml version="1.0" encoding="UTF-8"?>\n')
		dom.childNodes[0].writexml(w, '', '')
		s = w.getvalue()

		f = file(self.filePath + '.cpy', 'w')
		f.write(s)
		f.close()


	def newPageListener(self, page):
		newlineTextNode = self.cfgDom.createTextNode('\n');
		tabTextNode = self.cfgDom.createTextNode('\t');
		pageNode = self.cfgDom.createElement('page');
		urlNode = self.cfgDom.createElement('url');
		statusNode = self.cfgDom.createElement('status');
		urlTextNode = self.cfgDom.createTextNode(page.url);
		statusTextNode = self.cfgDom.createTextNode(page.getStatus());

		pagesNode = self.cfgDom.getElementsByTagName('pages')[0]
		pageNode.appendChild(urlNode)
		urlNode.appendChild(urlTextNode)
		pageNode.appendChild(newlineTextNode)
		pageNode.appendChild(statusNode)
		pageNode.appendChild(newlineTextNode)
		statusNode.appendChild(statusTextNode)


	def isLoaded(self):
		return self.__isLoaded


	addListener = Listened.getAddListenerMethod('')
	notifyListeners = Listened.getNotifyListenersMethod('')


