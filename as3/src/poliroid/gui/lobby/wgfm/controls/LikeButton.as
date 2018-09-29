package poliroid.gui.lobby.wgfm.controls {
	
	import flash.events.MouseEvent;
	
	import net.wg.gui.components.controls.SoundButtonEx;
	import net.wg.gui.interfaces.ISoundButtonEx;
	
	import poliroid.gui.lobby.wgfm.events.WGFMEvent;
	
	public class LikeButton extends SoundButtonEx implements ISoundButtonEx 
	{
		
		public function LikeButton()
		{
			super();
			focusable = false;
		}
		
		override protected function onMouseDownHandler(e:MouseEvent) : void
		{
			if (enabled)
			{
				dispatchEvent(new WGFMEvent(WGFMEvent.LIKE_CLICK));
			}
		}
		
		override protected function getStatePrefixes() : Vector.<String>
		{
			if (selected)
			{
				return Vector.<String>(['selected_', '']);
			}
			else
			{
				return Vector.<String>(['']);
			}
		}
		
		public function updateStatus(status:String) : void
		{
			if (status.indexOf("selected") != -1)
			{
				selected = true;
			} 
			else
			{
				selected = false;
			}
			
			if (status.indexOf("disabled") != -1)
			{
				enabled = false;
			} 
			else
			{
				enabled = true;
			}
		}
	}
}