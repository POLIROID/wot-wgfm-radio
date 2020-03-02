import time
from urllib import urlencode

from adisp import async, process
from debug_utils import LOG_DEBUG
from gui.wgfm.controllers import g_controllers
from gui.wgfm.data import g_dataHolder
from gui.wgfm.events import g_eventsManager
from gui.wgfm.utils import userDBID, fetchURL
from gui.wgfm._constants import PLAYER_STATUS, BUTTON_STATES, CONFIG, USER_AGENT

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
			likeButton = BUTTON_STATES.SELECTED if userLiked else BUTTON_STATES.NORMAL
			dislikeButton = BUTTON_STATES.NORMAL if userLiked else BUTTON_STATES.SELECTED
			if alreadySended:
				likeButton = BUTTON_STATES.SELECTED_DISABLED if userLiked else BUTTON_STATES.NORMAL_DISABLED
				dislikeButton = BUTTON_STATES.NORMAL_DISABLED if userLiked else BUTTON_STATES.SELECTED_DISABLED
			result = (likeButton, dislikeButton)
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

	def syncRatings(self, force=False, channelIdx=-1):
		player = g_controllers.player

		if not force and not player.tag:
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

		accountID = userDBID()
		if not g_dataHolder.settings.get('sendStatistic', True):
			accountID = None

		channelName = g_controllers.channel.channels[channelIdx].get('displayName', '')

		data = {'accID': accountID, 'rate': 1 if userLiked else -1, 'tag': savedTag, 'channelName': channelName}

		url = CONFIG.RATING_GATEWAY.format(url=g_dataHolder.config.get('ratingUrl', CONFIG.RATING_URL),
					time=str(int(time.time())), data=urlencode(data))

		self.__states[savedTag] = [userLiked, True]

		g_eventsManager.onRatingsUpdated()

		successful = yield self.__sendRatingData(url)
		if successful:
			del self.__votes[channelIdx]

	@async
	@process
	def __sendRatingData(self, url, callback=None):
		LOG_DEBUG('sendRatingData', url, self.__votes)
		status, _ = yield lambda callback: fetchURL(url=url, callback=callback, timeout=5.0,
													headers={'User-Agent': USER_AGENT})
		callback(status)

	def __onRadioTagChanged(self):
		self.syncRatings()
