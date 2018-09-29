package poliroid.gui.lobby.wgfm.controls 
{
	import flash.display.DisplayObject;
	import flash.display.MovieClip;
	import flash.events.Event;
	import flash.events.MouseEvent;
	import flash.geom.Point;
	import flash.text.TextField;
	
	import net.wg.data.daapi.ContextMenuOptionVO
	import net.wg.infrastructure.interfaces.IContextMenu;
	import net.wg.gui.components.controls.ContextMenu;
	import net.wg.gui.components.controls.SoundButtonEx;
	import net.wg.gui.interfaces.ISoundButtonEx;
	import net.wg.infrastructure.interfaces.entity.IDisposable;
	import net.wg.infrastructure.interfaces.IContextItem;
	
	import poliroid.gui.lobby.wgfm.data.HotkeyItemVO;
	import poliroid.gui.lobby.wgfm.events.WGFMDoubleValueEvent;
	
	public class Hotkey extends SoundButtonEx implements ISoundButtonEx  {
		
		private static const COMMAND_START_ACCEPT:String = 'startAccept';
		private static const COMMAND_STOP_ACCEPT:String = 'stopAccept';
		private static const COMMAND_DEFAULT:String = 'default';
		private static const COMMAND_CLEAN:String = 'clean';
		
		public var hitAreaA:MovieClip = null;
		public var labelTF:TextField = null;
		public var valueTF:TextField = null;
		public var acceptAnimMC:MovieClip = null;
		public var noKeyAnimMC:MovieClip = null;
		public var altModifierMC:MovieClip = null;
		public var ctrlModifierMC:MovieClip = null;
		public var shiftModifierMC:MovieClip = null;
		
		private var model:HotkeyItemVO = null;
		private var _contextMenu:ContextMenu = null;
		
		public function Hotkey() : void 
		{
			super();
			
		}
		
		override protected function configUI() : void 
		{
			super.configUI();
			
			focusable = false;
			hitArea = hitAreaA;
			labelTF.selectable = false;
			valueTF.selectable = false;
		}
		
		public function updateData(ctx:HotkeyItemVO) : void
		{
			model = ctx;
			labelTF.text = model.label;
			valueTF.text = model.value;
			acceptAnimMC.visible = model.isAccepting;
			noKeyAnimMC.visible = model.isEmpty;
			
			if (model.isAccepting || model.isEmpty)
			{
				valueTF.text = "";
			} 
			else 
			{
				valueTF.text = model.value;
			}
			shiftModifierMC.visible = model.modiferShift;
			altModifierMC.visible = model.modifierAlt;
			ctrlModifierMC.visible = model.modifierCtrl;
		}
		
		override protected function onMouseDownHandler(e:MouseEvent) : void
		{
			if (App.utils.commons.isRightButton(e)) 
			{
				if (model.isAccepting)
				{
					dispatchEvent(new WGFMDoubleValueEvent(WGFMDoubleValueEvent.HOTKEY_CHANGED, model.name, COMMAND_STOP_ACCEPT));
				}
				
				hidePopUp();
				
				_contextMenu = ContextMenu(App.utils.classFactory.getComponent("ContextMenu", ContextMenu));
				var options:Vector.<IContextItem> = new Vector.<IContextItem>();
				options.push( new ContextMenuOptionVO( { id:0, label: model.labelDefault, initData: 0, submenu: [] } ));
				options.push( new ContextMenuOptionVO( { id:1, label: model.labelClean, initData: 1, submenu: [] } ));
				App.utils.popupMgr.show(_contextMenu, e.stageX, e.stageY);
				
				var clickPoint:Point = new Point(e.stageX - 65, e.stageY + 30);
				clickPoint.x = clickPoint.x / App.appScale >> 0;
				clickPoint.y = clickPoint.y / App.appScale >> 0;
				_contextMenu.build(options, clickPoint);
				_contextMenu.onItemSelectCallback = handleMenuItemClick;
				_contextMenu.onReleaseOutsideCallback = hidePopUp;
				_contextMenu.stage.addEventListener(Event.RESIZE, hidePopUp);
			}
			
			if (App.utils.commons.isLeftButton(e)) 
			{
				if (!model.isAccepting)
				{
					dispatchEvent(new WGFMDoubleValueEvent(WGFMDoubleValueEvent.HOTKEY_CHANGED, model.name, COMMAND_START_ACCEPT));
				}
			}
		}
		
		
		private function hidePopUp() : void {
			if (_contextMenu != null) {
				var _cmdo :DisplayObject = DisplayObject(_contextMenu);
				if (_cmdo.stage && _cmdo.stage.hasEventListener(Event.RESIZE)) {
					_cmdo.stage.removeEventListener(Event.RESIZE, hidePopUp);
				}
				if (_contextMenu is IDisposable) {
					IDisposable(_contextMenu).dispose();
				}
				
				App.utils.popupMgr.popupCanvas.removeChild(_contextMenu);
				
				_contextMenu = null;
			}
		}
		
		private function handleMenuItemClick(event:String) : void {
			hidePopUp();
			if (event == "0") 
			{
				dispatchEvent(new WGFMDoubleValueEvent(WGFMDoubleValueEvent.HOTKEY_CHANGED, model.name, COMMAND_DEFAULT));
			}
			else if (event == "1") 
			{
				dispatchEvent(new WGFMDoubleValueEvent(WGFMDoubleValueEvent.HOTKEY_CHANGED, model.name, COMMAND_CLEAN));
			}
		}
	}
}
