package game.dinosaurs.general;

import java.util.ArrayList;
import java.util.Random;

import libs.engine.Action;
import libs.engine.Actor;
import libs.engine.Exit;
import libs.engine.GameMap;
import libs.engine.Location;
import game.dinosaurs.attack.DeathAction;

public class WanderBehaviour implements Behaviour {
	
	private Random random = new Random();


	/**
	 * Returns a MoveAction to wander to a random location, if possible.  
	 * If no movement is possible, returns null.
	 * 
	 * @param actor the Actor enacting the behaviour
	 * @param map the map that actor is currently on
	 * @return an Action, or null if no MoveAction is possible
	 */
	@Override
	public Action getAction(Actor actor, GameMap map) {
		Dinosaur dinosaur = (Dinosaur) actor;

		ArrayList<Action> actions = new ArrayList<Action>();

		// return DeathAction if the dinosaur is health or water critical
		if (dinosaur.isHealthCritical() || dinosaur.isWaterCritical()) {
			return new DeathAction();
		}

		// return null if the dino cannot move
		if (dinosaur.hasCapability(DinosaurCapabilities.CANNOTMOVE)) {
			return new EndTurnAction();
		}


		for (Exit exit : map.locationOf(actor).getExits()) {
            Location destination = exit.getDestination();
            if (destination.canActorEnter(actor)) {
            	actions.add(exit.getDestination().getMoveAction(actor, "around", exit.getHotKey()));
            }
        }
		
		if (!actions.isEmpty()) {
			return actions.get(random.nextInt(actions.size()));
		}
		else {
			return new EndTurnAction();
		}

	}
}
