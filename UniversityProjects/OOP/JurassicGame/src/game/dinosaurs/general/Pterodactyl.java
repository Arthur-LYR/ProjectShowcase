package game.dinosaurs.general;

import game.dinosaurs.attack.DyingBehaviour;
import game.dinosaurs.breed.SearchingMateBehaviour;
import game.dinosaurs.drink.SearchingWaterBehaviour;
import game.dinosaurs.food.SearchingFoodBehaviour;
import game.items.DinosaurType;
import game.items.Egg;
import game.terrain.Rain;
import libs.engine.*;

import java.util.ArrayList;
import java.util.Random;

public class Pterodactyl extends Dinosaur {

    /**
     * Code given to identify the dinosaurs
     */
    private static int nameCode = 1;

    /**
     * ArrayList to store the behaviours of the Pterodactyl
     */
    private ArrayList<Behaviour> behaviours = new ArrayList<>();

    /**
     * Fuel of the Pterodactyl used when flying
     */
    private int fuel;

    private final int MAXIMUM_FUEL = 30;

    /**
     * Boolean variable to determine if the Pterodactyl is feeding on a corpse
     */
    private boolean feedingOnCorpse;

    /**
     * Number of turns the Pterodactyl is feeding on a corpse
     */
    private int feedingTurns = 0;

    /**
     * Number of turns needed for Pterodactyl to finish feeding on the corpse
     */
    private int feedingTurnsNeeded;

    /**
     * Variable to check if the Pterodactyl is on a tree
     */
    private boolean isOnTree;

    /**
     * Variable to check if the Pterodactyl is trying to breed
     */
    private boolean isTryingToBreed;

    /**
     * Location of adjacent tree
     */
    private Location adjacentTreeLocation;

    /**
     * Constructor.
     *
     * @param status the growth status of the Pterodactyl
     */
    public Pterodactyl(Status status) {
        super("Pterodactyl" + nameCode, 'p',50, 100,60, 100, status, 90, 40, 50,  20, 15);
        nameCode++;
        setDinosaurMode(DinosaurMode.FLIGHT);
        setFuel(30);

        if (getStatus() == Status.BABY) {
            hurt(40);
        }

        // add behaviours to the Pterodactyl at instantiation
        behaviours.add(new DyingBehaviour());
        behaviours.add(new SearchingWaterBehaviour());
        behaviours.add(new SearchingFoodBehaviour());
        behaviours.add(new SearchingMateBehaviour());
        behaviours.add(new SearchingTreeBehaviour());
        behaviours.add(new WanderBehaviour());
    }

    /**
     * Constructor. (We can set the gender of the Pterodactyl)
     *
     * @param status the growth status of the Pterodactyl
     * @param gender the gender of the Pterodactyl
     */
    public Pterodactyl(Status status, Gender gender) {
        super("Pterodactyl" + nameCode, 'p',50, 100,60, 100, status, 90, 40, 50,  20, 15);
        nameCode++;
        setDinosaurMode(DinosaurMode.FLIGHT);
        setFuel(30);
        setGender(gender);

        if (getStatus() == Status.BABY) {
            hurt(40);
        }

        // add behaviours to the Pterodactyl at instantiation
        behaviours.add(new DyingBehaviour());
        behaviours.add(new SearchingWaterBehaviour());
        behaviours.add(new SearchingFoodBehaviour());
        behaviours.add(new SearchingMateBehaviour());
        behaviours.add(new SearchingTreeBehaviour());
        behaviours.add(new WanderBehaviour());
    }

    @Override
    public Action playTurn(Actions actions, Action lastAction, GameMap map, Display display) {

        if (getFuel() == 0) {
            System.out.println(this + " ran out of fuel and needs a tree to recharge");
            setDinosaurMode(DinosaurMode.LAND);
        }

        if (getDinosaurMode() == DinosaurMode.FLIGHT) {
            decrementFuel();
        }

        // Decrement food level and water level by 1 each turn
        if (!getIsHibernating()) {
            decrementHitPoints();
            decrementWaterLevel();
        }
        // Increment baby turns if dino is a baby
        if (getStatus() == Status.BABY) {
            incrementBabyTurns();
        }
        // Change dino status from baby to adult
        if (getBabyTurns() == 30) {
            this.setStatus(Status.ADULT);
        }

        if (isPregnant()) {
            if (getPregnantTurns() == 10) {
                if (isOnTree()) {
                    Egg egg = new Egg("Pterodactyl egg", 'e', DinosaurType.PTERODACTYL, false);
                    map.locationOf(this).addItem(egg);
                    getStomach().clear();
                    setPregnantTurns(0);
                    System.out.println(this + " laid an egg");
                    setOnTree(false);
                    setMobile(true);
                    removeCapability(DinosaurCapabilities.CANNOTMOVE);
                    setFuel(MAXIMUM_FUEL);
                    setDinosaurMode(DinosaurMode.FLIGHT);
                }
            } else {
                incrementPregnantTurns();
            }
        }

        if (Rain.isRaining()) {
            System.out.println(this + " can feel the rain!");
            reviveThirstyDinosaur();
        }

        Random rand = new Random();
        for (Behaviour behaviour: behaviours) {
            Action action = behaviour.getAction(this, map);
            if (action != null)
                return action;
        }

        return null;
    }

    /**
     * Method to get the code of Pterodactyl
     *
     * @return the code of Pterodactyl
     */
    @Override
    public int getDinosaurCode() {
        return 4;
    }

