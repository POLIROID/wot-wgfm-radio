package
{
	import mods.common.AbstractComponentInjector;
	import poliroid.gui.battle.wgfm.wgfmBattleWrapper;
	
	public class wgfmBattleUI extends AbstractComponentInjector 
	{
		override protected function onPopulate() : void
		{
			componentName = "wgfmBattle";
			componentUI = wgfmBattleWrapper;
		}
	}
}
