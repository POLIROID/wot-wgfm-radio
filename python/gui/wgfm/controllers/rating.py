
import time
from urllib import urlencode

from adisp import async, process
from debug_utils import LOG_ERROR, LOG_DEBUG, LOG_CURRENT_EXCEPTION

from gui.wgfm.controllers import g_controllers
from gui.wgfm.data import g_dataHolder
from gui.wgfm.events import g_eventsManager
from gui.wgfm.utils import userDBID, fetchURL
from gui.wgfm.wgfm_constants import PLAYER_STATUS, BUTTON_STATES, CONFIG, USER_AGENT

__all__ = ('RatingController', )

class RatingController(object):
	
	def __init__(self):
		self.__states = {}
		self.__votes = {}
	
	def init(self):
		g_eventsManager.onRadioTagChanged += self.__onRadioTagChanged
	
	def fini(self):
		g_eventsManager.onRadioTagChanged -= self.__onRadioTagChanged
	
	def get_buttonsStates(self):
		"""return rating button (like/dislike) states"""
		result = (BUTTON_STATES.NORMAL, BUTTON_STATES.NORMAL,)
		
		player = g_controllers.player

		if player.tag in self.__states:
			userLiked, alreadySended = self.__states[player.tag]
			if not alreadySended:
				result = ( BUTTON_STATES.SELECTED if userLiked else BUTTON_STATES.NORMAL, 
						BUTTON_STATES.NORMAL if userLiked else BUTTON_STATES.SELECTED, )
			else:
				result = ( BUTTON_STATES.SELECTED_DISABLED if userLiked else BUTTON_STATES.NORMAL_DISABLED, 
						BUTTON_STATES.NORMAL_DISABLED if userLiked else BUTTON_STATES.SELECTED_DISABLED, )
		return result
	
	buttonsState = property(get_buttonsStates)

	def vote(self, liked):
		"""vote for current tag in current channel"""
		player = g_controllers.player

		alreadyProcessed = False
		if player.tag in self.__states:
			_, alreadyProcessed = self.__states[player.tag]

		if player.status == PLAYER_STATUS.PLAYING and player.tag != '' and player.tag and not alreadyProcessed:
			self.__votes[player.channelIdx] = (player.tag, liked)
		else:
			return
		
		self.__states[player.tag] = (liked, False, )
		
		g_controllers.battle.showRatingsMessage()
		g_eventsManager.onRatingsUpdated()
	
	def syncRatings(self, force = False, channelIdx = -1):
		player = g_controllers.player
		
		if not force and player.tag == '':
			return
		
		savedTag, userLiked = None, None
		
		if force and channelIdx in self.__votes:
			savedTag, userLiked = self.__votes[channelIdx]
		elif player.channelIdx in self.__votes:
			savedTag, userLiked = self.__votes[player.channelIdx]
		
		if savedTag is None or userLiked is None:
			return
		
		if player.tag != savedTag or force:
			self.__processRatingData(userLiked, channelIdx if force else player.channelIdx, savedTag)
	
	@process
	def __processRatingData(self, userLiked, channelIdx, savedTag):
		
		url = CONFIG.RATING_GATEWAY.format(
			url = g_dataHolder.config.get('ratingUrl', 'http://cfg.wargaming.fm/cgi-bin/ratingwot.cgi'),
			time = str(int(time.time())),
			data = urlencode({
				'accID': None if g_dataHolder.settings.get('sendStatistic', True) == False else userDBID(),
				'rate': 1 if userLiked else -1,
				'channelName': g_controllers.channel.channels[channelIdx].get('displayName', ''),
				'tag': savedTag
			})
		)
		
		self.__states[savedTag] = [userLiked, True]
		
		g_eventsManager.onRatingsUpdated()
		
		g_controllers.telemetry.userVote(userLiked, savedTag)

		successful = yield self.__sendRatingData(url)
		if successful:
			del self.__votes[channelIdx]
	
	@async
	@process
	def __sendRatingData(self, url, callback):
		status, _ = yield lambda callback: fetchURL(url = url, callback = callback, timeout = 5.0, headers = {'User-Agent': USER_AGENT} )
		callback(status)
	
	def __onRadioTagChanged(self):
		self.syncRatings()
