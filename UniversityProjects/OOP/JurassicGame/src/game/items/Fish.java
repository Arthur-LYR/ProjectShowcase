package game.items;

import libs.engine.Item;

/**
 * Class that represents Fish
 */
public class Fish extends Item {
    /**
     * FoodLevel Item restores to Dinosaur
     */
    private int foodValue;

    /***
     * Constructor.
     */
    public Fish() {
        super("Fish", 'f', false);
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
}
