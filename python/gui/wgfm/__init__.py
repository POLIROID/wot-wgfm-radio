
__author__ = "Andruschyshyn Andrey"
__copyright__ = "Copyright 2019, Wargaming"
__credits__ = ["Andruschyshyn Andrey"]
__license__ = "CC BY-NC-SA 4.0"
__version__ = "3.4.2"
__maintainer__ = "Andruschyshyn Andrey"
__email__ = "prn.a_andruschyshyn@wargaming.net"
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
