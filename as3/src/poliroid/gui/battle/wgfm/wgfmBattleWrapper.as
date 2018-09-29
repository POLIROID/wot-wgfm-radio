package poliroid.gui.battle.wgfm
{
	import flash.utils.setTimeout;
	
	import net.wg.gui.battle.views.vehicleMessages.VehicleMessages;
	import net.wg.gui.battle.views.vehicleMessages.VehicleMessage;
	
	import mods.common.BattleDisplayable;
	
	public class wgfmBattleWrapper extends BattleDisplayable
	{
		
		public function as_showMessage(messageText:String, messageColor:uint, messageLifeTime:uint) : void
		{
			var vehicleMessages:VehicleMessages = battlePage.vehicleMessageList as VehicleMessages;
			var vehicleMessage:VehicleMessage = vehicleMessages._renderersPool.createItem() as VehicleMessage;
			if (vehicleMessage) 
			{
				vehicleMessage._lifeTime = messageLifeTime;
				vehicleMessage.markUsed();
				vehicleMessage.setData("wgfm", messageText, true, messageColor);
				vehicleMessages.pushMessage(vehicleMessage);
			}
			else
			{
				setTimeout(as_showMessage, 50, messageText, messageColor, messageLifeTime);
			}
		}
	}
}
