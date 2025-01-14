# SPDX-License-Identifier: MIT
# Copyright (c) 2015-2025 Andrii Andrushchyshyn

import Event

__all__ = ('g_eventsManager', )

class EventsManager(object):

	def __init__(self):

		self.showBattleMessage = Event.Event()

		self.onAppFinish = Event.Event()
		self.onShowBattlePage = Event.Event()
		self.onDestroyBattle = Event.Event()
		self.onSetVoipActive = Event.Event()

		self.onChannelsUpdated = Event.Event()

		self.onRatingsUpdated = Event.Event()

		self.onRadioTagChanged = Event.Event()
		self.onRadioChannelChanged = Event.Event()
		self.onRadioStatusUpdated = Event.Event()

		self.onVolumeChanged = Event.Event()
		self.onVolumeChangedHidden = Event.Event()

		self.onKeyEvent = Event.Event()
		self.onHotkeysChanged = Event.Event()

g_eventsManager = EventsManager()
