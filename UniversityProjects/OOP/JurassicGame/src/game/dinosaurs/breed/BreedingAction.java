package game.dinosaurs.breed;

import libs.engine.Action;
import libs.engine.Actor;
import libs.engine.GameMap;
import game.dinosaurs.general.*;

import java.util.Random;

/***
 * BreedingAction contains the logic for the dinosaurs to breed if certain pre-condtions are met
 */
public class BreedingAction extends Action {
    /**
     * The dinosaur to breed with
     */
    private Actor target;

    /**
     * Random number generator
     */
    protected Random rand = new Random();

    /**
     * Constructor.
     *
     * @param target the Dinosaur to breed with
     */
    public BreedingAction(Actor target) {
        this.target = target;
    }

    /**
     * Method to execute the process of dinosaur breeding if pre-conditions are met
     *
     * @param actor The actor performing the action.
     * @param map The map the actor is on.
     * @return String to explain what happened
     */
    @Override
    public String execute(Actor actor, GameMap map) {
        String result = "";

        if (suitableForMating(target)) {
            System.out.println(actor + " is trying to mate with " + target);
            if (target.getDisplayChar() == 's') {
                Stegosaur dino = (Stegosaur) target;
                if (dino.getGender() == Gender.FEMALE) {
                    dino.addEggToStomach();
                    result = "Mating successful with " + dino + " pregnant";
                } else {
                    ((Stegosaur) actor).addEggToStomach();
                    result = "Mating successful with " + actor + " pregnant";
                }
            } else if (target.getDisplayChar() == 'r') {
                Brachiosaur dino = (Brachiosaur) target;
                if (dino.getGender() == Gender.FEMALE) {
                    dino.addEggToStomach();
                    result = "Mating successful with " + dino + " pregnant";
                } else {
                    ((Brachiosaur) actor).addEggToStomach();
                    result = "Mating successful with " + actor + " pregnant";
                }
            } else if (target.getDisplayChar() == 'a') {
                Allosaur dino = (Allosaur) target;
                if (dino.getGender() == Gender.FEMALE) {
                    dino.addEggToStomach();
                    result = "Mating successful with " + dino + " pregnant";
                } else {
                    ((Allosaur) actor).addEggToStomach();
                    result = "Mating successful with " + actor + " pregnant";
                }
            } else if (target.getDisplayChar() == 'p') {
                Pterodactyl dino = (Pterodactyl) target;
                if (dino.getGender() == Gender.FEMALE) {
                    dino.addEggToStomach();
                    dino.setMobile(true);
                    dino.setOnTree(false);
                    result = "Mating successful with " + dino + " pregnant";
                } else {
                    Pterodactyl pterodactyl = (Pterodactyl) actor;
                    pterodactyl.addEggToStomach();
                    pterodactyl.setMobile(true);
                    pterodactyl.setOnTree(false);
                    result = "Mating successful with " + actor + " pregnant";
                }
            }
            return result;
        }
        return "nothing happened for " + actor + " during BreedingAction (Mate is not well fed or thirsty or pregnant)";
    }



    /**
     * Returns a descriptive string
     *
     * @param actor The actor performing the action.
     * @return the text we put on the menu
     */
    @Override
    public String menuDescription(Actor actor) {
        String statement = actor + "is mating with " + target;
        return statement;
    }

    /**
     * Method to determine if the dinosaur is suitable for mating/breeding
     * Check is pregnant and hit points
     *
     * @param actor the dinosaur finding a mate
     * @return true or false depending on whether the dinosaur is suitable for mating
     */
    public boolean suitableForMating(Actor actor) {
        boolean canBreed = false;
        if (actor.getDisplayChar() == 's') {
            Stegosaur dino = (Stegosaur) actor;
            if (!dino.isPregnant()) {
                int hitPoints = dino.getHitPoints();
                int threshold = dino.getMatingThreshold();
                if (hitPoints > threshold) {
                    canBreed = true;
                }
            }
        } else if (actor.getDisplayChar() == 'r') {
            Brachiosaur dino = (Brachiosaur) actor;
            if (!dino.isPregnant()) {
                int hitPoints = dino.getHitPoints();
                int threshold = dino.getMatingThreshold();
                if (hitPoints > threshold) {
                    canBreed = true;
                }
            }
        } else if (actor.getDisplayChar() == 'a') {
            Allosaur dino = (Allosaur) actor;
            if (!dino.isPregnant()) {
                int hitPoints = dino.getHitPoints();
                int threshold = dino.getMatingThreshold();
                if (hitPoints > threshold) {
                    canBreed = true;
                }
            }
        } else if (actor.getDisplayChar() == 'p') {
            Pterodactyl dino = (Pterodactyl) actor;
            if (!dino.isPregnant()) {
                int hitPoints = dino.getHitPoints();
                int threshold = dino.getMatingThreshold();
                if (hitPoints > threshold) {
                    canBreed = true;
                }
            }
        }
        return canBreed;
    }
}
