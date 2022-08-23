package libs.demo.conwayslife;

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
	 * @param name        Name to call the player in the UI
	 * @param displayChar Character to represent the player in the UI
	 * @param hitPoints   Player's starting number of hitpoints
	 */
	public Player(String name, char displayChar, int hitPoints) {
		super(name, displayChar, hitPoints);
	}

	@Override
	public Action playTurn(Actions actions, Action lastAction, GameMap map, Display display) {
		if (lastAction.getNextAction() != null)
			return lastAction.getNextAction();

		actions.add(new SleepAction());
		return menu.showMenu(this, actions, display);
	}

	private class SleepAction extends Action {

		private int sleepTime = 200;

		@Override
		public String execute(Actor actor, GameMap map) {
			sleepTime--;
			try {
				Thread.sleep(50);
			} catch (InterruptedException e) {
			}
			return actor + " is sleeping.";
		}

		@Override
		public String menuDescription(Actor actor) {
			return "Sleep a while";
		}

		@Override
		public Action getNextAction() {
			if (sleepTime > 0)
				return this;

			return null;
		}
	}
}
