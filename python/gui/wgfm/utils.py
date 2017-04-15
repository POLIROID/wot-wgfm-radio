
__all__ = ('byteify', 'override', 'getChannelName', 'parseKeyValue', 'parseKeyValueFull', 'parseKeyModifiers', \
 'previosChannel', 'nextChannel', 'checkKeySet', 'unpackTempFiles', 'fetchURL', 'userDBID', 'parseLangFields', \
 'readFromVFS', )

import threading
import httplib
import urlparse
import types
import os
import socket

from avatar_helpers import getAvatarDatabaseID
from account_helpers import getAccountDatabaseID
from debug_utils import *
import Keys
import ResMgr

def overrider(target, holder, name):
	"""using for override any staff"""
	original = getattr(holder, name)
	overrided = lambda *a, **kw: target(original, *a, **kw)
	if not isinstance(holder, types.ModuleType) and isinstance(original, types.FunctionType):
		setattr(holder, name, staticmethod(overrided))
	elif isinstance(original, property):
		setattr(holder, name, property(overrided))
	else:
		setattr(holder, name, overrided)
def decorator(function):
	def wrapper(*args, **kwargs):
		def decorate(handler):
			function(handler, *args, **kwargs)
		return decorate
	return wrapper
override = decorator(overrider)

def byteify(data):
	"""using for convert unicode key/value to utf-8"""
	if isinstance(data, types.DictType): 
		return { byteify(key): byteify(value) for key, value in data.iteritems() }
	elif isinstance(data, types.ListType) or isinstance(data, tuple) or isinstance(data, set):
		return [ byteify(element) for element in data ]
	elif isinstance(data, types.UnicodeType):
		return data.encode('utf-8')
	else: 
		return data

def getChannelName():
	"""using for format and cut WGFM on current channel name"""
	from gui.wgfm.controllers import g_controllers
	channelName = g_controllers.player.channelName
	formattedName = channelName.replace('WGFM ', '').replace('WGFM', '').replace(' ', '')
	return formattedName

def getCurrentChannelIdx():
	from gui.wgfm.controllers import g_controllers
	from gui.wgfm.data import g_dataHolder	
	from gui.wgfm.wgfm_constants import PLAYER_STATUS
	
	player = g_controllers.player
	if player.status == PLAYER_STATUS.ERROR:
		return -1	 
	elif player.status == PLAYER_STATUS.PLAYING or player.channelIdx != -1:
		return player.channelIdx
	else:
		channel = g_controllers.channel
		saveChannel = g_dataHolder.settings.get('saveChannel', True)
		if saveChannel:
			savedIdx = g_dataHolder.settings.get('lastChannel', 0)
			if channel.channels[savedIdx]['available']:
				return savedIdx
		for idx, item in enumerate(channel.channels):
			if item['available']:
				return idx
	return -1

def parseKeyNameByID(key_id):
	for attr in dir(Keys):
		if 'KEY_' in attr and getattr(Keys, attr) == key_id:
			return attr.replace('KEY_', '')
	return ''

def parseKeyValue(keyset):
	
	if isinstance(keyset, types.ListType):
		for keyItem in keyset:
			if isinstance(keyItem, types.IntType):
				return parseKeyNameByID(keyItem)
	return ''

def parseKeyValueFull(keyset):
	
	isAlt, isCtrl, isShift = parseKeyModifiers(keyset)
	
	if isAlt: result = "ALT + "
	elif isCtrl: result = "CTRL + "
	elif isShift: result = "SHIFT + "
	else: result = ""
	
	if isinstance(keyset, types.ListType):
		for keyItem in keyset:
			if isinstance(keyItem, types.IntType):
				return result + parseKeyNameByID(keyItem)
	
	return result

def parseKeyModifiers(keyset):
	alt, ctrl, shift = False, False, False
	if isinstance(keyset, types.ListType):
		alt = [Keys.KEY_LALT, Keys.KEY_RALT] in keyset
		ctrl = [Keys.KEY_LCONTROL, Keys.KEY_RCONTROL] in keyset
		shift = [Keys.KEY_LSHIFT, Keys.KEY_RSHIFT] in keyset
	return (alt, ctrl, shift)

def previosChannel():
	from gui.wgfm.controllers import g_controllers
	if not g_controllers.channel.inited:
		g_controllers.channel.grabChannels()
		return -1
	new = g_controllers.player.channelIdx - 1
	if new in range(0, len(g_controllers.channel.channels)):
		return new
	else:
		return -1

def nextChannel():
	from gui.wgfm.controllers import g_controllers
	if not g_controllers.channel.inited:
		g_controllers.channel.grabChannels()
		return -1
	new = g_controllers.player.channelIdx + 1
	if new in range(0, len(g_controllers.channel.channels)):
		return new
	else:
		return -1

def checkKeySet(keyset):
	result = True
	if not keyset:
		result = False
	for item in keyset:
		if isinstance(item, types.IntType) and not BigWorld.isKeyDown(item):
			result = False
			break
		if isinstance(item, types.ListType):
			for keyItem in item:
				if not BigWorld.isKeyDown(keyItem):
					result = False
					break
	return result

