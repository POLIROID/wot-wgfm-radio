package poliroid.gui.lobby.wgfm.interfaces.impl 
{
	
	import net.wg.data.constants.Errors;
	import net.wg.infrastructure.base.AbstractView;
	import net.wg.infrastructure.exceptions.AbstractException;
	
	import poliroid.gui.lobby.wgfm.data.StateVO;
	import poliroid.gui.lobby.wgfm.data.HotkeysVO;
	import poliroid.gui.lobby.wgfm.data.SettingsVO;
	import poliroid.gui.lobby.wgfm.data.LocalizationVO;
	
	public class PlayerMeta  extends AbstractView
	{
		
		public var closeView:Function;
		
		public var radioPause:Function;
		
		public var radioPlay:Function;
		
		public var updateVolume:Function;
		
		public var updateMuted:Function;
		
		public var updateChannel:Function;
		
		public var updateRating:Function;
		
		public var updateSettings:Function;
		
		public var updateHotkeys:Function;
		
		public var defaultHotkeys:Function;
		
		public var openExternal:Function;
		
		public function PlayerMeta()
		{
			super();
		}
		
		public function closeViewS() : void
		{
			App.utils.asserter.assertNotNull(closeView, "closeView" + Errors.CANT_NULL);
			closeView();
		}
		
		public function radioPlayS() : void
		{
			App.utils.asserter.assertNotNull(radioPlay, "radioPlay" + Errors.CANT_NULL);
			radioPlay();
		}
		
		public function radioPauseS() : void
		{
			App.utils.asserter.assertNotNull(radioPause, "radioPause" + Errors.CANT_NULL);
			radioPause();
		}
		
		public function updateVolumeS(volume: Number) : void
		{
			App.utils.asserter.assertNotNull(updateVolume, "updateVolume" + Errors.CANT_NULL);
			updateVolume(volume);
		}
		
		public function updateMutedS() : void
		{
			App.utils.asserter.assertNotNull(updateMuted, "updateMuted" + Errors.CANT_NULL);
			updateMuted();
		}
		
		public function updateChannelS(channelIdx: Number) : void
		{
			App.utils.asserter.assertNotNull(updateChannel, "updateChannel" + Errors.CANT_NULL);
			updateChannel(channelIdx);
		}
		
		public function updateRatingS(liked: Boolean) : void
		{
			App.utils.asserter.assertNotNull(updateRating, "updateRating" + Errors.CANT_NULL);
			updateRating(liked);
		}
		
		public function updateSettingsS(name: String, value:Boolean) : void
		{
			App.utils.asserter.assertNotNull(updateSettings, "updateSettings" + Errors.CANT_NULL);
			updateSettings(name, value);
		}
		
		public function updateHotkeysS(name: String, command:String) : void
		{
			App.utils.asserter.assertNotNull(updateHotkeys, "updateHotkeys" + Errors.CANT_NULL);
			updateHotkeys(name, command);
		}
		
		public function defaultHotkeysS() : void
		{
			App.utils.asserter.assertNotNull(defaultHotkeys, "defaultHotkeys" + Errors.CANT_NULL);
			defaultHotkeys();
		}
		
		public function openExternalS() : void
		{
			App.utils.asserter.assertNotNull(openExternal, "openExternal" + Errors.CANT_NULL);
			openExternal();
		}
		
		
		
		
		
		
		
		
		
		public final function as_showWaiting(message:String) : void
		{
			showWaiting(message);
		}
		
		public final function as_hideWaiting() : void
		{
			hideWaiting();
		}
		
		public final function as_setState(ctx:Object): void
		{
			var data:StateVO = new StateVO(ctx);
			setState(data);
		}
		
		public final function as_setChannels(ctx:Object) : void
		{
			setChannels(ctx.channels);
		}
		
		public final function as_setHotkeys(ctx:Object) : void
		{
			var data:HotkeysVO = new HotkeysVO(ctx);
			setHotkeys(data);
		}
		
		public final function as_setSettings(ctx:Object) : void
		{
			var data:SettingsVO = new SettingsVO(ctx);
			setSettings(data);
		}
		
		public final function as_setLocalization(ctx:Object) : void
		{
			var data:LocalizationVO = new LocalizationVO(ctx);
			setLocalization(data);
			if(data)
				data.dispose();
		}
		
		protected function showWaiting(message:String) : void
		{
			var message:String = "as_showWaiting" + Errors.ABSTRACT_INVOKE;
			DebugUtils.LOG_ERROR(message);
			throw new AbstractException(message);
		}
		
		protected function hideWaiting() : void
		{
			var message:String = "as_hideWaiting" + Errors.ABSTRACT_INVOKE;
			DebugUtils.LOG_ERROR(message);
			throw new AbstractException(message);
		}
		
		protected function setState(ctx:StateVO) : void
		{
			var message:String = "as_updateState" + Errors.ABSTRACT_INVOKE;
			DebugUtils.LOG_ERROR(message);
			throw new AbstractException(message);
		}
		
		protected function setChannels(channels:Array) : void
		{
			var message:String = "as_updateChannels" + Errors.ABSTRACT_INVOKE;
			DebugUtils.LOG_ERROR(message);
			throw new AbstractException(message);
		}
		
		protected function setHotkeys(ctx:HotkeysVO) : void
		{
			var message:String = "as_updateHotkeys" + Errors.ABSTRACT_INVOKE;
			DebugUtils.LOG_ERROR(message);
			throw new AbstractException(message);
		}
		
		protected function setSettings(data:SettingsVO) : void
		{
			var message:String = "as_setSettings" + Errors.ABSTRACT_INVOKE;
			DebugUtils.LOG_ERROR(message);
			throw new AbstractException(message);
		}
		
		protected function setLocalization(data:LocalizationVO) : void
		{
			var message:String = "as_setLocalization" + Errors.ABSTRACT_INVOKE;
			DebugUtils.LOG_ERROR(message);
			throw new AbstractException(message);
		}
	}
}