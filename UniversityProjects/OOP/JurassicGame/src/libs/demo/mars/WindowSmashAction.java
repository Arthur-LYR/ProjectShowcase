package libs.demo.mars;

import libs.engine.Action;
import libs.engine.Actor;
import libs.engine.GameMap;
import libs.engine.Location;

import java.util.Random;


public class WindowSmashAction extends Action {

	private String direction;
	private Location windowLocation;
	private Random rand = new Random();
	
	public WindowSmashAction(String direction, Location windowLocation) {
		this.direction = direction;
		this.windowLocation = windowLocation;
	}
	
	@Override
	public String execute(Actor actor, GameMap map) {
		if(rand.nextBoolean()) {
			return actor + " hurts their foot.";
		}
		else {
			windowLocation.setGround(new Floor());
			return "The window is smashed";
		}
	}

	@Override
	public String menuDescription(Actor actor) {
		return actor + " smashes the window to the " + direction;
	}
}
