package poliroid.gui.lobby.wgfm.controls
{
	
	import net.wg.gui.components.controls.SoundButtonEx;
	import net.wg.gui.interfaces.ISoundButtonEx;
	
	public class RatingButton extends SoundButtonEx implements ISoundButtonEx 
	{
		
		public function RatingButton()
		{
			focusable = false;
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
