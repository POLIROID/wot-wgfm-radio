package com.poliroid.infrastructure
{
	import net.wg.gui.battle.views.BaseBattlePage;
	import net.wg.gui.components.containers.MainViewContainer;
	import net.wg.infrastructure.base.AbstractView;
	import net.wg.infrastructure.interfaces.IManagedContainer;
	import net.wg.infrastructure.interfaces.ISimpleManagedContainer;
	import net.wg.gui.components.containers.ManagedContainer;
	import net.wg.infrastructure.interfaces.IView;
	import net.wg.infrastructure.managers.impl.ContainerManagerBase;
	import net.wg.data.constants.generated.APP_CONTAINERS_NAMES;
	
	public class AbstractComponentInjector extends AbstractView
	{
		public var transferBattlePage:Boolean = false;
		public var componentUI:Class = null;
		public var componentName:String = null;

		override protected function onPopulate() : void 
		{
			super.onPopulate();
			
			initSettings();
			
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
				var view:IView = mainViewContainer.getChildAt(idx) as IView;
				if ((view != null) && (view as AbstractView) is BaseBattlePage)
				{
					var battlePage:AbstractView = view as AbstractView;
					var component:* = new componentUI() as componentUI;
					if (transferBattlePage)
					{
						component.battlePage = battlePage;
					}
					battlePage.addChild(component);
					battlePage.registerFlashComponent(component, componentName);
					break;
				}
			}
			
			mainViewContainer.setFocusedView(mainViewContainer.getTopmostView());
			windowContainer.removeChild(this);
		}
		
		private function initSettings() : void
		{
			null;
		}
	}
}
