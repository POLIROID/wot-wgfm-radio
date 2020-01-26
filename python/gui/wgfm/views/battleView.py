
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent
from gui.Scaleform.framework.entities.DisposableEntity import EntityState

from gui.wgfm.events import g_eventsManager

__all__ = ('WGFMBattleView', )

class WGFMBattleViewMeta(BaseDAAPIComponent):

	def as_showMessageS(self, text, color, lifeTime):
		if self._isDAAPIInited():
			self.flashObject.as_showMessage(text, color, lifeTime)

	def destroy(self):
		if self.getState() != EntityState.CREATED:
			return
		super(WGFMBattleViewMeta, self).destroy()

class WGFMBattleView(WGFMBattleViewMeta):

	def _populate(self):
		super(WGFMBattleView, self)._populate()
		g_eventsManager.showBattleMessage += self.__showBattleMessage
		g_eventsManager.onDestroyBattle += self.destroy

	def _dispose(self):
		g_eventsManager.showBattleMessage -= self.__showBattleMessage
		g_eventsManager.onDestroyBattle -= self.destroy
		super(WGFMBattleView, self)._dispose()

	def __showBattleMessage(self, message, color, lifetime):
		self.as_showMessageS(message, color, lifetime)
