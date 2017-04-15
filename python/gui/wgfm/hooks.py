
import game
from gui.app_loader.loader import _AppLoader
from VOIP.VOIPManager import VOIPManager
from gui.app_loader.loader import g_appLoader
from gui.modsListApi import g_modsListApi

from gui.wgfm.data import g_dataHolder
from gui.wgfm.events import *
from gui.wgfm.lang import *
from gui.wgfm.utils import *
from gui.wgfm.wgfm_constants import WGFM_LOBBY_WINDOW_UI

__all__ = ()

# adding menu item to modslist
add = g_modsListApi.addModification
add(id = 'wgfm', name = l10n('modslist.name'), description = l10n('modslist.description'), \
	icon = 'gui/maps/wgfm/modsListApi.png',	enabled = True,	login = True, lobby = True, \
	callback = lambda : g_appLoader.getDefLobbyApp().loadView(WGFM_LOBBY_WINDOW_UI) )

# app battle loaded
@override(_AppLoader, 'showBattlePage')
def hooked_showBattlePage(baseMethod, baseObject):
	baseMethod(baseObject)
	g_eventsManager.onShowBattlePage()

# app battle destroyed
@override(_AppLoader, 'destroyBattle')
def hooked_destroyBattle(baseMethod, baseObject):
	baseMethod(baseObject)
	g_eventsManager.onDestroyBattle()

# app finished
@override(_AppLoader, 'fini')
def hooked_fini(baseMethod, baseObject):
	g_eventsManager.onAppFinish()
	baseMethod(baseObject)

# VOIP handlers
@override(VOIPManager, '_VOIPManager__muffleMasterVolume')
def hooked_muffleMasterVolume(baseMethod, baseObject):
	baseMethod(baseObject)
	g_eventsManager.onSetVoipActive(True)

@override(VOIPManager, '_VOIPManager__restoreMasterVolume')
def hooked_restoreMasterVolume(baseMethod, baseObject):
	baseMethod(baseObject)
	g_eventsManager.onSetVoipActive(False)

# track stat
if g_dataHolder.settings.get("sendStatistic", True):
	from gui.wgfm.data_collector import g_dataCollector
	g_dataCollector.addSoloMod('wgfm_mod', '3.0.7')
	if g_dataHolder.settings.get("isModpack", False):
		g_dataCollector.addSoloMod("wgfm_mod_modpack")
	else:
		g_dataCollector.addSoloMod("wgfm_mod_standalone")

# ingame keyHandler hook
@override(game, 'handleKeyEvent')
def handleKeyEvent(baseMethod, event):
	from gui.wgfm.controllers import g_controllers
	# handling forced keylistners
	for keyHandler in g_controllers.hotkey.forced:
		if keyHandler(event):
			return True
	# handling ingame logic
	result = baseMethod(event)
	# firing key event 
	g_eventsManager.onKeyEvent(event, result)
	return result
