
import game
from gui.app_loader.loader import _AppLoader
from VOIP.VOIPManager import VOIPManager
from gui.Scaleform.Flash import Flash

from gui.wgfm.events import *
from gui.wgfm.utils import *

__all__ = ( )

@override(_AppLoader, 'showBattlePage')
def hooked_showBattlePage(baseMethod, baseObject):
	baseMethod(baseObject)
	g_eventsManager.onShowBattlePage()

@override(_AppLoader, 'destroyBattle')
def hooked_destroyBattle(baseMethod, baseObject):
	baseMethod(baseObject)
	g_eventsManager.onDestroyBattle()

@override(_AppLoader, 'fini')
def hooked_fini(baseMethod, baseObject):
	g_eventsManager.onAppFinish()
	baseMethod(baseObject)

@override(VOIPManager, '_VOIPManager__muffleMasterVolume')
def hooked_muffleMasterVolume(baseMethod, baseObject):
	baseMethod(baseObject)
	g_eventsManager.onSetVoipActive(True)

@override(VOIPManager, '_VOIPManager__restoreMasterVolume')
def hooked_restoreMasterVolume(baseMethod, baseObject):
	baseMethod(baseObject)
	g_eventsManager.onSetVoipActive(False)

@override(game, 'handleKeyEvent')
def handleKeyEvent(baseMethod, event):
	result = baseMethod(event)
	g_eventsManager.onKeyEvent(event, result)
	return result

@override(Flash, '_Flash__onLogGui')
def onLogGui(baseMethod, baseObject, mtype, msg, *args):
	if mtype == 'ERROR':
		print msg + ' ' + ', '.join([unicode(s) for s in args])
	baseMethod(baseObject, mtype, msg, *args)