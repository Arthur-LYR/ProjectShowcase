package game.items;

import libs.engine.Location;
import game.dinosaurs.general.*;
import game.main.Player;

/**
 * Egg class to create the eggs that are produced by dinosaurs after breeding. It extends the PortableItem class.
 */
public class Egg extends PortableItem {
    /**
     * number of turns the egg has incubated
     */
    private int incubationTurns;

    /**
     * cost of the egg
     */
    private static int cost;

    /***
     * type of dinosaur in the egg
     */
    private DinosaurType dinosaurType;

    /***
     * variable to check if the egg is from the vending machine
     */
    private boolean isFromVending;


    /***
     * constructor for the egg.
     *
     * @param name name of the egg
     * @param displayChar character to display the egg
     * @param dinosaurType type of dinosaur in the egg
     * @param isFromVending check if the egg is from the vending machine
     */
    public Egg(String name, char displayChar, DinosaurType dinosaurType, boolean isFromVending) {
        super(name, displayChar);

        this.dinosaurType = dinosaurType;
        cost = dinosaurType.getCost();

        if (isFromVending) {
            this.incubationTurns = -1000000000;
        } else {
            this.incubationTurns = 0;
        }
    }


    /***
     * Method to let the egg experience the flow of time and to let the egg incubate
     *
     * @param currentLocation The location of the ground on which we lie.
     */
    @Override
    public void tick(Location currentLocation) {
        super.tick(currentLocation);

        incubationTurns++;
        System.out.println(this.name + " is incubating for " + incubationTurns + " turn(s)");
        if (incubationTurns == 50) {
            currentLocation.removeItem(this);
            if (dinosaurType == DinosaurType.STEGOSAUR) {
                currentLocation.addActor(new Stegosaur(Status.BABY));
                Player.gainEcoPoints(100);
            } else if (dinosaurType == DinosaurType.BRACHIOSAUR) {
                currentLocation.addActor(new Brachiosaur(Status.BABY));
                Player.gainEcoPoints(1000);
            } else if (dinosaurType == DinosaurType.ALLOSAUR) {
                currentLocation.addActor(new Allosaur(Status.BABY));
                Player.gainEcoPoints(1000);
            } else if (dinosaurType == DinosaurType.PTERODACTYL) {
                currentLocation.addActor(new Pterodactyl(Status.BABY));
                Player.gainEcoPoints(100);
            }
            System.out.println(this.name + " at (" + currentLocation.x() + ", " + currentLocation.y() + ") hatches" );
        }
    }

}
