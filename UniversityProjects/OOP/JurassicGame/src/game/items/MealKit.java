package game.items;

/**
 * Abstract class for the two Meal Kits to inherit from
 */
public class MealKit extends PortableItem {
    /**
     * FoodLevel Item restores to Dinosaur
     */
    private static int foodValue = 1000000000;

    /**
     * Cost of the Meal Kit in EcoPoints
     */
    private static int cost;

    /**
     * Constructor of the Meal Kit
     * @param name Name of the Meal Kit
     * @param displayChar The display character of the Meal Kit
     * @param cost Cost of the Meal Kit in EcoPoints
     */
    public MealKit(String name, char displayChar, int cost) {
        super(name, displayChar);
        this.cost = cost;
    }
}
