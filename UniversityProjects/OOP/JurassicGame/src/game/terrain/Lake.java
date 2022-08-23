package game.terrain;

import libs.engine.Actor;
import libs.engine.Ground;
import libs.engine.Location;
import game.dinosaurs.general.DinosaurMode;
import game.dinosaurs.general.Pterodactyl;
import game.items.Fish;
import game.main.Util;

import java.util.ArrayList;


/**
 * Class that represents a Lake
 */
public class Lake extends Ground implements RainAffected {
    /**
     * The number of sips that a Dinosaur can make before the Lake runs out of water
     */
    private int sips;

    /**
     * An ArrayList which contains all the Fish currently in the Lake (Maximum 25)
     */
    private ArrayList<Fish> fishList = new ArrayList<>();

    /**
     * Constructor.
     */
    public Lake() {
        super('~');
        this.sips = 25;
        fishList.add(new Fish());
        fishList.add(new Fish());
        fishList.add(new Fish());
        fishList.add(new Fish());
        fishList.add(new Fish());
    }

    /**
     * At the beginning of every turn, there is a 60% chance of a new Fish being added if the capacity has not been
     * reached
     * @param location The location of the Ground
     */
    @Override
    public void tick(Location location) {
        super.tick(location);

        // Add Fish
        if (fishList.size() < 25 && Util.eventSuccess(3, 5)) {
            fishList.add(new Fish());
        }

        // Add Water
        rainAction();
    }

    /**
     * When it Rains, the number of sips in the Lake is increased
     */
    @Override
    public void rainAction() {
        if (Rain.isRaining()) {
            int min = 10;
            int max = 60;
            double rainfall = (Math.floor(Math.random() * (max - min + 1) + min)) / 100;
            int sipsAdded = (int) Math.floor(rainfall * 20);
            sips += sipsAdded;
        }
    }

    /**
     * Get the number of sips the dinosaur can make from the lake
     *
     * @return the number of sips
     */
    public int getSips() {
        return sips;
    }

    /**
     * Decrement the sips in the lake when it is drank by dinosaurs
     */
    public void decrementSips() {
        sips--;
    }

    /**
     * Actors can't pass through except flying Pterodactyl
     * @param actor the Actor to check
     * @return true if can pass through, false otherwise
     */
    @Override
    public boolean canActorEnter(Actor actor) {
        if (actor instanceof Pterodactyl && ((Pterodactyl) actor).getDinosaurMode() == DinosaurMode.FLIGHT) {
            return true;
        } else {
            return false;
        }
    }

    /**
     * Method to check if there is fish in the lake
     *
     * @return true if there is fish in the lake, false otherwise
     */
    public boolean lakeContainsFish() {
        return !fishList.isEmpty();
    }

    /**
     * Method to remove specified number of fish from the lake
     *
     * @param number number of fish to be removed
     */
    public void removeFishFromLake(int number) {
        if (number > 0) {
            fishList.subList(0, number).clear();
        }
    }
}
