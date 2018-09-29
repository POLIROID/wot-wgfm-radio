
package poliroid.gui.lobby.wgfm.data 
{
	import net.wg.data.daapi.base.DAAPIDataClass;
	
	public class StateVO extends DAAPIDataClass
	{
		
		public var isError:Boolean = false;
		
		public var isPlaying:Boolean = false;
		
		public var isMuted:Boolean = false;
		
		public var currentVolume:Number = 5.0;
		
		public var currentChannelIdx:Number = 0;
		
		public var currentCompositionName:String = "test";
		
		public var likeButtonStatus:String = "test";
		
		public var dislikeButtonStatus:String = "test";
		
		public function StateVO(data:Object) 
		{
			super(data);
		}
	}
}