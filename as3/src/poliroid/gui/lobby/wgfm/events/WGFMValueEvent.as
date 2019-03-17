package poliroid.gui.lobby.wgfm.events
{
	import flash.events.Event;
	
	public class WGFMValueEvent extends Event
	{
		
		public static const CHANNEL_CHANGED:String = "channelChanged";
		
		public static const VOLUME_CHANGED:String = "volumeChanged";
		
		public static const SETTINGS_CHANGED:String = "settingsChanged";
		
		public static const HOTKEY_CHANGED:String = "hotkeyChanged";
		
		private var _name;
		private var _value;
		
		public function WGFMValueEvent(type:String, name = null, value = null, bubbles:Boolean = true, cancelable:Boolean = false)
		{
			super(type, bubbles, cancelable);
			_name = name;
			_value = value;
		}
		
		override public function clone() : Event
		{
			return new WGFMValueEvent(type, _name, _value, bubbles, cancelable);
		}
		
		public function get name()
		{
			return _name;
		}

		public function get value()
		{
			return _value;
		}
	}
}
