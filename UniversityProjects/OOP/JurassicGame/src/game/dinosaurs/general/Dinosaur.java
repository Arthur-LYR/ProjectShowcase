package game.dinosaurs.general;

import libs.engine.Actor;
import game.items.Egg;

import java.util.ArrayList;

/**
 * Abstract class that inherits from Actor class. It contains methods to be implemented by child classes, Stegosaur,
 * Brachiosaur and Allosaur
 */
public abstract class Dinosaur extends Actor {

    /**
     * Name of dinosaur
     */
    private String name;

    /**
     * Name code of dinosaur
     */
    private int nameCode;

    /**
     * Code to differentiate the dinosaur types
     */
    private int dinosaurCode;

    /**
     * Maximum hit points of the dinosaur
     */
    private int maximumHitPoints;

    /**
     * Water level of the dinosaur
     */
    private int waterLevel = 0;

    /**
     * Maximum water level of the dinosaur
     */
    private int maximumWaterLevel = 0;

    /**
     * Gender of the dinosaur
     */
    private Gender gender;

    /**
     * Growth status of the dinosaur (Adult or Child)
     */
    private Status status;

    /**
     * Number of turns dinosaur spend as baby
     */
    private int babyTurns = 0;

    /**
     * Threshold in which dinosaur starts to feel hunger
     */
    private int HUNGER_THRESHOLD;

    /**
     * Threshold in which dinosaur starts to feel thirst
     */
    private int THIRST_THRESHOLD;

    /**
     * Threshold of food level to determine if the dinosaur is able to breed
     */
    private int MATING_THRESHOLD;

    /**
     * Number of turns dinosaur can remain unconscious due to lack of food
     */
    private int UNCONSCIOUS_FOOD_THRESHOLD;

    /**
     * Number of turns dinosaur can remain unconscious due to lack of water
     */
    private int UNCONSCIOUS_WATER_THRESHOLD;

    /**
     * Reason for dinosaur being unconscious
     */
    private UnconsciousReason unconsciousReason;

    /**
     * Number of turns dinosaur spent unconscious
     */
    private int unconsciousTurns = 0;

    /**
     * Boolean variable to check if dinosaur is hibernating
     */
    private boolean isHibernating = false;

    /**
     * Boolean variable to check if dinosaur is pregnant
     */
    private boolean isPregnant = false;

    /**
     * Number of turns dinosaur spent pregnant
     */
    private int pregnantTurns = 0;

    /**
     * ArrayList to represent stomach of dinosaur to contain egg
     */
    private ArrayList<Egg> stomach = new ArrayList<>();

    /**
     * The mode of the dinosaur (Land or Flight)
     */
    private DinosaurMode dinosaurMode;

    /**
     * Boolean variable to check if the dinosaur is mobile
     */
    private boolean isMobile = true;

    /**
     * Constructor.
     *
     * @param name        the name of the Actor
     * @param displayChar the character that will represent the Actor in the display
     * @param hitPoints   the Actor's starting hit points
     */
    public Dinosaur(String name, char displayChar, int hitPoints, int maximumHitPoints,  int waterLevel, int maximumWaterLevel, Status status, int hungerThreshold, int waterThreshold, int matingThreshold,  int unconsciousFoodThreshold, int unconsciousWaterThreshold) {
        super(name, displayChar, maximumHitPoints);
        setHitPoints(hitPoints);
        setName(name);
        setMaximumHitPoints(maximumHitPoints);
        setWaterLevel(waterLevel);
        setMaximumWaterLevel(maximumWaterLevel);
        setGender(Gender.randomGender());
        setStatus(status);
        setHungerThreshold(hungerThreshold);
        setWaterThreshold(waterThreshold);
        setUnconsciousFoodThreshold(unconsciousFoodThreshold);
        setUnconsciousWaterThreshold(unconsciousWaterThreshold);
        setMobile(true);
    }

    /**
     * Method to set hit points of dinosaur
     *
     * @param hitPoints hit points of dinosaur
     */
    public void setHitPoints(int hitPoints) {
        this.hitPoints = hitPoints;
    }

    /**
     * Method to get name of dinosaur
     *
     * @return name of dinosaur
     */
    public String getName() {
        return name;
    }

