package libs.demo.mars;

import libs.engine.Actions;
import libs.engine.Actor;
import libs.engine.Ground;
import libs.engine.Location;


public class LockedDoor extends Ground {

	public LockedDoor() {
		super('+');
	}
	
	@Override
	public boolean canActorEnter(Actor actor) {
		return false;
	}
	
	@Override
	public Actions allowableActions(Actor actor, Location location, String direction){
		return new Actions(new WindowSmashAction(direction, location));
	}
	
	@Override
	public boolean blocksThrownObjects() {
		return true;
	}
}
