package poliroid.gui.lobby.wgfm.controls 
{
	import flash.display.MovieClip;
	import flash.events.Event;
	import flash.events.MouseEvent;
	import flash.text.TextField;
	
	import net.wg.gui.components.controls.SoundButtonEx;
	import net.wg.gui.interfaces.ISoundButtonEx;
	
	import poliroid.gui.lobby.wgfm.data.HotkeyItemVO;
	import poliroid.gui.lobby.wgfm.events.WGFMValueEvent;
	
	public class Hotkey extends SoundButtonEx implements ISoundButtonEx 
	{
		private static const COMMAND_START_ACCEPT:String = 'startAccept';
		private static const COMMAND_STOP_ACCEPT:String = 'stopAccept';
		
		public var hitAreaA:MovieClip = null;
		public var labelTF:TextField = null;
		public var valueTF:TextField = null;
		public var acceptAnimMC:MovieClip = null;
		public var noKeyAnimMC:MovieClip = null;
		public var altModifierMC:MovieClip = null;
		public var ctrlModifierMC:MovieClip = null;
		public var shiftModifierMC:MovieClip = null;
		
		private var model:HotkeyItemVO = null;
		
		public function Hotkey()
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
					dispatchEvent(new WGFMValueEvent(WGFMValueEvent.HOTKEY_CHANGED, model.name, COMMAND_STOP_ACCEPT));
				}
				App.contextMenuMgr.show('wgfmHotkeyContextHandler', this, {'controlName': model.name});
			}
			
			if (App.utils.commons.isLeftButton(e) && !model.isAccepting) 
			{
				dispatchEvent(new WGFMValueEvent(WGFMValueEvent.HOTKEY_CHANGED, model.name, COMMAND_START_ACCEPT));
			}
		}
	}
}