    /**
     * Method to add egg to the stomach of Pterodactyl
     */
    @Override
    public void addEggToStomach() {
        Egg egg = new Egg("Pterodactyl egg", 'e', DinosaurType.PTERODACTYL, false);
        getStomach().add(egg);
        setPregnant(true);
    }

    /**
     * Method to get the fuel of the Pterodactyl
     *
     * @return the fuel of the Pterodactyl
     */
    public int getFuel() {
        return fuel;
    }

    /**
     * Method to set the fuel of the Pterodactyl
     *
     * @param fuel the fuel of the Pterodactyl
     */
    public void setFuel(int fuel) {
        this.fuel = fuel;
    }

    /**
     * Method to allow Pterodactyl to gain specified amount of fuel
     *
     * @param fuel fuel of Pterodactyl
     */
    public void gainFuel(int fuel) {
        int currentFuel = getFuel();
        int newFuel = currentFuel + fuel;
        this.fuel = Math.min(newFuel, MAXIMUM_FUEL);
    }

    /**
     * Method to decrement fuel of the Pterodactyl
     */
    public void decrementFuel() {
        if (getFuel() > 0)
            fuel--;
    }

    /**
     * Method to check if the Pterodactyl is feeding on corpse
     *
     * @return true if Pterodactyl is feeding on a corpse, false otherwise
     */
    public boolean isFeedingOnCorpse() {
        return feedingOnCorpse;
    }

    /**
     * Method to set the state of Pterodactyl feeding on a corpse
     *
     * @param feedingOnCorpse true or false
     */
    public void setFeedingOnCorpse(boolean feedingOnCorpse) {
        this.feedingOnCorpse = feedingOnCorpse;
    }

    /**
     * Method to start feeding on the corpse
     *
     */
    public void startFeedingOnCorpse() {
        setFeedingOnCorpse(true);
        setDinosaurMode(DinosaurMode.LAND);
    }

    /**
     * Method to stop feeding on the corpse
     *
     */
    public void stopFeedingOnCorpse() {
        setFeedingOnCorpse(false);
        if (getFuel() > 0) {
            setDinosaurMode(DinosaurMode.FLIGHT);
        }
    }

    /**
     * Method to get the current number of feeding turns
     *
     * @return current number of feeding turns
     */
    public int getFeedingTurns() {
        return feedingTurns;
    }

    /**
     * Method to set the current number of feeding turns
     *
     * @param feedingTurns current number of feeding turns
     */
    public void setFeedingTurns(int feedingTurns) {
        this.feedingTurns = feedingTurns;
    }

    /**
     * Method to get the number of feeding turns needed
     *
     * @return number of feeding turns needed
     */
    public int getFeedingTurnsNeeded() {
        return feedingTurnsNeeded;
    }

    /**
     * Method to set the number of feeding turns needed
     *
     * @param feedingTurnsNeeded number of feeding turns needed
     */
    public void setFeedingTurnsNeeded(int feedingTurnsNeeded) {
        this.feedingTurnsNeeded = feedingTurnsNeeded;
    }


    /**
     * Method to check if the Pterodactyl is suitable for mating
     *
     * @return true if suitable for mating, false otherwise
     */
    public boolean suitableForMating() {
        if (!isHungry() && !isThirsty() && !isPregnant()) {
            return true;
        } else {
            return false;
        }
    }

    /**
     * Method to return if the Pterodactyl is on a tree
     *
     * @return true if on a tree, false otherwise
     */
    public boolean isOnTree() {
        return isOnTree;
    }

    /**
     * Method to set the Pterodactyl to be on the tree or not
     *
     * @param onTree true or false
     */
    public void setOnTree(boolean onTree) {
        isOnTree = onTree;
    }

    /**
     *  Method to get the location of the tree adjacent to the Pterodactyl
     *
     * @return location of the adjacent tree
     */
    public Location getAdjacentTreeLocation() {
        return adjacentTreeLocation;
    }

    /**
     * Method to set the location of the tree adjacent to the Pterodactyl
     * @param adjacentTreeLocation
     */
    public void setAdjacentTreeLocation(Location adjacentTreeLocation) {
        this.adjacentTreeLocation = adjacentTreeLocation;
    }

    /**
     * Method to check if there are dinosaurs nearby the Pterodactyl
     *
     * @param gameMap the game map with the Pterodactyl on it
     * @param actor the actor which is the Pterodactyl
     * @return true if there is dinosaur nearby, false otherwise
     */
    public boolean dinosaursNearby(GameMap gameMap, Actor actor) {
        int radius = 1;
        Location dinosaurLocation = gameMap.locationOf(actor);
        int xCoordinate = dinosaurLocation.x();
        int yCoordinate = dinosaurLocation.y();

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
                if (gameMap.isAnActorAt(there) && there.getActor() != actor) {
                    Actor actorAtThere = gameMap.getActorAt(there);
                    if (actorAtThere instanceof Dinosaur) {
                        return true;
                    }
                }
            }
        }
        return false;
    }

    /**
     * Method to return if the Pterodactyl is trying to breed
     *
     * @return true if trying to breed, false otherwise
     */
    public boolean isTryingToBreed() {
        return isTryingToBreed;
    }

    /**
     * Method to set the Pterodactyl is trying to breed or not
     *
     * @param tryingToBreed true or false
     */
    public void setTryingToBreed(boolean tryingToBreed) {
        isTryingToBreed = tryingToBreed;
    }
}
