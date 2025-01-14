# SPDX-License-Identifier: MIT
# Copyright (c) 2015-2025 Andrii Andrushchyshyn

from ..events import g_eventsManager

__all__ = ('g_controllers', )

class ControllersHolder():

	battle = None
	channel = None
	hotkey = None
	player = None
	rating = None
	volume = None

	def init(self):

		from .battle import BattleController
		from .channel import ChannelController
		from .hotkey import HotkeyController
		from .player import PlayerController
		from .rating import RatingController
		from .volume import VolumeController

		self.battle = BattleController()
		self.channel = ChannelController()
		self.hotkey = HotkeyController()
		self.player = PlayerController()
		self.rating = RatingController()
		self.volume = VolumeController()

		self.battle.init()
		self.channel.init()
		self.hotkey.init()
		self.player.init()
		self.rating.init()
		self.volume.init()

		g_eventsManager.onAppFinish += self.fini

	def fini(self):

		self.battle.fini()
		self.channel.fini()
		self.hotkey.fini()
		self.player.fini()
		self.rating.fini()
		self.volume.fini()

		self.battle = None
		self.channel = None
		self.hotkey = None
		self.player = None
		self.rating = None
		self.volume = None

g_controllers = ControllersHolder()
