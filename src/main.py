import os


from Config import Config
from model.Application import Application
from view.Ui import Ui

config = Config(os.path.abspath('%s/../..' % __file__))
application = Application(config)
ui = Ui(application)

ui.show()

