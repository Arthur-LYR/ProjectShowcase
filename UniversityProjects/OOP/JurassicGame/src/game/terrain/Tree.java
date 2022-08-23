package game.terrain;

import libs.engine.GameMap;
import libs.engine.Ground;
import libs.engine.Location;
import game.items.Fruit;
import game.main.Player;
import game.main.Util;

import java.util.ArrayList;

/**
 * Class that represents a Tree that can grow out in the wild.
 */
public class Tree extends Ground {
	/**
	 * Number of turns since tree was born
	 */
	private int age = 0;

	/**
	 * Stores a fruit whenever a Tree grows one. One Tree can only hold one Fruit.
	 */
	private Fruit fruit;

	/**
	 * ArrayList to store the fruits present on the tree.
	 */
	private static ArrayList<Fruit> fruitArrayList = new ArrayList<>();

	/**
	 * ArrayList to store the coordinates of the tree adjacent to this tree
	 */
	private ArrayList<Integer> adjacentTreeCoordinatesArrayList = new ArrayList<>();

	/**
	 * Boolean variable to check if the tree is occupied by Pterodactyl
	 */
	private boolean isOccupied = false;

	/**
	 * Constructor for Tree
	 */
	public Tree() {
		super('+');
	}

	/**
	 * Ages the tree, give the tree a chance to produce fruit, give the tree a chance to drop the fruit.
	 * @param location The location of the Ground
	 */
	@Override
	public void tick(Location location) {
		super.tick(location);

		// Aging Process
		age++;
		agingProcess();

		// 50% chance of growing fruit
		if (Util.eventSuccess(1, 2) && fruit == null) {
			fruit = new Fruit();
			fruit.setHabitat("Tree");
			displayChar = 'F';
			Player.gainEcoPoints(1);
		}

		// 5% chance of fruit dropping to ground
		if (Util.eventSuccess(1, 20) && fruit != null) {
			fruit.setHabitat("Floor");
			location.addItem(fruit);
			fruit = null;
			agingProcess();
		}
	}

	/**
	 * Checks the age of the tree and sets the appropriate display character
	 */
	public void agingProcess() {
		if (age >= 0 && age < 10) {
			displayChar = '+';
		} else if (age >= 10 && age < 20) {
			displayChar = 't';
		} else if (age >= 20) {
			displayChar = 'T';
		}
	}

	/***
	 * Returns the ArrayList containing the fruits on the tree (if any)
	 * @return
	 */
	public ArrayList<Fruit> getFruitArrayList() {
		return fruitArrayList;
	}

	/**
	 * Method to pick fruit from tree and return it
	 *
	 * @return Fruit from the tree
	 */
	public Fruit pickFruitFromTree() {
		Fruit pickedFruit = fruitArrayList.get(0);
		fruitArrayList.remove(0);
		return pickedFruit;
	}

	/**
	 * Method to check if tree is occupied
	 *
	 * @return true if occupied, false otherwise
	 */
	public boolean isOccupied() {
		return isOccupied;
	}

	/**
	 * Method to set the tree occupancy
	 *
	 * @param occupied true or false
	 */
	public void setOccupied(boolean occupied) {
		isOccupied = occupied;
	}

	/**
	 * Method to check if there is a tree adjacent to the tree
	 *
	 * @param gameMap the game map
	 * @param xCoordinate xCoordinate of the tree
	 * @param yCoordinate yCoordinate of the tree
	 * @return true if there is an adjacent tree, false otherwise
	 */
	public boolean adjacentTreeAvailable(GameMap gameMap, int xCoordinate, int yCoordinate) {
		int radius = 1;

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
				Ground ground = there.getGround();
				if (ground instanceof Tree) {
					adjacentTreeCoordinatesArrayList.clear();
					adjacentTreeCoordinatesArrayList.add(i);
					adjacentTreeCoordinatesArrayList.add(j);
					return true;
				}
			}
		}
		return false;
	}

	/**
	 * Method to get the adjacent tree coordinates arrayList
	 *
	 * @return the adjacent tree coordinates arrayList
	 */
	public ArrayList<Integer> getAdjacentTreeCoordinatesArrayList() {
		return adjacentTreeCoordinatesArrayList;
	}
}
