import model.MODEL as MODEL


def start(firstUrl, localDir, regExp):
	project = MODEL.siteDownloader.project

	project.cfg.set(
		firstUrl = firstUrl,
		localDir = localDir,
		regExp = regExp,
	)

	MODEL.siteDownloader.start()


def saveProject(name, firstUrl, localDir, regExp):
	MODEL.siteDownloader.project.cfg.set(
		name = name,
		firstUrl = firstUrl,
		localDir = localDir,
		regExp = regExp,
	)
	MODEL.siteDownloader.project.cfg.save()


def resetProject():
	MODEL.siteDownloader.project.cfg.load()


def toPrevProject(**args):
	__toProject(-1)


def toNextProject(**args):
	__toProject(1)


def __toProject(shift):
	curNum = MODEL.siteDownloader.projects.index(MODEL.siteDownloader.project)
	MODEL.siteDownloader.setActiveProject(MODEL.siteDownloader.projects[curNum + shift])

def clearPages(**args):
	"""
	Clears the project pages list.
	"""
	raise Exception;
	MODEL.siteDownloader.project.clearPages()
