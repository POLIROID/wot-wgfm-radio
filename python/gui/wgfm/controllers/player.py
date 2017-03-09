
import threading
import os
import subprocess
import urllib2
from xml.dom import minidom

import BigWorld
from debug_utils import LOG_ERROR, LOG_DEBUG, LOG_CURRENT_EXCEPTION

from gui.wgfm.data import g_dataHolder
from gui.wgfm.events import g_eventsManager
from gui.wgfm.lang import l10n
from gui.wgfm.controllers import g_controllers

from gui.wgfm.wgfm_constants import CONSOLE_PLAYER, PLAYER_COMMANDS, PLAYER_STATUS, TAGS_UPDATE_INTERVAL, USER_AGENT

__all__ = ('PlayerController', )

class PlayerController(object):
	
	status = property(lambda self: self.__get_status())
	errorLabel = property(lambda self: self.__errorLabel)
	tag = property(lambda self: self.__tag)
	channelName = property(lambda self: self.__channelName)
	channelIdx = property(lambda self: self.__currentChannel)
	
	def __init__(self):
		
		self.__status = PLAYER_STATUS.STOPPED
		self.__errorLabel = ''
		self.__tag = ''
		self.__channelName = ''
		self.__playerProcess = None
		self.__tagsCallback = None
		
		if g_dataHolder.settings.get('saveChannel', False):
			self.__currentChannel = g_dataHolder.settings.get('lastChannel', 0)
		else:
			self.__currentChannel = 0
	
	def init(self):

		def launch_player(data):
			self.__playerProcess = subprocess.Popen(data, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
			self.__executePlayerCommand(PLAYER_COMMANDS.INIT)
			self.__status = PLAYER_STATUS.INITED
			self.__executePlayerCommand(PLAYER_COMMANDS.VOLUME, g_controllers.volume.volume if not g_controllers.volume.muted else 0.0)
	
		data = [CONSOLE_PLAYER, '-pid', str(os.getpid())]
		threading.Thread(target=launch_player, args=(data, )).start()
		
		g_eventsManager.onVolumeChanged += self.__onVolumeChanged
		g_eventsManager.onChannelsUpdated += self.__onChannelsUpdated

	def fini(self):
		
		if self.__tagsCallback:
			BigWorld.cancelCallback(self.__tagsCallback)
			self.__tagsCallback = None
		
		g_eventsManager.onVolumeChanged -= self.__onVolumeChanged
		g_eventsManager.onChannelsUpdated -= self.__onChannelsUpdated

		self.__executePlayerCommand(PLAYER_COMMANDS.EXIT)
	
	def __onChannelsUpdated(self):
		data = list()
		for channel in g_controllers.channel.channels:
			if channel['availible']:
				data.append(channel['stream_url'])
	
		self.__executePlayerCommand(PLAYER_COMMANDS.ADD_CHANNELS, '##'.join(data))
	
	def playRadio(self, channelNum = None):
		
		g_controllers.channel.grabChannels()
		
		if not g_controllers.channel.inited:
			BigWorld.callback(0.1, lambda : self.playRadio(channelNum))
			return
		
		if channelNum is None:
			channelNum = self.channelIdx
		
		if g_dataHolder.settings.get('saveChannel', True):
			g_dataHolder.settings['lastChannel'] = channelNum
		
		LOG_DEBUG('playRadio - currentChannel: %s, newChannel: %s' % (self.channelIdx, channelNum))
		
		channel = g_controllers.channel.channels[channelNum]
		
		if not channel['availible']:
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
			
			g_controllers.rating.processRating(force = True, channelIdx = self.channelIdx)
			
			self.__currentChannel = channelIdx
			
			g_eventsManager.onRadioChannelChanged(channelIdx)
	
			if self.__status == PLAYER_STATUS.PLAYING:
				self.playRadio()
			
	def __executePlayerCommand(self, command, arg = None):
		if self.__playerProcess:
			self.__playerProcess.stdin.write(command + '\n')
			if arg is not None:
				self.__playerProcess.stdin.write(str(arg) + '\n')
			self.__playerProcess.stdin.flush()	
		else:
			BigWorld.callback(0.1, lambda : self.__executePlayerCommand(command, arg))
	
	def openExternal(self):
		try:
			channel = g_controllers.channel.channels[self.channelIdx]
			url = channel.get('ext_url', None)
			if url:
				BigWorld.wg_openWebBrowser(url)
		except:
			LOG_CURRENT_EXCEPTION()
	
	def __updateRadioTags(self):
		if self.__tagsCallback:
			BigWorld.cancelCallback(self.__tagsCallback)
			self.__tagsCallback = None
		self.__tagsCallback = BigWorld.callback(TAGS_UPDATE_INTERVAL, self.__updateRadioTags)
		threading.Thread(target=self.__getRadioTags).start()
		LOG_DEBUG('Updating tags')
	
	def __getRadioTags(self):
		try:
			channel = g_controllers.channel.channels[self.channelIdx]
			if channel.get('tags_url', None):
				request = urllib2.Request(channel.get('tags_url'))
				request.add_header('User-Agent', USER_AGENT)
				response = urllib2.urlopen(request, timeout = 5)				
				tags_xml = minidom.parse(response)
				response.close()
				tags_items = tags_xml.getElementsByTagName('ArtistTitle')
				if not tags_items:
					return
				tag_node = tags_items[0]
				if tag_node is not None and tag_node.childNodes:
					new_tag = tag_node.childNodes[0].data
					if new_tag != self.tag:												   
						self.__tag = new_tag
						g_eventsManager.onRadioTagChanged()
		except Exception as e:
			LOG_ERROR('PlayerController.__getRadioTags', e)
	
	def __get_status(self):
		if not g_controllers.channel.status:
			self.__status = PLAYER_STATUS.ERROR
			self.__errorLabel = l10n('#error_wgfm_url')
		return self.__status
	
	def __onVolumeChanged(self, volume):
		self.__executePlayerCommand(PLAYER_COMMANDS.VOLUME, volume if not g_controllers.volume.muted else 0.0)
