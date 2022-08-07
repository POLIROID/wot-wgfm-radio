package poliroid.gui.lobby.net_radio.components {
	
	
	import net.wg.infrastructure.base.UIComponentEx;
	
	import poliroid.gui.lobby.net_radio.components.hotkeys.HotkeysHolder;
	import poliroid.gui.lobby.net_radio.controls.GroupViewButton;
	import poliroid.gui.lobby.net_radio.data.LocalizationVO;
	import poliroid.gui.lobby.net_radio.data.StateVO;
	import poliroid.gui.lobby.net_radio.data.HotkeysVO;
	
	public class HotkeysPanel extends UIComponentEx
	{	
		public var header:GroupViewButton;
		
		public var body:HotkeysHolder;
		
		public function HotkeysPanel()
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
			header.setTitle(data.hotkeysTitle);
			body.setLinkLabel(data.hotkeysDefault);
		}
		
		public function updateHotkeys(data:HotkeysVO) : void
		{
			body.updateHotkeys(data);
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