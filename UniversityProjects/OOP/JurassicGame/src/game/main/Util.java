package game.main;

import java.util.Random;

/**
 * This class stores important methods that might be used in many other classes
 */
public class Util {
    /**
     * Given probability in form of number of success in number of trials, uses RNG to simulate a trial of the event
     * and returns a boolean depending on outcome of trial event.
     * @param successes probability = p/n, success = p
     * @param trials probability = p/n, success = n
     * @return true if event succeeds, false if event fails
     */
    public static boolean eventSuccess(int successes, int trials) {
        Random r = new Random();
        int number = r.nextInt(trials) + 1;
        if (number <= successes) {
            return true;
        } else {
            return false;
        }
    }
}