    /**
     * Method to set name of dinosaur
     *
     * @param name name of dinosaur
     */
    public void setName(String name) {
        this.name = name;
    }

    /**
     * Method to get the name code of dinosaur
     *
     * @return name code of dinosaur
     */
    public int getNameCode() {
        return nameCode;
    }

    /**
     * Method to set the name code of dinosaur
     *
     * @param nameCode name code of dinosaur
     */
    public void setNameCode(int nameCode) {
        this.nameCode = nameCode;
    }

    /**
     * Getter method to get the hit points of the dinosaur
     *
     * @return the hit points of the dinosaur
     */
    public int getHitPoints(){
        return hitPoints;
    }

    /**
     * Method to gain the specified amount of hit points
     *
     * @param hitPoints amount of hit points
     */
    public void gainHitPoints(int hitPoints) {
        int currentHitPoints = getHitPoints();
        int newHitPoints = currentHitPoints + hitPoints;
        this.hitPoints = Math.min(newHitPoints, getMaximumHitPoints());
    }

    /**
     * Method to get maximum hit points of dinosaur
     *
     * @return maximum hit points of dinosaur
     */
    public int getMaximumHitPoints() {
        return maximumHitPoints;
    }

    /**
     * Method to set maximum hit points of dinosaur
     *
     * @param maximumHitPoints maximum hit points of dinosaur
     */
    public void setMaximumHitPoints(int maximumHitPoints) {
        this.maximumHitPoints = maximumHitPoints;
    }

    /**
     * Method to increment baby turns of the dinosaur
     */
    public void incrementBabyTurns() {
        babyTurns++;
    }

    /**
     *  Method to get the hunger threshold of the dinosaur
     *
     * @return the hunger threshold of the dinosaur
     */
    public int getHungerThreshold() {
        return HUNGER_THRESHOLD;
    }



    /**
     * Get baby turns of dinosaur
     *
     * @return baby turns of dinosaur
     */
    public int getBabyTurns() {
        return babyTurns;
    }

    /**
     * Set the hunger threshold of the dinosaur
     * @param hungerThreshold hunger threshold of the dinosaur
     */
    public void setHungerThreshold(int hungerThreshold) {
        HUNGER_THRESHOLD = hungerThreshold;
    }

    /**
     * Get the thirst threshold of the dinosaur
     *
     *
     * @return thirst threshold of the dinosaur
     */
    public int getThirstThreshold() {
        return THIRST_THRESHOLD;
    }

    /**
     * Method to get the mating threshold for the dinosaur (food level needed before mating can occur)
     *
     * @return the mating food threshold for the dinosaur
     */
    public int getMatingThreshold() {
        return MATING_THRESHOLD;
    }

    /**
     * Method to set the mating threshold for the dinosaur (food level needed before mating can occur)
     *
     * @param MATING_THRESHOLD the mating threshold
     */
    public void setMatingThreshold(int MATING_THRESHOLD) {
        this.MATING_THRESHOLD = MATING_THRESHOLD;
    }

    /**
     * Set the water threshold of the dinosaur
     * @param waterThreshold water threshold of the dinosaur
     */
    public void setWaterThreshold(int waterThreshold) {
        THIRST_THRESHOLD = waterThreshold;
    }

    /**
     * Method to get the unconscious turns of the dinosaur
     *
     * @return the unconscious turns of the dinosaur
     */
    public int getUnconsciousTurns() {
        return unconsciousTurns;
    }

    /**
     * Method to get the unconscious food threshold of the dinosaur
     *
     * @return the unconscious food threshold of the dinosaur
     */
    public int getUnconsciousFoodThreshold() {
        return UNCONSCIOUS_FOOD_THRESHOLD;
    }

    /**
     * Method to set the unconscious food threshold of the dinosaur
     *
     * @param unconsciousFoodThreshold unconscious food threshold of the dinosaur
     */
    public void setUnconsciousFoodThreshold(int unconsciousFoodThreshold) {
        UNCONSCIOUS_FOOD_THRESHOLD = unconsciousFoodThreshold;
    }

