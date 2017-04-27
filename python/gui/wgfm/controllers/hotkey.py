
import BigWorld
import Keys
from debug_utils import LOG_ERROR
from messenger import MessengerEntry

from gui.wgfm.data import g_dataHolder
from gui.wgfm.events import g_eventsManager
from gui.wgfm.controllers import g_controllers
from gui.wgfm.utils import nextChannel, previosChannel, checkKeySet
from gui.wgfm.wgfm_constants import HOTKEYS_COMMANDS, DEFAULT_BINDINGS, PLAYER_STATUS

__all__ = ('HotkeyController', )

class HotkeyController(object):
	
	forced = property(lambda self: self.__forcedHandlers)
	accepting = property(lambda self: self.__isAccepting)
	acceptingName = property(lambda self: self.__acceptingHotkeyName)

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
	
	def handleHotkeyUIEvent(self, command, name = None):
		if command == HOTKEYS_COMMANDS.START_ACCEPT:
			self.__acceptingHotkeyName = name
			self.__isAccepting = True
			g_eventsManager.onHotkeysChanged()
		elif command == HOTKEYS_COMMANDS.STOP_ACCEPT:
			self.__acceptingHotkeyName = None
			self.__isAccepting = False
			g_eventsManager.onHotkeysChanged()
		elif command == HOTKEYS_COMMANDS.DEFAULT:
			self.defaultCertain(name)
		elif command == HOTKEYS_COMMANDS.CLEAN:
			self.cleanCertain(name)
		else:
			LOG_ERROR('unknown command', command)
	
	def defaultAll(self):
		g_dataHolder.settings['keyBindings'].update(DEFAULT_BINDINGS)
		g_eventsManager.onHotkeysChanged()
	
	def defaultCertain(self, name):
		value = DEFAULT_BINDINGS[name]
		g_dataHolder.settings['keyBindings'].update( { name: value } )
		g_eventsManager.onHotkeysChanged()
	
	def cleanCertain(self, name):
		value = []
		g_dataHolder.settings['keyBindings'].update( { name: value } )
		g_eventsManager.onHotkeysChanged()
	
	def onKeyEvent(self, event, prevresult):
		
		if not event.isKeyDown() or MessengerEntry.g_instance.gui.isFocused():
			return
	
		if self.__isAccepting:
			self.processAccept(event)
			return
		
		keyBindings = g_dataHolder.settings['keyBindings']

		if g_controllers.player.status == PLAYER_STATUS.ERROR:
			return
		
		if checkKeySet(keyBindings['broadcastHello']):
			g_controllers.battle.broadcastHelloMessage()
		
		if checkKeySet(keyBindings['broadcastCurrent']):
			g_controllers.battle.broadcastRadioTagMessage()
		
		if checkKeySet(keyBindings['likeCurrent']):
			if g_controllers.player.status == PLAYER_STATUS.PLAYING:
				g_controllers.rating.vote(True)
		
		if checkKeySet(keyBindings['dislikeCurrent']):
			if g_controllers.player.status == PLAYER_STATUS.PLAYING:
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
				
		if checkKeySet(keyBindings['volumeDown']):
			if g_controllers.volume.volumeDown():
				g_controllers.battle.showVolumeChangedMessage(False)
		
		if checkKeySet(keyBindings['volumeUp']):
			if g_controllers.volume.volumeUp():
				g_controllers.battle.showVolumeChangedMessage(True)		

	def processAccept(self, event):
		
		if event.key == Keys.KEY_ESCAPE:
			self.__isAccepting = False
			self.__acceptingHotkeyName = None
			g_eventsManager.onHotkeysChanged()
			return
		
		notAllowed = [ Keys.KEY_NULL, Keys.KEY_LCONTROL, Keys.KEY_LSHIFT, Keys.KEY_LALT, Keys.KEY_RCONTROL, \
					Keys.KEY_RSHIFT, Keys.KEY_RALT, Keys.KEY_CAPSLOCK, Keys.KEY_RETURN, Keys.KEY_MOUSE0, \
					Keys.KEY_LEFTMOUSE, Keys.KEY_MOUSE1, Keys.KEY_RIGHTMOUSE, Keys.KEY_MOUSE2, Keys.KEY_MIDDLEMOUSE ]
		
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

		g_dataHolder.settings["keyBindings"].update( { self.__acceptingHotkeyName: newKeySet } )
		self.__isAccepting = False
		self.__acceptingHotkeyName = None
		g_eventsManager.onHotkeysChanged()
