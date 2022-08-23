package game.items;

import libs.engine.Location;

/***
 * Corpse class is used to create corpse of dinosaurs. It extends the PortableItem class.
 */
public class Corpse extends PortableItem {
    /***
     * Lifetime of the corpse before it decays
     */
    private int corpseLifetime;
    /***
     * Threshold before unconscious dinosaur is removed from the map
     */
    private int unconsciousThreshold;

    /***
     * Code to distinguish the dinosaurs
     */
    private int dinosaurCode;

    /**
     * Number of turns spent as a corpse
     */
    private int corpseTurns = 0;

    /**
     * Variable to determine if the dinosaur reached 0 hit points due to being killed or hunger
     */
    private boolean isKilled;

    /**
     * Food value that the corpse provides
     */
    private int foodValue;

    /***
     *  constructor for Corpse when the dinosaur reached o hit points due to being killed / hunger
     *
     * @param name name of the dinosaur
     * @param displayChar character to display the corpse
     * @param dinosaurCode code of the dinosaur
     * @param isKilled check if dinosaur was killed
     */
    public Corpse(String name, char displayChar, int dinosaurCode, boolean isKilled) {
        super(name, displayChar);
        this.dinosaurCode = dinosaurCode;
        this.isKilled = isKilled;
        setCorpseLifetime(dinosaurCode);
        setFoodValue(dinosaurCode);
    }

    /***
     * Method to set the lifetime of the corpse
     *
     * @param code the code of the dinosaur
     */
    public void setCorpseLifetime(int code) {
        if (code == 1) {
            corpseLifetime = 20;
        } else if (code == 2) {
            corpseLifetime = 40;
        } else if (code == 3) {
            corpseLifetime = 20;
        }
    }

    /***
     * Method to allow corpse to experience the flow of time (check when to remove corpse)
     *
     * @param currentLocation The location of the ground on which we lie.
     */
    @Override
    public void tick(Location currentLocation) {
        super.tick(currentLocation);
        if (corpseTurns == corpseLifetime) {
            currentLocation.removeItem(this);
        } else {
            corpseTurns++;
        }

        if (getFoodValue() == 0) {
            currentLocation.removeItem(this);
        }
    }

    /***
     * Returns the dinosaur code to indentify type of dinosaur corpse
     * @return the dinosaur code
     */
    public int getDinosaurCode() {
        return dinosaurCode;
    }


    /**
     * Method to get the food value of the corpse
     *
     * @return food value of the corpse
     */
    public int getFoodValue() {
        return foodValue;
    }

    /**
     * Set the food value of the corpse based on the type of dinosaur
     *
     * @param dinosaurCode code of the dinosaur
     */
    public void setFoodValue(int dinosaurCode) {
        if (dinosaurCode == 1) {
            foodValue = 50;
        } else if (dinosaurCode == 2) {
            foodValue = 100;
        } else if (dinosaurCode == 3) {
            foodValue = 50;
        } else if (dinosaurCode == 4) {
            foodValue = 30;
        } else {
            foodValue = 0;
        }
    }

    /**
     * Method to decrease the food value of the corpse by the specified amount
     *
     * @param number the food value to decrease from the corpse
     */
    public void decreaseFoodValue(int number) {
        int currentFoodValue = getFoodValue();
        setFoodValue(currentFoodValue - number);
    }
}
