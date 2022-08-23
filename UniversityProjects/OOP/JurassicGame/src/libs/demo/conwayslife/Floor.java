package libs.demo.conwayslife;

import libs.engine.Ground;

public class Floor extends Ground {

	public Floor() {
		super('.');
		addCapability(Status.DEAD);
	}
}
