package
{
	import com.poliroid.infrastructure.AbstractComponentInjector;
	import com.poliroid.gui.battle.wgfm.wgfmBattleWrapper;
	
	public class wgfmBattleUI extends AbstractComponentInjector 
	{
		private function initSettings() : void 
		{
			componentName = "wgfmBattle";
			componentUI = wgfmBattleWrapper;
			transferBattlePage = true;
		}
	}
}
