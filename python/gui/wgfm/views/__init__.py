from gui.Scaleform.framework import g_entitiesFactories, ViewSettings, GroupedViewSettings, ScopeTemplates
from gui.Scaleform.framework.entities.View import View
from frameworks.wulf import WindowLayer

from gui.wgfm._constants import WGFM_BATTLE_INJECTOR_UI, WGFM_BATTLE_COMPONENTS_UI, WGFM_LOBBY_WINDOW_UI
from gui.wgfm.views.battleView import WGFMBattleView
from gui.wgfm.views.lobbyView import WGFMLobbyView

def getViewSettings():
	viewSettings = []
	viewSettings.append(ViewSettings(WGFM_BATTLE_INJECTOR_UI, View, 'wgfmBattle.swf', WindowLayer.WINDOW,
										None, ScopeTemplates.GLOBAL_SCOPE))
	viewSettings.append(ViewSettings(WGFM_BATTLE_COMPONENTS_UI, WGFMBattleView, None, WindowLayer.UNDEFINED,
										None, ScopeTemplates.DEFAULT_SCOPE))
	viewSettings.append(ViewSettings(WGFM_LOBBY_WINDOW_UI, WGFMLobbyView, 'wgfmLobby.swf', WindowLayer.OVERLAY,
										None, ScopeTemplates.GLOBAL_SCOPE))
	return viewSettings

for item in getViewSettings():
	g_entitiesFactories.addSettings(item)
