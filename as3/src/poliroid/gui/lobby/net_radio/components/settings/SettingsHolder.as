package poliroid.gui.lobby.net_radio.components.settings 
{
	import flash.display.MovieClip;
	import flash.geom.Rectangle;
	
	import scaleform.clik.motion.Tween;
	
	import poliroid.gui.lobby.net_radio.components.settings.SettingsRenderer;
	import poliroid.gui.lobby.net_radio.data.SettingsVO;
	
	public class SettingsHolder extends MovieClip
	{
		public var renderer:SettingsRenderer = null;
		
		public function SettingsHolder() 
		{
			super();
		}
		
		public function setSettings(data:SettingsVO) : void
		{
			renderer.setSettings(data);
			scrollRect = new Rectangle(0, 0, renderer.width, renderer.height);
		}
		
		public function show() : void
		{
			new Tween(400, renderer, {y: 0}, {fastTransform:false});
		}
		
		public function hide() : void
		{
			new Tween(400, renderer, {y: -renderer.height}, {fastTransform:false});
		}
	}

}