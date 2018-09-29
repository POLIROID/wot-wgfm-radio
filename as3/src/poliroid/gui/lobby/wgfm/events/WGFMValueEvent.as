package poliroid.gui.lobby.wgfm.events
{
	import flash.events.Event;
	
	public class WGFMValueEvent extends Event
	{
		
		public static const CHANNEL_CHANGED:String = "channelChanged";
		
		public static const VOLUME_CHANGED:String = "volumeChanged";
		
		private var _value:Number;
		
		public function WGFMValueEvent(type:String, value:Number = 0, bubbles:Boolean = true, cancelable:Boolean = false)
		{
			super(type, bubbles, cancelable);
			this._value = value;
		}
		
		override public function clone() : Event
		{
			return new WGFMValueEvent(type, this._value, bubbles, cancelable);
		}
		
		public function get value() : Number
		{
			return this._value;
		}
	}
}
