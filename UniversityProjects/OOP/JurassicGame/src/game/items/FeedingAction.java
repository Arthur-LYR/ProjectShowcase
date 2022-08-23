package game.items;

import libs.engine.Action;
import libs.engine.Actor;
import libs.engine.GameMap;
import libs.engine.Item;
import game.dinosaurs.food.AllosaurFood;
import game.dinosaurs.food.BrachiosaurFood;
import game.dinosaurs.food.PterodactylFood;
import game.dinosaurs.food.StegosaurFood;
import game.dinosaurs.general.*;
import game.main.Player;

import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

/***
 * FeedingAction class contains the logic for the player to feed the dinosaurs
 */
public class FeedingAction extends Action {

    /***
     * The dinosaur which the player is trying to feed
     */
    private Dinosaur target;

    /**
     * ArrayList that contains the items in the player's inventory
     */
    private List<Item> itemList = new ArrayList<>();

    /***
     * Constructor.
     *
     * @param target the dinosaur
     */
    public FeedingAction(Dinosaur target) {
        this.target = target;
    }

    /***
     * Method to execute the process of player obtaining item from inventory and feeding the dinosaur
     *
     * @param actor The actor performing the action.
     * @param map The map the actor is on.
     * @return String to explain what happened
     */
    @Override
    public String execute(Actor actor, GameMap map) {
        String result = "";
        itemList = actor.getInventory();
        if (itemList.size() == 0) {
            result += "Player Inventory is Empty. Failed to Feed Dinosaur";
        } else {
            int numberSelected = itemSelectionMenu();
            Item item = processSelection(numberSelected);
            if (item != null) {
                result += item + " was fed to " + target;
                actor.removeItemFromInventory(item);
                Player.gainEcoPoints(10);
            } else {
                result += "Nothing was fed to " + target;
            }
        }
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
        return actor + " feeds something to the dinosaurs";
    }

    /**
     * Method to create the menu for player to select item to attempt to feed the dinosaur
     *
     * @return the selected number by the player
     */
    public int itemSelectionMenu() {
        Scanner myObj = new Scanner(System.in);  // Create a Scanner object
        System.out.println("Select one item from below to feed the dinosaur:");
        String string = "";
        for (int i = 0; i < itemList.size(); i++) {
            string += (i + 1) + ". " + itemList.get(i);
        }
        System.out.println(string);
        int number = 0;
        boolean valid;
        do {
            try {
                number = Integer.parseInt(myObj.nextLine());
                if (number >= 1 && number <= itemList.size()) {
                    valid = true;
                } else {
                    valid = false;
                }
            } catch (Exception e) {
                valid = false;
            }
        } while (!valid);
        return number;
    }

    /***
     * Method to process the selection made by the player and feeds the dinosaur
     *
     * @param selectedNumber
     * @return the selected item by the player
     */
    public Item processSelection(int selectedNumber) {
        Item selectedItem = itemList.get(selectedNumber - 1);

        if (selectedItem instanceof Fruit && target instanceof Stegosaur) {
            target.heal(StegosaurFood.PLAYER_FRUIT.getFoodValue());
            if (target.getIsHibernating())
                reviveTarget(target);
        } else if (selectedItem instanceof Fruit && target instanceof Brachiosaur) {
            target.heal(BrachiosaurFood.PLAYER_FRUIT.getFoodValue());
            if (target.getIsHibernating())
                reviveTarget(target);
        } else if (selectedItem instanceof Egg && target instanceof Allosaur) {
            target.heal(AllosaurFood.EGGS.getFoodValue());
            if (target.getIsHibernating())
                reviveTarget(target);
        } else if (selectedItem instanceof Egg && target instanceof Pterodactyl) {
            target.heal(PterodactylFood.EGGS.getFoodValue());
            if (target.getIsHibernating())
                reviveTarget(target);
        } else if (selectedItem instanceof VegetarianMealKit && target instanceof Stegosaur) {
            target.heal(StegosaurFood.MEAL_KIT.getFoodValue());
            if (target.getIsHibernating())
                reviveTarget(target);
        } else if (selectedItem instanceof VegetarianMealKit && target instanceof Brachiosaur) {
            target.heal(BrachiosaurFood.MEAL_KIT.getFoodValue());
            if (target.getIsHibernating())
                reviveTarget(target);
        } else if (selectedItem instanceof CarnivoreMealKit && target instanceof Allosaur) {
            target.heal(AllosaurFood.MEAL_KIT.getFoodValue());
            if (target.getIsHibernating())
                reviveTarget(target);
        } else {
            return null;
        }
        return selectedItem;
    }

    /**
     * Method to revive an unconscious dinosaur that was due to lack of food
     *
     * @param target the dinosaur that was unconscious
     */
    public void reviveTarget(Dinosaur target) {
        if (target.getUnconsciousReason() == UnconsciousReason.FOOD) {
            target.isHibernating(false);
            target.removeUnconsciousReason();
            target.removeCapability(DinosaurCapabilities.HIBERNATING);
        }
    }
}
