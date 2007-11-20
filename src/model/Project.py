from PagesContainer import PagesContainer
from ProjectCfg import ProjectCfg
from Page import Page


class Project:
	def __init__(self, cfg):
		self.cfg = cfg
		self.pagesContainer = PagesContainer()
		self.cfg.addListener(self.cfgChanged)
		self.pagesContainer.addNewPageListener(self.cfg.newPageListener)


	def cfgChanged(self, **args):
		if args['firstUrl']:
			self.addUrl(args['firstUrl'])


	def setActive(self):
		if not self.cfg.isLoaded():
			self.cfg.load()

		self.isActive = True


	def addUrl(self, url, parentPage = None):
		if not self.pagesContainer.containsUrl(url):
			page = Page(url, self.cfg, parentPage)
			self.pagesContainer.add(page)


	def storeNextPage(self):
		page = self.pagesContainer.popQueued()
		if page.fetchContents():
			page.saveContents()
			page.parse()
			for link in page.links:
				self.addUrl(link, page)

