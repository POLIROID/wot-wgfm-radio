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
		
		public function updateState(state:StateVO) : void 
		{
			playButton.playing = state.isPlaying;
			
			volumeButton.volume = state.currentVolume;
			volumeButton.muted = state.isMuted;
			
			volumeSlider.value = state.currentVolume;
			volumeSlider.enabled = !state.isError && !state.isMuted;
			
			stationsDropdown.selectedIndex = state.currentChannelIdx;
			stationsDropdown.enabled = !state.isError;
			
			playButton.enabled = !state.isError;
			volumeButton.enabled = !state.isError;
		}
		
		private function handleVolumeSlider(e:SliderEvent) : void 
		{
			var volume:Number = volumeSlider.value;
			dispatchEvent(new WGFMValueEvent(WGFMValueEvent.VOLUME_CHANGED, '', volume));
		}
		
		private function handleStationsDropdown(e:ListEvent) : void 
		{
			var channelIdx:Number = stationsDropdown.selectedIndex;
			dispatchEvent(new WGFMValueEvent(WGFMValueEvent.CHANNEL_CHANGED, '', channelIdx));
		}
		
	}
}