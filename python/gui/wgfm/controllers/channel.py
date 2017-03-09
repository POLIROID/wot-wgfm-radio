
import threading
import urllib2
from debug_utils import LOG_DEBUG, LOG_ERROR

from gui.wgfm.data import g_dataHolder
from gui.wgfm.events import g_eventsManager
from gui.wgfm.controllers import g_controllers
from gui.wgfm.wgfm_constants import USER_AGENT

__all__ = ('ChannelController', )

class ChannelController(object):
	
	channels = property(lambda self: self.__channels)
	status = property(lambda self: self.__status)
	inited = property(lambda self: self.__inited)

	def __init__(self):
		self.__channels = list()
		self.__status = True
		self.__initStarted = False
		self.__inited = False
	
	def init(self):
		pass

	def fini(self):
		pass

	def grabChannels(self):
		if not self.__initStarted:
			self.__initStarted = True
			threading.Thread(target=self.__grabber).start()
	
	def __grabber(self):
		try:
			
			g_dataHolder.init_config_onstart()
			channels = g_dataHolder.config.get('channels')
			LOG_DEBUG('Checking channels: %s' % str(channels))
			availibleChannels = 0
			for channel in channels:
				LOG_DEBUG('Checking channel: %s' % str(channel.get('displayName')))
				availible = self.__checkChannelUrl(channel.get('stream_url'))
				channel['availible'] = availible
				if availible:
					availibleChannels += 1
				self.__channels.append(channel)
			
			self.__status = bool(availibleChannels)
			self.__inited = True
			
			g_eventsManager.onChannelsUpdated()

		except Exception as e:
			LOG_ERROR('ChannelsController.grabber', e)
	
	def __checkChannelUrl(self, url):
		LOG_DEBUG('Checking channel url: %s' % str(url))
		try:
			if url:
				request = urllib2.Request(url)			
				request.add_header('User-Agent', USER_AGENT)
				response = urllib2.urlopen(request, timeout = 1.0)
				response.close()
				if response.msg == 'OK':
					return True
				else:
					return False
			else:
				return False
		except Exception as e:
			LOG_ERROR('ChannelsController.__checkChannelUrl', e)
			return False
	
