package libs.demo.mars;

import libs.engine.Action;
import libs.engine.Actions;
import libs.engine.Actor;
import libs.engine.Display;
import libs.engine.GameMap;
import libs.engine.Menu;

/**
 * Class representing the Player.
 */
public class Player extends Actor {

	private Menu menu = new Menu();
	
	/**
	 * Constructor.
	 *
	 * @param name Name to call the player in the UI
	 * @param displayChar Character to represent the player in the UI
	 * @param hitPoints Player's starting number of hitpoints
	 */
	public Player(String name, char displayChar, int hitPoints) {
		super(name, displayChar, hitPoints);
	}

	@Override
	public Action playTurn(Actions actions, Action lastAction, GameMap map, Display display) {
		return menu.showMenu(this, actions, display);
	}
}
