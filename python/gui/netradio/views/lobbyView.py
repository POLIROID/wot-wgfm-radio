import BigWorld
import GUI
import Keys
from debug_utils import *

from gui.Scaleform.framework.entities.abstract.AbstractViewMeta import AbstractViewMeta
from gui.Scaleform.framework.entities.View import View
from gui.shared.view_helpers.blur_manager import CachedBlur
from frameworks.wulf import WindowLayer
from gui.netradio.events import g_eventsManager
from gui.netradio.controllers import g_controllers
from gui.netradio.data import g_dataHolder
from gui.netradio.utils import getCurrentChannelIdx, parseKeyValue, parseKeyModifiers
from gui.netradio.lang import l10n
from gui.netradio._constants import PLAYER_STATUS, UI_VOLUME_MULTIPLIYER

__all__ = ('NetRadioLobbyView', )

class NetRadioLobbyViewMeta(View, AbstractViewMeta):

	def as_showWaitingS(self, message):
		if self._isDAAPIInited():
			return self.flashObject.as_showWaiting(message)

	def as_hideWaitingS(self):
		if self._isDAAPIInited():
			return self.flashObject.as_hideWaiting()

	def as_setLocalizationS(self, ctx):
		"""ctx represented by LocalizationVO"""
		if self._isDAAPIInited():
			return self.flashObject.as_setLocalization(ctx)

	def as_setStateS(self, ctx):
		"""ctx represented by StateVO"""
		if self._isDAAPIInited():
			return self.flashObject.as_setState(ctx)

	def as_setSettingsS(self, ctx):
		"""ctx represented by SettingsVO"""
		if self._isDAAPIInited():
			return self.flashObject.as_setSettings(ctx)

	def as_setHotkeysS(self, ctx):
		"""ctx represented by HotKeysVO"""
		if self._isDAAPIInited():
			return self.flashObject.as_setHotkeys(ctx)

	def as_setChannelsS(self, ctx):
		if self._isDAAPIInited():
			return self.flashObject.as_setChannels(ctx)

