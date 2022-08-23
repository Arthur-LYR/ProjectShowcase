package game.items;

import game.main.Player;
import game.main.Util;
import game.terrain.Bush;
import game.terrain.Tree;
import libs.engine.Action;
import libs.engine.Actor;
import libs.engine.GameMap;
import libs.engine.Location;

/**
 * Class that represents the Action of Picking a Fruit up from a Tree, Bush, or the Ground
 */
public class PickFruitAction extends Action {
    /**
     * The Fruit to be picked up
     */
    private Fruit fruit;

    /**
     * Constructor for PickFruitAction
     * @param fruit The Fruit to be picked up
     */
    public PickFruitAction(Fruit fruit) {
        this.fruit = fruit;
    }

    /**
     * Executes the PickFruitAction
     * @param actor The actor performing the action.
     * @param map The map the actor is on.
     * @return The message of the Action outcome
     */
    @Override
    public String execute(Actor actor, GameMap map) {
        // Get location of Actor and Type of Ground
        Location location = map.locationOf(actor);
        char locationGround = location.getGround().getDisplayChar();

        // Initialise Variables
        Fruit fruit;
        String result = actor + " picks up a ripe Fruit from ";

        // Add Fruit to Inventory
        if (locationGround == 'B') {
            Bush bush = (Bush) location.getGround();
            fruit = bush.pickFruitFromBush();
            fruit.setHabitat("Inventory");
            actor.addItemToInventory(fruit);
            Player.gainEcoPoints(10);
            return result + " Bush";
        } else if (locationGround == 'O') {
            fruit = (Fruit) location.getItems().get(0);
            fruit.setHabitat("Inventory");
            actor.addItemToInventory(fruit);
            map.locationOf(actor).removeItem(fruit);
            Player.gainEcoPoints(10);
            return result + " Ground";
        } else if (locationGround == 'F' && Util.eventSuccess(2, 5)) {
            Tree tree = (Tree) location.getGround();
            fruit = tree.pickFruitFromTree();
            fruit.setHabitat("Inventory");
            actor.addItemToInventory(fruit);
            Player.gainEcoPoints(10);
            return result + " Tree";
        } else {
            return actor + " failed to pick up Fruit";
        }
    }

    /**
     * Displays the option in the menu
     * @param actor The actor performing the action.
     * @return Description in Menu
     */
    @Override
    public String menuDescription(Actor actor) {
        return actor + " searches for Fruits";
    }
}
