from adisp import async, process
from debug_utils import LOG_DEBUG

from gui.wgfm.data import g_dataHolder
from gui.wgfm.events import g_eventsManager
from gui.wgfm.utils import fetchURL
from gui.wgfm.wgfm_constants import USER_AGENT

__all__ = ('ChannelController', )

class ChannelController(object):

	@property
	def channels(self):
		return self.__channels

	@property
	def status(self):
		return self.__status

	@property
	def inited(self):
		return self.__inited

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
			self.__channelsStatusGrabber()

	@process
	def __channelsStatusGrabber(self):
		yield g_dataHolder.initConfigOnStart()
		channels = g_dataHolder.config.get('channels', [])
		statuses = yield map(self.__channelStatus, [channel.get('stream_url') for channel in channels])
		for idx, channel in enumerate(channels):
			available = statuses[idx]
			channel['available'] = available
			if available:
				self.__channels.append(channel)
		self.__status = bool(self.__channels)
		self.__inited = True
		g_eventsManager.onChannelsUpdated()

	@async
	@process
	def __channelStatus(self, url, callback=None):
		LOG_DEBUG('channelStatus', url, self.__status)
		status, _ = yield lambda callback: fetchURL(url=url, callback=callback, timeout=5.0, \
										headers={'User-Agent': USER_AGENT}, onlyResponceStatus=True)
		callback(status)
