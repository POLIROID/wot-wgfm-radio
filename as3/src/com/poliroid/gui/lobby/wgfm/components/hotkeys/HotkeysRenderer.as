package com.poliroid.gui.lobby.wgfm.components.hotkeys 
{
	import flash.display.MovieClip;
	import flash.events.Event;
	import flash.events.MouseEvent;
	import flash.utils.Dictionary;
	
	import net.wg.gui.components.controls.HyperLink;
	import net.wg.infrastructure.base.UIComponentEx;
	import net.wg.gui.components.controls.CheckBox;
	
	import com.poliroid.gui.lobby.wgfm.controls.Hotkey;
	import com.poliroid.gui.lobby.wgfm.events.WGFMEvent;
	import com.poliroid.gui.lobby.wgfm.events.WGFMDoubleValueEvent;
	import com.poliroid.gui.lobby.wgfm.data.HotkeysVO;
	import com.poliroid.gui.lobby.wgfm.data.HotkeyItemVO;
	
	import net.wg.gui.components.controls.InfoIcon;
	
	public class HotkeysRenderer extends UIComponentEx
	{
		private static const RENDERER_HEIGHT = 25;
		
		public var defaultHotkeys:HyperLink = null;
		
		private var _renderers:Dictionary = new Dictionary();
		
		private var inited:Boolean = false;
		
		public function HotkeysRenderer() 
		{
			super();
		}
		
		override protected function configUI() : void 
		{
			super.configUI();
			
			defaultHotkeys.addEventListener(MouseEvent.CLICK, handleDefaultHotkeysClick);
			defaultHotkeys.validateNow();
		}
		
		override protected function onDispose() : void 
		{
			var renderName:String;
			if(_renderers != null)
			{
				for (renderName in _renderers)
				{
					_renderers[renderName].dispose();
					delete _renderers[renderName];
				}
				_renderers = null;
			}
			
			defaultHotkeys.removeEventListener(MouseEvent.CLICK, handleDefaultHotkeysClick);
			defaultHotkeys.dispose();
			defaultHotkeys = null;
			
			super.onDispose();
		}
		
		public function setLinkLabel(linkLabel:String) : void 
		{
			defaultHotkeys.label = linkLabel;
		}
		
		public function updateHotkeys(data:HotkeysVO) : void
		{
			var hotKey:Hotkey;
			var hotKeyItem:HotkeyItemVO = null;
			var hotKeyItems:Array = data.hotKeys as Array;
			var heightOffset:Number = 0;
			
			for each(hotKeyItem in hotKeyItems)
			{
				if (_renderers.hasOwnProperty(hotKeyItem.name))
				{
					hotKey = _renderers[hotKeyItem.name]
					hotKey.updateData(hotKeyItem);
				} else {
					hotKey = App.utils.classFactory.getComponent('wgfmHotkeyUI', Hotkey);
					hotKey.updateData(hotKeyItem);
					_renderers[hotKeyItem.name] = hotKey;
					hotKey.x = 25;
					hotKey.y = heightOffset;
					addChild(hotKey);
				}
				heightOffset += RENDERER_HEIGHT;
			}
			
			defaultHotkeys.y = heightOffset;
			
			height = defaultHotkeys.y + defaultHotkeys.height;
			
			if (!inited) 
			{
				y = -height
			}
			
			
			inited = true;
		}
		
		private function handleDefaultHotkeysClick(e:MouseEvent) : void 
		{
			dispatchEvent(new WGFMEvent(WGFMEvent.DEFAULT_HOTKEYS_CLICK));
		}
	}
	
}