
import BigWorld
from debug_utils import LOG_ERROR, LOG_NOTE
from messenger.m_constants import PROTO_TYPE
from messenger.proto import proto_getter
import random
from gui.app_loader.loader import g_appLoader

__all__ = ('BattleController', )

from gui.wgfm.events import g_eventsManager
from gui.wgfm.lang import l10n
from gui.wgfm.utils import getChannelName, parseKeyValueFull
from gui.wgfm.wgfm_constants import PLAYER_STATUS, BROADCAST_INTERVAL, WGFM_BATTLE_INJECTOR_UI, DEFAULT_BATTLE_MESSAGE_COLOR, DEFAULT_BATTLE_MESSAGE_LIFETIME
from gui.wgfm.controllers import g_controllers
from gui.wgfm.data import g_dataHolder

class BattleController(object):
	
	@proto_getter(PROTO_TYPE.BW_CHAT2)
	def proto(self):
		return None
	
	def __init__(self):
		
		# last broadcast into ingame battle chat time
		# using foor cooldown system
		self.__lastBroadcastTime = -BROADCAST_INTERVAL
		
		# player inbattle indicator
		self.__isPlayerInBattle = False
	
	def init(self):
		g_eventsManager.onRadioTagChanged += self.__onRadioTagChanged
		g_eventsManager.onShowBattlePage += self.__onShowBattlePage
		g_eventsManager.onDestroyBattle += self.__onDestroyBattle
	
	def fini(self):
		g_eventsManager.onRadioTagChanged -= self.__onRadioTagChanged
		g_eventsManager.onShowBattlePage -= self.__onShowBattlePage
		g_eventsManager.onDestroyBattle -= self.__onDestroyBattle

	def showRadioTagMessage(self):
		"""fired on player tag changed"""
		if g_controllers.player.tag == '':
			self.__showInfoMessage(l10n('#battle_player_stop'))
		else:			
			self.__showInfoMessage(g_controllers.player.tag, useChannel=True, important=True)
		
	def broadcastRadioTagMessage(self):
		try:
			if not self.__isPlayerInBattle:
				return
			if g_controllers.player.tag == '':
				self.__showInfoMessage(l10n('#battle_player_stop'))
			else:
				if self.proto is None:
					self.__showInfoMessage(g_controllers.player.tag, useChannel=True, important=True)
				else:
					if BigWorld.time() - BROADCAST_INTERVAL > self.__lastBroadcastTime:
						self.__lastBroadcastTime = BigWorld.time()
						msg = l10n('#battle_broadcast_track_%s' % str(random.randint(1, 5))) % g_controllers.player.tag
						self.proto.arenaChat.broadcast(msg.encode('utf-8'), 0)
					else:
						self.__showInfoMessage(l10n('#battle_tips_cooldown'))
		except Exception as e:
			LOG_ERROR('broadcastRadioTagMessage',e)
	
	def broadcastHelloMessage(self):
		try:
			if not self.__isPlayerInBattle:
				return
			if self.proto:
				if BigWorld.time() - BROADCAST_INTERVAL > self.__lastBroadcastTime:
					self.__lastBroadcastTime = BigWorld.time()
					msg = l10n('#battle_broadcast_hello_%s' % str(random.randint(1, 4)))
					self.proto.arenaChat.broadcast(msg.encode('utf-8'), 0)
				else:
					self.__showInfoMessage(l10n('#battle_tips_cooldown'))
		except Exception as e:
			LOG_ERROR('broadcastHelloMessage',e)
	
	def showVolumeChangedMessage(self, isUP):
		if isUP:
			self.__showInfoMessage(l10n('#battle_player_volumeup'))
		else:
			self.__showInfoMessage(l10n('#battle_player_volumedown'))
	
	def showRatingsMessage(self):
		self.__showInfoMessage(l10n('#battle_tips_rating'))
	
	def showControlsMessage(self):
		
		if g_controllers.player.status == PLAYER_STATUS.ERROR:
			self.__showInfoMessage(g_controllers.player.error_label)
			return
		
		if g_controllers.player.tag != '':
			self.__showInfoMessage(g_controllers.player.tag, useChannel=True, important=True)
			
		self.__showInfoMessage(l10n('#battle_tips_control_%s' % str(random.randint(1, 8))).format(
				playRadio = parseKeyValueFull(g_dataHolder.settings['keyBindings']['playRadio']), 
				stopRadio = parseKeyValueFull(g_dataHolder.settings['keyBindings']['stopRadio']),
				nextChannel = parseKeyValueFull(g_dataHolder.settings['keyBindings']['nextChannel']),
				previosChannel = parseKeyValueFull(g_dataHolder.settings['keyBindings']['previosChannel']),
				volumeDown = parseKeyVparseKeyValueFullalue(g_dataHolder.settings['keyBindings']['volumeDown']),
				volumeUp = parseKeyValueFull(g_dataHolder.settings['keyBindings']['volumeUp']),
				dislikeCurrent = parseKeyValueFull(g_dataHolder.settings['keyBindings']['dislikeCurrent']),
				likeCurrent = parseKeyValueFull(g_dataHolder.settings['keyBindings']['likeCurrent'])
			), important=True)
	
	def __onShowBattlePage(self):
		
		self.__isPlayerInBattle = True
		
		g_appLoader.getDefBattleApp().loadView(WGFM_BATTLE_INJECTOR_UI)
		
		self.__lastBroadcastTime = - BROADCAST_INTERVAL
		BigWorld.callback(1.0, self.showControlsMessage)
	
	def __onDestroyBattle(self):
		
		self.__isPlayerInBattle = False

	def __onRadioTagChanged(self):
		self.showRadioTagMessage()
	
	def __showInfoMessage(self, text, useChannel = False, important = False):
		LOG_NOTE('__showInfoMessage', text, useChannel, important)
		color = DEFAULT_BATTLE_MESSAGE_COLOR
		
		if useChannel:
			message = '[WGFM-%s] %s' % (getChannelName(), text)
		else:
			message = '[WGFM] %s' % text
		
		if important:
			lifeTime = DEFAULT_BATTLE_MESSAGE_LIFETIME + 2000
		else:
			lifeTime = DEFAULT_BATTLE_MESSAGE_LIFETIME
		
		g_eventsManager.showBattleMessage(message, color, lifeTime)
	