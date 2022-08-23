package game.main;

import java.util.*;

import game.dinosaurs.general.*;
import game.items.VendingMachine;
import game.terrain.*;
import libs.engine.*;

/**
 * The main class for the Jurassic World game.
 *
 */
public class Application {
	/**
	 * Displays the Menu in which user selects game mode
	 */
	private static void displayMenu() {
		System.out.println("Select Game Mode:");
		System.out.println("-----------------------");
		System.out.println("1. Challenge");
		System.out.println("2. Sandbox");
		System.out.println("3. Close Program");
		System.out.println("-----------------------");
	}

	/**
	 * Gets the user input for the game mode they wish to play
	 * @return Option number of Selected game mode
	 */
	private static int getMenuInput() {
		Scanner menu = new Scanner(System.in);
		int userSelection = 0;
		do {
			try {
				userSelection = Integer.parseInt(menu.nextLine());
			} catch (NumberFormatException e) {
				// Do nothing
			}
		} while (userSelection < 1 || userSelection > 3);
		System.out.println("-----------------------");
		return userSelection;
	}

	/**
	 * If user selects challenge mode, gets the appropriate user inputs
	 * @return Array in form of [ecoPointLimit, moveLimit]
	 * @see Player
	 */
	private static int[] getChallengeInput() {
		System.out.println("Eco Point Goal:");
		Scanner ecoPointSelection = new Scanner(System.in);
		int ecoPointLimit = 0;
		do {
			try {
				ecoPointLimit = Integer.parseInt(ecoPointSelection.nextLine());
			} catch (NumberFormatException e) {
				// Do nothing
			}
		} while (ecoPointLimit <= 0);
		System.out.println("-----------------------");
		System.out.println("Move Limit:");
		Scanner moveSelection = new Scanner(System.in);
		int moveLimit = 0;
		do {
			try {
				moveLimit = Integer.parseInt(moveSelection.nextLine());
			} catch (NumberFormatException e) {
				// Do nothing
			}
		} while (moveLimit <= 0);
		System.out.println("-----------------------");
		int[] selections = {ecoPointLimit, moveLimit};
		return selections;
	}

