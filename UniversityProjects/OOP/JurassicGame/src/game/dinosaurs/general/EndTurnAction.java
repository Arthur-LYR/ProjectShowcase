package game.dinosaurs.general;

import libs.engine.Action;
import libs.engine.Actor;
import libs.engine.GameMap;

/**
 * An action that doesn't do anything. Just informing that the actor is done with the current behaviour (end of its turn)
 */
public class EndTurnAction extends Action {
    @Override
    public String execute(Actor actor, GameMap map) {
        return menuDescription(actor);
    }

    @Override
    public String menuDescription(Actor actor) {
        return actor + " ends its turn";
    }
}
