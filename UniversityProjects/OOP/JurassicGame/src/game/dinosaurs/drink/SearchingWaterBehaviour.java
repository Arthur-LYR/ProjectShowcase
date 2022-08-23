package game.dinosaurs.drink;

import game.dinosaurs.general.*;
import game.terrain.Lake;
import libs.engine.*;

import java.util.HashMap;
import java.util.Map;

public class SearchingWaterBehaviour implements Behaviour{

    /***
     * variable to check if we need to calculate the distance
     */
    private boolean checkValue;

    /***
     * HashMap to store the distances
     */
    private HashMap<Ground, Integer> distancesHashMap = new HashMap<>();

    /**
     * HashMap to store the lake locations
     */
    private HashMap<Ground, Location> lakeLocations = new HashMap<>();

    /***
     * Method to get the action that the dinosaur will perform. The map will be scanned to find location of water source
     * and the dinosaurs will approach the water source and attempt to drink from it. If no water source is available, the
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

        // if the Pterodactyl is thirsty allow it to leave the tree if it was on a tree
        if (dinosaur instanceof Pterodactyl && dinosaur.isThirsty()) {
            dinosaur.removeCapability(DinosaurCapabilities.CANNOTMOVE);
        }

        // skip looking for water if the dinosaur is not thirsty
        if (!dinosaur.isThirsty()) {
            return null;
        }

        // if dinosaur is both hungry and thirsty but hunger is more serious, skip this behaviour
        if (dinosaur.isHungry() && dinosaur.isThirsty()) {
            if (dinosaur.getHitPoints() < dinosaur.getWaterLevel()) {
                return null;
            }
        }

        // print a message telling that the dinosaur is thirsty
        System.out.println(actor + " at (" + map.locationOf(actor).x() + "," + + map.locationOf(actor).y() + ") is getting thirsty!");

        for (int x : widths) {
            for (int y : heights) {
                Location there = map.at(x, y);
                Ground ground = there.getGround();
                int newDistance = 0;
                if (ground instanceof Lake && ((Lake) ground).getSips() > 0) {
                    checkValue = true;
                } else {
                    checkValue = false;
                }

                if (checkValue) {
                    newDistance = distance(here, there);
                    Ground lake = new Lake();
                    distancesHashMap.put(lake, newDistance);
                    lakeLocations.put(lake, there);
                }
            }
        }

        Map.Entry<Ground, Integer> minimum = null;
        for (Map.Entry<Ground, Integer> entry: distancesHashMap.entrySet()) {
            if (minimum == null || minimum.getValue() > entry.getValue()) {
                minimum = entry;
            }
        }

        // The block below is to move the dinosaur and to return DrinkingAction
        if (minimum != null) {
            System.out.println(actor + " is searching for water");
            if (minimum.getValue() == 0 && ((Dinosaur) actor).getDinosaurMode() == DinosaurMode.FLIGHT) {
                return new DrinkingAction(minimum.getKey(), lakeLocations.get(minimum.getKey()));
            } else if (minimum.getValue() == 1 && ((Dinosaur) actor).getDinosaurMode() == DinosaurMode.LAND){
                return new DrinkingAction(minimum.getKey(), lakeLocations.get(minimum.getKey()));
            } else {
                Ground lakeKey = minimum.getKey();
                Location lakeLocation = lakeLocations.get(lakeKey);
                int currentDistanceOfDinosaurToLake = distance(here, lakeLocation);
                for (Exit exit : map.locationOf(actor).getExits()) {
                    Location destination = exit.getDestination();
                    if (destination.canActorEnter(actor)) {
                        int newDistance = distance(destination, lakeLocation);
                        if (newDistance < currentDistanceOfDinosaurToLake) {
                            map.moveActor(actor, destination);
                            System.out.println(actor + " has moved to : (" + map.locationOf(actor).x() + " " +  map.locationOf(actor).y() + ")");
                            break;

                        }
                    }
                }
            }
        } else {
            // if there is no water found on the map, skip this behaviour
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

    /***
     * Method to check if the hit points of the dinosaur reached zero and set unconscious reason
     *
     * @param actor the dinosaur
     * @return true if health is zero, false otherwise
     */
    public boolean healthCritical(Actor actor) {
        boolean isZeroHealth = false;
        if (actor.getDisplayChar() == 'd') {
            Stegosaur dino = (Stegosaur) actor;
            if (dino.getHitPoints() <= 0) {
                isZeroHealth = true;
                dino.setUnconsciousReason(UnconsciousReason.FOOD);
            }
        } else if (actor.getDisplayChar() == 'r') {
            Brachiosaur dino = (Brachiosaur) actor;
            if (dino.getHitPoints() <= 0) {
                isZeroHealth = true;
                dino.setUnconsciousReason(UnconsciousReason.FOOD);
            }
        } else if (actor.getDisplayChar() == 'a') {
            Allosaur dino = (Allosaur) actor;
            if (dino.getHitPoints() <= 0) {
                isZeroHealth = true;
                dino.setUnconsciousReason(UnconsciousReason.FOOD);
            }
        }
        return isZeroHealth;
    }

    /**
     * Method to check if the water level of the dinosaur reached zero and set unconscious reason
     *
     * @param actor the dinosaur
     * @return true if water level is zero, false otherwise
     */
    public boolean waterCritical(Actor actor) {
        boolean isZeroWater = false;
        if (actor.getDisplayChar() == 'd') {
            Stegosaur dino = (Stegosaur) actor;
            if (dino.getWaterLevel() <= 0) {
                isZeroWater = true;
                dino.setUnconsciousReason(UnconsciousReason.WATER);
            }
        } else if (actor.getDisplayChar() == 'r') {
            Brachiosaur dino = (Brachiosaur) actor;
            if (dino.getWaterLevel() <= 0) {
                isZeroWater = true;
                dino.setUnconsciousReason(UnconsciousReason.WATER);
            }
        } else if (actor.getDisplayChar() == 'a') {
            Allosaur dino = (Allosaur) actor;
            if (dino.getWaterLevel() <= 0) {
                isZeroWater = true;
                dino.setUnconsciousReason(UnconsciousReason.WATER);
            }
        }
        return isZeroWater;
    }
}
