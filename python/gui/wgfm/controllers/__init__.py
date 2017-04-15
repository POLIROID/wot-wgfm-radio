
from gui.wgfm.events import g_eventsManager

__all__ = ('g_controllers', )

class ControllersHolder():
	
	announcer = None
	battle = None
	channel = None
	hotkey = None
	player = None
	rating = None
	volume = None
	
	def init(self):
		
		from gui.wgfm.controllers.announcer import AnnounceController
		from gui.wgfm.controllers.battle import BattleController
		from gui.wgfm.controllers.channel import ChannelController
		from gui.wgfm.controllers.hotkey import HotkeyController
		from gui.wgfm.controllers.player import PlayerController
		from gui.wgfm.controllers.rating import RatingController
		from gui.wgfm.controllers.volume import VolumeController

		self.announcer = AnnounceController()
		self.battle = BattleController()
		self.channel = ChannelController()
		self.hotkey = HotkeyController()
		self.player = PlayerController()
		self.rating = RatingController()
		self.volume = VolumeController()

		self.announcer.init()
		self.battle.init()
		self.channel.init()
		self.hotkey.init()
		self.player.init()
		self.rating.init()
		self.volume.init()
		
		g_eventsManager.onAppFinish += self.fini
		
	def fini(self):
		
		self.announcer.fini()
		self.battle.fini()
		self.channel.fini()
		self.hotkey.fini()
		self.player.fini()
		self.rating.fini()
		self.volume.fini()
		
		self.announcer = None
		self.battle = None
		self.channel = None
		self.hotkey = None
		self.player = None
		self.rating = None
		self.volume = None

g_controllers = ControllersHolder()