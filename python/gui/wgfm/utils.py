
__all__ = ('byteify', 'override', 'getChannelName', 'parseKeyValue', 'parseKeyValueFull', 'parseKeyModifiers',\
 'previosChannel', 'nextChannel', 'checkKeySet', 'unpackTempFiles')

import ResMgr
import types
import Keys
import os
from debug_utils import *

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
	from gui.wgfm.controllers import g_controllers
	
	channelName = g_controllers.player.channelName
	return channelName.replace('WGFM ', '').replace('WGFM', '').replace(' ', '')

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
			if channel.channels[savedIdx]['availible']:
				return savedIdx
		for idx, item in enumerate(channel.channels):
			if item['availible']:
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
	