	/**
	 * Main Method that runs Application
	 * @param args -
	 */
	public static void main(String[] args) {
		// Basically an Infinite Loop until User decides to Close Program
		while (true) {
			// Get User to Select Game Mode
			displayMenu();
			int userSelection = getMenuInput();
			Player player = new Player("Player", '@', 100);
			switch (userSelection) {
				case 1:
					int[] playerInput = getChallengeInput();
					player.setChallenge(true);
					player.setEcoPointLimit(playerInput[0]);
					player.setMoveLimit(playerInput[1]);
					break;
				case 2:
					player.setChallenge(false);
					break;
				case 3:
					System.out.println("User Closes Program");
					System.exit(0);
					break;
			}

			// Create World
			World world = new World(new Display());

			// Create Northern Map
			FancyGroundFactory northGroundFactory = new FancyGroundFactory(new Dirt(), new Tree(), new Lake());
			List<String> northMap = Arrays.asList(
					"................................................................................",
					".............~~.................................................................",
					".............~~.................................................~~..............",
					".............~~.................................................~~..............",
					".............~~.................................................~~..............",
					"................................................................~~..............",
					"................................................................................",
					"......................................+++.......................................",
					".....................................++++++.....................................",
					"...................................+++++........................................",
					".....................................++++++.....................................",
					"......................................+++.......................................",
					".....................................+++........................................",
					"................................................................................",
					"............+++.................................................................",
					".............+++++..............................................................",
					"...............++........................................+++++..................",
					".............+++....................................++++++++....................",
					"............+++.......................................+++.......................",
					"............................++++++..............................................",
					"..............................++++.......................................++.....",
					"................................++......................................++.++...",
					".........................................................................++++...",
					"..........................................................................++....",
					"................................................................................");
			GameMap northGameMap = new GameMap(northGroundFactory, northMap);
			world.addGameMap(northGameMap);

			// Create Southern Map
			FancyGroundFactory groundFactory = new FancyGroundFactory(new Dirt(), new Wall(), new Floor(), new Tree(), new Lake());
			List<String> map = Arrays.asList(
					"................................................................................",
					"................................................................................",
					".....#######....................................................~~..............",
					".....#_____#....................................................~~..............",
					".....#_____#....................................................~~..............",
					".....###.###....................................................~~..............",
					"................................................................................",
					"......................................+++.......................................",
					".......................................++++.....................................",
					"...................................+++++........................................",
					".....................................++++++.....................................",
					"......................................+++.......................................",
					".....................................+++........................................",
					"................................................................................",
					"............+++.................................................................",
					".............+++++..............................................................",
					"...............++........................................+++++..................",
					".............+++....................................++++++++....................",
					"............+++.......................................+++.......................",
					"................................................................................",
					".........................................................................++.....",
					"........................................................................++.++...",
					".........................................................................++++...",
					"..........................................................................++....",
					"................................................................................");
			GameMap gameMap = new GameMap(groundFactory, map);
			world.addGameMap(gameMap);

			// Allow Player to Traverse Between Maps
			String[] maps = {"South", "North"};
			for (int i = 0; i < maps.length; i++) {
				// Initialise Variables
				int y;
				int y_destination;
				String mapName = maps[i];
				String sourceRow;
				GameMap sourceMap;
				GameMap destinationMap;
				ArrayList<String> hotKeys = new ArrayList<>();

				// Check Which Map
				if (i == maps.length - 1) {
					// Go from South to North
					y = 0;
					y_destination = northMap.size() - 1;
					sourceRow = map.get(y);
					sourceMap = gameMap;
					destinationMap = northGameMap;
					hotKeys.add("8");
					hotKeys.add("7");
					hotKeys.add("9");
				} else {
					// Go from North to South
					y = northMap.size() - 1;
					y_destination = 0;
					sourceRow = northMap.get(y);
					sourceMap = northGameMap;
					destinationMap = gameMap;
					hotKeys.add("2");
					hotKeys.add("1");
					hotKeys.add("3");
				}

				// Add appropriate Exits
				for (int x = 0; x < sourceRow.length(); x++) {
					Exit diagonalWest;
					Exit straight = new Exit(mapName, destinationMap.at(x, y_destination), hotKeys.get(0));
					Exit diagonalEast;

					// All will have a straight exit
					sourceMap.at(x, y).addExit(straight);

					// Check if square is at far end
					if (x == sourceRow.length() - 1) {
						// East Most, cannot go East
						diagonalWest = new Exit(mapName + "-West", destinationMap.at(x - 1, y_destination), hotKeys.get(1));
						sourceMap.at(x, y).addExit(diagonalWest);
					} else if (x == 0) {
						// West Most, cannot go West
						diagonalEast = new Exit(mapName + "-East", destinationMap.at(x + 1, y_destination), hotKeys.get(2));
						sourceMap.at(x, y).addExit(diagonalEast);
					} else {
						// Middle, can go both East and West
						diagonalWest = new Exit(mapName + "-West", destinationMap.at(x - 1, y_destination), hotKeys.get(1));
						diagonalEast = new Exit(mapName + "-East", destinationMap.at(x + 1, y_destination), hotKeys.get(2));
						sourceMap.at(x, y).addExit(diagonalWest);
						sourceMap.at(x, y).addExit(diagonalEast);
					}
				}
			}

			// Add Player into Game
			world.addPlayer(player, gameMap.at(9, 4));

			// Place a pair of stegosaurs in the middle of the map
			gameMap.at(59, 3).addActor(new Stegosaur(Status.ADULT, Gender.MALE));
			gameMap.at(32, 12).addActor(new Stegosaur(Status.ADULT, Gender.FEMALE));

			// Place a pair of brachiosaurs in the middle of the map
			gameMap.at(37, 14).addActor(new Brachiosaur(Status.ADULT, Gender.MALE));
			gameMap.at(39, 14).addActor(new Brachiosaur(Status.ADULT, Gender.MALE));

			// Place a pair of Pterodactyls in the middle of the map
//			gameMap.at(58, 3).addActor(new Pterodactyl(Status.ADULT, Gender.MALE));
//			gameMap.at(60, 3).addActor(new Pterodactyl(Status.ADULT, Gender.FEMALE));

			// Place an allosaur in the map
//			gameMap.at(37, 15).addActor(new Allosaur(Status.ADULT));

			// Add Vending Machine in Player's house
			gameMap.at(6, 3).addItem(new VendingMachine());

			// Add Rain to Game
			gameMap.at(5, 2).setGround(new Rain());

			// Run Game and Check Outcome
			try {
				world.run();
			} catch (InputMismatchException e) {
				// Player Quits
				System.out.println();
			} catch (IndexOutOfBoundsException e) {
				// Player Loses
				System.out.println("\n-----------------------");
				System.out.println("You Lose");
				System.out.println("-----------------------\n");
			} catch (ArithmeticException e) {
				// Player Wins
				System.out.println("\n-----------------------");
				System.out.println("You Win");
				System.out.println("-----------------------\n");
			}
		}
	}
}
