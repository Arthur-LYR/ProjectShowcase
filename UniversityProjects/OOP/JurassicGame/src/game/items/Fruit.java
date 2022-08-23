package game.items;

import libs.engine.Location;
import game.terrain.Dirt;

/**
 * Class that represents the Fruit
 */
public class Fruit extends PortableItem {
    /**
     * Current location of the Fruit (Tree, Bush, Inventory, Floor)
     */
    private String habitat;

    /**
     * FoodLevel Item restores to Dinosaur
     */
    private int foodValue;

    /**
     * Number of turns since Fruit was born
     */
    private int age;

    /**
     * Cost of the Fruit in EcoPoints
     */
    private static int cost;

    /**
     * Constructor of the Fruit
     */
    public Fruit() {
        super("Fruit", 'O');
        this.cost = 30;
    }

    /**
     * Getter method for habitat attribute
     * @return The habitat of the Fruit
     */
    public String getHabitat() {
        return habitat;
    }

    /**
     * Setter method for habitat attribute
     * @param habitat The new habitat of the Fruit
     */
    public void setHabitat(String habitat) {
        this.habitat = habitat;
    }

    /**
     * Getter method for foodValue attribute
     * @return The foodValue of the Fruit
     */
    public int getFoodValue() {
        return foodValue;
    }

    /**
     * Setter method for foodValue attribute
     * @param foodValue The new foodValue of the Fruit
     */
    public void setFoodValue(int foodValue) {
        this.foodValue = foodValue;
    }

    /**
     * Ages the Fruit appropriately if on Floor
     * @param currentLocation The location of the ground on which we lie.
     */
    @Override
    public void tick(Location currentLocation) {
        super.tick(currentLocation);
        if (habitat == "Floor") {
            age++;
        }
        if (age == 15) {
            currentLocation.setGround(new Dirt());
        }
    }
}
