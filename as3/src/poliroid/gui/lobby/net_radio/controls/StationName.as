package poliroid.gui.lobby.net_radio.controls {
	
	import flash.display.MovieClip;
	import flash.events.MouseEvent;
	import flash.events.TimerEvent;
	import flash.geom.Rectangle;
	import flash.text.TextField;
	import flash.utils.Timer;
	
	import net.wg.infrastructure.base.UIComponentEx;
	
	import poliroid.gui.lobby.net_radio.events.NetRadioEvent;
	
	public class StationName extends UIComponentEx 
	{
		
		private static const ANIM_TIME_BETWEN_FRAMES:Number = 50;
		private static const VISIBLE_FIELD_WIDTH:Number = 210;
		private static const VISIBLE_POS_X_OFFSET:Number = 350;
		
		public var stationNameTF:TextField = null;
		public var stationNameHiddenTF:TextField = null;
		public var clickMask:MovieClip = null;
		
		private var _timer:Timer = null;
		
		public function StationName()
		{
			super();
			_timer = new Timer(ANIM_TIME_BETWEN_FRAMES);
			stationNameTF.text = "";
			stationNameHiddenTF.visible = true;
			stationNameTF.x = clickMask.x = VISIBLE_POS_X_OFFSET; 
		}
		
		override protected function configUI() : void
		{
			super.configUI();
			clickMask.buttonMode = true;
			clickMask.useHandCursor = true;
			scrollRect = new Rectangle(VISIBLE_POS_X_OFFSET, 0, VISIBLE_FIELD_WIDTH, 27);
			stationNameTF.width = stationNameHiddenTF.width = 2000; 
			stationNameHiddenTF.y = VISIBLE_POS_X_OFFSET;
			clickMask.addEventListener(MouseEvent.CLICK, handleMouseClick);
			_timer.addEventListener(TimerEvent.TIMER, _handleTimer);
			
		}
		
		override protected function onDispose() : void
		{
			_timer.stop();
			_timer.removeEventListener(TimerEvent.TIMER, _handleTimer);
			_timer = null;
			clickMask.removeEventListener(MouseEvent.CLICK, handleMouseClick);
			clickMask = null;
			stationNameTF = null;
			stationNameHiddenTF = null;
			super.onDispose();
		}
		
		
		private function handleMouseClick(e:MouseEvent) : void 
		{
			dispatchEvent(new NetRadioEvent(NetRadioEvent.STATION_CLICK, true));
		}
		
		public function hasErrors(hasErrors:Boolean) : void
		{
			clickMask.visible = true;
			clickMask.mouseEnabled = !hasErrors;
			clickMask.mouseChildren = !hasErrors;
			clickMask.buttonMode = !hasErrors;
			clickMask.useHandCursor = !hasErrors;
		}
		
		public function setComposition(name:String) : void 
		{
			clickMask.visible = name == "" ? false : true;
			
			_timer.stop();
			
			stationNameHiddenTF.text = name;
			
			if (stationNameHiddenTF.textWidth > VISIBLE_FIELD_WIDTH) 
			{
				stationNameHiddenTF.text = "      " + name;
				stationNameTF.x = VISIBLE_POS_X_OFFSET;
				stationNameTF.text = "   " + name + "      " + name + "      " + name;
				_timer.start();
			} 
			else 
			{
				stationNameTF.x = (VISIBLE_POS_X_OFFSET + int((VISIBLE_FIELD_WIDTH - stationNameHiddenTF.textWidth) / 2));
				stationNameTF.text = name;
			}
		}
		
		public function _handleTimer() : void 
		{
			stationNameTF.x = stationNameTF.x - 1;
			if (stationNameHiddenTF.textWidth < (VISIBLE_POS_X_OFFSET - stationNameTF.x)) 
			{
				stationNameTF.x = VISIBLE_POS_X_OFFSET;
			}
		}
	}
}