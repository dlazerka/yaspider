import thread

from PagesContainer import NoMorePages
from Project import Project
import Listened


class SiteDownloader(object):
	def __init__(self):
		self.loadCfg()
		self.setActiveProject(self.defProjectData['project'])
		self.__isActive = False


	def loadCfg(self):
		import os.path
		import xml.dom.minidom as minidom

		cfgFilePath = os.path.dirname(__file__) + '/../SiteDownloader.cfg.xml'

		cfgNode = minidom.parse(cfgFilePath).getElementsByTagName('cfg')[0]
		projectsNode = cfgNode.getElementsByTagName('projects')[0]
		projectNodes = projectsNode.getElementsByTagName('project')

		self.projects = []
		self.projectsData = []
		self.defProjectData = None
		for projectNode in projectNodes:
			projectName = projectNode.getElementsByTagName('name')[0].childNodes[0].data
			projectCfgFilePath = projectNode.getElementsByTagName('cfgFilePath')[0].childNodes[0].data
			projectCfgFilePath = os.path.join(os.path.dirname(cfgFilePath), projectCfgFilePath)
			isDefault = projectNode.getElementsByTagName('isDefault').length == 1

			from ProjectCfg import ProjectCfg
			cfg = ProjectCfg(
				filePath = projectCfgFilePath,
				name = projectName
			)
			project = Project(cfg = cfg)
			projectData = {
				'project': project,
				'cfgFilePath': projectCfgFilePath,
				'isDefault': isDefault,
			}

			self.projectsData.append(projectData)
			self.projects.append(project)

			if isDefault:
				self.defProjectData = projectData

		if not self.defProjectData:
			self.defProjectData = self.projectsData[0]


	def __mainLoop(self):
		while self.isActive():
			try:
				self.project.storeNextPage()
			except NoMorePages:
				self.stop()
			except Exception:
				self.stop()
				raise


	def setActiveProject(self, project):
		# indexes in self.projectsData must equal to indexes in self.projects
		i = self.projects.index(project)
		self.projectData = self.projectsData[i]
		self.project = self.projectData['project']
		self.project.setActive()
		self.notifyProjectListeners()


	def isActive(self):
		return self.__isActive


	def start(self):
		self.__isActive = True
		self.notifyActivityListeners()
		self.__mainLoopThread = thread.start_new_thread(self.__mainLoop, ())


	def stop(self):
		self.__isActive = False
		self.notifyActivityListeners()


	addActivityListener = Listened.getAddListenerMethod('activity')
	notifyActivityListeners = Listened.getNotifyListenersMethod('activity')

	addProjectListener = Listened.getAddListenerMethod('project')
	notifyProjectListeners = Listened.getNotifyListenersMethod('project')
