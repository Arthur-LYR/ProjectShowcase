package libs.demo.mars;

import libs.engine.Action;
import libs.engine.Actor;
import libs.engine.GameMap;
import java.util.*;

public class KickAction extends Action {

	private Actor target;
	private Random rand = new Random();

	public KickAction(Actor target) {
		this.target = target;
	}

	@Override
	public String execute(Actor actor, GameMap map) {
		if (rand.nextBoolean()) {
			return target + " evades the clumsy kick.";
		} else {
			map.removeActor(target);
			return actor + " squashes " + target + " like a bug.";
		}
	}

	@Override
	public String menuDescription(Actor actor) {
		return actor + " kicks " + target;
	}
}
