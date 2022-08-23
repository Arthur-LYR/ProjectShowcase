package game.main;

import game.items.BuyAction;
import game.items.Fruit;
import game.items.PickFruitAction;
import game.items.VendingMachine;
import game.terrain.Bush;
import game.terrain.Tree;
import libs.engine.*;

import java.util.ArrayList;

/**
 * Class representing the Player.
 */
public class Player extends Actor {
	/**
	 * Menu for the Player
	 */
	private Menu menu = new Menu();

	/**
	 * The number of EcoPoints in owned by the Player
	 */
	private static int ecoPoints = 0;

	/**
	 * True if Player selects challenge mode, False if PLayer selects Sandbox mode
	 */
	private boolean challenge;

	/**
	 * Number of EcoPoints Player must obtain within move limit to win game
	 */
	private int ecoPointLimit;

	/**
	 * Number of Moves Player must achieve ecoPointLimit in order to win game
	 */
	private int moveLimit;

	/**
	 * Number of moves Player has made
	 */
	private int moveCount = 0;

	/**
	 * Constructor.
	 *
	 * @param name        Name to call the player in the UI
	 * @param displayChar Character to represent the player in the UI
	 * @param hitPoints   Player's starting number of hitpoints
	 */
	public Player(String name, char displayChar, int hitPoints) {
		super(name, displayChar, hitPoints);
	}

	/**
	 * Gets the allowable actions of the Player
	 * @param otherActor the Actor that might be performing attack
	 * @param direction  String representing the direction of the other Actor
	 * @param map        current GameMap
	 * @return List of Allowable Actions
	 */
	@Override
	public Actions getAllowableActions(Actor otherActor, String direction, GameMap map) {
		return super.getAllowableActions(otherActor, direction, map);
	}

	/**
	 * Executes at the beginning of each turn
	 * @param actions    collection of possible Actions for this Actor
	 * @param lastAction The Action this Actor took last turn. Can do interesting things in conjunction with Action.getNextAction()
	 * @param map        the map containing the Actor
	 * @param display    the I/O object to which messages may be written
	 * @return A Menu of Available Actions for the Player
	 */
	@Override
	public Action playTurn(Actions actions, Action lastAction, GameMap map, Display display) {
		// Handle multi-turn Actions
		if (lastAction.getNextAction() != null)
			return lastAction.getNextAction();

		// Player Makes a Move
		moveCount += 1;

		// Check Win Conditions if challenge mode activated
		if (challenge) {
			if (moveCount > moveLimit) {
				throw new IndexOutOfBoundsException("Player Loses");
			}
			if (ecoPoints >= ecoPointLimit) {
				throw new ArithmeticException("Player Wins");
			}
		}

		// Allow Player to Quit
		actions.add(new QuitAction());

		// Allow Player to Pick Fruits from Trees
		if (map.locationOf(this).getGround() instanceof Tree) {
			Tree tree = (Tree) map.locationOf(this).getGround();
			ArrayList<Fruit> fruitsOnTree = tree.getFruitArrayList();
			if (fruitsOnTree.size() != 0) {
				actions.add(new PickFruitAction(fruitsOnTree.get(0)));
			}
		}

		// Allow Player to Pick Fruits from Bushes
		if (map.locationOf(this).getGround() instanceof Bush) {
			Bush bush = (Bush) map.locationOf(this).getGround();
			ArrayList<Fruit> fruitsOnBush = bush.getFruitArrayList();
			if (fruitsOnBush.size() != 0) {
				actions.add(new PickFruitAction(fruitsOnBush.get(0)));
			}
		}

		// Allow Player to Buy Items from Vending Machine
		try {
			if (map.locationOf(this).getItems().get(0) instanceof VendingMachine) {
				actions.add(new BuyAction());
			}
		} catch (IndexOutOfBoundsException e){ }

		// Display Menu
		return menu.showMenu(this, actions, display);
	}

	/**
	 * Getter method for EcoPoints attribute
	 * @return ecoPoints
	 */
	public static int getEcoPoints() {
		return ecoPoints;
	}

	/**
	 * Increases the Player's EcoPoints by specified amount
	 * @param ecoPointGain Amount to increase EcoPoints
	 */
	public static void gainEcoPoints(int ecoPointGain) {
		ecoPoints += ecoPointGain;
	}

	/**
	 * Decreases the Player's EcoPoints by specified amount
	 * @param ecoPointSpend Amount to decrease EcoPoints
	 */
	public static void spendEcoPoints(int ecoPointSpend) {
		ecoPoints -= ecoPointSpend;
	}

	/**
	 * Setter method for challenge attribute
	 * @param challenge True if Player selects challenge mode, False if PLayer selects Sandbox mode
	 */
	public void setChallenge(boolean challenge) {
		this.challenge = challenge;
	}

	/**
	 * Setter Method for ecoPointLimit
	 * @param ecoPointLimit Number of EcoPoints Player must obtain within move limit to win game
	 */
	public void setEcoPointLimit(int ecoPointLimit) {
		this.ecoPointLimit = ecoPointLimit;
	}

	/**
	 * Setter method for moveLimit
	 * @param moveLimit Number of Moves Player must achieve ecoPointLimit in order to win game
	 */
	public void setMoveLimit(int moveLimit) {
		this.moveLimit = moveLimit;
	}
}
