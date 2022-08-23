package game.items;

import libs.engine.WeaponItem;

/**
 * Class for the LaserGun weapon
 */
public class LaserGun extends WeaponItem {
    /**
     * Cost of the Laser Gun in EcoPoints
     */
    private static int cost;

    /**
     * Constructor.
     */
    public LaserGun() {
        super("Laser Gun", '>', 200, "shoots");
        this.cost = 500;
    }
}
