package poliroid.gui.lobby.net_radio.components {
	
	import scaleform.clik.events.SliderEvent;
	import scaleform.clik.events.ListEvent;
	
	import net.wg.infrastructure.base.UIComponentEx;
	import net.wg.gui.components.controls.DropdownMenu;
	import net.wg.gui.components.controls.Slider;
	
	import poliroid.gui.lobby.net_radio.controls.PlayButton;
	import poliroid.gui.lobby.net_radio.controls.VolumeButton;
	import poliroid.gui.lobby.net_radio.events.NetRadioValueEvent;
	
	import poliroid.gui.lobby.net_radio.data.StateVO;
	
	public class ControlsPanelMain extends UIComponentEx
	{
		
		public var playButton:PlayButton = null;
		
		public var volumeButton:VolumeButton = null;
		
		public var volumeSlider:Slider = null;
		
		public function ControlsPanelMain()
		{
			super();
		}
		
		override protected function configUI() : void 
		{
			super.configUI();
			
			volumeSlider.focusable = false;
			
			volumeSlider.addEventListener(SliderEvent.VALUE_CHANGE, handleVolumeSlider);
		}
		
		override protected function onDispose() : void 
		{
			volumeSlider.removeEventListener(SliderEvent.VALUE_CHANGE, handleVolumeSlider);
			
			playButton = null;
			volumeButton = null;
			volumeSlider = null;
			
			super.onDispose();
		}
		
		public function updateState(state:StateVO) : void 
		{
			playButton.playing = state.isPlaying;
			
			volumeButton.volume = state.currentVolume;
			volumeButton.muted = state.isMuted;
			
			volumeSlider.value = state.currentVolume;
			volumeSlider.enabled = !state.isError && !state.isMuted;
			
			playButton.enabled = !state.isError;
			volumeButton.enabled = !state.isError;
		}
		
		private function handleVolumeSlider(e:SliderEvent) : void 
		{
			var volume:Number = volumeSlider.value;
			dispatchEvent(new NetRadioValueEvent(NetRadioValueEvent.VOLUME_CHANGED, '', volume));
		}
	
	}
}