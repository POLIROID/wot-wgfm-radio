package poliroid.gui.lobby.net_radio.components {
	
	import net.wg.infrastructure.base.UIComponentEx;
	
	import poliroid.gui.lobby.net_radio.components.settings.SettingsHolder;
	import poliroid.gui.lobby.net_radio.controls.GroupViewButton;
	import poliroid.gui.lobby.net_radio.data.LocalizationVO;
	import poliroid.gui.lobby.net_radio.data.SettingsVO;
	import poliroid.gui.lobby.net_radio.data.StateVO;
	
	public class SettingsPanel extends UIComponentEx
	{
		public var header:GroupViewButton;
		
		public var body:SettingsHolder;
		
		public function SettingsPanel()
		{
			super();
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