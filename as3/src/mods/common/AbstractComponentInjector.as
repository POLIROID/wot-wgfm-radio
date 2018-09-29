package mods.common
{
	import net.wg.data.constants.generated.APP_CONTAINERS_NAMES;
	import net.wg.gui.battle.views.BaseBattlePage;
	import net.wg.gui.components.containers.MainViewContainer;
	import net.wg.gui.components.containers.ManagedContainer;
	import net.wg.infrastructure.base.AbstractView;
	import net.wg.infrastructure.interfaces.ISimpleManagedContainer;
	import net.wg.infrastructure.interfaces.IManagedContainer;
	import net.wg.infrastructure.managers.impl.ContainerManagerBase;

	public class AbstractComponentInjector extends AbstractView
	{
		public var componentUI:Class = null;
		public var componentName:String = null;
		public var autoDestroy:Boolean = false;

		public var destroy:Function = null;

		private function createComponent() : BattleDisplayable 
		{
			var component: BattleDisplayable = new componentUI() as BattleDisplayable;
			configureComponent(component);
			return component;
		}

		protected function configureComponent(component: BattleDisplayable) : void
		{
			// You can configure your UI for any context
		}

		override protected function onPopulate() : void 
		{
			super.onPopulate();

			var mainViewContainer:IManagedContainer;
			var windowContainer:ISimpleManagedContainer;

			for each (var container:ISimpleManagedContainer in (App.containerMgr as ContainerManagerBase).containersMap)
			{
				if ((container as MainViewContainer) != null)
				{
					mainViewContainer = container as MainViewContainer;
				}
				var mngdContainer:ManagedContainer = container as ManagedContainer;
				if (mngdContainer != null && mngdContainer.type == APP_CONTAINERS_NAMES.WINDOWS)
				{
					windowContainer = container;
				}
			}
			
			for (var idx:int = 0; idx < mainViewContainer.numChildren; ++idx)
			{
				var view:BaseBattlePage = mainViewContainer.getChildAt(idx) as BaseBattlePage;
				if (view)
				{
					var component: BattleDisplayable = createComponent();
					component.componentName = componentName;
					component.battlePage = view;
					component.initBattle();
					break;
				}
			}
			
			mainViewContainer.setFocusedView(mainViewContainer.getTopmostView());
			
			if (windowContainer != null)
			{
				windowContainer.removeChild(this);
			}
			
			if (autoDestroy)
			{
				destroy();
			}
		}
	}
}
