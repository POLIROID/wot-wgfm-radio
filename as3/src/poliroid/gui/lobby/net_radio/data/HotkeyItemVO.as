package poliroid.gui.lobby.net_radio.data 
{
	import net.wg.data.daapi.base.DAAPIDataClass;
	
	public class HotkeyItemVO extends DAAPIDataClass
	{
		
		public var name:String = "";
		
		public var label:String = "";
		
		public var value:String = "";
		
		public var isEmpty:Boolean = false;
		
		public var isAccepting:Boolean = false;
		
		public var modifierAlt:Boolean = false;
		
		public var modifierCtrl:Boolean = false;
		
		public var modiferShift:Boolean = false;
		
		public function HotkeyItemVO(data:Object) 
		{
			super(data);
		}
		
	}

}