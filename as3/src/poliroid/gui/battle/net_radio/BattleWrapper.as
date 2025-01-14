package poliroid.gui.battle.net_radio
{
	import flash.utils.setTimeout;
	
	import net.wg.gui.battle.views.vehicleMessages.VehicleMessages;
	import net.wg.gui.battle.views.vehicleMessages.VehicleMessage;
	
	import mods.common.BattleDisplayable;
	
	public class BattleWrapper extends BattleDisplayable
	{
		public function as_showMessage(messageText:String, messageColor:uint, messageLifeTime:uint) : void {
			try {
				var vehicleMessages:VehicleMessages = battlePage.vehicleMessageList as VehicleMessages;
				var vehicleMessage:VehicleMessage = vehicleMessages._renderersPool.createItem() as VehicleMessage;
				if (vehicleMessage) {
					vehicleMessage._lifeTime = messageLifeTime;
					vehicleMessage.markUsed();
					vehicleMessage.setData("net_radio", messageText, true, messageColor);
					vehicleMessages.pushMessage(vehicleMessage);
				} else {
					setTimeout(as_showMessage, 50, messageText, messageColor, messageLifeTime);
				}
			} catch(error:Error){
			}
		}
	}
}
