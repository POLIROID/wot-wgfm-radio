# SPDX-License-Identifier: MIT
# Copyright (c) 2015-2025 Andrii Andrushchyshyn

from gui.Scaleform.framework import g_entitiesFactories, ViewSettings, ScopeTemplates
from gui.Scaleform.framework.entities.View import View
from frameworks.wulf import WindowLayer

from .._constants import BATTLE_INJECTOR_UI, BATTLE_COMPONENT_UI, LOBBY_WINDOW_UI
from ..views.battleView import NetRadioBattleView
from ..views.lobbyView import NetRadioLobbyView

def getViewSettings():
	viewSettings = []
	viewSettings.append(ViewSettings(BATTLE_INJECTOR_UI, View, 'netRadioBattle.swf', WindowLayer.WINDOW,
										None, ScopeTemplates.GLOBAL_SCOPE))
	viewSettings.append(ViewSettings(BATTLE_COMPONENT_UI, NetRadioBattleView, None, WindowLayer.UNDEFINED,
										None, ScopeTemplates.DEFAULT_SCOPE))
	viewSettings.append(ViewSettings(LOBBY_WINDOW_UI, NetRadioLobbyView, 'netRadioLobby.swf', WindowLayer.OVERLAY,
										None, ScopeTemplates.GLOBAL_SCOPE))
	return viewSettings

for item in getViewSettings():
	g_entitiesFactories.addSettings(item)
