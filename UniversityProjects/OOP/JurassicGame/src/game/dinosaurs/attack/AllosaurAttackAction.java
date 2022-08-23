package game.dinosaurs.attack;

import libs.engine.Action;
import libs.engine.Actor;
import libs.engine.GameMap;
import game.dinosaurs.general.*;

/***
 * Action class for Allosaur to attack its prey
 */
public class AllosaurAttackAction extends Action {

    /***
     * The dinosaur to be attacked
     */
    private Actor target;

    public AllosaurAttackAction(Actor target) {
        this.target = target;
    }

    @Override
    public String execute(Actor actor, GameMap map) {
        Allosaur allosaur = (Allosaur) actor;
        Dinosaur targetDinosaur = (Dinosaur) target;
        if (targetDinosaur instanceof Stegosaur) {
            targetDinosaur.hurt(20);
            allosaur.gainHitPoints(20);
        } else if (targetDinosaur instanceof Pterodactyl && targetDinosaur.getDinosaurMode() == DinosaurMode.LAND) {
            allosaur.gainHitPoints(allosaur.getMaximumHitPoints());
            System.out.println(targetDinosaur + " has been killed by " + actor);
            map.removeActor(targetDinosaur);
        }

        String targetName = targetDinosaur.getName();
//        allosaur.addAttackHistory(targetName);
        allosaur.getAttackHashMap().put(targetName, 0);

        return actor + " attacked " + target;
    }

    @Override
    public String menuDescription(Actor actor) {
        return actor + " is attacking " + target;
    }
}
