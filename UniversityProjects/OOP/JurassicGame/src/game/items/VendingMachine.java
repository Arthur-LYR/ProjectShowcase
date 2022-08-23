package game.items;

import libs.engine.Item;
import libs.engine.Location;

import java.util.HashMap;

public class VendingMachine extends Item {
    /**
     * Stores all the products that the Player can buy
     */
    private HashMap<String, Item> products = new HashMap<>();

    /**
     * Constructor.
     */
    public VendingMachine() {
        super("Vending Machine", 'M', false);
        products.put("Fruit", new Fruit());
        products.put("Vegetarian Meal Kit", new VegetarianMealKit());
        products.put("Carnivore Meal Kit", new CarnivoreMealKit());
        products.put("Stegosaur Egg", new Egg("Stegosaur egg", 'e', DinosaurType.STEGOSAUR, true));
        products.put("Brachiosaur Egg", new Egg("Brachiosaur egg", 'e', DinosaurType.BRACHIOSAUR, true));
        products.put("Allosaur Egg", new Egg("Allosaur egg", 'e', DinosaurType.ALLOSAUR, true));
        products.put("Pterodactyl Egg", new Egg("Pterodactyl egg", 'e', DinosaurType.PTERODACTYL, true));
        products.put("Laser Gun", new LaserGun());
    }

    @Override
    /**
     * Checks if the vending machine does not contain any items and restocks any empty items
     */
    public void tick(Location currentLocation) {
        super.tick(currentLocation);

        if (!this.products.containsKey("Fruit")) {
            products.put("Fruit", new Fruit());
        }
        if (!this.products.containsKey("Vegetarian Meal Kit")) {
            products.put("Vegetarian Meal Kit", new VegetarianMealKit());
        }
        if (!this.products.containsKey("Carnivore Meal Kit")) {
            products.put("Carnivore Meal Kit", new CarnivoreMealKit());
        }
        if (!this.products.containsKey("Stegosaur Egg")) {
            products.put("Stegosaur Egg", new Egg("Stegosaur egg", 'e', DinosaurType.STEGOSAUR, true));
        }
        if (!this.products.containsKey("Brachiosaur Egg")) {
            products.put("Brachiosaur Egg", new Egg("Brachiosaur egg", 'e', DinosaurType.BRACHIOSAUR, true));
        }
        if (!this.products.containsKey("Allosaur Egg")) {
            products.put("Allosaur Egg", new Egg("Allosaur egg", 'e', DinosaurType.ALLOSAUR, true));
        }
        if (!this.products.containsKey("Pterodactyl Egg")) {
            products.put("Pterodactyl Egg", new Egg("Pterodactyl egg", 'e', DinosaurType.PTERODACTYL, true));
        }
        if (!this.products.containsKey("Laser Gun")) {
            products.put("Laser Gun", new LaserGun());
        }
    }

    /**
     * Sells the selected Item to the Player
     * @param item Name of Item Player wishes to buy
     * @return An Object instance of the Item the Player bought
     */
    public Item sell(String item) {
        Item product = null;
        if (item == "Fruit") {
            product = products.remove("Fruit");
        } else if (item == "Vegetarian Meal Kit") {
            product = products.remove("Vegetarian Meal Kit");
        } else if (item == "Carnivore Meal Kit") {
            product = products.remove("Carnivore Meal Kit");
        } else if (item == "Stegosaur Egg") {
            product = products.remove("Stegosaur Egg");
        } else if (item == "Brachiosaur Egg") {
            product = products.remove("Brachiosaur Egg");
        } else if (item == "Allosaur Egg") {
            product = products.remove("Allosaur Egg");
        } else if (item == "Pterodactyl Egg") {
            product = products.remove("Pterodactyl Egg");
        } else if (item == "Laser Gun") {
            product = products.remove("Laser Gun");
        }
        return product;
    }
}
