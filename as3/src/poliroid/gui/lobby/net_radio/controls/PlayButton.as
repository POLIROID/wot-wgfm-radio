package poliroid.gui.lobby.net_radio.controls {
	
	import scaleform.clik.events.ButtonEvent;
	
	import net.wg.gui.components.controls.SoundButton;
	import net.wg.gui.interfaces.ISoundButton;
	
	import poliroid.gui.lobby.net_radio.events.NetRadioEvent;
	
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
					dispatchEvent(new NetRadioEvent(NetRadioEvent.PLAY_CLICK));
				else
					dispatchEvent(new NetRadioEvent(NetRadioEvent.PAUSE_CLICK));
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