class NetRadioLobbyView(NetRadioLobbyViewMeta):

	def _populate(self):

		super(NetRadioLobbyView, self)._populate()

		self._blur = CachedBlur(enabled=True, ownLayer=WindowLayer.OVERLAY - 1)

		if not g_controllers.channel.inited:
			g_controllers.channel.grabChannels()

		# localization
		self.as_setLocalizationS(self.__generateLocalizationCtx())

		# settings
		self.as_setSettingsS(self.__generateSettingsCtx())

		# update hotkeys
		self.as_setHotkeysS(self.__generateHotkeysCtx())

		# process depended Data with waiting
		self.as_showWaitingS(l10n('ui.waiting.grabbingData'))

		self._dependedData()

	def _dispose(self):
		g_eventsManager.onRadioChannelChanged -= self.__onRadioChannelChanged
		g_eventsManager.onRadioTagChanged -= self.__onRadioTagChanged
		g_eventsManager.onVolumeChanged -= self.__onVolumeChanged
		g_eventsManager.onRatingsUpdated -= self.__onRatingsUpdated
		g_eventsManager.onHotkeysChanged -= self.__onHotkeysChanged

		if g_controllers.hotkey:
			g_controllers.hotkey.delForced(self.__forcesKeyEventHandler)

		self._blur.fini()

		super(NetRadioLobbyView, self)._dispose()

	def _dependedData(self):

		# wait while data been processed
		if not g_controllers.channel.inited:
			BigWorld.callback(0.1, self._dependedData)
			return

		# depended data synced, hide waiting
		self.as_hideWaitingS()

		# update channels list
		self.as_setChannelsS(self.__generateChannelsCtx())

		# update states
		self.as_setStateS(self.__generateStateCtx())

		# subscribe to chage state on events
		g_eventsManager.onRadioChannelChanged += self.__onRadioChannelChanged
		g_eventsManager.onRadioTagChanged += self.__onRadioTagChanged
		g_eventsManager.onVolumeChanged += self.__onVolumeChanged
		g_eventsManager.onRatingsUpdated += self.__onRatingsUpdated
		g_eventsManager.onHotkeysChanged += self.__onHotkeysChanged
		g_controllers.hotkey.addForced(self.__forcesKeyEventHandler)

	def onFocusIn(self, *args):
		if self._isDAAPIInited():
			return False

	def closeView(self):
		"""fired by AS CloseButton click or ESC key press"""
		if g_controllers.hotkey.accepting:
			return
		self.destroy()

	def radioPause(self):
		"""fired by AS PauseButton click"""
		g_controllers.player.stopRadio()

	def radioPlay(self):
		"""fired by AS PlayButton click"""
		g_controllers.player.playRadio()

	def updateVolume(self, volume):
		"""fired by AS VolumeSlider value change"""
		if volume > 0:
			volume = volume / UI_VOLUME_MULTIPLIYER
		volume = round(volume, 2)
		g_controllers.volume.setVolume(volume)

	def updateMuted(self):
		"""fired by AS VolumeButton click"""
		g_controllers.volume.setMuted()

	def updateChannel(self, channelIdx):
		"""fired by AS ChannelsDropDown item select"""
		channelIdx = int(channelIdx)
		g_controllers.player.setChannel(channelIdx)

	def updateRating(self, liked):
		"""fired by AS like or dislike button"""
		g_controllers.rating.vote(liked)

	def updateSettings(self, name, value):
		"""fired on AS settings section values changed"""
		if name in g_dataHolder.settings:
			g_dataHolder.settings.update({name: value})

	def updateHotkeys(self, name, command):
		"""fired on AS hotkeys section by Hotkey control"""
		g_controllers.hotkey.handleHotkeyUIEvent(command, name)

	def defaultHotkeys(self):
		"""fired on AS hotkeys section SetDefaultButton click"""
		g_controllers.hotkey.defaultAll()

	def openExternal(self):
		"""fired by AS StationName click"""
		g_controllers.player.openExternal()

	def __onVolumeChanged(self, volume):
		"""sync volume states"""
		return self.as_setStateS(self.__generateStateCtx())

	def __onRadioTagChanged(self):
		"""sync current composition name"""
		return self.as_setStateS(self.__generateStateCtx())

	def __onRadioChannelChanged(self, _):
		"""sync current channel ID"""
		return self.as_setStateS(self.__generateStateCtx())

	def __onRatingsUpdated(self):
		"""sync rating buttons states"""
		return self.as_setStateS(self.__generateStateCtx())

	def __onHotkeysChanged(self):
		"""sync hotskeys settings"""
		return self.as_setHotkeysS(self.__generateHotkeysCtx())

	def __forcesKeyEventHandler(self, event):
		if event.isKeyDown() and event.key == Keys.KEY_ESCAPE and not g_controllers.hotkey.accepting:
			BigWorld.callback(0, self.closeView)
			return True
		return False

	def __generateLocalizationCtx(self):
		"""result represented by LocalizationVO"""
		return {'closeButton': l10n('ui.closeButton'), 'settingsTitle': l10n('ui.settings.title'),
				'titleLabel': l10n('ui.title'), 'hotkeysTitle': l10n('ui.hotkeys.title'),
				'hotkeysDefault': l10n('ui.hotkeys.defaultLink')}

	def __generateStateCtx(self):
		"""result represented by StateVO"""
		player = g_controllers.player
		playing = player.status == PLAYER_STATUS.PLAYING
		isError = player.status == PLAYER_STATUS.ERROR
		volume = round(g_controllers.volume.volume * UI_VOLUME_MULTIPLIYER, 2)
		tag = player.errorLabel if player.status == PLAYER_STATUS.ERROR else player.tag
		likeButtonStatus, dislikeButtonStatus = g_controllers.rating.buttonsState
		return {'isPlaying': playing, 'isMuted': g_controllers.volume.muted, 'currentVolume': volume,
				'currentChannelIdx': getCurrentChannelIdx(), 'currentCompositionName': tag, 'isError': isError,
				'likeButtonStatus': likeButtonStatus, 'dislikeButtonStatus': dislikeButtonStatus}

	def __generateHotkeysCtx(self):
		"""result represented by HotKeysVO"""
		hotkeys = []
		keySetNames = ['playRadio', 'stopRadio', 'volumeUp', 'volumeDown', 'nextChannel', 'previosChannel',
				 	 'likeCurrent', 'dislikeCurrent', 'broadcastCurrent', 'broadcastHello']

		for keySetName in keySetNames:
			keySetData = g_dataHolder.settings['keyBindings'].get(keySetName, [])
			keyValue = parseKeyValue(keySetData)
			keyHasAlt, keyHasCtrl, keyHasShift = parseKeyModifiers(keySetData)
			isAccepting = g_controllers.hotkey.accepting and g_controllers.hotkey.acceptingName == keySetName
			hotkeys.append({'name': keySetName, 'label': l10n('ui.hotkeys.%s' % keySetName), 'value': keyValue,
					 'modifierCtrl': keyHasCtrl, 'modiferShift': keyHasShift, 'modifierAlt': keyHasAlt,
					 'isEmpty': not keySetData, 'isAccepting': isAccepting})
		return {'hotkeys': hotkeys}

	def __generateSettingsCtx(self):
		"""result represented by SettingsVO"""
		settings = []
		settingsFields = ['saveVolume', 'saveChannel', 'muteOnVoip', 'autoPlay', 'sendStatistic',
							'showBattleTips', 'muteOnMinimize']
		for settingName in settingsFields:
			value = g_dataHolder.settings.get(settingName, False)
			localName = l10n('ui.settings.label.%s' % settingName)
			localTooltip = l10n('ui.settings.tooltip.%s' % settingName)
			settings.append({'name': settingName, 'value': value, 'label': localName, 'tooltip': localTooltip})
		return {'settings': settings}

	def __generateChannelsCtx(self):
		channels = []
		for channelIdx, channelData in enumerate(g_controllers.channel.channels):
			channels.append({'data': channelIdx, 'label': channelData['displayName'],
							'enabled': channelData['available']})
		return {'channels': channels}
