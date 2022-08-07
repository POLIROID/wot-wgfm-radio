package poliroid.gui.lobby.net_radio.controls {
	
	import flash.events.TimerEvent;
	import flash.utils.Timer;
	import net.wg.infrastructure.base.UIComponentEx;
	
	public class EqualizerAnimation extends UIComponentEx 
	{
		
		private static const ANIM_TIME_BETWEN_FRAMES:Number = 80;
		
		private static const PAUSE_STATE_FRAME:Number = 10;
		
		private var _playing:Boolean = false;
		
		private var _muted:Boolean = false;
		
		private var _timer:Timer = null;
		
		public function EqualizerAnimation() 
		{
			super();
			_timer = new Timer(ANIM_TIME_BETWEN_FRAMES);
		}
		
		override protected function configUI() : void
		{
			super.configUI();
			_timer.addEventListener(TimerEvent.TIMER, _handleTimer);
			updateState();
		}
		
		override protected function onDispose() : void
		{
			_timer.stop();
			_timer.removeEventListener(TimerEvent.TIMER, _handleTimer);
			_timer = null;
			super.onDispose();	
		}
		
		private function updateState() : void
		{
			_timer.stop();
			if (_playing)
			{
				_handleTimer();
				_timer.start();
			}
			else
			{
				gotoAndStop(PAUSE_STATE_FRAME);
			}
		}
		
		private function _handleTimer() : void 
		{
			var nextAnimFrame:Number;
			
			if (!muted) {
				nextAnimFrame = Number(Math.random() * 9 + 1);
			} 
			else 
			{
				nextAnimFrame = 1;
			}
			
			gotoAndStop(nextAnimFrame);
		}
		
		public function set playing(isPlaying:Boolean) : void
		{
			if(_playing == isPlaying)
				return;
			_playing = isPlaying;
			updateState();
		}
		
		public function get playing() : Boolean
		{
			return _playing;
		}
		
		public function set muted(isMuted:Boolean) : void
		{
			if(_muted == isMuted)
				return;
			_muted = isMuted;
			updateState();
		}
		
		public function get muted() : Boolean
		{
			return _muted;
		}
	}

}