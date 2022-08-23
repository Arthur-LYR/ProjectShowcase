package game.terrain;

import libs.engine.Actor;
import libs.engine.Ground;
import libs.engine.Location;
import game.main.Util;

/**
 * Class to tell if it is raining
 */
public class Rain extends Ground {
    /**
     * Number of turns that have passed
     */
    private static int turns = 0;

    /**
     * Boolean that randomly switches value each turn
     */
    private static boolean checkRain;

    /**
     * Constructor.
     */
    public Rain() {
        super('#');
    }

    /**
     * Simply increments turns and updates checkRain each turn
     * @param location The location of the Ground
     */
    @Override
    public void tick(Location location) {
        super.tick(location);
        turns++;
        checkRain = Util.eventSuccess(1, 5);
    }

    /**
     * This method decides if it is raining for the entire map
     * @return true - If raining, false - otherwise
     */
    public static boolean isRaining() {
        return turns % 10 == 0 && checkRain;
    }

    /**
     * Actors can't pass through
     * @param actor the Actor to check
     * @return false
     */
    @Override
    public boolean canActorEnter(Actor actor) {
        return false;
    }

    /**
     * Thrown objects are blocked
     * @return true
     */
    @Override
    public boolean blocksThrownObjects() {
        return true;
    }
}
