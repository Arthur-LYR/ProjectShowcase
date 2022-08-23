package game.dinosaurs.general;

import java.util.Random;

/***
 * The gender of the dinosaurs
 */
public enum Gender {
    MALE,
    FEMALE;

    /***
     * Method to randomly return a gender for the dinosaur
     *
     * @return the gender of the dinosaur
     */
    public static Gender randomGender() {
        return Gender.values() [new Random().nextInt(Gender.values().length)];
    }
}
