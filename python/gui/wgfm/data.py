
import os
import cPickle
import json
import urllib2
import zlib
import time

from debug_utils import LOG_ERROR, LOG_DEBUG

from gui.wgfm.events import g_eventsManager
from gui.wgfm.utils import *
from gui.wgfm.wgfm_constants import CONFIG, DEFAULT_CONFIG, DEFAULT_SETTINGS, SETTINGS_FILE, CACHE_FILE, TEMP_DATA_FOLDER, TEMP_DATA_FOLDER_VFS

__all__ = ('g_dataHolder', )

class DataHolder(object):
	
	config = property(lambda self: self.__config)
	settings = property(lambda self: self.__settings)
	
	def __init__(self):
		
		self.__config = DEFAULT_CONFIG
		self.__settings = DEFAULT_SETTINGS

		data_dir = os.path.dirname(SETTINGS_FILE)
		if not os.path.exists(data_dir):
			os.makedirs(data_dir)
		
		g_eventsManager.onAppFinish += self.__save
		
		# unpack temp files
		unpackTempFiles(TEMP_DATA_FOLDER_VFS, TEMP_DATA_FOLDER)

		if (os.path.exists(SETTINGS_FILE)):
			self.loadSettings()
		else:
			LOG_DEBUG('No settings file')
			self.saveSettings()	
	
	def init_config_onstart(self):
		LOG_DEBUG('init_config_onstart')
		if self.__parseConfig():
			self.createConfigCache()
		else:
			self.loadConfigCache()
	
	def __parseConfig(self):
		try:
			
			def parse(response):
				try:			
					response = response.decode('utf-8-sig')
					obj = byteify(json.loads(response))
					return obj
				except Exception as e:
					LOG_ERROR('__parseConfig.parse', e)
			
			req = urllib2.Request(CONFIG.CONFIG_URL)
			conn = urllib2.urlopen(req, timeout = 5.0)
			response = conn.read()			
			self.__config = parse(response)
			conn.close()
			return True
		
		except urllib2.URLError:
			LOG_ERROR('DataHolder.__parseConfig', 'Site not available', False)
		
		except Exception as e:
			LOG_ERROR('DataHolder.__parseConfig', e)
			return False		
	
	def createConfigCache(self):
		try:
			cache = dict()
			cache['create_time'] = int(time.time())
			if self.__config:
				cache['data'] = self.__config			   
				with open(CACHE_FILE, 'wb') as fh:
					p = cPickle.dumps(cache)
					fh.write(zlib.compress(p, 1))
		except Exception as e:
			LOG_ERROR('DataHolder.createConfigCache', e)
	
	def loadConfigCache(self):
		try:
			with open(CACHE_FILE, 'rb') as fh:
				dec = zlib.decompress(fh.read())
				p = cPickle.loads(dec)
				self.__config = dict()
				self.__config = p['data']			   
		except IOError:
			LOG_ERROR('DataHolder.loadConfigCache', 'Cache not found', False)
		except Exception as e:
			LOG_ERROR('DataHolder.loadConfigCache', e)
	
	def loadSettings(self):
		try:
			with open(SETTINGS_FILE, 'rb') as fh:
				dec = zlib.decompress(fh.read())
				pickle = cPickle.loads(dec)
				self.__settings = pickle['data']			   
		except Exception as e:
			LOG_ERROR('DataHolder.load_settings', e)
	
	def saveSettings(self):
		try:
			data = dict()
			if self.__settings:
				data['data'] = self.__settings			   
				with open(SETTINGS_FILE, 'wb') as fh:
					p = cPickle.dumps(data)
					fh.write(zlib.compress(p, 1))
		except Exception as e:
			LOG_ERROR('DataHolder.saveSettings', e)
	
	def __save(self):
		self.saveSettings()	
		self.createConfigCache()
	
g_dataHolder = DataHolder()