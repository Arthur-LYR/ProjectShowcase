package game.terrain;

/**
 * Interface for Lakes and Dinosaurs to inherit in which the appropriate action can be taken when it rains
 */
public interface RainAffected {
    /**
     * Method which contains actions the subclass will perform
     */
    void rainAction();
}
