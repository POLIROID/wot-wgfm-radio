package com.poliroid.gui.lobby.wgfm.components {
	
	import flash.geom.Rectangle;
	
	import net.wg.infrastructure.base.UIComponentEx;
	
	import com.poliroid.gui.lobby.wgfm.data.StateVO;
	
	import com.poliroid.gui.lobby.wgfm.controls.EqualizerAnimation;
	import com.poliroid.gui.lobby.wgfm.controls.LikeButton;
	import com.poliroid.gui.lobby.wgfm.controls.DislikeButton;
	import com.poliroid.gui.lobby.wgfm.controls.StationName;
	
	public class ControlsPanelActive extends UIComponentEx
	{
		
		private static const ANIM_SHOW_START_FRAME:Number = 21;
		private static const ANIM_SHOW_END_FRAME:Number = 40;
		private static const ANIM_HIDE_START_FRAME:Number = 1;
		private static const ANIM_HIDE_END_FRAME:Number = 20;
		
		public var equalizerAnimation:EqualizerAnimation = null;
		
		public var stationName:StationName = null;
		
		public var likeButton:LikeButton = null;
		
		public var dislikeButton:DislikeButton = null;
		
		private var inited:Boolean = false;
		
		public function ControlsPanelActive()
		{
			super();
			gotoAndStop(ANIM_HIDE_END_FRAME);
		}
		
		override protected function configUI() : void 
		{
			super.configUI();
			scrollRect = new Rectangle(0, 0, 305, 28);
		}
		
		override protected function onDispose() : void 
		{
			equalizerAnimation = null;
			stationName = null;
			likeButton = null;
			dislikeButton = null;
			super.onDispose();
		}
		
		public function updateState(oldState:StateVO, newState:StateVO) : void 
		{
			
			if (newState.isError)
			{
				gotoAndStop(ANIM_SHOW_END_FRAME);
			}
			
			else if (oldState.isPlaying != newState.isPlaying)
			{
				if (newState.isPlaying)
				{
					inited ? gotoAndPlay(ANIM_SHOW_START_FRAME) : gotoAndStop(ANIM_SHOW_END_FRAME);
				} 
				else 
				{
					inited ? gotoAndPlay(ANIM_HIDE_START_FRAME) : gotoAndStop(ANIM_HIDE_END_FRAME);
				}
			}
			
			equalizerAnimation.playing = newState.isPlaying;
			equalizerAnimation.muted = newState.isMuted;
			
			if (oldState.currentCompositionName != newState.currentCompositionName)
			{
				stationName.setComposition(newState.currentCompositionName);
			}
			stationName.hasErrors(newState.isError);
			
			likeButton.visible = !newState.isError;
			likeButton.updateStatus(newState.likeButtonStatus);
			
			dislikeButton.visible = !newState.isError;
			dislikeButton.updateStatus(newState.dislikeButtonStatus);
			
			inited = true;
		}
	}
}