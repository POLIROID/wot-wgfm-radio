# SPDX-License-Identifier: MIT
# Copyright (c) 2015-2025 Andrii Andrushchyshyn

import BigWorld
import Keys

from debug_utils import LOG_ERROR
from gui.Scaleform.framework.managers import context_menu
from gui.Scaleform.framework.managers.context_menu import AbstractContextMenuHandler
from messenger import MessengerEntry

from ..controllers import g_controllers
from ..data import g_dataHolder
from ..events import g_eventsManager
from ..lang import l10n
from ..utils import nextChannel, previosChannel, checkKeySet
from .._constants import HOTKEYS_COMMANDS, DEFAULT_BINDINGS, PLAYER_STATUS

__all__ = ('HotkeyController', )

class HotkeyController(object):

	@property
	def forced(self):
		return self.__forcedHandlers

	@property
	def accepting(self):
		return self.__isAccepting

	@property
	def acceptingName(self):
		return self.__acceptingHotkeyName

	def __init__(self):
		self.__isAccepting = False
		self.__acceptingHotkeyName = None
		self.__forcedHandlers = []

	def init(self):
		g_eventsManager.onKeyEvent += self.onKeyEvent

	def fini(self):
		g_eventsManager.onKeyEvent -= self.onKeyEvent
		self.__forcedHandlers = []

	def addForced(self, handler):
		if handler not in self.__forcedHandlers:
			self.__forcedHandlers.append(handler)

	def delForced(self, handler):
		if handler in self.__forcedHandlers:
			self.__forcedHandlers.remove(handler)

	def handleHotkeyUIEvent(self, command, name=None):
		if command == HOTKEYS_COMMANDS.START_ACCEPT:
			self.__acceptingHotkeyName = name
			self.__isAccepting = True
			g_eventsManager.onHotkeysChanged()
		elif command == HOTKEYS_COMMANDS.STOP_ACCEPT:
			self.__acceptingHotkeyName = None
			self.__isAccepting = False
			g_eventsManager.onHotkeysChanged()
		else:
			LOG_ERROR('unknown command', command)

	@staticmethod
	def defaultAll():
		g_dataHolder.settings['keyBindings'].update(DEFAULT_BINDINGS)
		g_eventsManager.onHotkeysChanged()

	@staticmethod
	def defaultCertain(name):
		value = DEFAULT_BINDINGS[name]
		g_dataHolder.settings['keyBindings'].update({name: value})
		g_eventsManager.onHotkeysChanged()

	@staticmethod
	def cleanCertain(name):
		value = []
		g_dataHolder.settings['keyBindings'].update({name: value})
		g_eventsManager.onHotkeysChanged()

	def onKeyEvent(self, event, alreadyHandled):

		if not event.isKeyDown() or MessengerEntry.g_instance.gui.isFocused():
			return

		if self.__isAccepting:
			self.processAccept(event)
			return

		keyBindings = g_dataHolder.settings['keyBindings']

		if g_controllers.player.status == PLAYER_STATUS.ERROR:
			return

		if not alreadyHandled:

			if checkKeySet(keyBindings['broadcastHello']):
				g_controllers.battle.broadcastHelloMessage()

			if checkKeySet(keyBindings['broadcastCurrent']):
				g_controllers.battle.broadcastRadioTagMessage()

			playing = g_controllers.player.status == PLAYER_STATUS.PLAYING

			if checkKeySet(keyBindings['likeCurrent']) and playing:
				g_controllers.rating.vote(True)

			if checkKeySet(keyBindings['dislikeCurrent']) and playing:
				g_controllers.rating.vote(False)

		if checkKeySet(keyBindings['previosChannel']):
			idx = previosChannel()
			if idx != -1:
				g_controllers.player.setChannel(idx)

		if checkKeySet(keyBindings['nextChannel']):
			idx = nextChannel()
			if idx != -1:
				g_controllers.player.setChannel(idx)

		if checkKeySet(keyBindings['playRadio']):
			if g_controllers.player.status == PLAYER_STATUS.PLAYING:
				g_controllers.battle.showRadioTagMessage()
			else:
				g_controllers.player.playRadio(g_controllers.player.channelIdx)

		if checkKeySet(keyBindings['stopRadio']):
			g_controllers.player.stopRadio()

		if checkKeySet(keyBindings['volumeDown']) and g_controllers.volume.volumeDown():
			g_controllers.battle.showVolumeChangedMessage(False)

		if checkKeySet(keyBindings['volumeUp']) and g_controllers.volume.volumeUp():
			g_controllers.battle.showVolumeChangedMessage(True)

	def processAccept(self, event):

		if event.key == Keys.KEY_ESCAPE:
			self.__isAccepting = False
			self.__acceptingHotkeyName = None
			g_eventsManager.onHotkeysChanged()
			return

		notAllowed = [Keys.KEY_NULL, Keys.KEY_LCONTROL, Keys.KEY_LSHIFT, Keys.KEY_LALT, Keys.KEY_RCONTROL,
					Keys.KEY_RSHIFT, Keys.KEY_RALT, Keys.KEY_CAPSLOCK, Keys.KEY_RETURN, Keys.KEY_MOUSE0,
					Keys.KEY_LEFTMOUSE, Keys.KEY_MOUSE1, Keys.KEY_RIGHTMOUSE, Keys.KEY_MOUSE2, Keys.KEY_MIDDLEMOUSE]

		if event.key in notAllowed:
			return

		newKeySet = [event.key]

		if BigWorld.isKeyDown(Keys.KEY_LCONTROL) or BigWorld.isKeyDown(Keys.KEY_RCONTROL):
			newKeySet.append([Keys.KEY_LCONTROL, Keys.KEY_RCONTROL])
		elif BigWorld.isKeyDown(Keys.KEY_LALT) or BigWorld.isKeyDown(Keys.KEY_RALT):
			newKeySet.append([Keys.KEY_LALT, Keys.KEY_RALT])
		elif BigWorld.isKeyDown(Keys.KEY_LSHIFT) or BigWorld.isKeyDown(Keys.KEY_RSHIFT):
			newKeySet.append([Keys.KEY_LSHIFT, Keys.KEY_RSHIFT])

		for keySetValue in g_dataHolder.settings["keyBindings"].values():
			if keySetValue == newKeySet:
				return

		g_dataHolder.settings["keyBindings"].update({self.__acceptingHotkeyName: newKeySet})
		self.__isAccepting = False
		self.__acceptingHotkeyName = None
		g_eventsManager.onHotkeysChanged()

class HotkeyContextHandler(AbstractContextMenuHandler):

	def __init__(self, cmProxy, ctx=None):
		self._controlName = None
		super(HotkeyContextHandler, self).__init__(cmProxy, ctx, handlers={
			'setValueToEmpty': 'setValueToEmpty',
			'setValueToDefault': 'setValueToDefault'
		})

	def _initFlashValues(self, ctx):
		self._controlName = ctx.controlName

	def _clearFlashValues(self):
		self._controlName = None

	def setValueToEmpty(self):
		if self._controlName:
			g_controllers.hotkey.cleanCertain(self._controlName)

	def setValueToDefault(self):
		if self._controlName:
			g_controllers.hotkey.defaultCertain(self._controlName)

	def _generateOptions(self, ctx=None):
		return [
			self._makeItem('setValueToEmpty', l10n('ui.hotkeys.cmdClean'), None),
			self._makeItem('setValueToDefault', l10n('ui.hotkeys.cmdDefault'), None)
		]

context_menu.registerHandlers(('NetRadioHotkeyContextHandler', HotkeyContextHandler))
