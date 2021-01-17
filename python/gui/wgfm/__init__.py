
__author__ = "Andruschyshyn Andrey"
__copyright__ = "Copyright 2021, poliroid"
__credits__ = ["Andruschyshyn Andrey"]
__license__ = "CC BY-NC-SA 4.0"
__version__ = "3.5.3"
__maintainer__ = "Andruschyshyn Andrey"
__email__ = "p0lir0id@yandex.ru"
__status__ = "Production"

from gui.wgfm.data import *
from gui.wgfm.hooks import *
from gui.wgfm.events import g_eventsManager
from gui.wgfm.controllers import g_controllers
from gui.wgfm.views import *

__all__ = ('init', 'fini')

def init():
	g_controllers.init()

def fini():
	g_eventsManager.onAppFinish()