def file_read(vfs_path, as_binary=True):
	"""Reads file from VFS
	vfs_path: path in VFS, for example, 'scripts/client/gui/mods/mod_.pyc'
	as_binary: set to True if file is binary
	"""
	vfs_file = ResMgr.openSection(vfs_path)
	if vfs_file is not None and ResMgr.isFile(vfs_path):
		if as_binary:
			return str(vfs_file.asBinary)
		else:
			return str(vfs_file.asString)
	return None

def directory_list(vfs_path):
	"""Lists files in directory from VFS
	vfs_path: path in VFS, for example, 'scripts/client/gui/mods/'
	"""
	result = []
	folder = ResMgr.openSection(vfs_path)
	if folder is not None and ResMgr.isDir(vfs_path):
		for name in folder.keys():
			if name not in result:
				result.append(name)
	return sorted(result)

def unpackTempFiles(vfs_path, realfs_path):
	"""Unpack files to AppData/Local/Temp 
	for work with tham from real FS
	"""
	if ResMgr.isFile(vfs_path):
		LOG_DEBUG('unpackTempFiles file', vfs_path)
		realfs_dir = os.path.dirname(realfs_path)
		if not os.path.exists(realfs_dir):
			os.makedirs(realfs_dir)
		data = file_read(vfs_path)
		if data:
			with open(realfs_path, 'wb') as fh:
				fh.write(data)
	elif ResMgr.isDir(vfs_path):
		LOG_DEBUG('unpackTempFiles dir', vfs_path)
		for item in directory_list(vfs_path):
			unpackTempFiles(vfs_path + '/' + item, realfs_path + '\\' + item)

def userDBID():
	return int(getAccountDatabaseID() or getAvatarDatabaseID()) or None

def fetchURL(url, callback, headers = None, timeout = 30.0, method = 'GET', postData = None, onlyResponceStatus = False):
	""" Implementation of http requester like BigWorld.fetchUrl
	Ingame BigWorld.fetchUrl cant work with self-signed ssl certificates
	"""
	def request_thread(url, callback, headers, timeout, method, postData, onlyResponceStatus):
		
		try:
			req = urlparse.urlparse(url)
		except:
			LOG_ERROR('fetchURL', 'bad request url', url)
			LOG_CURRENT_EXCEPTION()
			return callback((False, None))
		
		if req.scheme == 'http':
			connectionClass = httplib.HTTPConnection
		elif req.scheme == 'https':
			connectionClass = httplib.HTTPSConnection
		else:
			LOG_ERROR('fetchURL', 'bad request scheme', req.scheme)
			return callback((False, None))
		
		try:
			connection = connectionClass(host = req.hostname, port = req.port, timeout = timeout)
		except:
			LOG_ERROR('fetchURL', 'cant create connection')
			LOG_CURRENT_EXCEPTION()
			return callback((False, None))
		
		try:
			connection.putrequest(method, req.path)
		except:
			LOG_ERROR('fetchURL', 'cant pur request', method, req.path)
			LOG_CURRENT_EXCEPTION()
			return callback((False, None))
		
		try:
			if headers is not None:
				for key, val in headers.iteritems():
					connection.putheader(key, val)
			if req.scheme == 'https' and 'Content-length' not in headers:
				connection.putheader('Content-length', len(postData))
		except:
			LOG_WARNING('fetchURL', 'cant pur headers', headers)
		
		try:
			connection.endheaders()
		except socket.timeout:
			LOG_WARNING('fetchURL', 'socket timed out')
			return callback((False, None))
		except:
			LOG_ERROR('fetchURL', 'cant endheaders')
			LOG_CURRENT_EXCEPTION()
			return callback((False, None))
		
		try:
			if postData and method == "POST":
				connection.send(postData)
		except:
			LOG_ERROR('fetchURL', 'cant send postdata', postData)
			LOG_CURRENT_EXCEPTION()
			return callback((False, None))
		
		try:
			# @buffering for lag fix in [thread; @process; @async] bunch
			responce = connection.getresponse(buffering=True) 
		except:
			LOG_ERROR('fetchURL', 'cant get responce')
			LOG_CURRENT_EXCEPTION()
			return callback((False, None))
		
		if responce.status != 200:
			LOG_WARNING('fetchURL', 'bad responce status', responce.status, url)
		
		if onlyResponceStatus:
			return callback((responce.status == 200, None))
		
		try:
			responceData = responce.read()
		except socket.timeout:
			LOG_WARNING('fetchURL', 'socket timed out')
			responceData = None
		connection.close()
		return callback((responce.status == 200, responceData))

	threading.Thread(target = request_thread, args = (url, callback, headers, timeout, method, postData, onlyResponceStatus, )).start()

def parseLangFields(langCode):
	"""split items by lines and key value by : 
	like yaml format"""
	from gui.wgfm.wgfm_constants import LANGUAGE_FILE_PATH
	result = {}
	langData = readFromVFS(LANGUAGE_FILE_PATH % langCode)
	if langData:
		for item in langData.splitlines():
			if ': ' not in item: continue
			key, value = item.split(": ", 1)
			result[key] = value
	return result

def readFromVFS(path):
	"""using for read files from VFS"""
	file = ResMgr.openSection(path)
	if file is not None and ResMgr.isFile(path):
		return str(file.asBinary)
	return None