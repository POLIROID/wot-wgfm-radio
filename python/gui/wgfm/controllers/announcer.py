
__all__ = ('AnnounceController', )

import json

import BigWorld
from adisp import async, process
from debug_utils import LOG_WARNING
from helpers import time_utils, isPlayerAccount
from gui import SystemMessages
from PlayerEvents import g_playerEvents

from gui.wgfm.data import g_dataHolder
from gui.wgfm.utils import byteify, fetchURL
from gui.wgfm.wgfm_constants import APIv2, USER_AGENT, TAGS_UPDATE_INTERVAL, ANNOUNCMENTS_UPDATE_INTERVAL

class AnnounceController(object):
	
	cache = property(lambda self : self.__showedIds)
	timestamp = property(lambda self: time_utils.getCurrentLocalServerTimestamp())
	
	def __init__(self):
		self.__cache = {}
		self.__showedIds = []
		self.__lastRequestTime = 0
		self.__cheackCallbackID = None
	
	def init(self):
		g_playerEvents.onAccountShowGUI += self.__onAccountShowGUI
		self.__showedIds = g_dataHolder.cache['announced_ids']
		self.cheackAnnouncements()
	
	def fini(self):
		g_playerEvents.onAccountShowGUI -= self.__onAccountShowGUI
		if self.__cheackCallbackID:
			BigWorld.cancelCallback(self.__cheackCallbackID)
			self.__cheackCallbackID = None
		g_dataHolder.cache['announced_ids'] = self.__showedIds
	
	def __onAccountShowGUI(self, ctx):
		self.cheackAnnouncements()
	
	def cheackAnnouncements(self):
		
		if self.__cheackCallbackID:
			BigWorld.cancelCallback(self.__cheackCallbackID)
			self.__cheackCallbackID = None
		
		currentTime = self.timestamp
		self.__synckAnnouncement(currentTime)
		
		for announcement in self.__cache.values():
			if announcement['showed']:
				continue
			startTime = announcement['start']
			finishTime = announcement['finish']
			if startTime < currentTime < finishTime:
				SystemMessages.pushMessage(announcement['message'], SystemMessages.SM_TYPE.GameGreeting)
				announcement['showed'] = True
				self.__showedIds.append(announcement['id'])
		
		self.__cheackCallbackID = BigWorld.callback(TAGS_UPDATE_INTERVAL, self.cheackAnnouncements)
	
	def __processAnnounceData(self, announcementData):
		for announcementItem in announcementData:
			idNum = announcementItem['id']
			if idNum in self.__showedIds:
				continue
			if idNum not in self.__cache:
				self.__cache[idNum] = {
					'showed': False
				}
			self.__cache[idNum]['id'] = announcementItem['id']
			self.__cache[idNum]['start'] = announcementItem['start']
			self.__cache[idNum]['finish'] = announcementItem['finish']
			self.__cache[idNum]['message'] = announcementItem['message']
	
	@process
	def __synckAnnouncement(self, currentTime):
		if isPlayerAccount() and self.__lastRequestTime + ANNOUNCMENTS_UPDATE_INTERVAL < currentTime:
			successfully, announcementData = yield self.__getAnnounceData()
			if successfully:
				self.__lastRequestTime = currentTime
				self.__processAnnounceData(announcementData)
	
	@async
	@process
	def __getAnnounceData(self, callback):
		
		request = {
			'url': APIv2.BASE_URL + APIv2.ANNOUNCE_GATEWAY,
			'timeout': 5.0,
			'headers': {
				'User-Agent': USER_AGENT
			}
		}

		status, data = yield lambda callback : fetchURL(callback = callback, **request)
		announcementData = []
		if status:
			try:
				announcementData = byteify(json.loads(data))['announcements']
			except:
				LOG_WARNING('__getAnnounceData', 'cant parse data')
				status = False
		
		callback((status, announcementData))