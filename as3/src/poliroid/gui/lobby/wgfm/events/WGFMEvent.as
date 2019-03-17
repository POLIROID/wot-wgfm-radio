package poliroid.gui.lobby.wgfm.events
{
	import flash.events.Event;
	
	public class WGFMEvent extends Event
	{
		
		public static const CLOSE_CLICK:String = "closeClick";
		
		public static const PLAY_CLICK:String = "backClick";
		
		public static const PAUSE_CLICK:String = "pauseClick";
		
		public static const VOLUME_CLICK:String = "volumeClick";
		
		public static const LIKE_CLICK:String = "likeClick";
		
		public static const DISLIKE_CLICK:String = "dislikeClick";
		
		public static const STATION_CLICK:String = "stationClick";
		
		public static const HEADER_CLICK:String = "headerClick";
		
		public static const DEFAULT_HOTKEYS_CLICK:String = "defaultHotkeysClick";
		
		public static const UPDATE_POSITIONS:String = "updatePositions";
		
		public function WGFMEvent(type:String, bubbles:Boolean = true, cancelable:Boolean = false)
		{
			super(type, bubbles, cancelable);
		}
		
		override public function clone() : Event
		{
			return new WGFMEvent(type, bubbles, cancelable);
		}
	}
}
