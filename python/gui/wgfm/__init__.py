
__all__ = ( )


from gui.wgfm.data import *
from gui.wgfm.hooks import *
from gui.wgfm.lang import *
from gui.wgfm.events import *
from gui.wgfm.utils import *
from gui.wgfm.wgfm_constants import *
from gui.wgfm.controllers import *
from gui.wgfm.views import *



g_controllers.init()

if g_dataHolder.settings.get('autoPlay', False):
	g_controllers.player.playRadio()



from gui.app_loader.loader import g_appLoader
from gui.modsListApi import g_modsListApi
g_modsListApi.addModification(
	id = 'wgfm', 
	name = l10n('#modslist_name'), 
	description = l10n('#modslist_description'), 
	icon = 'gui/maps/wgfm/modsListApi.png',
	enabled = True, 
	login = True, 
	lobby = True, 
	callback = lambda : g_appLoader.getDefLobbyApp().loadView(WGFM_LOBBY_WINDOW_UI)
)

