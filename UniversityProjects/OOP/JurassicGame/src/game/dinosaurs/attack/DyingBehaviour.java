package game.dinosaurs.attack;

import libs.engine.Action;
import libs.engine.Actor;
import libs.engine.GameMap;
import game.dinosaurs.general.Behaviour;
import game.dinosaurs.general.Dinosaur;

public class DyingBehaviour implements Behaviour {

    /***
     * Method to get the action that the dinosaur will perform.
     *
     * @param actor the Actor acting
     * @param map the GameMap containing the Actor
     * @return action the dinosaur will take
     */
    @Override
    public Action getAction(Actor actor, GameMap map) {
        Dinosaur dinosaur = (Dinosaur) actor;
        if (dinosaur.isHealthCritical() || dinosaur.isWaterCritical()) {
            return new DeathAction();
        } else {
            return null;
        }
    }
}
