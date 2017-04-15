
import time
from urllib import urlencode

from adisp import async, process
from debug_utils import LOG_ERROR, LOG_DEBUG, LOG_CURRENT_EXCEPTION
from PlayerEvents import g_playerEvents

from gui.wgfm.controllers import g_controllers
from gui.wgfm.data import g_dataHolder
from gui.wgfm.events import g_eventsManager
from gui.wgfm.utils import userDBID, fetchURL, getChannelName
from gui.wgfm.wgfm_constants import USER_AGENT, PLAYER_STATUS, MOD_VERSION

__all__ = ('TelemetryController', )

TELEMETRY_APPID = 'UA-96929906-2'
TELEMETRY_APPNAME = 'wgfm'

class TelemetryController(object):
	
	userDatabaseID = property(lambda self: self.__userDatabaseID)

	def __init__(self):
		self.__userDatabaseID = None
	
	def init(self):
		g_eventsManager.onRadioStatusUpdated += self.__onPlayerStateChanged
		g_playerEvents.onAccountShowGUI += self.__onAccountShowGUI
	
	def fini(self):
		g_eventsManager.onRadioStatusUpdated -= self.__onPlayerStateChanged
		g_playerEvents.onAccountShowGUI -= self.__onAccountShowGUI
	
	def userVote(self, liked, tag):
		self.sendEvent('rating', 'like' if liked else 'dislike', tag)
	
	def __onPlayerStateChanged(self):
		if g_controllers.player.status == PLAYER_STATUS.ERROR:
			self.sendScreen('error')
		elif g_controllers.player.status == PLAYER_STATUS.PLAYING:
			self.sendScreen('playing-%s' % getChannelName().lower())
		else:
			self.sendScreen('stopped')
	
	def __onAccountShowGUI(self, ctx):
		self.__userDatabaseID = userDBID()
		self.__onPlayerStateChanged()
	
	@process
	def sendEvent(self, eventName, eventType, eventResult):
		if not self.userDatabaseID:
			return
		postData = urlencode( { 'v': '1', 'tid': TELEMETRY_APPID, 'cid': self.userDatabaseID, 't': 'event', \
							'ec': eventName, 'ea': eventType, 'el': eventResult } )
		successful = yield self.__requestAnalitics(postData)
		LOG_DEBUG('sendEvent', successful, postData)
	
	@process
	def sendScreen(self, screenName):
		if not self.userDatabaseID:
			return
		postData = urlencode( { 'v': '1', 'tid': TELEMETRY_APPID, 'cid': self.userDatabaseID, 't': 'screenview', \
							'cd': screenName, 'an': TELEMETRY_APPNAME, 'av': MOD_VERSION} )
		successful = yield self.__requestAnalitics(postData)
		LOG_DEBUG('sendScreen', successful, postData)
	
	@async
	@process
	def __requestAnalitics(self, postData, callback):
		status, _ = yield lambda callback: fetchURL(url = 'https://ssl.google-analytics.com/collect', \
				method = 'POST', callback = callback, timeout = 5.0, postData = postData, \
				headers = {'User-Agent': USER_AGENT } )
		callback(status)
