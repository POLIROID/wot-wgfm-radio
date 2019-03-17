package poliroid.gui.lobby.wgfm.controls
{
	
	import flash.events.MouseEvent;
	import poliroid.gui.lobby.wgfm.events.WGFMEvent;
	
	public class DislikeButton extends RatingButton
	{
		override protected function onMouseDownHandler(e:MouseEvent) : void
		{
			if (enabled)
			{
				dispatchEvent(new WGFMEvent(WGFMEvent.DISLIKE_CLICK));
			}
		}
	}
}
