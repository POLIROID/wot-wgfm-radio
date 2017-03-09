package com.poliroid.gui.lobby.wgfm.controls {
	
	import flash.display.MovieClip;
	import scaleform.clik.events.ButtonEvent;
	
	import net.wg.gui.components.controls.SoundButton;
	import net.wg.gui.interfaces.ISoundButton;
	
	import com.poliroid.gui.lobby.wgfm.events.WGFMEvent;
	
	public class VolumeButton extends SoundButton implements ISoundButton 
	{
		private var _volume:Number = -1;
		private var _muted:Boolean = false;
		
		public function VolumeButton() 
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
				dispatchEvent(new WGFMEvent(WGFMEvent.VOLUME_CLICK, true));
			}
		}
		
		override protected function getStatePrefixes() : Vector.<String>
		{
			if (muted)
				return Vector.<String>(['muted_', '']);
			else if (volume >= 7.0)
				return Vector.<String>(['volume_max_', '']);
			else if (volume >= 3.0)
				return Vector.<String>(['volume_mid_', '']);
			else if (volume > 0.0)
				return Vector.<String>(['volume_min_', '']);
			else
				return Vector.<String>(['volume_none_', '']);
		}
		
		public function get muted() : Boolean
		{
			return _muted;
		}
		
		public function set muted(isMuted:Boolean) : void
		{
			if(_muted == isMuted)
				return;
			
			_muted = isMuted;
			
			setState(state);
		}
		
		public function get volume() : Number
		{
			return _volume;
		}
		
		public function set volume(newVolume:Number) : void
		{
			if(_volume == newVolume)
				return;
			
			_volume = newVolume;
			
			setState('up');
		}
	}
}