package game.dinosaurs.food;

/***
 * Food consumable by Pterodactyl and the food value provided
 */
public enum PterodactylFood {
    EGGS(10),
    FISH(5),
    MEAL_KIT(100);

    /***
     * the food value provided by the food
     */
    private int foodValue;

    /***
     * constructor.
     *
     * @param foodValue food value provided by the food
     */
    PterodactylFood(int foodValue) {
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
