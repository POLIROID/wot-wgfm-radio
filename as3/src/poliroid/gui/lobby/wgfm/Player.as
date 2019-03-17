package poliroid.gui.lobby.wgfm 
{
	
	import flash.events.Event;
	import flash.events.KeyboardEvent;
	import flash.events.IEventDispatcher;
	import flash.ui.Keyboard;
	import flash.display.MovieClip;
	
	import scaleform.clik.events.InputEvent;
	
	import net.wg.gui.components.common.waiting.Waiting;
	
	import poliroid.gui.lobby.wgfm.components.PlayerPanel;
	import poliroid.gui.lobby.wgfm.data.HotkeysVO;
	import poliroid.gui.lobby.wgfm.data.LocalizationVO;
	import poliroid.gui.lobby.wgfm.data.SettingsVO;
	import poliroid.gui.lobby.wgfm.data.StateVO;
	import poliroid.gui.lobby.wgfm.events.WGFMEvent;
	import poliroid.gui.lobby.wgfm.events.WGFMValueEvent;
	import poliroid.gui.lobby.wgfm.interfaces.impl.PlayerMeta;
	
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
			
			addEventListener(WGFMEvent.VOLUME_CLICK, onVolumeClickHandler);
			addEventListener(WGFMEvent.PLAY_CLICK, onPlayClickHandler);
			addEventListener(WGFMEvent.PAUSE_CLICK, onPauseClickHandler);
			addEventListener(WGFMEvent.STATION_CLICK, onStationClickHandler);
			addEventListener(WGFMEvent.LIKE_CLICK, onLikeClickHandler);
			addEventListener(WGFMEvent.DISLIKE_CLICK, onDislikeClickHandler);
			addEventListener(WGFMEvent.CLOSE_CLICK, onCloseButtonClickHandler);
			addEventListener(WGFMEvent.DEFAULT_HOTKEYS_CLICK, onDefaultHotkeysClickHandler);
			addEventListener(WGFMValueEvent.VOLUME_CHANGED, onVolumeChanged);
			addEventListener(WGFMValueEvent.CHANNEL_CHANGED, onChannelChanged);
			addEventListener(WGFMValueEvent.SETTINGS_CHANGED, onSettingsChangedHandler);
			addEventListener(WGFMValueEvent.HOTKEY_CHANGED, onHotkeysChangedHandler);
			
			updatePositions();
		}
		
		override protected function onDispose() : void 
		{
			removeEventListener(WGFMEvent.VOLUME_CLICK, onVolumeClickHandler);
			removeEventListener(WGFMEvent.PLAY_CLICK, onPlayClickHandler);
			removeEventListener(WGFMEvent.PAUSE_CLICK, onPauseClickHandler);
			removeEventListener(WGFMEvent.STATION_CLICK, onStationClickHandler);
			removeEventListener(WGFMEvent.LIKE_CLICK, onLikeClickHandler);
			removeEventListener(WGFMEvent.DISLIKE_CLICK, onDislikeClickHandler);
			removeEventListener(WGFMEvent.CLOSE_CLICK, onCloseButtonClickHandler);
			removeEventListener(WGFMEvent.DEFAULT_HOTKEYS_CLICK, onDefaultHotkeysClickHandler);
			removeEventListener(WGFMValueEvent.VOLUME_CHANGED, onVolumeChanged);
			removeEventListener(WGFMValueEvent.CHANNEL_CHANGED, onChannelChanged);
			removeEventListener(WGFMValueEvent.SETTINGS_CHANGED, onSettingsChangedHandler);
			removeEventListener(WGFMValueEvent.HOTKEY_CHANGED, onHotkeysChangedHandler);
			
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
		
		private function onPlayClickHandler(e:WGFMEvent) : void
		{
			radioPauseS();
		}
		
		private function onPauseClickHandler(e:WGFMEvent) : void
		{
			radioPlayS();
		}
		
		private function onVolumeClickHandler(e:WGFMEvent) : void
		{
			updateMutedS();
		}
		
		private function onStationClickHandler(e:WGFMEvent) : void
		{
			openExternalS();
		}
		
		private function onLikeClickHandler(e:WGFMEvent) : void
		{
			updateRatingS(true);
		}
		
		private function onDislikeClickHandler(e:WGFMEvent) : void
		{
			updateRatingS(false);
		}
		
		private function onVolumeChanged(e:WGFMValueEvent) : void
		{
			updateVolumeS(e.value);
		}
		
		private function onChannelChanged(e:WGFMValueEvent) : void
		{
			updateChannelS(e.value);
		}
		
		private function onCloseButtonClickHandler(e:WGFMEvent) : void
		{
			closeViewS();
		}
		
		private function onSettingsChangedHandler(e:WGFMValueEvent) : void
		{
			updateSettingsS(e.name, e.value);
		}
		
		private function onHotkeysChangedHandler(e:WGFMValueEvent) : void
		{
			updateHotkeysS(e.name, e.value);
		}
		
		private function onDefaultHotkeysClickHandler(e:WGFMEvent) : void
		{
			defaultHotkeysS();
		}
	}
}
