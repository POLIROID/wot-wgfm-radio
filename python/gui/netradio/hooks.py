import game

from debug_utils import LOG_ERROR
from gui.app_loader.settings import APP_NAME_SPACE
from gui.shared.personality import ServicesLocator
from gui.Scaleform.framework.managers.loaders import SFViewLoadParams
from skeletons.gui.app_loader import GuiGlobalSpaceID
from VOIP.VOIPManager import VOIPManager

from .data import g_dataHolder
from .events import g_eventsManager
from .lang import l10n
from .utils import override, getParentWindow
from ._constants import LOBBY_WINDOW_UI

__all__ = ()

# adding menu item to modslist
def showPlayer():
	"""fire load popover view on button click"""
	app = ServicesLocator.appLoader.getApp(APP_NAME_SPACE.SF_LOBBY)
	if not app:
		return
	app.loadView(SFViewLoadParams(LOBBY_WINDOW_UI, parent=getParentWindow()))

# Data Collect
g_dataCollector = None
try:
	from . import __version__ #NOSONAR
	from .data_collector import g_dataCollector #NOSONAR
except ImportError:
	LOG_ERROR('datacollector broken')
if g_dataCollector and g_dataHolder.settings.get("sendStatistic", True):
	g_dataCollector.addSoloMod('wgfm_mod', __version__)

# modsListApi
g_modsListApi = None
try:
	from gui.modsListApi import g_modsListApi #NOSONAR
except ImportError:
	LOG_ERROR('modsListApi not installed')
if g_modsListApi:
	g_modsListApi.addModification(id='net-radio', name=l10n('modslist.name'), enabled=True,
		description=l10n('modslist.description'), icon='gui/maps/netradio/modsListApi.png',
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
	from .controllers import g_controllers
	# handling forced keylistners
	for keyHandler in g_controllers.hotkey.forced:
		if keyHandler(event):
			return True
	# handling ingame logic
	result = baseMethod(event)
	# firing key event
	g_eventsManager.onKeyEvent(event, result)
	return result
