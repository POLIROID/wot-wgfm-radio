package com.poliroid.gui.lobby.wgfm.components {
	
	import net.wg.infrastructure.base.UIComponentEx;
	
	import com.poliroid.gui.lobby.wgfm.components.settings.SettingsHolder;
	import com.poliroid.gui.lobby.wgfm.controls.GroupViewButton;
	import com.poliroid.gui.lobby.wgfm.events.WGFMEvent;
	import com.poliroid.gui.lobby.wgfm.data.LocalizationVO;
	import com.poliroid.gui.lobby.wgfm.data.SettingsVO;
	import com.poliroid.gui.lobby.wgfm.data.StateVO;
	
	public class SettingsPanel extends UIComponentEx
	{
		public var header:GroupViewButton;
		
		public var body:SettingsHolder;
		
		public function SettingsPanel()
		{
			super();
		}
		
		override protected function configUI() : void 
		{
			super.configUI();
		}
		
		override protected function onDispose() : void 
		{
			header = null;
			super.onDispose();
		}
		
		public function setLocalization(data:LocalizationVO) : void 
		{
			header.setTitle(data.settingsTitle);
		}
		
		public function setSettings(data:SettingsVO) : void
		{
			body.setSettings(data);
		}
		
		public function hide() : void
		{
			if (header.opened)
			{
				header.opened = false;
				body.hide();
			}
		}
	}
}