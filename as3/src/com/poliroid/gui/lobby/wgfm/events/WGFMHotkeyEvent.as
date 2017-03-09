
package com.poliroid.gui.lobby.wgfm.events
{
	import flash.events.Event;
	
	public class WGFMHotkeyEvent extends Event
	{
		
		public static const START_ACCEPT:String = "settingsChanged";
		public static const STOP_ACCEPT:String = "settingsChanged";
		public static const CLEAN:String = "settingsChanged";
		public static const DEFAULT:String = "settingsChanged";
		
		private var _name:String;
		
		private var _cmd:*;
		
		public function WGFMHotkeyEvent(type:String, name:String = "", cmd:* = null, bubbles:Boolean = true, cancelable:Boolean = false)
		{
			super(type, bubbles, cancelable);
			this._name = name;
			this._cmd = cmd;
		}
		
		override public function clone() : Event
		{
			return new WGFMHotkeyEvent(type, this._value, this._cmd, bubbles, cancelable);
		}
		
		public function get cmd() : *
		{
			return this._cmd;
		}
		
		public function get name() : String
		{
			return this._name;
		}
		
	}
}