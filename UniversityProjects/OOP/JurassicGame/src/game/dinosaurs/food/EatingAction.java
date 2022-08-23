package game.dinosaurs.food;

import game.dinosaurs.general.*;
import game.items.*;
import game.terrain.Lake;
import libs.engine.*;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;

/***
 * EatingAction contains the logic for dinosaurs to eat food
 */
public class EatingAction extends Action {

    /**
     * The item to be consumed by the dinosaur
     */
    private Item target;

    /**
     * The location of the item
     */
    private Location itemLocation;

    /**
     * The food value the item provides
     */
    private int foodValue;

    /**
     * Constructor for FeedingAction
     *
     * @param targetItem the item to be consumed by the dinosaur
     */
    public EatingAction(Item targetItem, Location itemLocation) {
        this.target = targetItem;
        this.itemLocation = itemLocation;
    }

    /**
     *  method to allow dinosaurs to eat and heal according to the food value the item provides
     *
     * @param actor The actor performing the action.
     * @param map The map the actor is on.
     * @return String explaining what happened
     */
    @Override
    public String execute(Actor actor, GameMap map) {
        String result = "";
        boolean isNextTo = checkIfNextTo(actor, map);
        boolean isOn = checkIfOn(actor, map);
        if (isNextTo) {
            foodValue = getFoodValue(target, actor);
            actor.heal(foodValue);

            if (!(target instanceof Fish)) {
                itemLocation.removeItem(target);
            } else {
                // remove the eaten fish from the lake
                Lake lake = (Lake) itemLocation.getGround();
                lake.removeFishFromLake(1);
            }

            return actor + " has eaten " + target + " which healed for " + foodValue + " HP";
        } else if (isOn) {
            result += eatingProcessForFlyingPterodactyl(target, actor);
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
        return actor + " eats";
    }


    /**
     *  Method to check if the dinosaur is next to the item
     *
     * @param actor the actor
     * @param map the game map
     * @return boolean variable true or false
     */
    public boolean checkIfNextTo(Actor actor, GameMap map) {
        Location actorLocation = map.locationOf(actor);
        if (distance(actorLocation, itemLocation) == 1) {
            return true;
        }
        return false;
    }

    /**
     * Method to check if the dinosaur is on the item
     *
     * @param actor the actor
     * @param map the game map
     * @return boolean variable true or false
     */
    public boolean checkIfOn(Actor actor, GameMap map) {
        Location actorLocation = map.locationOf(actor);
        if (distance(actorLocation, itemLocation) == 0) {
            return true;
        }
        return false;
    }

    /**
     * Compute the Manhattan distance between two locations.
     *
     * @param a the first location
     * @param b the first location
     * @return the number of steps between a and b if you only move in the four cardinal directions.
     */
    private int distance(Location a, Location b) {
        return Math.abs(a.x() - b.x()) + Math.abs(a.y() - b.y());
    }

    /**
     * Method to randomly return an integer 0, 1 or 2
     *
     * @return integer 0, 1 or 2
     */
    private int getRandomNumber() {
        List<Integer> list = new ArrayList<>();
        list.add(0);
        list.add(1);
        list.add(2);

        Random rand = new Random();
        return list.get(rand.nextInt(list.size()));
    }

    /**
     * Method to get the food value provided by the item to the dinosaur
     *
     * @param target the item
     * @param actor the dinosaur
     * @return the food value provided by the item
     */
    private int getFoodValue(Item target, Actor actor) {
        if (target instanceof Fruit) {
            if (actor instanceof Stegosaur) {
                foodValue = StegosaurFood.FRUIT.getFoodValue();
            } else if (actor instanceof Brachiosaur) {
                foodValue = BrachiosaurFood.FRUIT.getFoodValue();
            } else {
                foodValue = 0;
            }
        } else if (target instanceof Egg) {
            if (actor instanceof Allosaur) {
                foodValue = AllosaurFood.EGGS.getFoodValue();
            } else if (actor instanceof Pterodactyl) {
                foodValue = PterodactylFood.EGGS.getFoodValue();
            } else {
                foodValue = 0;
            }
        } else if (target instanceof VegetarianMealKit) {
            if (actor instanceof Stegosaur) {
                foodValue = StegosaurFood.MEAL_KIT.getFoodValue();
            } else if (actor instanceof Brachiosaur) {
                foodValue = BrachiosaurFood.MEAL_KIT.getFoodValue();
            } else {
                foodValue = 0;
            }
        } else if (target instanceof CarnivoreMealKit) {
            if (actor instanceof Allosaur) {
                foodValue = AllosaurFood.MEAL_KIT.getFoodValue();
            } else if (actor instanceof Pterodactyl) {
                foodValue = PterodactylFood.MEAL_KIT.getFoodValue();
            } else {
                foodValue = 0;
            }
        } else if (target instanceof Corpse) {
            if (actor instanceof Allosaur) {
                foodValue = ((Corpse) target).getFoodValue();
            } else if (actor instanceof Pterodactyl) {
                Pterodactyl pterodactyl = (Pterodactyl) actor;
                pterodactyl.startFeedingOnCorpse();
                ((Corpse) target).decreaseFoodValue(10);
                pterodactyl.heal(10);
                System.out.println(actor + " is starting to feed on " + target);
                pterodactyl.stopFeedingOnCorpse();
            }
        } else if (target instanceof Fish) {
            if (actor instanceof Allosaur) {
                foodValue = AllosaurFood.FISH.getFoodValue();
            } else if (actor instanceof Pterodactyl) {
                foodValue = PterodactylFood.FISH.getFoodValue();
            }

        }
        return foodValue;
    }

    /**
     * Method which runs the logic of eating for flying Pterodactyl and returns a String to explain what happened
     * during eating action
     * @param target
     * @param actor
     * @return String explaining what happened in the eating process for flying Pterodactyl
     */
    private String eatingProcessForFlyingPterodactyl(Item target, Actor actor) {
        String result = "";
        if (target instanceof Corpse) {
            if (actor instanceof Pterodactyl && ((Dinosaur) actor).getDinosaurMode() == DinosaurMode.FLIGHT) {
                Pterodactyl pterodactyl = (Pterodactyl) actor;
                pterodactyl.startFeedingOnCorpse();
                ((Corpse) target).decreaseFoodValue(10);
                pterodactyl.heal(10);
                pterodactyl.stopFeedingOnCorpse();
                result += actor + " is feeding on " + target + " which healed for 10 HP";
            }
        } else if (target instanceof Fish) {
            if (actor instanceof Pterodactyl && ((Dinosaur) actor).getDinosaurMode() == DinosaurMode.FLIGHT) {
                int number = getRandomNumber();
                Pterodactyl pterodactyl = (Pterodactyl) actor;
                int healAmount = 5 * number;
                pterodactyl.heal(healAmount);

                //remove the eaten fish from the lake
                Lake lake = (Lake) itemLocation.getGround();
                lake.removeFishFromLake(number);

                result += actor + " has eaten " + target + " which healed for " + healAmount + " HP";
            }
        }
        return result;
    }
}
