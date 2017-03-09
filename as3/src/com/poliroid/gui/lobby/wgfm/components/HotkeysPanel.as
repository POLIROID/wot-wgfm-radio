package com.poliroid.gui.lobby.wgfm.components {
	
	
	import net.wg.infrastructure.base.UIComponentEx;
	
	import com.poliroid.gui.lobby.wgfm.components.hotkeys.HotkeysHolder;
	import com.poliroid.gui.lobby.wgfm.controls.GroupViewButton;
	import com.poliroid.gui.lobby.wgfm.events.WGFMEvent;
	import com.poliroid.gui.lobby.wgfm.data.LocalizationVO;
	import com.poliroid.gui.lobby.wgfm.data.StateVO;
	import com.poliroid.gui.lobby.wgfm.data.HotkeysVO;
	
	public class HotkeysPanel extends UIComponentEx
	{	
		public var header:GroupViewButton;
		
		public var body:HotkeysHolder;
		
		public function HotkeysPanel()
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