package game.dinosaurs.attack;

import game.dinosaurs.general.Dinosaur;
import game.dinosaurs.general.DinosaurCapabilities;
import game.dinosaurs.general.UnconsciousReason;
import game.items.Corpse;
import libs.engine.*;

/**
 * DeathAction contains the logic for the dinosaurs to die and be removed from the game
 */
public class DeathAction extends Action {
    /**
     * String that explains what happened when the action took place
     */
    private String result = "";

    /**
     * Method to cause dinosaurs with 0 hit points to go unconscious and unconscious dinosaurs to be removed from the
     * game after certain number of turns while incrementing number of turns for the unconscious dinosaurs that have
     * not reached the threshold
     *
     * @param actor The actor performing the action.
     * @param map The map the actor is on.
     * @return String to explain what happened
     */
    @Override
    public String execute(Actor actor, GameMap map) {
        Dinosaur dino = (Dinosaur) actor;   // down-cast to use Dinosaur methods
        if (!dino.getIsHibernating()) {
            dino.isHibernating(true);
            dino.addCapability(DinosaurCapabilities.HIBERNATING);
            dino.incrementUnconsciousTurns();
            if (dino.getUnconsciousReason() == UnconsciousReason.FOOD) {
                return actor + " is hibernating due to extreme hunger";
            } else if (dino.getUnconsciousReason() == UnconsciousReason.WATER) {
                return actor + " is hibernating due to extreme thirst";
            }
        } else {
            if ((dino.getUnconsciousTurns() >= dino.getUnconsciousFoodThreshold() && dino.getUnconsciousReason() == UnconsciousReason.FOOD) ||
                    (dino.getUnconsciousTurns() >= dino.getUnconsciousWaterThreshold() && dino.getUnconsciousReason() == UnconsciousReason.WATER)) {
                Item corpse = new Corpse("dead " + dino, '%', dino.getDinosaurCode(), true);
                map.locationOf(dino).addItem(corpse);
                Actions dropActions = new Actions();
                for (Item item : dino.getInventory())
                    dropActions.add(item.getDropAction());
                for (Action drop : dropActions)
                    drop.execute(dino, map);
                map.removeActor(dino);

                result += dino + " is dead.";
                return result;
            } else {
                dino.incrementUnconsciousTurns();
            }
        }
        result += actor + " has hibernated for " + dino.getUnconsciousTurns() + " turn(s)";
        return result;
    }

    /**
     * Returns a descriptive string
     *
     * @param actor The actor performing the action.
     * @return the text we put on the menu
     */
    @Override
    public String menuDescription(Actor actor) {
        return actor + "cannot move or do anything until fed";
    }
}
