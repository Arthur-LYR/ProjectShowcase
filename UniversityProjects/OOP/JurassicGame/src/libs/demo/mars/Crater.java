package libs.demo.mars;

import libs.engine.Actor;
import libs.engine.Ground;


public class Crater extends Ground {

	public Crater() {
		super('o');
	}
	
	@Override
	public boolean canActorEnter(Actor a) {
		return a.hasCapability(DemoCapabilities.SPACETRAVELLER);
	}
}