package game.terrain;

import libs.engine.Ground;
import libs.engine.Location;
import game.items.Fruit;
import game.main.Util;

import java.util.ArrayList;

/**
 * Class that represents a Bush that can grow out in the wild.
 */
public class Bush extends Ground {
    /**
     * Stores a Fruit within the Bush
     */
    private Fruit fruit;

    /**
     * Stores all the Fruits currently grown by Bush
     */
    private static ArrayList<Fruit> fruitArrayList = new ArrayList<>();

    /**
     * Constructor
     */
    public Bush() {
        super('b');
    }

    /**
     * Gives a chance for a Bush to grow a Fruit based on required probability
     * @param location The location of the Ground
     */
    @Override
    public void tick(Location location) {
        super.tick(location);

        // 10% chance of growing fruit
        if (Util.eventSuccess(1, 10)) {
            fruit = new Fruit();
            fruit.setHabitat("Bush");
//            location.addItem(fruit);
            fruitArrayList.add(fruit);
            displayChar = 'B';
        }
    }

    /**
     * Returns the ArrayList containing the fruits on the bush (if any)
     *
     * @return ArrayList containing the fruits in the bush
     */
    public ArrayList<Fruit> getFruitArrayList() {
        return fruitArrayList;
    }


    /**
     * Method to pick a fruit from the bush and returns it
     *
     * @return a fruit from the bush
     */
    public Fruit pickFruitFromBush() {
        Fruit pickedFruit = fruitArrayList.get(0);
        fruitArrayList.remove(0);
        return pickedFruit;
    }

}
