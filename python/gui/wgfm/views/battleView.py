
from gui.Scaleform.framework.entities.BaseDAAPIComponent import BaseDAAPIComponent

from gui.wgfm.events import g_eventsManager
from gui.wgfm.wgfm_constants import DEFAULT_BATTLE_MESSAGE_COLOR, DEFAULT_BATTLE_MESSAGE_LIFETIME

__all__ = ('WGFMBattleView', )

class WGFMBattleViewMeta(BaseDAAPIComponent):

	def as_showMessageS(self, text, color, lifeTime):
		if self._isDAAPIInited():
			self.flashObject.as_showMessage(text, color, lifeTime)

class WGFMBattleView(WGFMBattleViewMeta):
	
	def _populate(self):
		super(WGFMBattleView, self)._populate()
		g_eventsManager.showBattleMessage += self.__showBattleMessage
	
	def _dispose(self):
		g_eventsManager.showBattleMessage -= self.__showBattleMessage
		super(WGFMBattleView, self)._dispose()	   
	
	def __showBattleMessage(self, message, color = DEFAULT_BATTLE_MESSAGE_COLOR, lifetime = DEFAULT_BATTLE_MESSAGE_LIFETIME):
		self.as_showMessageS(message, color, lifetime)
	