# SPDX-License-Identifier: MIT
# Copyright (c) 2015-2025 Andrii Andrushchyshyn

__version__ = "1.2.5"

from .data import *
from .hooks import *
from .events import g_eventsManager
from .controllers import g_controllers
from .views import *

__all__ = ('init', 'fini')

def init():
	g_controllers.init()

def fini():
	g_eventsManager.onAppFinish()