    /**
     * Method to get the unconscious water threshold of the dinosaur
     *
     * @return the unconscious water threshold of the dinosaur
     */
    public int getUnconsciousWaterThreshold() {
        return UNCONSCIOUS_WATER_THRESHOLD;
    }

    /**
     * Method to set the unconscious water threshold of the dinosaur
     *
     * @param unconsciousWaterThreshold unconscious water threshold of the dinosaur
     */
    public void setUnconsciousWaterThreshold(int unconsciousWaterThreshold) {
        UNCONSCIOUS_WATER_THRESHOLD = unconsciousWaterThreshold;
    }

    /**
     * Method to get the code of dinosaur
     *
     * @return the code of dinosaur
     */
    public abstract int getDinosaurCode();

    /**
     * Method to set the code of dinosaur
     *
     * @param dinosaurCode code of dinosaur
     */
    public void setDinosaurCode(int dinosaurCode) {
        this.dinosaurCode = dinosaurCode;
    }

    /**
     * Method to get the state of the dinosaur if it is hibernating
     *
     * @return the state of hibernation of the dinosaur
     */
    public boolean getIsHibernating() {
        return isHibernating;
    }

    /**
     * Method to set if dinosaur is hibernating
     *
     * @param isHibernating state of hibernation of dinosaur
     */
    public void isHibernating(boolean isHibernating){
        this.isHibernating = isHibernating;
    }

    /**
     * Method to increment number of turns the dinosaur is unconscious
     */
    public void incrementUnconsciousTurns() {
        unconsciousTurns++;
    }

    /**
     * Method to add the egg to the female dinosaur stomach once it has mated
     */
    public abstract void addEggToStomach();

    /**
     * Method to get the water level of the dinosaur
     *
     * @return water level of the dinosaur
     */
    public int getWaterLevel(){
        return waterLevel;
    }

    /**
     * Method to set water level of dinosaur
     *
     * @param waterLevel water level
     */
    public void setWaterLevel(int waterLevel) {
        this.waterLevel = waterLevel;
    }

    /**
     * Method to allow dinosaurs to gain a specified water level
     *
     * @param waterLevel the water level
     */
    public void gainWaterLevel(int waterLevel) {
        int currentWaterLevel = getWaterLevel();
        int newWaterLevel = currentWaterLevel + waterLevel;
        this.waterLevel = Math.min(newWaterLevel, getMaximumWaterLevel());
    }

    /**
     * Method to set the maximum water level of dinosaur
     *
     * @param maximumWaterLevel maximum water level
     */
    public void setMaximumWaterLevel(int maximumWaterLevel) {
        this.maximumWaterLevel = maximumWaterLevel;
    }

    /**
     * Method to get the maximum water level of the dinosaur
     *
     * @return maximum water level of the dinosaur
     */
    public int getMaximumWaterLevel() {
        return maximumWaterLevel;
    }

    /**
     * Method to get the gender of the dinosaur
     *
     * @return gender of the dinosaur
     */
    public Gender getGender() {
        return gender;
    }

    /**
     * Method to set the gender of the dinosaur
     *
     * @param gender gender of the dinosaur
     */
    public void setGender(Gender gender) {
        this.gender = gender;
    }

    /**
     * Method to get status of dinosaur
     *
     * @return status of dinosaur
     */
    public Status getStatus() {
        return status;
    }

    /**
     * Method to set status of dinosaur
     *
     * @param status status of dinosaur
     */
    public void setStatus(Status status) {
        this.status = status;
    }

    /**
     * Method to decrement water level of dinosaur by 1 (limit is set at 0)
     */
    public void decrementWaterLevel() {
        if (getWaterLevel() > 0)
        waterLevel--;
    }

    /**
     * Method to decrement hit points of dinosaur by 1 (limit is set at 0)
     */
    public void decrementHitPoints() {
        if (getHitPoints() > 0)
            hitPoints--;
    }

    /**
     * Method to get unconscious reason of dinosaur
     *
     * @return unconscious reason of dinosaur
     */
    public UnconsciousReason getUnconsciousReason(){
        return unconsciousReason;
    }

    /**
     * Method to set unconscious reason of dinosaur
     */
    public void setUnconsciousReason(UnconsciousReason unconsciousReason) {
        this.unconsciousReason = unconsciousReason;
    }

