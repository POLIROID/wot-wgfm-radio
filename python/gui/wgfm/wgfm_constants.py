
import os
import Keys
import tempfile
import BigWorld

DEFAULT_CONFIG = {
    "version": 1,
    "updateUrl": "http://res-mods.ru/mod/46093",
    "ratingUrl"    :"http://cfg.wargaming.fm/cgi-bin/ratingwot.cgi",
    "channels": [
        {
            "displayName": "WGFM Main",
            "stream_url": "http://sv.wargaming.fm:8061/128",
            "ext_url": "http://wargaming.fm/1",
            "tags_url": "http://sv.wargaming.fm:81/broad.xml"
        },
        {
            "displayName": "WGFM Music only",
            "stream_url": "http://sv.wargaming.fm:8062/128",
            "ext_url": "http://wargaming.fm/2",
            "tags_url": "http://sv.wargaming.fm:82/broad.xml"
        },
        {
            "displayName": "WGFM Trance",
            "stream_url": "http://sv.wargaming.fm:8063/128",
            "ext_url": "http://wargaming.fm/3",
            "tags_url": "http://sv.wargaming.fm:83/broad.xml"
        },
        {
            "displayName": "WGFM Rock",
            "stream_url": "http://sv.wargaming.fm:8064/128",
            "ext_url": "http://wargaming.fm/4",
            "tags_url": "http://sv.wargaming.fm:84/broad.xml"
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
	'lastVolume': 1.0,
	'saveChannel': True,
	'lastChannel': 0,
	'muteOnVoip': False,
	'sendStatistic': True,
	'autoPlay': False,
	'showBattleTips': True,
	'isModpack': False,
	'muteOnMinimize': True,
	'keyBindings': DEFAULT_BINDINGS
}

DEFAULT_CACHE = {
	'announced_ids': []
}

class CONFIG:
	SAVE_SETTINGS = True
	SAVE_CACHE = True
	CONFIG_URL = 'http://cfg.wargaming.fm/v1'
	EXPIRE_TIME = 6
	RATING_GATEWAY = '{url}?time={time}&{data}'

class APIv2:
	BASE_URL = 'http://wgfm.wgmods.org/api'
	ANNOUNCE_GATEWAY = '/announcements'

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
ANNOUNCMENTS_UPDATE_INTERVAL = 15 * 60
VOLUME_STEP = 0.1
VOLUME_STEP_LOW = 0.05
VOLUME_STEP_VERY_LOW = 0.02
MOD_VERSION = '3.3.1'
MOD_VERSION_NUM = 7
USER_AGENT = 'WGFM-RadioPlayer/' + MOD_VERSION

WGFM_LOBBY_WINDOW_UI = 'wgfmLobby'
WGFM_BATTLE_INJECTOR_UI = 'wgfmBattleInjector'
WGFM_BATTLE_COMPONENTS_UI = 'wgfmBattle'

LANGUAGE_CODES = ('ru', 'uk', 'be', 'en', 'de', 'et', 'bg', 'da', 'fi', 'fil', 'fr', 'el', 'hu', 'id', \
	'it', 'ja', 'ms', 'nl', 'no', 'pl', 'pt', 'pt_br', 'ro', 'sr', 'vi', 'zh_sg', 'zh_tw', 'hr', 'th', \
	'lv', 'lt', 'cs', 'es_ar', 'tr', 'zh_cn', 'es', 'kk', 'sv', )

LANGUAGE_FILE_PATH = 'mods/net.wargaming.wgfmradio/text/%s.yml'

DEFAULT_UI_LANGUAGE = 'ru'

wgAppDataFolder = os.path.normpath(os.path.join(os.path.dirname(unicode(BigWorld.wg_getPreferencesFilePath(), 'utf-8', errors='ignore'))))
SETTINGS_FILE = "%s\\wgfm\\%s" % (wgAppDataFolder, 'setting.dat')
CONFIG_CACHE_FILE = "%s\\wgfm\\%s" % (wgAppDataFolder, 'config.dat')
CACHE_FILE = "%s\\wgfm\\%s" % (wgAppDataFolder, 'cache.dat')

TEMP_DATA_FOLDER = '%s\\world_of_tanks\\%s' % (tempfile.gettempdir(), 'wgfm')
TEMP_DATA_FOLDER_VFS = 'mods/net.wargaming.wgfmradio/temp'

CONSOLE_PLAYER = '%s\\wgfm_player.exe' % TEMP_DATA_FOLDER 

# RED = 14753553; GREEN = 7653168; YELLOW = 16745752; PURPLE = 8886779
DEFAULT_BATTLE_MESSAGE_COLOR = 7653168
DEFAULT_BATTLE_MESSAGE_LIFETIME = 4000

UI_VOLUME_MULTIPLIYER = 10.0

del wgAppDataFolder, os, Keys, tempfile, BigWorld
