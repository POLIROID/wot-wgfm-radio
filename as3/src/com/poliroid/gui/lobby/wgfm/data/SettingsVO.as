package com.poliroid.gui.lobby.wgfm.data 
{
	
	import net.wg.infrastructure.interfaces.entity.IDisposable;
	import net.wg.data.daapi.base.DAAPIDataClass;
	
	import com.poliroid.gui.lobby.wgfm.data.SettingItemVO;
	
	public class SettingsVO extends DAAPIDataClass
	{
		
		private static const SETTINGS_FIELD_NAME:String = "settings";
		
		public var settings:Array = null;
		
		public function SettingsVO(data:Object)
		{
			super(data);
		}
		
		override protected function onDataWrite(name:String, data:Object) : Boolean
		{
			if(name == SETTINGS_FIELD_NAME)
			{
				var settingsItem:Object = null;
				var settingsItemItems:Array = data as Array;
				
				settings = [];
				
				for each(settingsItem in settingsItemItems)
				{
					settings.push(new SettingItemVO(settingsItem));
				}
				return false;
			}
			
			return super.onDataWrite(name, data);
		}
		
		override protected function onDispose() : void
		{
			var disposable:IDisposable = null;
			
			if(settings != null)
			{
				for each(disposable in settings)
				{
					disposable.dispose();
				}
				settings.splice(0, settings.length);
				settings = null;
			}
			
			super.onDispose();
		}
	}

}