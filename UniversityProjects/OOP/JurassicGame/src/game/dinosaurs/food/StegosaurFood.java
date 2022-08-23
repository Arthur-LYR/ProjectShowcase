package game.dinosaurs.food;

/**
 * Food consumable by Stegosaur and the food value provided
 */

public enum StegosaurFood {
    FRUIT(10),
    PLAYER_FRUIT(20),
    MEAL_KIT(200);

    /**
     * the food value provided by the food
     */
    private int foodValue;

    /**
     * constructor.
     *
     * @param foodValue food value provided by the food
     */
    StegosaurFood(int foodValue) {
        this.foodValue = foodValue;
    }

    /**
     * Method to get the food value
     *
     * @return the food value provided by the food
     */
    public int getFoodValue() {
        return foodValue;
    }
}
