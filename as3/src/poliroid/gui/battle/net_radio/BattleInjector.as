package poliroid.gui.battle.net_radio
{
	import mods.common.AbstractComponentInjector;
	import poliroid.gui.battle.net_radio.BattleWrapper;
	
	public class BattleInjector extends AbstractComponentInjector 
	{
		override protected function onPopulate() : void
		{
			autoDestroy = false;
			componentName = "NetRadioBattle";
			componentUI = BattleWrapper;
			super.onPopulate();
		}
	}
}
