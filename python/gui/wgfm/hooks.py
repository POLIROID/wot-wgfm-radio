
import game
from gui.app_loader.loader import _AppLoader
from gui.app_loader.loader import g_appLoader
from gui.app_loader.settings import APP_NAME_SPACE, GUI_GLOBAL_SPACE_ID
from gui.modsListApi import g_modsListApi
from gui.Scaleform.framework.managers.loaders import SFViewLoadParams
from gui.shared import g_eventBus, events, EVENT_BUS_SCOPE
from VOIP.VOIPManager import VOIPManager

from gui.wgfm.data import g_dataHolder
from gui.wgfm.events import g_eventsManager
from gui.wgfm.lang import l10n
from gui.wgfm.utils import override
from gui.wgfm.wgfm_constants import WGFM_LOBBY_WINDOW_UI

__all__ = ()

# adding menu item to modslist
def showPlayer():
	"""fire load popover view on button click"""
	app = g_appLoader.getApp(APP_NAME_SPACE.SF_LOBBY)
	if not app:
		return
	app.loadView(SFViewLoadParams(WGFM_LOBBY_WINDOW_UI), {})

g_modsListApi.addModification(id = 'wgfm', name = l10n('modslist.name'), description = l10n('modslist.description'), \
	enabled = True, callback = showPlayer, login = True, lobby = True, icon = 'gui/maps/wgfm/modsListApi.png' )



# app finished
@override(_AppLoader, 'fini')
def hooked_fini(baseMethod, baseObject):
	g_eventsManager.onAppFinish()
	baseMethod(baseObject)

# app battle loaded
def onGUISpaceEntered(spaceID):
	
	if spaceID != GUI_GLOBAL_SPACE_ID.BATTLE:
		return

	g_eventsManager.onShowBattlePage()

g_appLoader.onGUISpaceEntered += onGUISpaceEntered

# app battle destroyed
def onGUISpaceLeft(spaceID):

	if spaceID != GUI_GLOBAL_SPACE_ID.BATTLE:
		return

	g_eventsManager.onDestroyBattle()

g_appLoader.onGUISpaceLeft += onGUISpaceLeft



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
	g_dataCollector.addSoloMod('wgfm_mod', '3.2.9')
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
