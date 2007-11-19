from Tkinter import *
from tkFont import *
import re

import controller.CONTROLLER as CONTROLLER
import model.MODEL as MODEL


class Ui:
	def show(self):
		"""
		Main method, populates and shows GUI.
		"""
		self.widgets = dict()
		self.fonts = dict()
		self.pagesShown = []
		self.tk = Tk()
		self.tk.wm_title('Spider')

		self.createWidgets()
		self.bind()
		self.refreshControls()
		self.regExpTyping()

		#self.actStart()

		#root = Tk()
		#root.configure({'parent': self.widgets['mainFrame']})
		#self.widgets['buttonControl'].configure({'text': 'Start', 'command': self.actStart})
		#Frame.mainloop(self.widgets['mainFrame'])
		#wm = Wm()
		#wm.wm_title('Spider')
		self.tk.mainloop()


	def bind(self):
		"""
		Binds action handlers to the widgets
		"""
		# Binds
		def quit(*args):
			self.tk.quit()

		self.tk.bind('<Escape>', quit)
		self.widgets['buttonProjectPrev'].configure({'command': CONTROLLER.toPrevProject})
		self.widgets['buttonProjectNext'].configure({'command': CONTROLLER.toNextProject})
		self.widgets['buttonProjectSave'].configure({'command': self.saveProject})
		self.widgets['buttonProjectReset'].configure({'command': self.resetProject})
		self.widgets['checkbuttonShowAllPages'].configure({'command': self.refreshPagesList})
		self.widgets['buttonQuit'].configure({'command': quit})
		self.widgets['buttonControl'].configure({'command': self.actStart})
		self.widgets['entryRegExp'].bind('<KeyRelease>', self.regExpTyping)
		self.widgets['buttonClear'].bind('command', CONTROLLER.clearPages)

		MODEL.siteDownloader.addActivityListener(self.refreshControls)
		MODEL.siteDownloader.addProjectListener(self.projectSuperseded)
		MODEL.siteDownloader.project.pagesContainer.addNewPageListener(self.addPage)


	def saveProject(self):
		"""
		Saves current project config to the file (xml)
		"""
		name = self.widgets['entryProject'].get()
		localDir = self.widgets['entryLocalDir'].get()
		firstUrl = self.widgets['entryFirstUrl'].get()
		regExp = self.widgets['entryRegExp'].get()
		CONTROLLER.saveProject(
			name = name,
			localDir = localDir,
			firstUrl = firstUrl,
			regExp = regExp
		)


	def resetProject(self):
		"""
		Reads project config from file
		"""
		CONTROLLER.resetProject()
		self.refreshControls()


	def projectSuperseded(self):
		"""
		Called after project changed. We should clear and refresh all controls and output
		"""
		MODEL.siteDownloader.project.pagesContainer.addNewPageListener(self.addPage)
		self.refreshControls()
		self.refreshPagesList()


	def actStart(self):
		"""
		What happens after application is started ("Start" button pressed)
		"""
		localDir = self.widgets['entryLocalDir'].get()
		firstUrl = self.widgets['entryFirstUrl'].get()
		regExp = self.widgets['entryRegExp'].get()
		CONTROLLER.start(
			localDir = localDir,
			firstUrl = firstUrl,
			regExp = regExp
		)
		#self.refreshControls()


	def actStop(self):
		"""
		What happens if application is stopped ("Stop" button pressed)
		"""
		pass


	def refreshControls(self):
		"""
		Clears and populates the controls (textfields, disables/enables buttons etc) based on current state of the application
		"""
		if MODEL.siteDownloader.isActive():
			self.widgets['buttonControl'].configure({'text': 'Stop', 'command': self.actStop})
			self.widgets['entryFirstUrl'].configure({'state': 'readonly'})
			self.widgets['entryLocalDir'].configure({'state': 'readonly'})
		else:
			self.widgets['buttonControl'].configure({'text': 'Start', 'command': self.actStart})
			self.widgets['entryFirstUrl'].configure({'state': 'normal'})
			self.widgets['entryLocalDir'].configure({'state': 'normal'})

		project = MODEL.siteDownloader.project
		isFirst = MODEL.siteDownloader.projects.index(project) == 0
		isLast = MODEL.siteDownloader.projects.index(project) + 1 == len(MODEL.siteDownloader.projects)
		if isFirst:
			self.widgets['buttonProjectPrev'].configure({'state': 'disabled'})
		else:
			self.widgets['buttonProjectPrev'].configure({'state': 'normal'})
		if isLast:
			self.widgets['buttonProjectNext'].configure({'state': 'disabled'})
		else:
			self.widgets['buttonProjectNext'].configure({'state': 'normal'})
		self.widgets['entryProject'].delete('0', 'end')
		self.widgets['entryFirstUrl'].delete('0', 'end')
		self.widgets['entryLocalDir'].delete('0', 'end')
		self.widgets['entryRegExp'].delete('0', 'end')
		self.widgets['entryTestUrl'].delete('0', 'end')
		self.widgets['entryProject'].insert('0', project.cfg.name)
		self.widgets['entryFirstUrl'].insert('0', project.cfg.firstUrl)
		self.widgets['entryLocalDir'].insert('0', project.cfg.localDir)
		self.widgets['entryRegExp'].insert('0', project.cfg.regExp)
		self.widgets['entryTestUrl'].insert('0', self.widgets['entryFirstUrl'].get())


	def addPage(self, page):
		"""
		Adds an entry to the widgets['pagesList']
		"""
		if page.getStatus() == 'failed regexp' \
			and not self.widgets['checkbuttonShowAllPages'].isSelected.get():
			return

		page.addStatusListener(self.pageStatusListener)

		lineStart = self.widgets['pagesList'].index('End')

		self.widgets['pagesList'].insert('End', '%s ' % page.id);
		if page.parent:
			self.widgets['pagesList'].insert('End', '%s ' % page.parent.id);
		self.widgets['pagesList'].insert('End', page.relPath);
		self.widgets['pagesList'].insert('End', '    ');

		self.widgets['pagesList'].mark_set('Page%sStatusStart' % id(page), 'End')
		self.widgets['pagesList'].mark_gravity('Page%sStatusStart' % id(page), 'left')
		self.widgets['pagesList'].insert('End', page.getStatus());
		self.widgets['pagesList'].mark_set('Page%sStatusEnd' % id(page), 'End')
		self.widgets['pagesList'].mark_gravity('Page%sStatusEnd' % id(page), 'left')
		self.widgets['pagesList'].insert('End', '\n');
		self.widgets['pagesList'].mark_gravity('Page%sStatusEnd' % id(page), 'right')


		self.widgets['pagesList'].tag_add('Page%s' % id(page), lineStart, 'End');

		if page.getStatus() == 'failed regexp':
			self.widgets['pagesList'].tag_configure('Page%s' % id(page), {
				'background': '#eeeeee',
			});


	def pageStatusListener(self, page):
		"""
		Listens for the given page status and shows its status as it changes.
		"""
		self.widgets['pagesList'].delete('Page%sStatusStart' % id(page), 'Page%sStatusEnd' % id(page));
		self.widgets['pagesList'].insert('Page%sStatusStart' % id(page), page.getStatus());



	def refreshPagesList(self):
		"""
		Clears and populates the widgets['pagesList'] by current project pages.
		"""
		self.clearPagesList()
		for page in MODEL.siteDownloader.project.pagesContainer.pages:
			self.addPage(page)


	def clearPagesList(self):
		"""
		Clears pages list.
		"""
		self.widgets['pagesList'].delete('1.0', 'End')
		self.pagesCnt = 0



	def regExpTyping(self, *args):
		"""
		Called each time a key pressed in regExpEntry.
		"""
		regExp = self.widgets['entryRegExp'].get()
		testUrl = self.widgets['entryTestUrl'].get()

		try:
			re.compile(regExp)
		except re.error, e:
			text = e.__str__()
			fg = 'red'
		else:
			if (re.search(regExp, testUrl)):
				text =  'True'
				fg = '#080'
			else:
				text =  'False'
				fg = 'red'

		self.widgets['labelTestResult'].configure({'fg': fg, 'text': text})


	def createWidgets(self):
		"""
		Creates widdgets, sets theirs UI properties and packs them.
		"""
		# Create frames to pack widgets to
		self.widgets['mainFrame'] = Frame(self.tk)

		self.widgets['frameParams'] = Frame(self.widgets['mainFrame'])
		self.widgets['frameCheckboxes'] = Frame(self.widgets['mainFrame'])
		self.widgets['frameButtons'] = Frame(self.widgets['mainFrame'], {
			'cursor': 'hand2',
		})

		self.widgets['frameProject'] = Frame(self.widgets['frameParams'])
		self.widgets['frameFirstUrl'] = Frame(self.widgets['frameParams'])
		self.widgets['frameLocalDir'] = Frame(self.widgets['frameParams'])
		self.widgets['frameRegExp'] = Frame(self.widgets['frameParams'])
		self.widgets['frameTestUrl'] = Frame(self.widgets['frameParams'])
		self.widgets['frameTestResult'] = Frame(self.widgets['frameParams'])


		# Create widgets
		self.widgets['buttonProjectPrev'] = Button(self.widgets['frameProject'], {
			'text': ' < '
		})
		self.widgets['entryProject'] = Entry(self.widgets['frameProject'], {
			'justify': 'center',
		})
		self.widgets['buttonProjectNext'] = Button(self.widgets['frameProject'], {
			'text': ' > '
		})
		self.widgets['buttonProjectSave'] = Button(self.widgets['frameProject'], {
			'text': 'Save',
			'padx': '4',
		})
		self.widgets['buttonProjectReset'] = Button(self.widgets['frameProject'], {
			'text': 'Reset'
		})
		self.widgets['labelFirstUrl'] = Label(self.widgets['frameFirstUrl'], {
			'text': 'First URL: '
		})
		self.widgets['labelLocalDir'] = Label(self.widgets['frameLocalDir'], {
			'text': 'Local Path: '
		})
		self.widgets['labelRegExp'] = Label(self.widgets['frameRegExp'], {
			'text': 'RegExp: '
		})
		self.widgets['labelTestUrl'] = Label(self.widgets['frameTestUrl'], {
			'text': 'Test URL: '
		})
		self.widgets['labelTestResultLabel'] = Label(self.widgets['frameTestResult'], {
			'text': 'Test Result:'
		})
		self.widgets['labelTestResult'] = Label(self.widgets['frameTestResult'], {
		})

		self.widgets['entryFirstUrl'] = Entry(self.widgets['frameFirstUrl'])
		self.widgets['entryLocalDir'] = Entry(self.widgets['frameLocalDir'])
		self.widgets['entryRegExp'] = Entry(self.widgets['frameRegExp'])
		self.widgets['entryTestUrl'] = Entry(self.widgets['frameTestUrl'])

		self.widgets['checkbuttonShowAllPages'] = Checkbutton(self.widgets['frameCheckboxes'], {
			'text': 'Show All Pages',
			'pady': 3,
			'cursor': 'hand2',
		})
		self.widgets['checkbuttonShowAllPages'].isSelected = IntVar()
		self.widgets['checkbuttonShowAllPages'].configure({
			'variable': self.widgets['checkbuttonShowAllPages'].isSelected,
		})

		self.widgets['buttonQuit'] = Button(self.widgets['frameButtons'], {
			'text': 'Quit',
			'width': 8
		})
		self.widgets['buttonControl'] = Button(self.widgets['frameButtons'], {
			'width': 8
		})

		self.fonts['pagesList'] = Font(self.tk,
			size = 10,
			family = 'Courier',
			weight = 'bold'
		)
		self.widgets['pagesList'] = Text(self.widgets['mainFrame'], {
			'width': 100,
			'height': 20,
			'font': self.fonts['pagesList']
		})
		self.widgets['pagesList'].mark_set('End', '1.end')
		self.widgets['pagesList'].mark_gravity('End', 'right')
		
		self.widgets['buttonClear'] = Scale(self.widgets['pagesList'], {
			#'text': 'Clear',
			#'cursor': 'hand2'
		})

		self.fonts['log'] = Font(self.tk,
			size = 10,
			family = 'Courier',
		)
		self.widgets['log'] = Text(self.widgets['mainFrame'], {
			'width': 100,
			'height': 10,
			'font': self.fonts['log']
		})


		# Pack level 0
		self.widgets['mainFrame'].pack({'fill': 'both', 'expand': 'yes'});


		# Pack level 1
		self.widgets['log'].pack({'side': 'bottom', 'fill': 'x', 'expand': 'yes'})
		self.widgets['pagesList'].pack({'side': 'bottom', 'fill': 'both', 'expand': 'yes'})
		self.widgets['buttonClear'].place({'anchor': 'se', 'relx': '1', 'rely': '1'})
		self.widgets['frameParams'].pack({'side': 'left', 'fill': 'x', 'expand': 'yes'})
		self.widgets['frameCheckboxes'].pack({'side': 'left', 'fill': 'y'})
		self.widgets['frameButtons'].pack({'side': 'left', 'fill': 'y'})


		# Pack level 2
		self.widgets['frameProject'].pack({'side': 'top', 'fill': 'x'})
		self.widgets['buttonProjectPrev'].pack({'side': 'left', 'fill': 'x'})
		self.widgets['entryProject'].pack({'side': 'left', 'fill': 'x',
			'expand': 'yes',
		})
		self.widgets['buttonProjectNext'].pack({'side': 'left', 'fill': 'x'})
		self.widgets['buttonProjectSave'].pack({'side': 'left', 'fill': 'x',
			'expand': 'yes', 'padx': '5 0',
		})
		self.widgets['buttonProjectReset'].pack({'side': 'left', 'fill': 'x',
			'expand': 'yes', 'padx': '5 0',
		})

		self.widgets['frameFirstUrl'].pack({'side': 'top', 'fill': 'x'})
		self.widgets['labelFirstUrl'].pack({'side': 'left'})
		self.widgets['entryFirstUrl'].pack({'side': 'left', 'fill': 'x', 'expand': 'yes'})

		self.widgets['frameLocalDir'].pack({'side': 'top', 'fill': 'x'})
		self.widgets['labelLocalDir'].pack({'side': 'left'})
		self.widgets['entryLocalDir'].pack({'side': 'left', 'fill': 'x', 'expand': 'yes'})

		self.widgets['frameRegExp'].pack({'side': 'top', 'fill': 'x'})
		self.widgets['labelRegExp'].pack({'side': 'left'})
		self.widgets['entryRegExp'].pack({'side': 'left', 'fill': 'x', 'expand': 'yes'})

		self.widgets['frameTestUrl'].pack({'side': 'top', 'fill': 'x'})
		self.widgets['labelTestUrl'].pack({'side': 'left'})
		self.widgets['entryTestUrl'].pack({'side': 'left', 'fill': 'x', 'expand': 'yes'})

		self.widgets['frameTestResult'].pack({'side': 'top', 'fill': 'x'})
		self.widgets['labelTestResultLabel'].pack({'side': 'left'})
		self.widgets['labelTestResult'].pack({'side': 'left'})

		self.widgets['checkbuttonShowAllPages'].pack({'side': 'top'})

		self.widgets['buttonQuit'].pack({'side': 'top', 'fill':'y', 'expand': 'yes'});
		self.widgets['buttonControl'].pack({'side': 'top', 'fill':'y', 'expand': 'yes'});


ui = Ui()
