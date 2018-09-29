package poliroid.gui.lobby.wgfm.controls {
	
	import flash.display.Bitmap;
	import flash.display.MovieClip;
	import flash.events.Event;
	import flash.events.MouseEvent;
	import flash.text.TextFormat;
	import net.wg.gui.components.controls.LabelControl;
	import poliroid.views.WgfmPlayer;
	import flash.events.TimerEvent;
	import flash.utils.Timer;
	import flash.geom.Rectangle;
	import scaleform.clik.core.UIComponent;
	
	public class KeyHolder  extends UIComponent {
		
		public var is_pressed:Boolean = false;
		public var is_hovered:Boolean = false;
		public var is_accepting:Boolean = false;
		public var is_setted:Boolean = false;
		
		
		public var key_id:String;
		private var __handler:SettingsFirst;
		
		
		public var sectionName:LabelControl;
		public var keyName:LabelControl;
		private var elements:Array;
		
		private var animTimer:Timer;
		private var animVector:Number = 0;
		
		//[Embed(source="../../../res/wgfmPlayer/key_input_normal.png")]
		private static var key_input_normal:Class;
		private var image_key_input_normal:Bitmap;
		//[Embed(source="../../../res/wgfmPlayer/key_input_hovered.png")]
		private static var key_input_hovered:Class;
		private var image_key_input_hovered:Bitmap;
		//[Embed(source="../../../res/wgfmPlayer/key_input_pressed.png")]
		private static var key_input_pressed:Class;
		private var image_key_input_pressed:Bitmap;
		//[Embed(source="../../../res/wgfmPlayer/key_input_accept_key.png")]
		private static var key_input_accept_key:Class;
		private var image_key_input_accept_key:Bitmap;
		//[Embed(source="../../../res/wgfmPlayer/key_input_no_key.png")]
		private static var key_input_no_key:Class;
		private var image_key_input_no_key:Bitmap;
		
		
		
		
		
		
		
		
		public function KeyHolder(_handler:SettingsFirst, _id:String, _label:String):void {
			
			super();
			
			this.key_id = _id
			this.__handler = _handler;
			
			
			this.sectionName = App.utils.classFactory.getComponent("LabelControl", LabelControl); 
			this.sectionName.y = 2; 
			this.sectionName.x = 10; 
			this.sectionName.text = _label
			this.sectionName.width = 200;
			this.sectionName.height = 24;
			this.addChild(this.sectionName);
			
			this.sectionName.validateNow();
			this.sectionName.width = this.sectionName.textField.textWidth + 10;
			
			
			this.image_key_input_normal = new key_input_normal();
			this.image_key_input_hovered = new key_input_hovered();
			this.image_key_input_pressed = new key_input_pressed();
			this.image_key_input_no_key = new key_input_no_key();
			this.image_key_input_accept_key = new key_input_accept_key();
			
			this.image_key_input_normal.visible = false;
			this.image_key_input_hovered.visible = false;
			this.image_key_input_pressed.visible = false;
			this.image_key_input_no_key.visible = false;
			this.image_key_input_accept_key.visible = false;
			
			
			
			
			this.keyName = App.utils.classFactory.getComponent("LabelControl", LabelControl); 
			this.keyName.y = 3;
			this.keyName.width = 60;
			this.keyName.textAlign = "center";
			
			var KeyHolder:UIComponent = new UIComponent();
			KeyHolder.buttonMode = true;
			KeyHolder.useHandCursor = true;
			KeyHolder.y = 1;
			KeyHolder.x = 180;
			KeyHolder.width = 60;
			KeyHolder.height = 25;
			KeyHolder.addChild(this.image_key_input_normal);
			KeyHolder.addChild(this.image_key_input_hovered);
			KeyHolder.addChild(this.image_key_input_pressed);
			KeyHolder.addChild(this.image_key_input_no_key);
			KeyHolder.addChild(this.image_key_input_accept_key);
			KeyHolder.addChild(this.keyName);
			
			var click_mask:MovieClip = new MovieClip();
			click_mask.x = 0;
			click_mask.y = 0;
			click_mask.width = 60;
			click_mask.height = 25;
			click_mask.buttonMode = true;
			click_mask.useHandCursor = true;
			click_mask.graphics.beginFill(0xFF0000, 0.5);
			click_mask.graphics.drawRect(0, 0, 60, 25);
			click_mask.graphics.endFill();
			KeyHolder.addChild(click_mask);
			
			KeyHolder.addEventListener(MouseEvent.CLICK, this.handleMouseClick);
			KeyHolder.addEventListener(MouseEvent.MOUSE_DOWN, this.handleMouseDown);
			KeyHolder.addEventListener(MouseEvent.MOUSE_UP, this.handleMouseUp);
			KeyHolder.addEventListener(MouseEvent.ROLL_OUT, this.handleMouseRollOut);
			KeyHolder.addEventListener(MouseEvent.ROLL_OVER, this.handleMouseRollOver);
			this.addChild(KeyHolder);
			
			this.elements = new Array();
			this.elements.push(this.image_key_input_normal);
			this.elements.push(this.image_key_input_hovered);
			this.elements.push(this.image_key_input_pressed);
			
			this.update();
			
			this.animTimer = new Timer(80);
			this.animTimer.addEventListener(TimerEvent.TIMER, this.playAnimFrame);
		}
		
		
		public function setKey(text:String):void {
			if (text == "") {
				this.is_setted = false;
			} else {
				this.is_setted = true;
			}
			this.is_accepting = false;
			this.keyName.text = text;
			this.updateVisibility();
		}
		
		
		private function handleMouseClick(event:MouseEvent):void {
			this.is_accepting = true;
			this.__handler.onStartSetNewKey(this);
			this.updateVisibility();
			this.animTimer.start();
		}
		
		private function handleMouseRollOver(event:MouseEvent):void {
			this.is_hovered = true;
			this.updateVisibility();
		}
		
		private function handleMouseRollOut(event:MouseEvent):void {
			this.is_hovered = false;
			this.is_pressed = false;
			this.updateVisibility();
		}
		
		private function handleMouseDown(event:MouseEvent):void {
			this.is_pressed = true;
			this.is_hovered = true;
			this.updateVisibility();
		}
		
		private function handleMouseUp(event:MouseEvent):void {
			this.is_pressed = false;
			this.updateVisibility();
		}
		
		public function update():void {
			this.updateVisibility();
		}
		
		private function updateVisibility():void {
			
			var for_show:Bitmap = null;
			
			if (this.is_pressed) {
				for_show = this.image_key_input_pressed;
			} else if (this.is_hovered) { 
				for_show = this.image_key_input_hovered;
			} else {
				for_show = this.image_key_input_normal;
			}
			
			for_show.visible = true;
			
			this.image_key_input_accept_key.visible = this.is_accepting;
			this.image_key_input_no_key.visible = this.is_accepting? false : !this.is_setted;
			
			for (var key:String in this.elements) {
				if (this.elements[key] != for_show) {
					this.elements[key].visible = false;
				}
			}
			
		}
		
		private function playAnimFrame():void {
			if (this.is_accepting) {
				
				if (this.animVector == 0) {
					this.image_key_input_accept_key.alpha -= 0.1
					if (this.image_key_input_accept_key.alpha < 0.4) {
						this.animVector = 1;
					}
				} 
				if (this.animVector == 1) {
					this.image_key_input_accept_key.alpha += 0.1
					if (this.image_key_input_accept_key.alpha >= 1) {
						this.animVector = 0;
					}
				} 
				
			} else {
				this.animTimer.stop();
			}
		}
	}

}