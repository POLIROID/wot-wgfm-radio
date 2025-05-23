# SPDX-License-Identifier: MIT
# Copyright (c) 2015-2025 Andrii Andrushchyshyn

import random

import BigWorld

from debug_utils import LOG_DEBUG, LOG_ERROR, LOG_CURRENT_EXCEPTION
from gui.shared.personality import ServicesLocator
from gui.app_loader.settings import APP_NAME_SPACE
from gui.Scaleform.framework.managers.loaders import SFViewLoadParams
from messenger.m_constants import PROTO_TYPE
from messenger.proto import proto_getter

from ..events import g_eventsManager
from ..lang import l10n
from ..utils import parseKeyValueFull, getParentWindow
from .._constants import (PLAYER_STATUS, BROADCAST_INTERVAL, BATTLE_INJECTOR_UI,
									DEFAULT_BATTLE_MESSAGE_COLOR, DEFAULT_BATTLE_MESSAGE_LIFETIME)
from ..controllers import g_controllers
from ..data import g_dataHolder

__all__ = ('BattleController', )

class BattleController(object):

	@proto_getter(PROTO_TYPE.BW_CHAT2)
	def proto(self): #NOSONAR
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
			self.__showInfoMessage(l10n('battle.player.stop'))
		else:
			self.__showInfoMessage(g_controllers.player.tag, useChannel=True, important=True)

	def broadcastRadioTagMessage(self):
		try:
			if not self.__isPlayerInBattle:
				return
			if g_controllers.player.tag == '':
				self.__showInfoMessage(l10n('battle.player.stop'))
			else:
				if self.proto is None:
					self.__showInfoMessage(g_controllers.player.tag, useChannel=True, important=True)
				else:
					if BigWorld.time() - BROADCAST_INTERVAL > self.__lastBroadcastTime:
						self.__lastBroadcastTime = BigWorld.time()
						msg = l10n('battle.broadcast.track%s' % str(random.randint(1, 5))) % g_controllers.player.tag
						self.proto.arenaChat.broadcast(msg.encode('utf-8'), 0)
					else:
						self.__showInfoMessage(l10n('battle.tips.cooldown'))
		except: #NOSONAR
			LOG_ERROR('broadcastRadioTagMessage')
			LOG_CURRENT_EXCEPTION()

	def broadcastHelloMessage(self):
		try:
			if not self.__isPlayerInBattle:
				return
			if self.proto:
				if BigWorld.time() - BROADCAST_INTERVAL > self.__lastBroadcastTime:
					self.__lastBroadcastTime = BigWorld.time()
					msg = l10n('battle.broadcast.hello%s' % str(random.randint(1, 6)))
					self.proto.arenaChat.broadcast(msg.encode('utf-8'), 0)
				else:
					self.__showInfoMessage(l10n('battle.tips.cooldown'))
		except: #NOSONAR
			LOG_ERROR('broadcastHelloMessage')
			LOG_CURRENT_EXCEPTION()

	def showVolumeChangedMessage(self, isUP):
		if isUP:
			self.__showInfoMessage(l10n('battle.player.volumeup'))
		else:
			self.__showInfoMessage(l10n('battle.player.volumedown'))

	def showRatingsMessage(self):
		self.__showInfoMessage(l10n('battle.tips.rating'))

	def showControlsMessage(self):

		if g_controllers.player.status == PLAYER_STATUS.ERROR:
			self.__showInfoMessage(g_controllers.player.errorLabel)
			return

		if g_controllers.player.tag:
			self.__showInfoMessage(g_controllers.player.tag, useChannel=True, important=True)

		self.__showInfoMessage(l10n('battle.tips.control%s' % str(random.randint(1, 7))).format(
				playRadio=parseKeyValueFull(g_dataHolder.settings['keyBindings']['playRadio']),
				stopRadio=parseKeyValueFull(g_dataHolder.settings['keyBindings']['stopRadio']),
				nextChannel=parseKeyValueFull(g_dataHolder.settings['keyBindings']['nextChannel']),
				previosChannel=parseKeyValueFull(g_dataHolder.settings['keyBindings']['previosChannel']),
				volumeDown=parseKeyValueFull(g_dataHolder.settings['keyBindings']['volumeDown']),
				volumeUp=parseKeyValueFull(g_dataHolder.settings['keyBindings']['volumeUp']),
				dislikeCurrent=parseKeyValueFull(g_dataHolder.settings['keyBindings']['dislikeCurrent']),
				likeCurrent=parseKeyValueFull(g_dataHolder.settings['keyBindings']['likeCurrent'])
			), important=True)

	def __onShowBattlePage(self):

		self.__isPlayerInBattle = True
		app = ServicesLocator.appLoader.getApp(APP_NAME_SPACE.SF_BATTLE)
		if not app:
			return
		app.loadView(SFViewLoadParams(BATTLE_INJECTOR_UI, parent=getParentWindow()))

		self.__lastBroadcastTime = - BROADCAST_INTERVAL
		BigWorld.callback(1.0, self.showControlsMessage)

	def __onDestroyBattle(self):
		self.__isPlayerInBattle = False

	def __onRadioTagChanged(self):
		self.showRadioTagMessage()

	def __showInfoMessage(self, text, useChannel=False, important=False):
		LOG_DEBUG('showInfoMessage', self.__isPlayerInBattle, text, useChannel, important)
		color = DEFAULT_BATTLE_MESSAGE_COLOR
		message = '[NetRadio] %s' % text
		if important:
			lifeTime = DEFAULT_BATTLE_MESSAGE_LIFETIME + 2000
		else:
			lifeTime = DEFAULT_BATTLE_MESSAGE_LIFETIME
		g_eventsManager.showBattleMessage(message, color, lifeTime)
