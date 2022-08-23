package game.dinosaurs.food;

import game.dinosaurs.general.*;
import game.items.*;
import game.terrain.Bush;
import game.terrain.Lake;
import game.terrain.Tree;
import libs.engine.*;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

/***
 * Dinosaur behaviour to search for food. Dinosaur will
 */
public class SearchingFoodBehaviour implements Behaviour {

    /***
     * variable to check if we need to calculate the distance
     */
    private boolean checkValue;

    /***
     * HashMap to store the distances
     */
    private HashMap<Item, Integer> distancesHashMap = new HashMap<>();

    /**
     * HashMap to store the item locations
     */
    private HashMap<Item, Location> itemLocations = new HashMap<>();

    /***
     * Method to get the action that the dinosaur will perform. The map will be scanned to find location of food source
     * and the dinosaurs will approach the food source and attempt to eat it. If no food source is available, the
     * dinosaurs will wander around.
     *
     * @param actor the Actor acting
     * @param map the GameMap containing the Actor
     * @return action the dinosaur will take
     */
    @Override
    public Action getAction(Actor actor, GameMap map) {
        Dinosaur dinosaur = (Dinosaur) actor;

        NumberRange widths = map.getXRange();
        NumberRange heights = map.getYRange();
        Location here = map.locationOf(actor);

        // return null if the dino is hibernating
        if (dinosaur.hasCapability(DinosaurCapabilities.HIBERNATING)) {
            return null;
        }

        // if the Pterodactyl is hungry allow it to leave the tree if it was on a tree
        if (dinosaur instanceof Pterodactyl && dinosaur.isHungry()) {
            dinosaur.removeCapability(DinosaurCapabilities.CANNOTMOVE);
        }

        // skip looking for food if the dinosaur is not hungry
        if (!dinosaur.isHungry()) {
            return null;
        }

        // if dinosaur is thirsty and the water level is closer to 0 compared to HP, skip this behaviour
        if (dinosaur.isThirsty() && (dinosaur.getWaterLevel() < dinosaur.getHitPoints())) {
            return null;
        }

        // print a message telling that the dinosaur is hungry
        System.out.println(actor + " at (" + map.locationOf(actor).x() + "," + + map.locationOf(actor).y() + ") is getting hungry!");

        for (int x : widths) {
            for (int y : heights) {
                Location there = map.at(x, y);
                List<Item> items = there.getItems();
                Ground ground = there.getGround();
                int newDistance = 0;
                // if the item is on the ground
                if (items.size() != 0) {
                    for (Item item : items) {
                        if ((actor instanceof Stegosaur || actor instanceof Brachiosaur) && (item instanceof Fruit || item instanceof VegetarianMealKit)) {
                            checkValue = true;
                        } else if (actor instanceof Allosaur && (item instanceof Corpse || item instanceof Egg || item instanceof CarnivoreMealKit)) {
                            checkValue = true;
                        } else if (actor instanceof Pterodactyl && item instanceof Corpse && !dinosaursNearby(map, x, y)) {
                            checkValue = true;
                        }
                        if (checkValue) {
                            newDistance = distance(here, there);
                            distancesHashMap.put(item, newDistance);
                            itemLocations.put(item, there);
                        }
                    }
                }  else {
                    if (actor instanceof Stegosaur && ground instanceof Bush && ((Bush) ground).getFruitArrayList().size() != 0) {
                        checkValue = true;
                        newDistance = distance(here, there);
                        Item item = new Fruit();
                        distancesHashMap.put(item, newDistance);
                        itemLocations.put(item, there);
                    } else if (actor instanceof Brachiosaur && ground instanceof Tree && ((Tree) ground).getFruitArrayList().size() != 0) {
                        checkValue = true;
                        newDistance = distance(here, there);
                        Item item = new Fruit();
                        distancesHashMap.put(item, newDistance);
                        itemLocations.put(item, there);
                    } else if ((actor instanceof Allosaur || actor instanceof Pterodactyl) && ground instanceof Lake && ((Lake) ground).lakeContainsFish()) {
                        checkValue = true;
                        newDistance = distance(here, there);
                        Item item = new Fish();
                        distancesHashMap.put(item, newDistance);
                        itemLocations.put(item, there);
                    }
                }
            }
        }

        Map.Entry<Item, Integer> minimum = null;
        for (Map.Entry<Item, Integer> entry: distancesHashMap.entrySet()) {
            if (minimum == null || minimum.getValue() > entry.getValue()) {
                minimum = entry;
            }
        }

        // The block below is to move the dinosaur and to return EatingAction
        if (minimum != null) {
            System.out.println(actor + " is searching for food");
            if (minimum.getValue() <= 1 && dinosaur.getDinosaurMode() == DinosaurMode.LAND) {
                return new EatingAction(minimum.getKey(), itemLocations.get(minimum.getKey()));
            } else if (minimum.getValue() == 0 && dinosaur.getDinosaurMode() == DinosaurMode.FLIGHT) {
                return new EatingAction(minimum.getKey(), itemLocations.get(minimum.getKey()));
            } else {
                Item foodKey = minimum.getKey();
                Location foodLocation = itemLocations.get(foodKey);
                int currentDistanceOfDinosaurToFood = distance(here, foodLocation);
                for (Exit exit : map.locationOf(actor).getExits()) {
                    Location destination = exit.getDestination();
                    if (destination.canActorEnter(actor)) {
                        int newDistance = distance(destination, foodLocation);
                        if (newDistance < currentDistanceOfDinosaurToFood) {
                            map.moveActor(actor, destination);
                            System.out.println(actor + " has moved to : (" + map.locationOf(actor).x() + " " +  map.locationOf(actor).y() + ")");
                            break;
                        }
                    }
                }
            }
        } else {
            // if no food found on the map, skip this behaviour
            return null;
        }

        // this point is reached as a result of breaking from loop
        return new EndTurnAction();
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
     * Method to check if there are dinosaurs nearby the item
     *
     * @param gameMap the GameMap containing the Actor
     * @param xCoordinate xCoordinate of the item
     * @param yCoordinate yCoordinate of the item
     * @return true if there are dinosaurs nearby the item, false otherwise
     */
    public boolean dinosaursNearby( GameMap gameMap, int xCoordinate, int yCoordinate) {
        int radius = 1;

        int minXCoordinate = gameMap.getXRange().min();
        int maxXCoordinate = gameMap.getXRange().max();
        int minYCoordinate = gameMap.getYRange().min();
        int maxYCoordinate = gameMap.getYRange().max();

        int lowerBoundX = Math.max(xCoordinate - radius, minXCoordinate);
        int upperBoundX = Math.min(xCoordinate + radius, maxXCoordinate);
        int lowerBoundY = Math.max(yCoordinate - radius, minYCoordinate);
        int upperBoundY = Math.min(yCoordinate + radius, maxYCoordinate);


        for (int i = lowerBoundX; i <= upperBoundX; i++) {
            for (int j = lowerBoundY; j <= upperBoundY; j++) {
                Location there = gameMap.at(i, j);
                if (gameMap.isAnActorAt(there)) {
                    Actor actorAtThere = gameMap.getActorAt(there);
                    if (actorAtThere instanceof Dinosaur) {
                        return true;
                    }
                }
            }
        }
        return false;
    }

}
