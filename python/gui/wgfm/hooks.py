import game
from debug_utils import LOG_ERROR
from gui.app_loader.settings import APP_NAME_SPACE
from gui.shared.personality import ServicesLocator
from gui.Scaleform.framework.managers.loaders import SFViewLoadParams
from gui.wgfm.data import g_dataHolder
from gui.wgfm.events import g_eventsManager
from gui.wgfm.lang import l10n
from gui.wgfm.utils import override
from gui.wgfm.wgfm_constants import WGFM_LOBBY_WINDOW_UI
from skeletons.gui.app_loader import GuiGlobalSpaceID
from VOIP.VOIPManager import VOIPManager

__all__ = ()

# adding menu item to modslist
def showPlayer():
	"""fire load popover view on button click"""
	app = ServicesLocator.appLoader.getApp(APP_NAME_SPACE.SF_LOBBY)
	if not app:
		return
	app.loadView(SFViewLoadParams(WGFM_LOBBY_WINDOW_UI), {})

# Data Collect
g_dataCollector = None
try:
	from gui.wgfm import __version__ #NOSONAR
	from gui.wgfm.data_collector import g_dataCollector #NOSONAR
except ImportError:
	LOG_ERROR('datacollector broken')
if g_dataCollector and g_dataHolder.settings.get("sendStatistic", True):
	g_dataCollector.addSoloMod('wgfm_mod', __version__)
	if g_dataHolder.settings.get("isModpack", False):
		g_dataCollector.addSoloMod("wgfm_mod_modpack")
	else:
		g_dataCollector.addSoloMod("wgfm_mod_standalone")

# modsListApi
g_modsListApi = None
try:
	from gui.modsListApi import g_modsListApi #NOSONAR
except ImportError:
	LOG_ERROR('modsListApi not installed')
if g_modsListApi:
	g_modsListApi.addModification(id='wgfm', name=l10n('modslist.name'), enabled=True, \
		description=l10n('modslist.description'), icon='gui/maps/wgfm/modsListApi.png', \
		login=True, lobby=True, callback=showPlayer)

# app battle loaded
def onGUISpaceEntered(spaceID):
	if spaceID != GuiGlobalSpaceID.BATTLE:
		return
	g_eventsManager.onShowBattlePage()
ServicesLocator.appLoader.onGUISpaceEntered += onGUISpaceEntered

# app battle destroyed
def onGUISpaceLeft(spaceID):
	if spaceID != GuiGlobalSpaceID.BATTLE:
		return
	g_eventsManager.onDestroyBattle()
ServicesLocator.appLoader.onGUISpaceLeft += onGUISpaceLeft



# VOIP handlers
@override(VOIPManager, '_VOIPManager__muffleMasterVolume')
def hooked_muffleMasterVolume(baseMethod, baseObject):
	baseMethod(baseObject)
	g_eventsManager.onSetVoipActive(True)

@override(VOIPManager, '_VOIPManager__restoreMasterVolume')
def hooked_restoreMasterVolume(baseMethod, baseObject):
	baseMethod(baseObject)
	g_eventsManager.onSetVoipActive(False)

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
