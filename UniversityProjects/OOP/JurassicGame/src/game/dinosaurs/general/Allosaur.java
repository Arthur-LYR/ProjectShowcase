package game.dinosaurs.general;

import game.dinosaurs.attack.AttackAction;
import game.dinosaurs.attack.DeathAction;
import game.dinosaurs.attack.DyingBehaviour;
import game.dinosaurs.attack.SearchingPreyBehaviour;
import game.dinosaurs.breed.SearchingMateBehaviour;
import game.dinosaurs.drink.SearchingWaterBehaviour;
import game.dinosaurs.food.SearchingFoodBehaviour;
import game.items.DinosaurType;
import game.items.Egg;
import game.items.FeedingAction;
import game.terrain.Rain;
import libs.engine.*;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;
import java.util.Random;

/**
 * Allosaur class which is the child class of Dinosaur allows the instantiation of Allosaur objects which is a type of
 * dinosaur present in the game.
 */
public class Allosaur extends Dinosaur {

    /**
     * Code given to identify the dinosaurs
     */
    private static int nameCode = 1;
    /**
     * ArrayList to store the behaviours of the Allosaur
     */
    private ArrayList<Behaviour> behaviours = new ArrayList<>();

    /**
     * HashMap to store the names of the dinosaurs that this Allosaur had previously attacked as key and the number of
     * turns after the attack as value
     */
    private HashMap<String, Integer> attackHashMap = new HashMap<>();

    /**
     * All Allosaurs are represented by an 'a' and have 100 hit points max
     *
     * @param status the growth status of the Allosaur
     */
    public Allosaur(Status status) {
        super("Allosaur" + nameCode, 'a', 60, 100, 60, 100, status, 90, 40, 70,  20, 15);
        nameCode++;
        setDinosaurMode(DinosaurMode.LAND);

        if (status == Status.BABY) {
            hurt(40);
        }

        // add behaviours to the Allosaurs at instantiation
        behaviours.add(new DyingBehaviour());
        behaviours.add(new SearchingWaterBehaviour());
        behaviours.add(new SearchingFoodBehaviour());
        behaviours.add(new SearchingPreyBehaviour());
        behaviours.add(new SearchingMateBehaviour());
        behaviours.add(new WanderBehaviour());
    }

    /**
     * Constructor. (We can set the gender for Allosaur)
     *
     * @param status the growth status of the Allosaur
     * @param gender the gender of the Allosaur
     */
    public Allosaur(Status status, Gender gender) {
        super("Allosaur" + nameCode, 'a', 60, 100, 60, 100, status, 90, 40, 70,  20, 15);
        nameCode++;
        setDinosaurMode(DinosaurMode.LAND);
        setGender(gender);

        if (status == Status.BABY) {
            hurt(40);
        }

        // add behaviours to the Allosaurs at instantiation
        behaviours.add(new DyingBehaviour());
        behaviours.add(new SearchingWaterBehaviour());
        behaviours.add(new SearchingFoodBehaviour());
        behaviours.add(new SearchingPreyBehaviour());
        behaviours.add(new SearchingMateBehaviour());
        behaviours.add(new WanderBehaviour());
    }


    /**
     * Method to select and return an action for the Allosaur to perform in the current turn. Also decrements the
     * Allosaur's health and tracks the growth status of the Allosaur.
     *
     * @param actions    collection of possible Actions for this Actor
     * @param lastAction The Action this Actor took last turn. Can do interesting things in conjunction with Action.getNextAction()
     * @param map        the map containing the Actor
     * @param display    the I/O object to which messages may be written
     * @return Action to be performed
     */
    @Override
    public Action playTurn(Actions actions, Action lastAction, GameMap map, Display display) {

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
        if (getBabyTurns() == 50) {
            this.setStatus(Status.ADULT);
        }

        if (isPregnant()) {
            if (getPregnantTurns() == 40) {
                Egg egg = new Egg("Allosaur egg", 'e', DinosaurType.ALLOSAUR, false);
                map.locationOf(this).addItem(egg);
                getStomach().clear();
                setPregnantTurns(0);
                System.out.println(this + " laid an egg");
            } else {
                incrementPregnantTurns();
            }
        }

        if (Rain.isRaining()) {
            System.out.println(this + " can feel the rain!");
            reviveThirstyDinosaur();
        }

        checkAttackHashMap(attackHashMap);
        incrementTurnsInAttackHashMap(attackHashMap);

        Random rand = new Random();
        for (Behaviour behaviour: behaviours) {
            Action action = behaviour.getAction(this, map);
            if (action != null)
                return action;
        }

        return null;
    }

    /**
     * Method to return a collection of the Actions that can be done on Allosaur
     *
     * @param otherActor the Actor that might be performing attack
     * @param direction  String representing the direction of the other Actor
     * @param map        current GameMap
     * @return Actions that the Allosaur can do
     */
    @Override
    public Actions getAllowableActions(Actor otherActor, String direction, GameMap map) {
        Actions list = super.getAllowableActions(otherActor, direction, map);
        list.add(new AttackAction(this));
        list.add(new FeedingAction(this));
        list.add(new DeathAction());
        return list;
    }

    /**
     * Method to get the code of Allosaur
     *
     * @return the code of Allosaur
     */
    @Override
    public int getDinosaurCode() {
        return 3;
    }

    /**
     * Method to add egg to the stomach of Allosaur
     */
    @Override
    public void addEggToStomach() {
        Egg egg = new Egg("Allosaur egg", 'a', DinosaurType.ALLOSAUR, false);
        getStomach().add(egg);
        setPregnant(true);
    }

    /**
     * Get the attack hash map of the Allosaur
     *
     * @return attack hash map of the Allosaur
     */
    public HashMap<String, Integer> getAttackHashMap() {
        return attackHashMap;
    }

    /**
     * Method to check the attack hash map to remove the dinosaurs that have reached 20 turns of last being attacked
     *
     * @param attackHashMap the attack hash map of Allosaur
     */
    public void checkAttackHashMap(HashMap<String, Integer> attackHashMap) {
        if (!attackHashMap.isEmpty()) {
            for (Map.Entry<String, Integer> entry : attackHashMap.entrySet()) {
                if (entry.getValue() == 20) {
                    attackHashMap.remove(entry.getKey());
                }
            }
        }
    }

    /**
     * Method to increment the number of turns the dinosaur was last attacked by the Allosaur in the hash map
     *
     * @param attackHashMap the attack hash map of Allosaur
     */
    public void incrementTurnsInAttackHashMap(HashMap<String, Integer> attackHashMap) {
        if (!attackHashMap.isEmpty()){
            for (Map.Entry<String, Integer> entry : attackHashMap.entrySet()) {
                int value = entry.getValue();
                value++;
                attackHashMap.put(entry.getKey(), value);
            }
        }

    }

}




