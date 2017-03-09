package com.poliroid.gui.lobby.wgfm.data 
{
	import net.wg.data.daapi.base.DAAPIDataClass;
	
	public class SettingItemVO extends DAAPIDataClass
	{
		public var name:String = "";
		
		public var value:Boolean = false;
		
		public var label:String = "";
		
		public var tooltip:String = "";
		
		public function SettingItemVO(data:Object) 
		{
			super(data);
		}
	}
}