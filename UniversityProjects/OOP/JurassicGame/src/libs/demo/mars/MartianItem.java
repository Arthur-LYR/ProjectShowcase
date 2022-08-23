package libs.demo.mars;

import libs.engine.Action;
import libs.engine.Item;

public class MartianItem extends Item{

	public MartianItem(String name, char displayChar, boolean portable) {
		super(name, displayChar, portable);
	}
	
	public void addAction(Action action) {
		this.allowableActions.add(action);
	}
}
