
import time
import urllib
import urllib2
import hashlib
from adisp import process, async
from avatar_helpers import getAvatarDatabaseID
from account_helpers import getAccountDatabaseID
from debug_utils import LOG_DEBUG, LOG_NOTE

from gui.wgfm.data import g_dataHolder
from gui.wgfm.events import g_eventsManager
from gui.wgfm.controllers import g_controllers
from gui.wgfm.wgfm_constants import PLAYER_STATUS, BUTTON_STATES

__all__ = ('RatingController', )

class RatingController(object):
	
	buttonsState = property(lambda self: self.__getButtonsStates())

	def __init__(self):
		self.__states = {}
		self.__votes = {}
	
	def init(self):
		g_eventsManager.onRadioTagChanged += self.__onRadioTagChanged
	
	def fini(self):
		g_eventsManager.onRadioTagChanged -= self.__onRadioTagChanged
	
	def vote(self, liked):
		"""vote for current tag in current channel"""
		player = g_controllers.player

		if player.status == PLAYER_STATUS.PLAYING and player.tag != '':
			self.__votes[player.channelIdx] = (player.tag, liked)
		else:
			return
		
		if player.channelIdx not in self.__states:
			self.__states[player.channelIdx] = {}
		
		self.__states[player.channelIdx][player.tag] = (liked, False, )
		
		g_controllers.battle.showRatingsMessage()
		g_eventsManager.onRatingsUpdated()

	def __getButtonsStates(self):
		"""return rating button (like/dislike) states"""
		result = (BUTTON_STATES.NORMAL, BUTTON_STATES.NORMAL,)
		
		player = g_controllers.player

		if player.channelIdx in self.__states and player.tag in self.__states[player.channelIdx]:
			userLiked, alreadySended = self.__states[player.channelIdx][player.tag]
			if not alreadySended:
				result = ( BUTTON_STATES.SELECTED if userLiked else BUTTON_STATES.NORMAL, 
						BUTTON_STATES.NORMAL if userLiked else BUTTON_STATES.SELECTED, )
			else:
				result = ( BUTTON_STATES.SELECTED_DISABLED if userLiked else BUTTON_STATES.NORMAL_DISABLED, 
						BUTTON_STATES.NORMAL_DISABLED if userLiked else BUTTON_STATES.SELECTED_DISABLED, )
		
		return result
	
	def processRating(self, force = False, channelIdx = -1):
		
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
			
			if force:
				self.__states[channelIdx][savedTag] = [userLiked, True]
				del self.__votes[channelIdx]
			else:
				self.__states[player.channelIdx][savedTag] = [userLiked, True]
				del self.__votes[player.channelIdx]
			
			g_eventsManager.onRatingsUpdated()
			
			self.__requestAPI({'force': force, 'savedTag': savedTag, 'userLiked': userLiked})
		
	@async
	@process
	def __requestAPI(self, ctx, callback = None):
		
		accID = int(getAccountDatabaseID() or getAvatarDatabaseID())
			
		data = {
			'accID': None if accID == 0 or g_dataHolder.settings.get('sendStatistic', True) == False else accID,
			'rate': 1 if ctx['userLiked'] else -1,
			'channelName': g_controllers.channel.channels[channelIdx].get('displayName', '') if ctx['force'] else g_controllers.channel.channels[player.channelIdx].get('displayName', ''),
			'tag': ctx['savedTag']
		}
		
		url = '{url}?time={time}&{data}'.format(
			url = g_dataHolder.config.get('ratingUrl', 'http://cfg.wargaming.fm/cgi-bin/ratingwot.cgi'),
			time = str(int(time.time())),
			data = urllib.urlencode(data)
		)
		
		LOG_DEBUG('RatingController.processRating', url)
		try:
			request = urllib2.urlopen(url, timeout = 5)
			response = request.read()
			LOG_DEBUG('RatingController.processRating', response.replace('\n', ''))
		except Exceptin as e:
			LOG_ERROR('RatingController.processRating', e)
			
	def __onRadioTagChanged(self):
		self.processRating()
	
