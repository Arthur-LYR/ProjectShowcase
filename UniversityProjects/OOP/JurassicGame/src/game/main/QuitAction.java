package game.main;

import libs.engine.Action;
import libs.engine.Actor;
import libs.engine.GameMap;

import java.util.InputMismatchException;

/**
 * A Class that represents the action that allows a Player to quit the current game
 */
public class QuitAction extends Action {
    /**
     * Raises an exception to inform that the Player has quit the game
     * @param actor The actor performing the action.
     * @param map The map the actor is on.
     * @return Does not return anything
     */
    @Override
    public String execute(Actor actor, GameMap map) {
        throw new InputMismatchException("Player Quits Current Game");
    }

    /**
     * Returns an appropriate menu message
     * @param actor The actor performing the action.
     * @return String in Menu Option
     */
    @Override
    public String menuDescription(Actor actor) {
        return "Quit Current Game";
    }
}
