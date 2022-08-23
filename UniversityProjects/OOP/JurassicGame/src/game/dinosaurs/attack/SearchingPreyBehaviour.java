package game.dinosaurs.attack;

import game.dinosaurs.general.*;
import libs.engine.*;

import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;

/**
 * Class for the AttackingBehaviour
 */
public class SearchingPreyBehaviour implements Behaviour {

    /**
     * HashMap for Targets and their locations
     */
    HashMap<Actor, Location> locationsHashMap = new HashMap<>();

    /**
     * Hashmap for Targets and their distance from actor
     */
    HashMap<Actor, Integer> distanceHashMap = new HashMap<>();

    /**
     * Constructor
     */
    public SearchingPreyBehaviour() {    }

    /**
     * Gets the appropriate action
     * @param actor the Actor acting
     * @param map the GameMap containing the Actor
     * @return An instance of AttackAction
     */
    @Override
    public Action getAction(Actor actor, GameMap map) {
        locationsHashMap = getDinosaurLocations(map, actor);
        if (!locationsHashMap.isEmpty()) {
            distanceHashMap = getDistanceHashMap(actor, locationsHashMap, map);
            Map.Entry<Actor, Integer> minimum = null;
            for (Map.Entry<Actor, Integer> entry: distanceHashMap.entrySet()) {
                if (minimum == null || minimum.getValue() > entry.getValue()) {
                    minimum = entry;
                }
            }

            if (minimum != null) {
                System.out.println(actor + " is on the hunt!");
                if (minimum.getValue() <= 1) {
                    return new AllosaurAttackAction(minimum.getKey());
                } else {
                    Actor key = minimum.getKey();
                    Location location = locationsHashMap.get(key);
                    int distanceBetweenDinos = distance(map.locationOf(actor), location);
                    for (Exit exit : map.locationOf(actor).getExits()) {
                        Location destination = exit.getDestination();
                        if (destination.canActorEnter(actor)) {
                            int newDistance = distance(destination, location);
                            if (newDistance < distanceBetweenDinos) {
                                map.moveActor(actor, destination);
                                System.out.println(actor + " has moved to : (" + map.locationOf(actor).x() + " " +  map.locationOf(actor).y() + ")");
                                break;
                            }
                        }
                    }
                }
            }
        } else {
            // if no target to attack is found, skip this behaviour
        }

        return new EndTurnAction();
    }

    /**
     * Method to get the location of Stegosaurs and Pterodactyls on land (that are not recently attacked) and save in a HashMap and return it
     * @param map the game map
     * @param actor the dinosaur finding prey
     * @return the HashMap containing Stegosaurs and location
     */
    public HashMap<Actor, Location> getDinosaurLocations(GameMap map, Actor actor) {
        NumberRange widths = map.getXRange();
        NumberRange heights = map.getYRange();
        HashMap<Actor, Location> hashMap = new HashMap<>();

        for (int x : widths) {
            for (int y : heights) {
                Location there = map.at(x, y);
                if (map.isAnActorAt(there)) {
                    Actor actorAtThere = map.getActorAt(there);
                    if (actorAtThere.getDisplayChar() == 's' || (actorAtThere.getDisplayChar() == 'p' && ((Pterodactyl) actorAtThere).getDinosaurMode() == DinosaurMode.LAND)) {
                        if (!targetInAttackHistory(actor, actorAtThere) && ((Dinosaur) actorAtThere).getDinosaurMode() == DinosaurMode.LAND)
                            hashMap.put(actorAtThere, there);
                    }
                }
            }
        }
        return hashMap;
    }

    /***
     * Method to get the distances of the Stegosaurs and Pterodactyls on land to the main dinosaur and store them in HashMap
     * and return the HashMap
     *
     * @param actor the dinosaur looking for prey
     * @param hashMap the hash map containing actor and location
     * @param map the game map
     * @return hash map containing actor and distance
     */
    public HashMap<Actor, Integer> getDistanceHashMap(Actor actor, HashMap<Actor, Location> hashMap, GameMap map) {
        HashMap<Actor, Integer> distanceHashMap = new HashMap<>();
        Iterator<Map.Entry<Actor, Location>> itr = hashMap.entrySet().iterator();

        while (itr.hasNext()) {
            Map.Entry<Actor, Location> entry = itr.next();
            Location targetLocation = entry.getValue();
            Location actorLocation = map.locationOf(actor);
            int distance = distance(actorLocation, targetLocation);
            distanceHashMap.put(entry.getKey(), distance);
        }

        return distanceHashMap;
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
     * Check to see if the target dinosaur has been recently attacked by the attacking Dinosaur
     * @param actor the attacking dinosaur
     * @param target the prey
     * @return true if recently attacked, false otherwise
     */
    public boolean targetInAttackHistory(Actor actor, Actor target) {
        //downcast actor to Allosaur
        Allosaur allosaur = (Allosaur) actor;
        // only Stegosaur and Pterodactyl can be attacked by Allosaur
        Dinosaur stegosaur = (Dinosaur) target;
//        for (String name : allosaur.getAttackHistory()) {
//            if (name.equals(stegosaur.getName()))
//                return true;
//        }

        for (Map.Entry<String, Integer> entry : allosaur.getAttackHashMap().entrySet()) {
            if (entry.getKey().equals(stegosaur.getName()))
                return true;
        }
        return false;
    }
}
