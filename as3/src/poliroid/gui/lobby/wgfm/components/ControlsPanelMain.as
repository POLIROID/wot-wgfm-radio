package poliroid.gui.lobby.wgfm.components {
	
	import scaleform.clik.events.SliderEvent;
	import scaleform.clik.events.ListEvent;
	
	import net.wg.infrastructure.base.UIComponentEx;
	import net.wg.gui.components.controls.DropdownMenu;
	import net.wg.gui.components.controls.Slider;
	
	import poliroid.gui.lobby.wgfm.controls.PlayButton;
	import poliroid.gui.lobby.wgfm.controls.VolumeButton;
	import poliroid.gui.lobby.wgfm.events.WGFMValueEvent;
	
	import poliroid.gui.lobby.wgfm.data.StateVO;
	
	public class ControlsPanelMain extends UIComponentEx
	{
		
		public var playButton:PlayButton = null;
		
		public var volumeButton:VolumeButton = null;
		
		public var volumeSlider:Slider = null;
		
		public var stationsDropdown:DropdownMenu = null;
		
		public function ControlsPanelMain()
		{
			super();
		}
		
		override protected function configUI() : void 
		{
			super.configUI();
			
			volumeSlider.focusable = false;
			stationsDropdown.focusable = false;
			
			volumeSlider.addEventListener(SliderEvent.VALUE_CHANGE, handleVolumeSlider);
			stationsDropdown.addEventListener(ListEvent.INDEX_CHANGE, handleStationsDropdown);
		}
		
		override protected function onDispose() : void 
		{
			volumeSlider.removeEventListener(SliderEvent.VALUE_CHANGE, handleVolumeSlider);
			stationsDropdown.removeEventListener(ListEvent.INDEX_CHANGE, handleStationsDropdown);
			
			playButton = null;
			volumeButton = null;
			volumeSlider = null;
			stationsDropdown = null;
			
			super.onDispose();
		}
		
		public function updateState(oldState:StateVO, newState:StateVO) : void 
		{
			playButton.playing = newState.isPlaying;
			
			volumeButton.volume = newState.currentVolume;
			volumeButton.muted = newState.isMuted;
			
			volumeSlider.value = newState.currentVolume;
			volumeSlider.enabled = !newState.isError && !newState.isMuted;
			
			stationsDropdown.selectedIndex = newState.currentChannelIdx;
			stationsDropdown.enabled = !newState.isError;
			
			playButton.enabled = !newState.isError;
			volumeButton.enabled = !newState.isError;
		}
		
		private function handleVolumeSlider(e:SliderEvent) : void 
		{
			var volume:Number = volumeSlider.value;
			dispatchEvent(new WGFMValueEvent(WGFMValueEvent.VOLUME_CHANGED, volume));
		}
		
		private function handleStationsDropdown(e:ListEvent) : void 
		{
			var channelIdx:Number = stationsDropdown.selectedIndex;
			dispatchEvent(new WGFMValueEvent(WGFMValueEvent.CHANNEL_CHANGED, channelIdx));
		}
		
	}
}