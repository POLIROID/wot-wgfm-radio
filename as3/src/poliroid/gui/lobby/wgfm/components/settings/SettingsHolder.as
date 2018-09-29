package poliroid.gui.lobby.wgfm.components.settings 
{
	import flash.display.MovieClip;
	import flash.geom.Rectangle;
	
	import com.greensock.TweenLite;
	
	import poliroid.gui.lobby.wgfm.components.settings.SettingsRenderer;
	import poliroid.gui.lobby.wgfm.data.SettingsVO;
	
	public class SettingsHolder extends MovieClip
	{
		public var renderer:SettingsRenderer = null;
		
		public function SettingsHolder() 
		{
			super();
		}
		
		public function setSettings(data:SettingsVO) : void
		{
			try {
				renderer.setSettings(data);
			} catch (e:Error) {
				DebugUtils.LOG_ERROR("setSettings");
				DebugUtils.LOG_ERROR(e.name);
				DebugUtils.LOG_ERROR(e.message);
				DebugUtils.LOG_ERROR(e.getStackTrace());
			}
			scrollRect = new Rectangle(0, 0, renderer.width, renderer.height);
		}
		
		public function show() : void
		{
			TweenLite.to(renderer, 0.5, {y: 0});
		}
		
		public function hide() : void
		{
			TweenLite.to(renderer, 0.5, {y: -renderer.height});
		}
	}

}