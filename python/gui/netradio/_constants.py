import os
import tempfile
import platform

import BigWorld
import Keys

from external_strings_utils import unicode_from_utf8
from . import __version__

DEFAULT_CONFIG = {
	"version": 1,
	"ratingUrl": "http://cfg.netradio.by/cgi-bin/ratingwot.cgi",
	"channels": [
		{
			"displayName": "netradio.by/wot",
			"stream_url": "http://sv.netradio.by:8061/128",
			"ext_url": "http://nr.by/wot",
			"tags_url": "http://sv.netradio.by:81/broad.xml"
		}
	]
}

DEFAULT_BINDINGS = {
	'broadcastHello': [Keys.KEY_L, [Keys.KEY_LCONTROL, Keys.KEY_RCONTROL]],
	'broadcastCurrent': [Keys.KEY_L],
	'likeCurrent': [Keys.KEY_Y],
	'dislikeCurrent': [Keys.KEY_U],
	'previosChannel': [Keys.KEY_PGDN],
	'nextChannel': [Keys.KEY_PGUP],
	'playRadio': [Keys.KEY_F9],
	'stopRadio': [Keys.KEY_F10],
	'volumeDown': [Keys.KEY_F11],
	'volumeUp': [Keys.KEY_F12]
}

DEFAULT_SETTINGS = {
	'saveVolume': True,
	'lastVolume': 0.5,
	'saveChannel': True,
	'lastChannel': 0,
	'muteOnVoip': False,
	'sendStatistic': True,
	'autoPlay': False,
	'showBattleTips': True,
	'muteOnMinimize': True,
	'keyBindings': DEFAULT_BINDINGS
}

DEFAULT_CACHE = {}

class CONFIG:
	SAVE_SETTINGS = True
	SAVE_CACHE = True
	CONFIG_URL = 'http://cfg.netradio.by/v1'
	EXPIRE_TIME = 6
	RATING_URL = 'http://cfg.netradio.by/cgi-bin/ratingwot.cgi'
	RATING_GATEWAY = '{url}?time={time}&{data}'

class PLAYER_STATUS:
	INITED = 'inited'
	ERROR = 'error'
	PLAYING = 'playing'
	STOPPED = 'stopped'

class PLAYER_COMMANDS:
	INIT = 'init'
	ADD_CHANNELS = 'add_channels'
	PLAY = 'play_channel'
	STOP = 'stop'
	VOLUME = 'volume'
	TEST = 'test'
	EXIT = 'exit'

class BUTTON_STATES:
	NORMAL = 'normal'
	SELECTED = 'selected'
	NORMAL_DISABLED = NORMAL + 'disabled'
	SELECTED_DISABLED = SELECTED + 'disabled'

class HOTKEYS_COMMANDS:
	START_ACCEPT = 'startAccept'
	STOP_ACCEPT = 'stopAccept'
	DEFAULT = 'default'
	CLEAN = 'clean'

BROADCAST_INTERVAL = 300
TAGS_UPDATE_INTERVAL = 20
VOLUME_STEP = 0.1
VOLUME_STEP_LOW = 0.05
VOLUME_STEP_VERY_LOW = 0.02

USER_AGENT = 'NetRadio-RadioPlayer/' + __version__

LOBBY_WINDOW_UI = 'NetRadioLobby'
BATTLE_INJECTOR_UI = 'NetRadioBattleInjector'
BATTLE_COMPONENT_UI = 'NetRadioBattle'

LANGUAGE_CODES = ('ru', 'uk', 'be', 'en', 'de', 'et', 'bg', 'da', 'fi', 'fil', 'fr', 'el', 'hu', 'id',
	'it', 'ja', 'ms', 'nl', 'no', 'pl', 'pt', 'pt_br', 'ro', 'sr', 'vi', 'zh_sg', 'zh_tw', 'hr', 'th',
	'lv', 'lt', 'cs', 'es_ar', 'tr', 'zh_cn', 'es', 'kk', 'sv', )

LANGUAGE_FILE_MASK = 'mods/me.poliroid.netradio/text/%s.yml'

DEFAULT_UI_LANGUAGE = 'ru'

prefsFilePath = unicode_from_utf8(BigWorld.wg_getPreferencesFilePath())[1]
SETTINGS_FILE = os.path.normpath(os.path.join(os.path.dirname(prefsFilePath), 'mods', 'netradio', 'setting.dat'))
CACHE_FILE = os.path.normpath(os.path.join(os.path.dirname(prefsFilePath), 'mods', 'netradio', 'cache.dat'))
CONFIG_CACHE_FILE = os.path.normpath(os.path.join(os.path.dirname(prefsFilePath), 'mods', 'netradio', 'config.dat'))

TEMP_DATA_FOLDER = os.path.normpath(os.path.join(tempfile.gettempdir(), 'world_of_tanks', 'netradio'))
TEMP_DATA_FOLDER_VFS = 'mods/me.poliroid.netradio/temp'

CONSOLE_PLAYER = os.path.normpath(os.path.join(TEMP_DATA_FOLDER, 'win32', 'net_radio_player.exe'))
if platform.architecture()[0] == '64bit':
	CONSOLE_PLAYER = os.path.normpath(os.path.join(TEMP_DATA_FOLDER, 'win64', 'net_radio_player.exe'))
MAX_RESTART_ATTEMPS = 10

# (r, g, b) color to AS3 Flash RGBHEX(uint)
DEFAULT_BATTLE_MESSAGE_COLOR = 116 << 16 | 199 << 8 | 48
DEFAULT_BATTLE_MESSAGE_LIFETIME = 4000

SETTINGS_VERSION = 1

UI_VOLUME_MULTIPLIYER = 10.0
