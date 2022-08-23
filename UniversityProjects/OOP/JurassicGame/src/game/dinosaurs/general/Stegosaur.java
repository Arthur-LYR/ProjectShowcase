package game.dinosaurs.general;


import game.dinosaurs.attack.AttackAction;
import game.dinosaurs.attack.DeathAction;
import game.dinosaurs.attack.DyingBehaviour;
import game.dinosaurs.breed.SearchingMateBehaviour;
import game.dinosaurs.drink.SearchingWaterBehaviour;
import game.dinosaurs.food.SearchingFoodBehaviour;
import game.items.DinosaurType;
import game.items.Egg;
import game.items.FeedingAction;
import game.terrain.Rain;
import libs.engine.*;

import java.util.ArrayList;
import java.util.Random;

/**
 * Stegosaur class which is the child class of Dinosaur allows the instantiation of Stegosaur objects which is a type
 * of dinosaur present in the game.
 */
public class Stegosaur extends Dinosaur {

	/**
	 * Code given to identify the dinosaurs
	 */
	private static int nameCode = 1;

	/**
	 * ArrayList to store the behaviours of the Stegosaur
	 */
	private ArrayList<Behaviour> behaviours = new ArrayList<>();


	/** 
	 * Constructor.
	 * All Stegosaurs are represented by a 's' and have 100 hit points max
	 * 
	 * @param status the growth status of the Stegosaur
	 */
	public Stegosaur(Status status) {
		super("Stegosaur" + nameCode, 's', 50, 100, 60, 100, status, 90, 40, 50, 20, 15);
		nameCode++;
		setDinosaurMode(DinosaurMode.LAND);

		if (getStatus() == Status.BABY) {
			hurt(40);
		}

		// add behaviours to the Stegosaurs at instantiation
		behaviours.add(new DyingBehaviour());
		behaviours.add(new SearchingWaterBehaviour());
		behaviours.add(new SearchingFoodBehaviour());
		behaviours.add(new SearchingMateBehaviour());
		behaviours.add(new WanderBehaviour());
	}

	/**
	 * Constructor. (We can choose the gender of Stegosaur)
	 *
	 * @param status the growth status of the Stegosaur
	 * @param gender the gender of the Stegosaur
	 */
	public Stegosaur(Status status, Gender gender) {
		super("Stegosaur" + nameCode, 's', 50, 100, 60, 100, status, 90, 40, 50, 20, 15);
		nameCode++;
		setDinosaurMode(DinosaurMode.LAND);
		setGender(gender);

		if (getStatus() == Status.BABY) {
			hurt(40);
		}


		// add behaviours to the Stegosaurs at instantiation
		behaviours.add(new DyingBehaviour());
		behaviours.add(new SearchingWaterBehaviour());
		behaviours.add(new SearchingFoodBehaviour());
		behaviours.add(new SearchingMateBehaviour());
		behaviours.add(new WanderBehaviour());
	}
	/**
	 * Method to return a collection of the Actions that Stegosaur can do
	 *
	 * @param otherActor the Actor that might be performing attack
	 * @param direction  String representing the direction of the other Actor
	 * @param map        current GameMap
	 * @return Actions that the Stegosaur can do
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
	 * Method to select and return an action for the Stegosaur to perform in the current turn. Also decrements the
	 * Stegosaur's health and tracks the growth status of the Stegosaur.
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
		if (getBabyTurns() == 30) {
			this.setStatus(Status.ADULT);
		}

		if (isPregnant()) {
			if (getPregnantTurns() == 10) {
				Egg egg = new Egg("Stegosaur egg", 'e', DinosaurType.STEGOSAUR, false);
				map.locationOf(this).addItem(egg);
				getStomach().clear();
				setPregnantTurns(0);
				System.out.println(this + " laid an egg");
			} else {
				incrementPregnantTurns();
			}
		}

		// if the map is raining, hibernating Stegosaur due to thirst will be revived
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
	 * Method to get the code of Stegosaur
	 *
	 * @return the code of Stegosaur
	 */
	@Override
	public int getDinosaurCode() {
		return 1;
	}

	/**
	 * Method to add egg to the stomach of Stegosaur
	 */
	@Override
	public void addEggToStomach() {
		Egg egg = new Egg("Stegosaur egg", 'e', DinosaurType.STEGOSAUR, false);
		getStomach().add(egg);
		setPregnant(true);
	}
}


