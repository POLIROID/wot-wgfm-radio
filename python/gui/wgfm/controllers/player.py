import os
import subprocess
import threading
from xml.dom import minidom

import BigWorld
from adisp import async, process
from debug_utils import LOG_DEBUG, LOG_WARNING
from gui.wgfm.controllers import g_controllers
from gui.wgfm.data import g_dataHolder
from gui.wgfm.events import g_eventsManager
from gui.wgfm.lang import l10n
from gui.wgfm.utils import fetchURL
from gui.wgfm.wgfm_constants import CONSOLE_PLAYER, PLAYER_COMMANDS, PLAYER_STATUS, TAGS_UPDATE_INTERVAL, USER_AGENT

__all__ = ('PlayerController', )

class PlayerController(object):

	@property
	def channelName(self):
		return self.__channelName

	@property
	def channelIdx(self):
		return self.__currentChannel

	@property
	def tag(self):
		return self.__tag

	@property
	def status(self):
		if not g_controllers.channel.status:
			self.errorLabel = l10n('error.wgfmUrl')
		return self.__status

	@property
	def errorLabel(self):
		return self.__errorLabel

	@errorLabel.setter
	def set_errorLebel(self, errorLabel):
		if not self.__errorLabel:
			self.__status = PLAYER_STATUS.ERROR
			self.__errorLabel = errorLabel
			g_eventsManager.onRadioStatusUpdated()

	def __init__(self):
		self.__status = PLAYER_STATUS.STOPPED
		self.__tag = ''
		self.__errorLabel = None
		self.__channelName = ''
		self.__playerProcess = None
		self.__tagsCallback = None
		if g_dataHolder.settings.get('saveChannel', False):
			self.__currentChannel = g_dataHolder.settings.get('lastChannel', 0)
		else:
			self.__currentChannel = 0

	def init(self):

		def launch_player(data):
			# starting player process
			self.__playerProcess = subprocess.Popen(data, stdout=subprocess.PIPE, stdin=subprocess.PIPE,
													stderr=subprocess.PIPE, shell=True)
			# initing player
			self.__executePlayerCommand(PLAYER_COMMANDS.INIT)
			# updating status
			self.__status = PLAYER_STATUS.INITED
			# setting volume
			volume = 0.0
			if not g_controllers.volume.muted:
				volume = g_controllers.volume.volume
			self.__executePlayerCommand(PLAYER_COMMANDS.VOLUME, volume)

		data = [CONSOLE_PLAYER, '-pid', str(os.getpid())]
		threading.Thread(target=launch_player, args=(data, )).start()

		g_eventsManager.onVolumeChanged += self.__onVolumeChanged
		g_eventsManager.onVolumeChangedHidden += self.__onVolumeChanged
		g_eventsManager.onChannelsUpdated += self.__onChannelsUpdated

		if g_dataHolder.settings.get('autoPlay', False):
			self.playRadio()

	def fini(self):

		if self.__tagsCallback:
			BigWorld.cancelCallback(self.__tagsCallback)
			self.__tagsCallback = None

		g_eventsManager.onVolumeChanged -= self.__onVolumeChanged
		g_eventsManager.onVolumeChangedHidden += self.__onVolumeChanged
		g_eventsManager.onChannelsUpdated -= self.__onChannelsUpdated

		self.__executePlayerCommand(PLAYER_COMMANDS.EXIT)

	def __onChannelsUpdated(self):
		data = list()
		for channel in g_controllers.channel.channels:
			if channel['available']:
				data.append(channel['stream_url'])

		self.__executePlayerCommand(PLAYER_COMMANDS.ADD_CHANNELS, '##'.join(data))

	def playRadio(self, channelNum=None):

		g_controllers.channel.grabChannels()

		if not g_controllers.channel.inited:
			BigWorld.callback(0.1, lambda: self.playRadio(channelNum))
			return

		if channelNum is None:
			channelNum = self.channelIdx

		if g_dataHolder.settings.get('saveChannel', True):
			g_dataHolder.settings['lastChannel'] = channelNum

		channel = g_controllers.channel.channels[channelNum]

		if not channel['available']:
			return

		self.__executePlayerCommand(PLAYER_COMMANDS.PLAY, channelNum)

		self.__status = PLAYER_STATUS.PLAYING
		self.__tag = channel.get('displayName')
		self.__channelName = channel.get('displayName')

		g_eventsManager.onRadioStatusUpdated()

		self.__updateRadioTags()

	def stopRadio(self):

		self.__executePlayerCommand(PLAYER_COMMANDS.STOP)

		self.__status = PLAYER_STATUS.STOPPED
		self.__tag = ''

		if self.__tagsCallback:
			BigWorld.cancelCallback(self.__tagsCallback)
			self.__tagsCallback = None

		g_eventsManager.onRadioTagChanged()
		g_eventsManager.onRadioStatusUpdated()

	def setChannel(self, channelIdx):
		if channelIdx != self.__currentChannel:
			g_controllers.rating.syncRatings(force=True, channelIdx=self.channelIdx)
			self.__currentChannel = channelIdx
			g_eventsManager.onRadioChannelChanged(channelIdx)
			if self.__status == PLAYER_STATUS.PLAYING:
				self.playRadio()

	def __executePlayerCommand(self, command, arg=None):
		if self.__playerProcess:
			self.__playerProcess.stdin.write(command + '\n')
			if arg is not None:
				self.__playerProcess.stdin.write(str(arg) + '\n')
			self.__playerProcess.stdin.flush()
		else:
			BigWorld.callback(0.1, lambda: self.__executePlayerCommand(command, arg))

	def openExternal(self):
		channel = g_controllers.channel.channels[self.channelIdx]
		url = channel.get('ext_url', None)
		if url:
			BigWorld.wg_openWebBrowser(url)

	def __onVolumeChanged(self, volume):
		self.__executePlayerCommand(PLAYER_COMMANDS.VOLUME, volume if not g_controllers.volume.muted else 0.0)

	def __updateRadioTags(self):
		if self.__tagsCallback:
			BigWorld.cancelCallback(self.__tagsCallback)
			self.__tagsCallback = None
		self.__tagsCallback = BigWorld.callback(TAGS_UPDATE_INTERVAL, self.__updateRadioTags)
		self.__grabChannelTag()

	@process
	def __grabChannelTag(self):
		tagUrl = g_controllers.channel.channels[self.channelIdx].get('tags_url', None)
		if not tagUrl:
			return
		successful, parsedTag = yield self.__parseChannelTag(tagUrl)
		if successful and parsedTag != self.tag:
			self.__tag = parsedTag
			g_eventsManager.onRadioTagChanged()

	@async
	@process
	def __parseChannelTag(self, url, callback=None):
		LOG_DEBUG('parseChannelTag', url, self.__tag)
		status, data = yield lambda callback: fetchURL(url=url, callback=callback, timeout=5.0,
										headers={'User-Agent': USER_AGENT})
		parsedTag = None
		if status:
			try:
				tagsXml = minidom.parseString(data)
				tagsItems = tagsXml.getElementsByTagName('ArtistTitle')
				if tagsItems:
					tagNode = tagsItems[0]
					if tagNode is not None and tagNode.childNodes:
						parsedTag = tagNode.childNodes[0].data
			except: #NOSONAR
				LOG_WARNING('__parseChannelTag', 'cant parse data')
				status = False
		callback((status, parsedTag))
