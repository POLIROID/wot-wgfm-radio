
from constants import DEFAULT_LANGUAGE
from helpers import getClientLanguage

from gui.wgfm.wgfm_constants import DEFAULT_UI_LANGUAGE

__all__ = ('l10n', )

_LANGUAGES = {
	'ru': { # русский
		'#error_working_dir': 'Ошибка. Файлы мода не найдены!',
		'#error_local_radio_url': 'Ошибка. Чтото блокирует файлу wgfm_player.exe доступ к сети интернет.',
		'#error_cache': 'Ошибка. Не удалось получить ссылку на вещание!',
		'#error_wgfm_url': 'Ошибка. Радио Wargaming.Fm недоступно!',
		'#error_stream_tags': 'Ошибка. Нет соединения с WarGaming.Fm. Вещание будет восстановлено в ближайшее время!',	
		
		'#battle_tips_cooldown': 'Вещать в чат можно не чаще чем раз в 5 минут',
		'#battle_tips_rating': 'Спасибо. Ваш голос учтён!',
		'#battle_player_volumeup': 'Громкость увеличена',
		'#battle_player_volumedown': 'Громкость уменьшена',
		'#battle_player_stop': 'Радио-плеер остановлен',
		'#battle_player_loading': 'Загрузка...',
		
		'#battle_tips_control_1': 'Включить Wargaming.FM — [{playRadio}], выключить — [{stopRadio}]',
		'#battle_tips_control_2': 'Переключайте каналы Wargaming.FM в бою клавишами [{nextChannel}] и [{previosChannel}]',
		'#battle_tips_control_3': 'Регулируйте громкость Wargaming.FM клавишами [{volumeDown}] — тише, и [{volumeUp}] — громче',
		'#battle_tips_control_4': 'Вечернее шоу начинается в 19:00 МСК. Включайте Wargaming.FM',
		'#battle_tips_control_5': 'Нравится трек — жми лайк [{likeCurrent}] хочешь убрать из эфира песню — жми дизлайк [{dislikeCurrent}]',
		'#battle_tips_control_6': 'Настраивайте удобную для вас громкость в бою клавишами [{volumeDown}] и [{volumeUp}]',
		'#battle_tips_control_7': 'Включить хорошее настроение в бою можно клавишей [{playRadio}]',
		
		'#battle_broadcast_track_1': 'Танкуем под [%s] на Wargaming.FM!',
		'#battle_broadcast_track_2': 'Тащим до победы вместе с [%s] на Wargaming.FM!',
		'#battle_broadcast_track_3': 'Включай [%s] на Wargaming.FM!',
		'#battle_broadcast_track_4': 'Мне нравится! Присоединяйся! [%s] на Wargaming.FM!',
		'#battle_broadcast_track_5': 'Выбери музыку для победы! [%s] на Wargaming.FM!',
		
		'#battle_broadcast_hello_1': 'Всем #хорошейигры!',
		'#battle_broadcast_hello_2': 'Мы все хотим #хорошейигры! Так желаю же вам удачи!',
		'#battle_broadcast_hello_3': '#хорошейигры вам, танкисты!',
		'#battle_broadcast_hello_4': '#хорошейигры много не бывает! Удачи!',
		
		'#modslist_name': 'WarGaming.FM',
		'#modslist_description': 'Слушайте радио WarGaming.FM прямо в клиенте игры',
		
		'#ui_waiting_grabbingData': 'Получение данных',
		'#ui_title': 'Wargaming.FM',
		'#ui_closeButton': 'ЗАКРЫТЬ',
		
		'#ui_settings_title': 'Другие настройки',
		'#ui_settings_label_saveVolume': 'Запомнить громкость',
		'#ui_settings_label_saveChannel': 'Запомнить выбранный канал',
		'#ui_settings_label_muteOnVoip': 'Использовать настройки VOIP',
		'#ui_settings_label_autoPlay': 'Авто-воспроизведение при старте',
		'#ui_settings_label_sendStatistic': 'Отправлять статистику',
		'#ui_settings_label_showBattleTips': 'Отображать подсказки в бою',
		'#ui_settings_tooltip_saveVolume': '{HEADER}Запомнить громкость{/HEADER}{BODY}При следующем включении громкость останется на том же уровне{/BODY}',
		'#ui_settings_tooltip_saveChannel': '{HEADER}Запомнить выбранный канал{/HEADER}{BODY}При следующем включении звучать будет последний выбранный вами канал{/BODY}',
		'#ui_settings_tooltip_muteOnVoip': '{HEADER}Использовать настройки VOIP{/HEADER}{BODY}При использовании внутриигровой связи радио будет приглушаться. Уровень приглушения зависит от настройки "Общий уровень громкости окружения во время разговора" в игровом клиенте{/BODY}',
		'#ui_settings_tooltip_autoPlay': '{HEADER}Авто-воспроизведение при старте{/HEADER}{BODY}При запуске клиента радио будет автоматически включаться{/BODY}',
		'#ui_settings_tooltip_sendStatistic': '{HEADER}Отправлять статистику{/HEADER}{BODY}Помогите нам улучшить радио, отправив нам статистику его использования вами!{/BODY}',
		'#ui_settings_tooltip_showBattleTips': '{HEADER}Отображать подсказки в бою{/HEADER}{BODY}Вот сюда текст тоже надо завезти, а не только название{/BODY}',
		
		'#ui_hotkeys_title': 'Горячие клавиши',
		'#ui_hotkeys_defaultLink': 'Стандартные настройки',
		'#ui_hotkeys_cmdDefault': 'По умолчанию',
		'#ui_hotkeys_cmdClean': 'Очистить',
		'#ui_hotkeys_playRadio': 'Начать воспроизведение',
		'#ui_hotkeys_stopRadio': 'Остановить радио',
		'#ui_hotkeys_volumeUp': 'Увеличить громкость',
		'#ui_hotkeys_volumeDown': 'Уменьшить громкость',
		'#ui_hotkeys_nextChannel': 'Следующий канал',
		'#ui_hotkeys_previosChannel': 'Предыдущий канал',
		'#ui_hotkeys_broadcastCurrent': 'Вещание песни в чат',
		'#ui_hotkeys_likeCurrent': 'Мне нравится!',
		'#ui_hotkeys_dislikeCurrent': 'Мне не нравится',
		'#ui_hotkeys_broadcastHello': 'Пожелать хорошей игры',
	},
	'uk': {}, # украинский
	'be': {}, # белорусский
	'en': {}, # английский
	'de': {}, # немецкий
	'et': {}, # эстонский
	'bg': {}, # болгарский
	'da': {}, # датский
	'fi': {}, # финский
	'fil': {}, # филиппинский
	'fr': {}, # французский
	'el': {}, # греческий
	'hu': {}, # венгерский
	'id': {}, # индонезийский
	'it': {}, # италийский
	'ja': {}, # японский
	'ms': {}, # малайский
	'nl': {}, # нидерландский
	'no': {}, # норвежский
	'pl': {}, # польский
	'pt': {}, # португальский
	'pt_br': {}, # португальско-бразилийский
	'ro': {}, # румынский
	'sr': {}, # боснийский
	'vi': {}, # вьетнамский
	'zh_sg': {}, # китайский-сингапур
	'zh_tw': {}, # китайский-тайвань
	'hr': {}, # хорватский
	'th': {}, # тайский
	'lv': {}, # латишский
	'lt': {}, # литовский
	'cs': {}, # чешский
	'es_ar': {}, # испанский-аргентинский
	'tr': {}, # турецкий
	'zh_cn': {}, # китайский
	'es': {}, # испанский
	'kk': {}, # казахский
	'sv': {} # шведский
}

_CLIENT_LANGUAGE = getClientLanguage()
if _CLIENT_LANGUAGE in _LANGUAGES.keys():
	_LANGUAGE = _LANGUAGES[_CLIENT_LANGUAGE]
elif DEFAULT_LANGUAGE in _LANGUAGES.keys():
	_LANGUAGE = _LANGUAGES[DEFAULT_LANGUAGE]
else:
	_LANGUAGE = _LANGUAGES[DEFAULT_UI_LANGUAGE]

def l10n(key):
	'''returns localized value relative to key'''
	if key in _LANGUAGE:
		return _LANGUAGE[key]
	elif key in _LANGUAGES[DEFAULT_UI_LANGUAGE]:
		return _LANGUAGES[DEFAULT_UI_LANGUAGE][key]
	else:
		return key.replace('#', '')
	