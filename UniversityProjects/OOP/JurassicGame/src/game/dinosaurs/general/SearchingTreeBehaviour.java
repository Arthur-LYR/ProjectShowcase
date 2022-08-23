package game.dinosaurs.general;

import game.dinosaurs.attack.DeathAction;
import game.terrain.Tree;
import libs.engine.*;

import java.util.HashMap;
import java.util.Map;

public class SearchingTreeBehaviour implements Behaviour {

    @Override
    public Action getAction(Actor actor, GameMap map) {
        Pterodactyl pterodactyl = (Pterodactyl) actor;

        // return DeathAction if the dinosaur is health or water critical
        if (pterodactyl.isHealthCritical() || pterodactyl.isWaterCritical()) {
            return new DeathAction();
        }

        // return null if the dino cannot move
        if (pterodactyl.hasCapability(DinosaurCapabilities.CANNOTMOVE)) {
            return null;
        }

        // return null if pterodactyl is thirsty
        if (pterodactyl.isThirsty()) {
            return null;
        }

        // if fuel is empty, purpose of finding tree is to refuel
        if (pterodactyl.getFuel() == 0) {
            pterodactyl.setTryingToBreed(false);
        }

        // if Pterodactyl is not trying to breed, don't go to a tree
        if (!pterodactyl.isTryingToBreed()) {
            return null;
        }

        // if the Pterodactyl is not trying to mate and fuel is not empty, it has no business going to a tree
        if (!pterodactyl.isTryingToBreed() && pterodactyl.getFuel() > 0) {
            return null;
        }

        NumberRange widths = map.getXRange();
        NumberRange heights = map.getYRange();
        HashMap<Ground, Integer> distancesHashMap = new HashMap<>();
        // hash map containing ground and location of trees
        HashMap<Ground, Location> locationsHashMap = new HashMap<>();

        for (int x : widths) {
            for (int y : heights) {
                Location there = map.at(x, y);
                Ground ground = there.getGround();
                if (ground instanceof Tree && !((Tree) ground).isOccupied()) {
                    if (pterodactyl.isTryingToBreed()) {
                        if (((Tree) ground).adjacentTreeAvailable(map, x, y)) {
                            Location locationOfDino = map.locationOf(actor);
                            int distanceBetweenDinoAndTree = distance(locationOfDino, there);
                            distancesHashMap.put(ground, distanceBetweenDinoAndTree);
                            locationsHashMap.put(ground, there);
                        }
                    } else {
                        Location locationOfDino = map.locationOf(actor);
                        int distanceBetweenDinoAndTree = distance(locationOfDino, there);
                        distancesHashMap.put(ground, distanceBetweenDinoAndTree);
                        locationsHashMap.put(ground, there);
                    }
                }
            }
        }

        Map.Entry<Ground, Integer> minimum = null;
        for (Map.Entry<Ground, Integer> entry: distancesHashMap.entrySet()) {
            if (minimum == null || minimum.getValue() > entry.getValue()) {
                minimum = entry;
            }
        }

        if (minimum != null) {
            System.out.println(actor + " is searching for a tree");
            if (minimum.getValue() == 0) {
                Tree tree = (Tree) minimum.getKey();
                tree.setOccupied(true);
                pterodactyl.setMobile(false);
                pterodactyl.setOnTree(true);
                pterodactyl.addCapability(DinosaurCapabilities.CANNOTMOVE);
                pterodactyl.setFuel(30);
                System.out.println(actor + " is on the tree");
                return new DoNothingAction();
            } else {
                Ground groundKey = minimum.getKey();
                int distanceBetweenDinoAndTree = minimum.getValue();
                Location treeLocation = locationsHashMap.get(groundKey);
                for (Exit exit : map.locationOf(actor).getExits()) {
                    Location destination = exit.getDestination();
                    if (destination.canActorEnter(actor)) {
                        int newDistance = distance(destination, treeLocation);
                        if (newDistance < distanceBetweenDinoAndTree) {
                            map.moveActor(actor, destination);
                            System.out.println(actor + " has moved to : (" + map.locationOf(actor).x() + " " +  map.locationOf(actor).y() + ")");
                            break;
                        }
                    }
                }
            }
        } else {
            // if no tree found, return null
            return null;
        }

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
}
