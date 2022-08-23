package game.items;

import libs.engine.Action;
import libs.engine.Actor;
import libs.engine.GameMap;
import game.main.Player;

import java.util.Scanner;

/**
 * Class that represents the Action of buying an Item from the Vending Machine
 */
public class BuyAction extends Action {
    /**
     * Executes the BuyAction
     * @param actor The actor performing the action.
     * @param map The map the actor is on.
     * @return The message of the Action outcome
     */
    @Override
    public String execute(Actor actor, GameMap map) {
        String item = null;
        int cost = 0;
        if (map.locationOf(actor).x() == 6 && map.locationOf(actor).y() == 3) {
            VendingMachine vendingMachine = (VendingMachine) map.locationOf(actor).getItems().get(0);
            int option = itemSelectionMenu();
            if (option == 1 && Player.getEcoPoints() >= 30) {
                actor.addItemToInventory(vendingMachine.sell("Fruit"));
                Player.spendEcoPoints(cost);
                item = "Fruit";
            } else if (option == 2 && Player.getEcoPoints() >= 100) {
                actor.addItemToInventory(vendingMachine.sell("Vegetarian Meal Kit"));
                Player.spendEcoPoints(cost);
                item = "Vegetarian Meal Kit";
            } else if (option == 3 && Player.getEcoPoints() >= 500) {
                actor.addItemToInventory(vendingMachine.sell("Carnivore Meal Kit"));
                Player.spendEcoPoints(cost);
                item = "Carnivore Meal Kit";
            } else if (option == 4 && Player.getEcoPoints() >= 200) {
                actor.addItemToInventory(vendingMachine.sell("Stegosaur Egg"));
                Player.spendEcoPoints(cost);
                item = "Stegosaur Egg";
            } else if (option == 5 && Player.getEcoPoints() >= 500) {
                actor.addItemToInventory(vendingMachine.sell("Brachiosaur Egg"));
                Player.spendEcoPoints(cost);
                item = "Brachiosaur Egg";
            } else if (option == 6 && Player.getEcoPoints() >= 1000) {
                actor.addItemToInventory(vendingMachine.sell("Allosaur Egg"));
                Player.spendEcoPoints(cost);
                item = "Allosaur Egg";
            } else if (option == 7 && Player.getEcoPoints() >= 200) {
                actor.addItemToInventory(vendingMachine.sell("Pterodactyl Egg"));
                Player.spendEcoPoints(cost);
                item = "Allosaur Egg";
            }else if (option == 8 && Player.getEcoPoints() >= 500) {
                actor.addItemToInventory(vendingMachine.sell("Laser Gun"));
                Player.spendEcoPoints(cost);
                item = "Laser Gun";
            } else {
                return "Not enough EcoPoints to buy item";
            }
        }
        return actor + " successfully buys " + item + " from Vending Machine";
    }

    /**
     * Displays the option in the menu
     * @param actor The actor performing the action.
     * @return Description in Menu
     */
    @Override
    public String menuDescription(Actor actor) {
        return actor + " shops for items in Vending Machine";
    }

    /**
     * Menu to display Items available to Player
     * @return Option selected by Player
     */
    public int itemSelectionMenu() {
        Scanner myObj = new Scanner(System.in);  // Create a Scanner object
        System.out.println("Choose Item to buy from Vending Machine:");
        System.out.println("1. Fruit");
        System.out.println("2. Vegetarian Meal Kit");
        System.out.println("3. Carnivore Meal Kit");
        System.out.println("4. Stegosaur Egg");
        System.out.println("5. Brachiosaur Egg");
        System.out.println("6. Allosaur Egg");
        System.out.println("7. Pterodactyl Egg");
        System.out.println("8. Laser Gun");

        int number = 0;
        boolean valid;
        do {
            try {
                number = Integer.parseInt(myObj.nextLine());
                if (number >= 1 && number <= 8) {
                    valid = true;
                } else {
                    valid = false;
                }
            } catch (Exception e) {
                valid = false;
            }
        } while (!valid);
        return number;
    }
}
