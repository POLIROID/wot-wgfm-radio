package poliroid.gui.lobby.wgfm.data 
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
		
		public var labelDefault:String = "";
		
		public var labelClean:String = "";
		
		public function HotkeyItemVO(data:Object) 
		{
			super(data);
		}
		
	}

}