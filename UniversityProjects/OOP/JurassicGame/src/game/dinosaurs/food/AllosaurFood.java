package game.dinosaurs.food;

/***
 * Food consumable by Allosaur and the food value provided
 */
public enum AllosaurFood {
    DEAD_ALLOSAUR(50),
    DEAD_STEGOSAUR(50),
    DEAD_BRACHIOSAUR(100),
    EGGS(10),
    MEAL_KIT(200),
    FISH(5);

    /***
     * the food value provided by the food
     */
    private int foodValue;

    /***
     * constructor.
     *
     * @param foodValue food value provided by the food
     */
    AllosaurFood(int foodValue) {
        this.foodValue = foodValue;
    }

    /***
     * Method to get the food value
     *
     * @return the food value provided by the food
     */
    public int getFoodValue() {
        return foodValue;
    }
}
