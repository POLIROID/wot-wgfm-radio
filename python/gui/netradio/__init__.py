
__author__ = "Andruschyshyn Andrey"
__copyright__ = "Copyright 2021, poliroid"
__credits__ = ["Andruschyshyn Andrey"]
__license__ = "LGPL-3.0-or-later"
__version__ = "3.5.5"
__maintainer__ = "Andruschyshyn Andrey"
__email__ = "poliroid@pm.me"
__status__ = "Production"

from gui.netradio.data import *
from gui.netradio.hooks import *
from gui.netradio.events import g_eventsManager
from gui.netradio.controllers import g_controllers
from gui.netradio.views import *

__all__ = ('init', 'fini')

def init():
	g_controllers.init()

def fini():
	g_eventsManager.onAppFinish()
