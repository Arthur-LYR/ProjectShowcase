package game.dinosaurs.breed;

import game.dinosaurs.general.*;
import game.terrain.Tree;
import libs.engine.*;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;

public class SearchingMateBehaviour implements Behaviour {


    HashMap<Actor, Location> locationsHashMap = new HashMap<>();

    HashMap<Actor, Integer> distanceHashMap = new HashMap<>();

    @Override
    public Action getAction(Actor actor, GameMap map) {
        Dinosaur dinosaur = (Dinosaur) actor;

        HashMap<Actor, Location> hashMap = getSameSpeciesDinosaurs(actor, map);
        locationsHashMap = filterDinosaurs(actor, hashMap, map);

        // return null if the dino is hibernating
        if (dinosaur.hasCapability(DinosaurCapabilities.HIBERNATING)) {
            return null;
        }

        // if the dinosaur is thirsty or too hungry, we don't execute this behaviour
        if (dinosaur.isThirsty() || dinosaur.tooHungryToBreed()) {
            return null;
        }

        // if dinosaur is female Pterodactyl and wants to breed, skip this behaviour (they wait for male to find them)
        if (dinosaur instanceof Pterodactyl && dinosaur.getGender() == Gender.FEMALE) {
            ((Pterodactyl) dinosaur).setTryingToBreed(true);
            return null;
        }

        // if there is no suitable mate found, we skip this behaviour
        if (locationsHashMap.isEmpty()) {
            return null;
        }

        if (!dinosaur.isPregnant()) {
            if (!locationsHashMap.isEmpty()) {
                distanceHashMap = getDistanceHashMap(actor, locationsHashMap, map);
                Map.Entry<Actor, Integer> minimum = null;
                for (Map.Entry<Actor, Integer> entry: distanceHashMap.entrySet()) {
                    if (minimum == null || minimum.getValue() > entry.getValue()) {
                        minimum = entry;
                    }
                }

                if (minimum != null) {
                    System.out.println(actor + " is searching for a mate");
                    if (minimum.getValue() == 1 && !(actor instanceof Pterodactyl)) {
                        return new BreedingAction(minimum.getKey());
                    } else if (actor instanceof Pterodactyl && minimum.getValue() <= 1) {
                        Pterodactyl pterodactyl = (Pterodactyl) actor;
                        pterodactyl.setOnTree(true);
                        pterodactyl.setMobile(false);
                        return new BreedingAction(minimum.getKey());
                    }
                    else {
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
            }
        }

        return new EndTurnAction();
    }

    /**
     * Method to get the location of dinosaurs of same species and save in a HashMap and return it
     *
     * @param actor the dinosaur finding a mate
     * @param map the game map
     * @return the HashMap containing actor and location
     */
    public HashMap<Actor, Location> getSameSpeciesDinosaurs(Actor actor, GameMap map) {
        NumberRange widths = map.getXRange();
        NumberRange heights = map.getYRange();
        HashMap<Actor, Location> hashMap = new HashMap<>();

        for (int x : widths) {
            for (int y : heights) {
                Location there = map.at(x, y);
                if (map.isAnActorAt(there)) {
                    Actor actorAtThere = map.getActorAt(there);
                    if (actor.getDisplayChar() == actorAtThere.getDisplayChar() && !((Dinosaur) actor).getName().equals(((Dinosaur) actorAtThere).getName())) {
                        hashMap.put(actorAtThere, there);
                    }
                }
            }
        }
        return hashMap;
    }

    /**
     * Method to filter the dinosaurs in the HashMap so only dinosaurs of different gender , suitable hit points and
     * water level remain (for Pterodactyl check if the dinosaur is on the tree)
     * @param actor the dinosaur finding a mate
     * @param hashMap the hash map containing actor and location
     * @return the filtered hash map
     */
    public HashMap<Actor, Location> filterDinosaurs(Actor actor, HashMap<Actor, Location> hashMap, GameMap map) {
        char character = actor.getDisplayChar();
        if (character == 's') {
            Stegosaur mainDino = (Stegosaur) actor;
            Gender mainDinoGender = mainDino.getGender();
            Iterator<Map.Entry<Actor, Location>> itr = hashMap.entrySet().iterator();

            while (itr.hasNext()) {
                Map.Entry<Actor, Location> entry = itr.next();
                Stegosaur secondaryDino = (Stegosaur) entry.getKey();
                Gender secondaryDinoGender = secondaryDino.getGender();
                if (mainDinoGender == secondaryDinoGender || secondaryDino.isHungry() || secondaryDino.isThirsty()) {
                    itr.remove();
                }
            }
        } else if (character == 'r') {
            Brachiosaur mainDino = (Brachiosaur) actor;
            Gender mainDinoGender = mainDino.getGender();
            Iterator<Map.Entry<Actor, Location>> itr = hashMap.entrySet().iterator();

            while (itr.hasNext()) {
                Map.Entry<Actor, Location> entry = itr.next();
                Brachiosaur secondaryDino = (Brachiosaur) entry.getKey();
                Gender secondaryDinoGender = secondaryDino.getGender();
                if (mainDinoGender == secondaryDinoGender || secondaryDino.isHungry() || secondaryDino.isThirsty()) {
                    itr.remove();
                }
            }
        } else if (character == 'a') {
            Allosaur mainDino = (Allosaur) actor;
            Gender mainDinoGender = mainDino.getGender();
            Iterator<Map.Entry<Actor, Location>> itr = hashMap.entrySet().iterator();

            while (itr.hasNext()) {
                Map.Entry<Actor, Location> entry = itr.next();
                Allosaur secondaryDino = (Allosaur) entry.getKey();
                Gender secondaryDinoGender = secondaryDino.getGender();
                if (mainDinoGender == secondaryDinoGender || secondaryDino.isHungry() || secondaryDino.isThirsty()) {
                    itr.remove();
                }
            }
        } else if (character == 'p') {
            Pterodactyl mainDino = (Pterodactyl) actor;
            Gender mainDinoGender = mainDino.getGender();
            Iterator<Map.Entry<Actor, Location>> itr = hashMap.entrySet().iterator();

            while (itr.hasNext()) {
                Map.Entry<Actor, Location> entry = itr.next();
                Pterodactyl secondaryDino = (Pterodactyl) entry.getKey();
                Gender secondaryDinoGender = secondaryDino.getGender();
                if (mainDinoGender == secondaryDinoGender || secondaryDino.isHungry() || secondaryDino.isThirsty() || !secondaryDino.isOnTree()) {
                    itr.remove();
                } else {
                    Location locationOfSecondaryDino = entry.getValue();
                    if (locationOfSecondaryDino.getGround() instanceof Tree) {
                        Tree tree = (Tree) locationOfSecondaryDino.getGround();
                        ArrayList<Integer> arrayList = tree.getAdjacentTreeCoordinatesArrayList();
                        int xCoordOfAdjacentTree = arrayList.get(0);
                        int yCoordOfAdjacentTree = arrayList.get(1);
                        Location locationOfAdjacentTree = map.at(xCoordOfAdjacentTree, yCoordOfAdjacentTree);
                        hashMap.put(entry.getKey(), locationOfAdjacentTree);
                    }
                }
            }
        }

        return hashMap;
    }

    /***
     * Method to get the distances of the opposite gender dinosaurs to the main dinosaur and store them in HashMap
     * and return the HashMap
     *
     * @param actor the dinosaur finding a mate
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

}
