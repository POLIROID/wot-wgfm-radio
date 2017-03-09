
from gui.wgfm.events import g_eventsManager

__all__ = ('g_controllers', )

class ControllersHolder():
	
	battle = None
	channel = None
	player = None
	rating = None
	volume = None
	hotkey = None
	
	def init(self):
		
		from gui.wgfm.controllers.battle import BattleController
		from gui.wgfm.controllers.channel import ChannelController
		from gui.wgfm.controllers.player import PlayerController
		from gui.wgfm.controllers.rating import RatingController
		from gui.wgfm.controllers.volume import VolumeController
		from gui.wgfm.controllers.hotkey import HotkeyController

		self.battle = BattleController()
		self.channel = ChannelController()
		self.player = PlayerController()
		self.rating = RatingController()
		self.volume = VolumeController()
		self.hotkey = HotkeyController()

		self.battle.init()
		self.channel.init()
		self.player.init()
		self.rating.init()
		self.volume.init()
		self.hotkey.init()
		
		g_eventsManager.onAppFinish += self.fini
		
	def fini(self):

		self.battle.fini()
		self.channel.fini()
		self.player.fini()
		self.rating.fini()
		self.volume.fini()
		self.hotkey.fini()
		
		self.battle = None
		self.channel = None
		self.player = None
		self.rating = None
		self.volume = None
		self.hotkey = None

g_controllers = ControllersHolder()