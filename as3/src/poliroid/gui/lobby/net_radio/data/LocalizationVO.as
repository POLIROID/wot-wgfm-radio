package poliroid.gui.lobby.net_radio.data 
{
	
	import net.wg.data.daapi.base.DAAPIDataClass;
	
	public class LocalizationVO extends DAAPIDataClass
	{
		
		public var closeButton:String = "";
		
		public var titleLabel:String = "";
		
		public var settingsTitle:String = "";
		
		public var hotkeysTitle:String = "";
		
		public var hotkeysDefault:String = "";
		
		public function LocalizationVO(data:Object) 
		{
			super(data);
		}
	}
}