    /**
     * Method to remove unconscious reason of dinosaur
     */
    public void removeUnconsciousReason() {
        unconsciousReason = null;
    }


    public void setHibernating(boolean hibernating) {
        isHibernating = hibernating;
    }

    /**
     * Method to check if dinosaur is pregnant
     *
     * @return true if dinosaur is pregnant, false otherwise
     */
    public boolean isPregnant() {
        return stomach.size() != 0;
    }

    /**
     * Method to set if dinosaur is pregnant
     *
     * @param pregnant dinosaur is pregnant or not
     */
    public void setPregnant(boolean pregnant) {
        isPregnant = pregnant;
    }

    /**
     * Method to get the number of turns the dinosaur is pregnant
     *
     * @return number of turns the dinosaur is pregnant
     */
    public int getPregnantTurns() {
        return pregnantTurns;
    }

    /**
     * Method to set the number of turns the dinosaur is pregnant
     *
     * @param pregnantTurns number of turns the dinosaur is pregnant
     */
    public void setPregnantTurns(int pregnantTurns) {
        this.pregnantTurns = pregnantTurns;
    }

    /**
     * Method to increment pregnant turns of dinosaur
     */
    public void incrementPregnantTurns() {
        pregnantTurns++;
    }

    /**
     * Method to get the dinosaur mode (Land or flight)
     *
     * @return dinosaur mode
     */
    public DinosaurMode getDinosaurMode() {
        return dinosaurMode;
    }

    /**
     * Method to set the dinosaur mode (Land or flight)
     *
     * @param dinosaurMode the dinosaur mode
     */
    public void setDinosaurMode(DinosaurMode dinosaurMode) {
        this.dinosaurMode = dinosaurMode;
    }

    /**
     * Method to get the stomach of the dinosaur
     *
     * @return arrayList representing stomach of dinosaur
     */
    public ArrayList<Egg> getStomach() {
        return stomach;
    }

    /**
     * Method to check if dinosaur is hungry
     *
     * @return true if dinosaur is hungry, false otherwise
     */
    public boolean isHungry() {
        if (getHitPoints() < getHungerThreshold()) {
            return true;
        } else {
            return false;
        }
    }

    /**
     * Method to check if dinosaur is thirsty
     *
     * @return true if dinosaur is thirsty, false otherwise
     */
    public boolean isThirsty() {
        if (getWaterLevel() < getThirstThreshold()) {
            return true;
        } else {
            return false;
        }
    }

    /**
     * Method to revive the dinosaur that was unconscious due to lack of water
     */
    public void reviveThirstyDinosaur() {
        if (getIsHibernating() && getUnconsciousReason() == UnconsciousReason.WATER) {
            setWaterLevel(15);
            setHibernating(false);
            removeCapability(DinosaurCapabilities.CANNOTMOVE);
            System.out.println(this + " has been revived by the rain!");
        }
    }

    /**
     * Method to return the mobility of the dinosaur
     *
     * @return true if dinosaur is mobile, false if not
     */
    public boolean isMobile() {
        return isMobile;
    }

    /**
     * Method to set the mobility of the dinosaur
     *
     * @param mobile mobility of the dinosaur
     */
    public void setMobile(boolean mobile) {
        isMobile = mobile;
    }

    /**
     * Method to check if health of dinosaur is critical (zero)
     *
     * @return true if heath critical, false otherwise
     */
    public boolean isHealthCritical() {
        if (getHitPoints() == 0) {
            setUnconsciousReason(UnconsciousReason.FOOD);
            return true;
        } else {
            return false;
        }
    }

    /**
     * Method to check if water level of dinosaur is critical (zero)
     *
     * @return true if water level critical, false otherwise
     */
    public boolean isWaterCritical() {
        if (getWaterLevel() == 0) {
            setUnconsciousReason(UnconsciousReason.WATER);
            return true;
        } else {
            return false;
        }
    }

    /**
     * Method to check if the dinosaur is too hungry to engage in breeding
     *
     * @return true if dinosaur is too hungry to breed, false otherwise
     */
    public boolean tooHungryToBreed() {
        if (getHitPoints() < getMatingThreshold()) {
            return true;
        } else {
            return false;
        }
    }

}
