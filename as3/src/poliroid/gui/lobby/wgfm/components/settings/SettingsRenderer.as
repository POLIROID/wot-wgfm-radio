package poliroid.gui.lobby.wgfm.components.settings 
{
	import flash.events.Event;
	import flash.utils.Dictionary;
	
	import net.wg.infrastructure.base.UIComponentEx;
	import net.wg.gui.components.controls.CheckBox;
	
	import poliroid.gui.lobby.wgfm.events.WGFMEvent;
	import poliroid.gui.lobby.wgfm.events.WGFMValueEvent;
	import poliroid.gui.lobby.wgfm.data.SettingsVO;
	import poliroid.gui.lobby.wgfm.data.SettingItemVO;
	
	import net.wg.gui.components.controls.InfoIcon;
	
	public class SettingsRenderer extends UIComponentEx
	{
		
		private static const RENDERER_HEIGHT = 25;
		
		private var _renderers:Dictionary = new Dictionary();
		
		private var inited:Boolean = false;
		
		public function SettingsRenderer() 
		{
			super();
		}
		
		override protected function configUI() : void 
		{
			super.configUI();
			var renderName:String;
			if(_renderers != null)
			{
				for (renderName in _renderers)
				{
					_renderers[renderName].validateNow();
				}
			}
		}
		
		override protected function onDispose() : void 
		{
			var renderName:String;
			if(_renderers != null)
			{
				for (renderName in _renderers)
				{
					_renderers[renderName].removeEventListener(Event.SELECT, handleSettingsItemClick);
					_renderers[renderName].dispose();
					_renderers[renderName] = null;
					delete _renderers[renderName];
				}
				_renderers = null;
			}
			
			super.onDispose();
		}
		
		public function setSettings(data:SettingsVO) : void
		{
			var setting:CheckBox;
			var settingsItem:SettingItemVO;
			var settingsItems:Array = data.settings;
			var heightOffset:Number = 5;
			
			for each(settingsItem in settingsItems)
			{
				if (_renderers.hasOwnProperty(settingsItem.name))
				{
					setting = _renderers[settingsItem.name]
					setting.selected = settingsItem.value;
				} else {
					setting = App.utils.classFactory.getComponent('CheckBox', CheckBox);
					setting.name = settingsItem.name;
					setting.selected = settingsItem.value;
					setting.label = settingsItem.label;
					setting.toolTip = settingsItem.tooltip;
					setting.infoIcoType = InfoIcon.TYPE_INFO;
					setting.width = 275;
					setting.addEventListener(Event.SELECT, handleSettingsItemClick);
					_renderers[settingsItem.name] = setting;
					setting.x = 25;
					setting.y = heightOffset;
					addChild(setting);
				}
				heightOffset += RENDERER_HEIGHT;
			}
			
			height = heightOffset;
			
			if (!inited) 
			{
				y = -height
			}
			
			inited = true;
		}
		
		private function handleSettingsItemClick(e:Event) : void 
		{
			var target:CheckBox = e.target as CheckBox;
			dispatchEvent(new WGFMValueEvent(WGFMValueEvent.SETTINGS_CHANGED, target.name, target.selected));
		}
		
	}
	
}