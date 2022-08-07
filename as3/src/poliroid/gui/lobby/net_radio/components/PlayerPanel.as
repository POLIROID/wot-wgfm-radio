package poliroid.gui.lobby.net_radio.components 
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
	
	import poliroid.gui.lobby.net_radio.components.ControlsPanelMain;
	import poliroid.gui.lobby.net_radio.components.ControlsPanelActive;
	import poliroid.gui.lobby.net_radio.components.HotkeysPanel;
	import poliroid.gui.lobby.net_radio.components.SettingsPanel;
	import poliroid.gui.lobby.net_radio.data.HotkeysVO;
	import poliroid.gui.lobby.net_radio.data.LocalizationVO;
	import poliroid.gui.lobby.net_radio.data.SettingsVO;
	import poliroid.gui.lobby.net_radio.data.StateVO;
	import poliroid.gui.lobby.net_radio.events.NetRadioEvent;
	
	public class PlayerPanel extends UIComponentEx
	{

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
			settingsPanel.header.addEventListener(NetRadioEvent.HEADER_CLICK, updateSettingsPanelState);
			hotkeysPanel.header.addEventListener(NetRadioEvent.HEADER_CLICK, updateHotkeysPanelState);
			closeButton.addEventListener(ButtonEvent.CLICK, onCloseClick);
			addEventListener(NetRadioEvent.UPDATE_POSITIONS, updatePanelsPositions);
		}
		
		override protected function onDispose() : void 
		{
			settingsPanel.header.removeEventListener(NetRadioEvent.HEADER_CLICK, updateSettingsPanelState);
			hotkeysPanel.header.removeEventListener(NetRadioEvent.HEADER_CLICK, updateHotkeysPanelState);
			closeButton.removeEventListener(ButtonEvent.CLICK, onCloseClick);
			removeEventListener(NetRadioEvent.UPDATE_POSITIONS, updatePanelsPositions);
			
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
		
		public function updatePositions():void 
		{
			updatePanelsPositions();
		}
		
		public function updateState(newState:StateVO) : void
		{
			
			controlsPanelMain.updateState(newState);
			
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
			dispatchEvent(new NetRadioEvent(NetRadioEvent.CLOSE_CLICK));
		}
		
		private function updatePanelsPositions() : void 
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
		
		private function updateHotkeysPanelState() : void 
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
		
		private function updateSettingsPanelState() : void 
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