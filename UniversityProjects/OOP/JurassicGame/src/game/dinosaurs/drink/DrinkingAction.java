package game.dinosaurs.drink;

import game.dinosaurs.general.*;
import game.terrain.Lake;
import libs.engine.*;

public class DrinkingAction extends Action {

    /**
     * The Lake to be drank from by the dinosaur
     */
    private Ground lake;

    /**
     * The location of the lake
     */
    private Location lakeLocation;

    public DrinkingAction(Ground lake, Location lakeLocation) {
        this.lake = lake;
        this.lakeLocation = lakeLocation;
    }

    @Override
    public String execute(Actor actor, GameMap map) {
        boolean isNextTo = checkIfNextTo(actor, map);
        boolean isAbove = checkIfAbove(actor, map);
        Dinosaur dino = (Dinosaur) actor;
        if (isNextTo || isAbove) {
            if (isNextTo && dino.getDinosaurMode() == DinosaurMode.LAND) {
                if (dino instanceof Stegosaur || dino instanceof Allosaur || dino instanceof Pterodactyl) {
                    dino.gainWaterLevel(30);
                    ((Lake) lake).decrementSips();
                } else if (dino instanceof Brachiosaur) {
                    dino.gainWaterLevel(80);
                    ((Lake) lake).decrementSips();
                }
            } else if (isAbove && dino.getDinosaurMode() == DinosaurMode.FLIGHT) {
                if (dino instanceof Pterodactyl) {
                    dino.gainWaterLevel(30);
                    ((Lake) lake).decrementSips();
                }
            }
        }
        return actor + " drank some water | current water level is " + ((Dinosaur) actor).getWaterLevel();
    }

    @Override
    public String menuDescription(Actor actor) {
        return actor + " drinks";
    }

    /**
     *  Method to check if the dinosaur is next to the lake
     *
     * @param actor the actor
     * @param map the game map
     * @return boolean variable true or false
     */
    public boolean checkIfNextTo(Actor actor, GameMap map) {
        Location actorLocation = map.locationOf(actor);
        if (distance(actorLocation, lakeLocation) == 1) {
            return true;
        }
        return false;
    }

    /**
     * Method to check if dinosaur is above the lake
     *
     * @param actor the actor
     * @param map the game map
     * @return boolean variable true or false
     */
    public boolean checkIfAbove(Actor actor, GameMap map) {
        Location actorLocation = map.locationOf(actor);
        if (distance(actorLocation, lakeLocation) == 0) {
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
}
