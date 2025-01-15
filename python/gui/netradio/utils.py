# SPDX-License-Identifier: MIT
# Copyright (c) 2015-2025 Andrii Andrushchyshyn

import httplib
import os
import socket
import threading
import functools
import types
import urlparse

import BigWorld
import Keys
import ResMgr
from avatar_helpers import getAvatarDatabaseID
from account_helpers import getAccountDatabaseID
from debug_utils import LOG_ERROR, LOG_WARNING, LOG_CURRENT_EXCEPTION
from helpers import dependency
from skeletons.gui.impl import IGuiLoader

__all__ = ('byteify', 'override', 'getChannelName', 'parseKeyValue', 'parseKeyValueFull', 'parseKeyModifiers',
 'previosChannel', 'nextChannel', 'checkKeySet', 'unpackTempFiles', 'fetchURL', 'userDBID', 'parse_localization_file',
 'vfs_file_read', 'timestamp', 'cache_result', 'fixed_environ', 'getParentWindow')

def override(holder, name, wrapper=None, setter=None):
	"""Override methods, properties, functions, attributes
	:param holder: holder in which target will be overrided
	:param name: name of target to be overriden
	:param wrapper: replacement for override target
	:param setter: replacement for target property setter"""
	if wrapper is None:
		return lambda wrapper, setter=None: override(holder, name, wrapper, setter)
	target = getattr(holder, name)
	wrapped = lambda *a, **kw: wrapper(target, *a, **kw)
	if not isinstance(holder, types.ModuleType) and isinstance(target, types.FunctionType):
		setattr(holder, name, staticmethod(wrapped))
	elif isinstance(target, property):
		prop_getter = lambda *a, **kw: wrapper(target.fget, *a, **kw)
		prop_setter = target.fset if not setter else lambda *a, **kw: setter(target.fset, *a, **kw)
		setattr(holder, name, property(prop_getter, prop_setter, target.fdel))
	else:
		setattr(holder, name, wrapped)

def byteify(data):
	"""Encodes data with UTF-8
	:param data: Data to encode"""
	result = data
	if isinstance(data, dict):
		result = {byteify(key): byteify(value) for key, value in data.iteritems()}
	elif isinstance(data, (list, tuple, set)):
		result = [byteify(element) for element in data]
	elif isinstance(data, unicode):
		result = data.encode('utf-8')
	return result

def getChannelName():
	"""using for format and cut WGFM on current channel name"""
	from .controllers import g_controllers
	channelName = g_controllers.player.channelName
	formattedName = channelName.replace('WGFM ', '').replace('WGFM', '').replace(' ', '')
	return formattedName

def getCurrentChannelIdx():
	from .controllers import g_controllers
	from .data import g_dataHolder
	from ._constants import PLAYER_STATUS

	result = 0
	player = g_controllers.player
	if player.status == PLAYER_STATUS.ERROR:
		result = -1
	elif player.status == PLAYER_STATUS.PLAYING or player.channelIdx != -1:
		result = player.channelIdx
	else:
		channel = g_controllers.channel
		saveChannel = g_dataHolder.settings.get('saveChannel', True)
		savedIdx = g_dataHolder.settings.get('lastChannel', 0)
		if saveChannel and channel.channels[savedIdx]['available']:
			result = savedIdx
		else:
			for idx, item in enumerate(channel.channels):
				if item['available']:
					result = idx
					break
	return result

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

	if isAlt:
		result = "ALT + "
	elif isCtrl:
		result = "CTRL + "
	elif isShift:
		result = "SHIFT + "
	else:
		result = ""

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
	return alt, ctrl, shift

def previosChannel():
	from .controllers import g_controllers
	result = -1
	if not g_controllers.channel.inited:
		g_controllers.channel.grabChannels()
		result = -1
	else:
		new = g_controllers.player.channelIdx - 1
		if new in range(0, len(g_controllers.channel.channels)):
			result = new
	return result

def nextChannel():
	from .controllers import g_controllers
	result = -1
	if not g_controllers.channel.inited:
		g_controllers.channel.grabChannels()
		return -1
	else:
		new = g_controllers.player.channelIdx + 1
		if new in range(0, len(g_controllers.channel.channels)):
			result = new
	return result

def checkKeySet(keyset):
	"""Verify is keys is pressed
	:param keyset: list of keys to be checked"""
	result = True
	if not keyset:
		result = False
	for item in keyset:
		if isinstance(item, int) and not BigWorld.isKeyDown(item):
			result = False
		if isinstance(item, list):
			result = result and any(map(BigWorld.isKeyDown, item))
	return result

def unpackTempFiles(vfs_path, realfs_path):
	"""Unpack files to AppData/Local/Temp
	for work with tham from real FS
	"""
	if ResMgr.isFile(vfs_path):
		realfs_dir = os.path.dirname(realfs_path)
		if not os.path.exists(realfs_dir):
			os.makedirs(realfs_dir)
		data = vfs_file_read(vfs_path)
		if data and not os.path.isfile(realfs_path):
			with open(realfs_path, 'wb') as fh:
				fh.write(data)
	elif ResMgr.isDir(vfs_path):
		for item in vfs_dir_list(vfs_path):
			unpackTempFiles(vfs_path + '/' + item, realfs_path + '\\' + item)

