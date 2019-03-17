import cPickle
import json
import os
import time
import zlib
from adisp import async, process

from debug_utils import LOG_ERROR, LOG_DEBUG, LOG_CURRENT_EXCEPTION

from gui.wgfm.events import g_eventsManager
from gui.wgfm.utils import byteify, fetchURL, unpackTempFiles
from gui.wgfm.wgfm_constants import CONFIG, DEFAULT_CONFIG, DEFAULT_SETTINGS, DEFAULT_CACHE, SETTINGS_FILE, \
	CONFIG_CACHE_FILE, CACHE_FILE, TEMP_DATA_FOLDER, TEMP_DATA_FOLDER_VFS, USER_AGENT, SETTINGS_VERSION

__all__ = ('g_dataHolder', )

class DataHolder(object):

	@property
	def cache(self):
		return self.__cache

	@property
	def config(self):
		return self.__config

	@property
	def settings(self):
		return self.__settings

	def __init__(self):

		self.__cache = DEFAULT_CACHE
		self.__config = DEFAULT_CONFIG
		self.__settings = DEFAULT_SETTINGS

		data_dir = os.path.dirname(SETTINGS_FILE)
		if not os.path.exists(data_dir):
			os.makedirs(data_dir)

		g_eventsManager.onAppFinish += self.__save

		# unpack temp files
		unpackTempFiles(TEMP_DATA_FOLDER_VFS, TEMP_DATA_FOLDER)

		if os.path.exists(SETTINGS_FILE):
			self.loadSettings()
		else:
			LOG_DEBUG('No settings file')
			self.saveSettings()

		if os.path.exists(CACHE_FILE):
			self.loadCache()
		else:
			LOG_DEBUG('No settings file')
			self.saveCache()

	@async
	@process
	def initConfigOnStart(self, callback):
		parsedFromNet = yield self.__parseConfig()
		if parsedFromNet:
			self.createConfigCache()
		else:
			self.loadConfigCache()
		callback(True)

	@async
	@process
	def __parseConfig(self, callback=None):
		result = True
		status, data = yield lambda callback: fetchURL(url=CONFIG.CONFIG_URL, callback=callback, timeout=5.0, \
										headers={'User-Agent': USER_AGENT})
		if not status:
			result = False

		try:
			cfg = byteify(json.loads(data.decode('utf-8-sig')))
			self.__config = cfg
		except: #NOSONAR
			LOG_ERROR('DataHolder.__parseConfig', data)
			LOG_CURRENT_EXCEPTION()
			result = False

		callback(result)

	def createConfigCache(self):
		try:
			cache = dict()
			cache['create_time'] = int(time.time())
			if self.__config:
				cache['data'] = self.__config
				with open(CONFIG_CACHE_FILE, 'wb') as fh:
					p = cPickle.dumps(cache)
					fh.write(zlib.compress(p, 1))
		except: #NOSONAR
			LOG_ERROR('DataHolder.createConfigCache')
			LOG_CURRENT_EXCEPTION()

	def loadConfigCache(self):
		try:
			with open(CONFIG_CACHE_FILE, 'rb') as fh:
				dec = zlib.decompress(fh.read())
				p = cPickle.loads(dec)
				self.__config = dict()
				self.__config = p['data']
		except IOError:
			LOG_ERROR('DataHolder.loadConfigCache', 'Cache not found')
		except: #NOSONAR
			LOG_ERROR('DataHolder.loadConfigCache')
			LOG_CURRENT_EXCEPTION()

	def loadSettings(self):
		try:
			with open(SETTINGS_FILE, 'rb') as fh:
				raw_data = zlib.decompress(fh.read())
				pickle_data = cPickle.loads(raw_data)
				(version, settings, ) = pickle_data
				if version == SETTINGS_VERSION:
					self.__settings = settings
				else:
					self.saveSettings()
		except ValueError:
			self.saveSettings()
		except: #NOSONAR
			LOG_ERROR('DataHolder.loadSettings')
			LOG_CURRENT_EXCEPTION()

	def saveSettings(self):
		try:
			with open(SETTINGS_FILE, 'wb') as fh:
				pickle_data = cPickle.dumps((SETTINGS_VERSION, self.__settings,))
				raw_data = zlib.compress(pickle_data, 1)
				fh.write(raw_data)
		except: #NOSONAR
			LOG_ERROR('DataHolder.saveSettings')
			LOG_CURRENT_EXCEPTION()

	def loadCache(self):
		try:
			with open(CACHE_FILE, 'rb') as fh:
				dec = zlib.decompress(fh.read())
				pickle = cPickle.loads(dec)
				self.__cache = pickle['data']
		except: #NOSONAR
			LOG_ERROR('DataHolder.loadCache')
			LOG_CURRENT_EXCEPTION()

	def saveCache(self):
		try:
			data = dict()
			if self.__cache:
				data['data'] = self.__cache
				with open(CACHE_FILE, 'wb') as fh:
					p = cPickle.dumps(data)
					fh.write(zlib.compress(p, 1))
		except: #NOSONAR
			LOG_ERROR('DataHolder.saveCache')
			LOG_CURRENT_EXCEPTION()

	def __save(self):
		self.saveSettings()
		self.saveCache()
		self.createConfigCache()

g_dataHolder = DataHolder()
