package poliroid.gui.lobby.net_radio.data 
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