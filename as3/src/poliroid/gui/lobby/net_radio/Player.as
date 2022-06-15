package poliroid.gui.lobby.net_radio
{
	
	import flash.events.Event;
	import flash.events.KeyboardEvent;
	import flash.events.IEventDispatcher;
	import flash.ui.Keyboard;
	import flash.display.MovieClip;
	
	import scaleform.clik.events.InputEvent;
	
	import net.wg.gui.components.common.waiting.Waiting;
	
	import poliroid.gui.lobby.net_radio.components.PlayerPanel;
	import poliroid.gui.lobby.net_radio.data.HotkeysVO;
	import poliroid.gui.lobby.net_radio.data.LocalizationVO;
	import poliroid.gui.lobby.net_radio.data.SettingsVO;
	import poliroid.gui.lobby.net_radio.data.StateVO;
	import poliroid.gui.lobby.net_radio.events.NetRadioEvent;
	import poliroid.gui.lobby.net_radio.events.NetRadioValueEvent;
	import poliroid.gui.lobby.net_radio.interfaces.impl.PlayerMeta;
	
	public class Player extends PlayerMeta implements IEventDispatcher 
	{
		
		public var waiting:Waiting = null;
		
		public var background:MovieClip = null;
		
		public var player:PlayerPanel = null;
		
		public function Player()
		{
			super();
		}
		
		override protected function onPopulate() : void 
		{
			super.onPopulate();
			
			App.stage.addEventListener(Event.RESIZE, updatePositions);
			
			addEventListener(NetRadioEvent.VOLUME_CLICK, onVolumeClickHandler);
			addEventListener(NetRadioEvent.PLAY_CLICK, onPlayClickHandler);
			addEventListener(NetRadioEvent.PAUSE_CLICK, onPauseClickHandler);
			addEventListener(NetRadioEvent.STATION_CLICK, onStationClickHandler);
			addEventListener(NetRadioEvent.LIKE_CLICK, onLikeClickHandler);
			addEventListener(NetRadioEvent.DISLIKE_CLICK, onDislikeClickHandler);
			addEventListener(NetRadioEvent.CLOSE_CLICK, onCloseButtonClickHandler);
			addEventListener(NetRadioEvent.DEFAULT_HOTKEYS_CLICK, onDefaultHotkeysClickHandler);
			addEventListener(NetRadioValueEvent.VOLUME_CHANGED, onVolumeChanged);
			addEventListener(NetRadioValueEvent.CHANNEL_CHANGED, onChannelChanged);
			addEventListener(NetRadioValueEvent.SETTINGS_CHANGED, onSettingsChangedHandler);
			addEventListener(NetRadioValueEvent.HOTKEY_CHANGED, onHotkeysChangedHandler);
			
			updatePositions();
		}
		
		override protected function onDispose() : void 
		{
			removeEventListener(NetRadioEvent.VOLUME_CLICK, onVolumeClickHandler);
			removeEventListener(NetRadioEvent.PLAY_CLICK, onPlayClickHandler);
			removeEventListener(NetRadioEvent.PAUSE_CLICK, onPauseClickHandler);
			removeEventListener(NetRadioEvent.STATION_CLICK, onStationClickHandler);
			removeEventListener(NetRadioEvent.LIKE_CLICK, onLikeClickHandler);
			removeEventListener(NetRadioEvent.DISLIKE_CLICK, onDislikeClickHandler);
			removeEventListener(NetRadioEvent.CLOSE_CLICK, onCloseButtonClickHandler);
			removeEventListener(NetRadioEvent.DEFAULT_HOTKEYS_CLICK, onDefaultHotkeysClickHandler);
			removeEventListener(NetRadioValueEvent.VOLUME_CHANGED, onVolumeChanged);
			removeEventListener(NetRadioValueEvent.CHANNEL_CHANGED, onChannelChanged);
			removeEventListener(NetRadioValueEvent.SETTINGS_CHANGED, onSettingsChangedHandler);
			removeEventListener(NetRadioValueEvent.HOTKEY_CHANGED, onHotkeysChangedHandler);
			
			App.stage.removeEventListener(Event.RESIZE, updatePositions);
			
			super.onDispose();
		}
		
		private function updatePositions() : void
		{
			var appWidth:Number = App.appWidth;
			var appHeight:Number = App.appHeight;
			
			background.width = appWidth;
			background.height = appHeight;
			
			if (waiting)
			{
				waiting.setSize(appWidth, appHeight);
			}
			
			player.x = int((appWidth - 300) / 2);
			player.y = int((appHeight / 2) - 200);
			player.updatePositions();
		}
		
		override protected function showWaiting(message:String) : void
		{
			if (!waiting) 
			{
				waiting = new Waiting();
				addChild(waiting);
			}
			waiting.setMessage(message);
			waiting.setSize(App.appWidth, App.appHeight);
			waiting.validateNow();
			waiting.show();
		}
		
		override protected function hideWaiting() : void
		{
			if (waiting)
			{
				waiting.hide();
				removeChild(waiting);
				waiting = null;
			}
		}
		
		override protected function setState(newState:StateVO) : void
		{
			player.updateState(newState);
		}
		
		override protected function setChannels(channels:Array) : void
		{
			player.updateChannels(channels);
		}
		
		override protected function setHotkeys(ctx:HotkeysVO) : void
		{
			player.updateHotkeys(ctx);
		}
		
		override protected function setSettings(data:SettingsVO) : void
		{
			player.setSettings(data);
		}
		
		override protected function setLocalization(data:LocalizationVO) : void
		{
			player.setLocalization(data);
		}
		
		private function onPlayClickHandler(e:NetRadioEvent) : void
		{
			radioPauseS();
		}
		
		private function onPauseClickHandler(e:NetRadioEvent) : void
		{
			radioPlayS();
		}
		
		private function onVolumeClickHandler(e:NetRadioEvent) : void
		{
			updateMutedS();
		}
		
		private function onStationClickHandler(e:NetRadioEvent) : void
		{
			openExternalS();
		}
		
		private function onLikeClickHandler(e:NetRadioEvent) : void
		{
			updateRatingS(true);
		}
		
		private function onDislikeClickHandler(e:NetRadioEvent) : void
		{
			updateRatingS(false);
		}
		
		private function onVolumeChanged(e:NetRadioValueEvent) : void
		{
			updateVolumeS(e.value);
		}
		
		private function onChannelChanged(e:NetRadioValueEvent) : void
		{
			updateChannelS(e.value);
		}
		
		private function onCloseButtonClickHandler(e:NetRadioEvent) : void
		{
			closeViewS();
		}
		
		private function onSettingsChangedHandler(e:NetRadioValueEvent) : void
		{
			updateSettingsS(e.name, e.value);
		}
		
		private function onHotkeysChangedHandler(e:NetRadioValueEvent) : void
		{
			updateHotkeysS(e.name, e.value);
		}
		
		private function onDefaultHotkeysClickHandler(e:NetRadioEvent) : void
		{
			defaultHotkeysS();
		}
	}
}