def vfs_dir_list(vfs_path, only_files=False):
	"""using for list files in VFS dir"""
	result = []
	folder = ResMgr.openSection(vfs_path)
	if folder is not None and ResMgr.isDir(vfs_path):
		for item_name in folder.keys():
			if item_name in result:
				continue
			vfs_item_path = '%s/%s' % (vfs_path, item_name)
			if only_files and ResMgr.isFile(vfs_item_path):
				result.append(item_name)
			elif not only_files:
				result.append(item_name)
	return result

def vfs_file_read(path):
	"""using for read files from VFS"""
	fileInst = ResMgr.openSection(path)
	if fileInst is not None and ResMgr.isFile(path):
		return str(fileInst.asBinary)
	return None

def parse_localization_file(file_path):
	"""split items by lines and key value by ':'
	like yaml format"""
	result = {}
	file_data = vfs_file_read(file_path)
	if file_data:
		for test_line in file_data.splitlines():
			if ': ' not in test_line:
				continue
			key, value = test_line.split(': ', 1)
			result[key] = value.replace('\\n', '\n').strip()
	return result

def cache_result(function):
	memo = {}
	@functools.wraps(function)
	def wrapper(*args):
		try:
			return memo[args]
		except KeyError:
			rv = function(*args)
			memo[args] = rv
			return rv
	return wrapper

def userDBID():
	return int(getAccountDatabaseID() or getAvatarDatabaseID()) or None

def request_thread(url, callback, headers, timeout, method, postData, onlyResponceStatus):

	try:
		req = urlparse.urlparse(url)
	except: #NOSONAR
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
		connection = connectionClass(host=req.hostname, port=req.port, timeout=timeout)
	except: #NOSONAR
		LOG_ERROR('fetchURL', 'cant create connection')
		LOG_CURRENT_EXCEPTION()
		return callback((False, None))

	try:
		connection.putrequest(method, req.path if req.query == '' else '%s?%s' % (req.path, req.query))
	except: #NOSONAR
		LOG_ERROR('fetchURL', 'cant pur request', method, req.path)
		LOG_CURRENT_EXCEPTION()
		return callback((False, None))

	try:
		if headers is not None:
			for key, val in headers.iteritems():
				connection.putheader(key, val)
		if req.scheme == 'https' and 'Content-length' not in headers and postData is not None:
			connection.putheader('Content-length', len(postData))
	except: #NOSONAR
		LOG_WARNING('fetchURL', 'cant put headers', headers)

	try:
		connection.endheaders()
	except socket.timeout:
		LOG_WARNING('fetchURL', 'socket timed out')
		return callback((False, None))
	except: #NOSONAR
		LOG_ERROR('fetchURL', 'cant endheaders')
		LOG_CURRENT_EXCEPTION()
		return callback((False, None))

	try:
		if postData and method == "POST":
			connection.send(postData)
	except: #NOSONAR
		LOG_ERROR('fetchURL', 'cant send postdata', postData)
		LOG_CURRENT_EXCEPTION()
		return callback((False, None))

	try:
		# @buffering for lag fix in [thread; @process; @async] bunch
		responce = connection.getresponse(buffering=True)
	except: #NOSONAR
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

def fetchURL(url, callback, headers=None, timeout=30.0, method='GET', postData=None,
			onlyResponceStatus=False):
	""" piece of shit down
	Ingame BigWorld.fetchUrl cant work with self-signed ssl certificates
	Ingame BigWorld.fetchUrl cant get only headers of request response without body (Method HEAD)
	Ingame _ssl fail with handshake on cloudflare.com (SSL routines:SSL23_GET_SERVER_HELLO:sslv3 alert handshake failure)
	"""
	if onlyResponceStatus:
		threading.Thread(target=request_thread, args=(url, callback, headers, timeout, method,
					postData, onlyResponceStatus)).start()
	else:
		if headers:
			headers = tuple(('{}: {}'.format(k, v) for k, v in headers.iteritems() if v))
		else:
			headers = tuple()
		args = [headers, timeout, method]
		if postData:
			args.append(postData)
		def responseProcessor(response):
			callback((response.responseCode, response.body))
		BigWorld.fetchURL(url, responseProcessor, *args)

def timestamp():
	from helpers import time_utils
	return time_utils.getCurrentLocalServerTimestamp()

def fixed_environ():
	fixe_env = {}
	for (key, val) in os.environ.items():
		try:
			key, val = str(key), str(val)
			fixe_env[key] = val
		except:
			pass
	return fixe_env

def getParentWindow():
	uiLoader = dependency.instance(IGuiLoader)
	if uiLoader and uiLoader.windowsManager:
		return uiLoader.windowsManager.getMainWindow()
