
package poliroid.gui.lobby.wgfm.events
{
	import flash.events.Event;
	
	public class WGFMDoubleValueEvent extends Event
	{
		
		public static const SETTINGS_CHANGED:String = "settingsChanged";
		
		public static const HOTKEY_CHANGED:String = "hotkeyChanged";
		
		private var _name:String;
		
		private var _value:*;
		
		public function WGFMDoubleValueEvent(type:String, name:String = "", value:* = null, bubbles:Boolean = true, cancelable:Boolean = false)
		{
			super(type, bubbles, cancelable);
			this._name = name;
			this._value = value;
		}
		
		override public function clone() : Event
		{
			return new WGFMDoubleValueEvent(type, this._value, this._name, bubbles, cancelable);
		}
		
		public function get value() : *
		{
			return this._value;
		}
		
		public function get name() : String
		{
			return this._name;
		}
		
	}
}