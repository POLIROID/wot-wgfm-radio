package com.poliroid.gui.lobby.wgfm.components 
{
	
	import flash.text.TextField;
	import flash.utils.setInterval;
	import flash.utils.setTimeout;
	import flash.utils.clearInterval;
	import flash.utils.clearTimeout;
	
	import scaleform.clik.data.DataProvider;
	import scaleform.clik.events.ButtonEvent;
	import scaleform.clik.events.InputEvent;
	
	import net.wg.infrastructure.base.AbstractView;
	import net.wg.infrastructure.base.UIComponentEx;
	import net.wg.gui.components.controls.CloseButtonText;
	import net.wg.gui.components.common.waiting.Waiting;
	
	import com.poliroid.gui.lobby.wgfm.components.ControlsPanelMain;
	import com.poliroid.gui.lobby.wgfm.components.ControlsPanelActive;
	import com.poliroid.gui.lobby.wgfm.components.HotkeysPanel;
	import com.poliroid.gui.lobby.wgfm.components.SettingsPanel;
	import com.poliroid.gui.lobby.wgfm.data.HotkeysVO;
	import com.poliroid.gui.lobby.wgfm.data.LocalizationVO;
	import com.poliroid.gui.lobby.wgfm.data.SettingsVO;
	import com.poliroid.gui.lobby.wgfm.data.StateVO;
	import com.poliroid.gui.lobby.wgfm.events.WGFMEvent;
	
	public class PlayerPanel extends UIComponentEx
	{
		
		private static const PANELS_PADDING:Number = 10;
		
		private var state:StateVO = new StateVO( {} );
		
		public var controlsPanelMain:ControlsPanelMain = null;
		
		public var controlsPanelActive:ControlsPanelActive = null;
		
		public var hotkeysPanel:HotkeysPanel = null;
		
		public var settingsPanel:SettingsPanel = null;
		
		public var closeButton:CloseButtonText = null;
		
		public var titleTF:TextField = null;
		
		private var _intervalID:uint = 0;
		
		private var _timeoutID:uint = 0;
		
		public function PlayerPanel() 
		{
			super();
		}
		
		override protected function configUI() : void 
		{
			super.configUI();
			settingsPanel.header.addEventListener(WGFMEvent.HEADER_CLICK, updateSettingsPanelState);
			hotkeysPanel.header.addEventListener(WGFMEvent.HEADER_CLICK, updateHotkeysPanelState);
			closeButton.addEventListener(ButtonEvent.CLICK, onCloseClick);
			addEventListener(WGFMEvent.UPDATE_POSITIONS, updatePanelsPositions);
		}
		
		override protected function onDispose() : void 
		{
			settingsPanel.header.removeEventListener(WGFMEvent.HEADER_CLICK, updateSettingsPanelState);
			hotkeysPanel.header.removeEventListener(WGFMEvent.HEADER_CLICK, updateHotkeysPanelState);
			closeButton.removeEventListener(ButtonEvent.CLICK, onCloseClick);
			removeEventListener(WGFMEvent.UPDATE_POSITIONS, updatePanelsPositions);
			
			controlsPanelMain = null;
			controlsPanelActive = null;
			hotkeysPanel = null;
			settingsPanel = null;
			
			super.onDispose();
		}
		
		override protected function draw() : void 
		{
			super.draw();
			
			if (isInvalid('ANIMATION_UPDATE'))
			{
				hotkeysPanel.y = int(controlsPanelActive.y + controlsPanelActive.height + controlsPanelActive.likeButton.y);
				settingsPanel.y = int(hotkeysPanel.y + hotkeysPanel.header.height + hotkeysPanel.body.renderer.height + hotkeysPanel.body.renderer.y);
			}
		}
		
		public function updatePositions(appWidth:Number, appHeight:Number):void 
		{
			updatePanelsPositions();
		}
		
		public function updateState(newState:StateVO) : void
		{
			
			controlsPanelMain.updateState(state, newState);
			
			controlsPanelActive.updateState(state, newState);
			
			if (state.isPlaying != newState.isPlaying || newState.isError) 
			{
				settingsPanel.hide();
				hotkeysPanel.hide();
				updatePanelsPositions();
			}
			
			state = newState;
		}
		
		public function setLocalization(data:LocalizationVO) : void
		{
			titleTF.text = data.titleLabel;
			closeButton.label = data.closeButton;
			settingsPanel.setLocalization(data);
			hotkeysPanel.setLocalization(data);
			
		}
		
		public function updateChannels(channels:Array) : void
		{
			var dp:DataProvider = new DataProvider(channels);
			controlsPanelMain.stationsDropdown.dataProvider = dp;
			controlsPanelMain.stationsDropdown.rowCount = dp.length;
			controlsPanelMain.stationsDropdown.validateNow();
		}
		
		public function updateHotkeys(ctx:HotkeysVO) : void
		{
			hotkeysPanel.updateHotkeys(ctx);
		}
		
		public function setSettings(data:SettingsVO) : void
		{
			settingsPanel.setSettings(data);
		}
		
		private function onCloseClick(e:ButtonEvent) : void 
		{
			dispatchEvent(new WGFMEvent(WGFMEvent.CLOSE_CLICK));
		}
		
		private function updatePanelsPositions(e:WGFMEvent = null) : void 
		{
			invalidate('ANIMATION_UPDATE');
			if (_timeoutID != 0) 
			{
				clearTimeout(_timeoutID)
				_timeoutID = 0;
			}
			if (_intervalID != 0) {
				clearInterval(_intervalID);
				_intervalID = 0;
			}
			_intervalID = setInterval(invalidate, 1, 'ANIMATION_UPDATE');
			_timeoutID = setTimeout(clearInterval, 500, _intervalID);
		}
		
		private function updateHotkeysPanelState(e:WGFMEvent = null) : void 
		{
			if (hotkeysPanel.header.opened)
			{
			 	hotkeysPanel.body.show();
			 	settingsPanel.hide();
			}
			else
			{
				hotkeysPanel.body.hide();
			}
			updatePanelsPositions();
		}
		
		private function updateSettingsPanelState(e:WGFMEvent = null) : void 
		{
			if (settingsPanel.header.opened)
			{
			 	settingsPanel.body.show();
				hotkeysPanel.hide();
			}
			else
			{
				settingsPanel.body.hide();
			}
			updatePanelsPositions();
		}
		
	}

}