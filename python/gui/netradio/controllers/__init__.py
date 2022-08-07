from gui.netradio.events import g_eventsManager

__all__ = ('g_controllers', )

class ControllersHolder():

	battle = None
	channel = None
	hotkey = None
	player = None
	rating = None
	volume = None

	def init(self):

		from gui.netradio.controllers.battle import BattleController
		from gui.netradio.controllers.channel import ChannelController
		from gui.netradio.controllers.hotkey import HotkeyController
		from gui.netradio.controllers.player import PlayerController
		from gui.netradio.controllers.rating import RatingController
		from gui.netradio.controllers.volume import VolumeController

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
