
__author__ = "Andrii Andrushchyshyn"
__copyright__ = "Copyright 2022, poliroid"
__credits__ = ["Andrii Andrushchyshyn"]
__license__ = "LGPL-3.0-or-later"
__version__ = "1.0.2"
__maintainer__ = "Andrii Andrushchyshyn"
__email__ = "contact@poliroid.me"
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
