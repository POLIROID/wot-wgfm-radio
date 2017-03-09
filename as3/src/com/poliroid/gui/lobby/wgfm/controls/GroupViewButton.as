package com.poliroid.gui.lobby.wgfm.controls 
{
	import flash.display.MovieClip;
	import flash.events.MouseEvent;
	import flash.utils.setTimeout;
	
	import net.wg.gui.components.controls.SoundButtonEx;
	import net.wg.gui.interfaces.ISoundButtonEx;
	
	import com.poliroid.gui.lobby.wgfm.events.WGFMEvent;
	
	public class GroupViewButton extends SoundButtonEx implements ISoundButtonEx
	{
		
		public var titleLabel:GroupViewButtonTitle;
		
		private var _opened:Boolean = false;
		
		public function GroupViewButton() 
		{
			super();
			focusable = false;
		}
		override protected function configUI() : void
		{
			super.configUI();
			addEventListener(MouseEvent.MOUSE_UP, handleMouseUpListner);
		}
		
		override protected function onDispose() : void
		{
			removeEventListener(MouseEvent.MOUSE_UP, handleMouseUpListner);
			super.onDispose();
		}
		
		private function handleMouseUpListner(e:MouseEvent) : void
		{
			opened = !opened;
			dispatchEvent(new WGFMEvent(WGFMEvent.HEADER_CLICK, false));
		}
		
		override protected function getStatePrefixes() : Vector.<String>
		{
			if (opened)
			{
				return Vector.<String>(['hide_', '']);
			}
			else
			{
				return Vector.<String>(['show_', '']);
			}
		}
		
		public function setTitle(titleText:String) : void 
		{
			titleLabel.titleTF.text = titleText;
		}
		
		public function get opened() : Boolean
		{
			return _opened;
		}
		
		public function set opened(isOpened:Boolean) : void
		{
			if(_opened == isOpened)
				return;
			
			_opened = isOpened;
			setState('up');
		}
	}
}