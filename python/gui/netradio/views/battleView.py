# SPDX-License-Identifier: MIT
# Copyright (c) 2015-2025 Andrii Andrushchyshyn

from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent
from gui.Scaleform.framework.entities.DisposableEntity import EntityState

from ..events import g_eventsManager

__all__ = ('NetRadioBattleView', )

class NetRadioBattleViewMeta(BaseDAAPIComponent):

	def as_showMessageS(self, text, color, lifeTime):
		if self._isDAAPIInited():
			self.flashObject.as_showMessage(text, color, lifeTime)

	def destroy(self):
		if self.getState() != EntityState.CREATED:
			return
		super(NetRadioBattleViewMeta, self).destroy()

class NetRadioBattleView(NetRadioBattleViewMeta):

	def _populate(self):
		super(NetRadioBattleView, self)._populate()
		g_eventsManager.showBattleMessage += self.__showBattleMessage
		g_eventsManager.onDestroyBattle += self.destroy

	def _dispose(self):
		g_eventsManager.showBattleMessage -= self.__showBattleMessage
		g_eventsManager.onDestroyBattle -= self.destroy
		super(NetRadioBattleView, self)._dispose()

	def __showBattleMessage(self, message, color, lifetime):
		self.as_showMessageS(message, color, lifetime)
