package game.items;

import java.util.Random;

/***
 * the types of dinosaurs present in the game and the cost of their eggs
 */
public enum DinosaurType {
    STEGOSAUR(200),
    BRACHIOSAUR(500),
    ALLOSAUR(1000),
    PTERODACTYL(200);

    /***
     * the cost of the dinosaur's egg
     */
    private int cost;

    /***
     * Constructor.
     *
     * @param cost the cost of the dinosaur's egg
     */
    DinosaurType(int cost) {
        this.cost = cost;
    }

    /***
     * Method to randomly return a dinosaur type
     * @return Dinosaur type
     */
    public static DinosaurType randomDinoType() {
        return DinosaurType.values() [new Random().nextInt(DinosaurType.values().length)];
    }

    /***
     * Method to get the cost of the dinosaur egg
     * @return cost of dinosaur egg
     */
    public int getCost() {
        return cost;
    }
}
