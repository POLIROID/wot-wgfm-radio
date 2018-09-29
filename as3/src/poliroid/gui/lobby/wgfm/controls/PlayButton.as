package poliroid.gui.lobby.wgfm.controls {
	
	import scaleform.clik.events.ButtonEvent;
	
	import net.wg.gui.components.controls.SoundButton;
	import net.wg.gui.interfaces.ISoundButton;
	
	import poliroid.gui.lobby.wgfm.events.WGFMEvent;
	
	public class PlayButton extends SoundButton implements ISoundButton 
	{
		
		private var _playing:Boolean = false;
		
		public function PlayButton() 
		{
			super();
			focusable = false;
		}
		
		override protected function configUI() : void
		{
			super.configUI();
			addEventListener(ButtonEvent.CLICK, handleButtonClick);			
		}
		
		override protected function onDispose() : void
		{
			removeEventListener(ButtonEvent.CLICK, handleButtonClick);
			super.onDispose();	
		}
		
		private function handleButtonClick(e:ButtonEvent) : void 
		{
			if (enabled)
			{
				if (playing)
					dispatchEvent(new WGFMEvent(WGFMEvent.PLAY_CLICK));
				else
					dispatchEvent(new WGFMEvent(WGFMEvent.PAUSE_CLICK));
			}
		}
		
		override protected function getStatePrefixes() : Vector.<String>
		{
			if (playing)
				return Vector.<String>(['pause_', '']);
			else
				return Vector.<String>(['play_', '']);
		}
		
		public function set playing(isPlaying:Boolean) : void
		{
			if(_playing == isPlaying)
				return;
			
			_playing = isPlaying;
			
			setState(state == "over"? "up": state);
		}
		
		public function get playing() : Boolean
		{
			return _playing;
		}
		
	}

}