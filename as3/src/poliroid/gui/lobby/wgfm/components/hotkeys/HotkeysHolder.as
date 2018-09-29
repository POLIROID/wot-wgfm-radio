package poliroid.gui.lobby.wgfm.components.hotkeys 
{
	import flash.display.MovieClip;
	import flash.geom.Rectangle;
	
	import com.greensock.TweenLite;
	
	import poliroid.gui.lobby.wgfm.components.hotkeys.HotkeysRenderer;
	import poliroid.gui.lobby.wgfm.data.HotkeysVO;
	
	public class HotkeysHolder extends MovieClip
	{
		
		public var renderer:HotkeysRenderer = null;
		
		public function HotkeysHolder() 
		{
			super();
		}
		
		public function setLinkLabel(linkLabel:String) : void 
		{
			renderer.setLinkLabel(linkLabel);
		}
		
		public function updateHotkeys(data:HotkeysVO) : void
		{
			renderer.updateHotkeys(data);
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