package poliroid.gui.lobby.net_radio.controls
{
	
	import flash.events.MouseEvent;
	import poliroid.gui.lobby.net_radio.events.NetRadioEvent;
	
	public class DislikeButton extends RatingButton
	{
		override protected function onMouseDownHandler(e:MouseEvent) : void
		{
			if (enabled)
			{
				dispatchEvent(new NetRadioEvent(NetRadioEvent.DISLIKE_CLICK));
			}
		}
	}
}
