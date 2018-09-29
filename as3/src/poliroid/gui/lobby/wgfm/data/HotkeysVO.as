package poliroid.gui.lobby.wgfm.data 
{
	
	import net.wg.infrastructure.interfaces.entity.IDisposable;
	import net.wg.data.daapi.base.DAAPIDataClass;
	
	import poliroid.gui.lobby.wgfm.data.HotkeyItemVO;
	
	public class HotkeysVO extends DAAPIDataClass
	{
		
		private static const HOTKEYS_FIELD_NAME:String = "hotkeys";
		
		public var hotKeys:Array = null;
		
		public function HotkeysVO(data:Object)
		{
			super(data);
		}
		
		override protected function onDataWrite(name:String, data:Object) : Boolean
		{
			if(name == HOTKEYS_FIELD_NAME)
			{
				var hotKeyItem:Object = null;
				var hotKeyItems:Array = data as Array;
				
				hotKeys = [];
				
				for each(hotKeyItem in hotKeyItems)
				{
					hotKeys.push(new HotkeyItemVO(hotKeyItem));
				}
				return false;
			}
			
			return super.onDataWrite(name, data);
		}
		
		override protected function onDispose() : void
		{
			var disposable:IDisposable = null;
			
			if(hotKeys != null)
			{
				for each(disposable in hotKeys)
				{
					disposable.dispose();
				}
				hotKeys.splice(0, hotKeys.length);
				hotKeys = null;
			}
			
			super.onDispose();
		}
	}

}