package game.terrain;

import libs.engine.Ground;
import libs.engine.Location;
import game.main.Util;

import java.util.ArrayList;

/**
 * A class that represents bare dirt.
 */
public class Dirt extends Ground {

	/**
	 * Constructor.
	 */
	public Dirt() {
		super('.');
	}

	/**
	 * Checks the neighbouring squares and grows a Bush following the appropriate probability
	 * @param location The location of the Ground
	 */
	@Override
	public void tick(Location location) {
		super.tick(location);

		// Initialise Variables
		boolean nextToTree = false;
		int bushCount = 0;

		// Get Characters of Neighbouring Tiles
		ArrayList<Character> neighbours = new ArrayList();
		for (int i = -1; i <= 1; i++) {
			for (int j = -1; j <= 1; j++) {
				if (i != 0 && j != 0) {
					try {
						neighbours.add(location.map().at(location.x() + i, location.y() + j).getGround().getDisplayChar());
					} catch (ArrayIndexOutOfBoundsException e) {
						break;
					}
				}
			}
		}

		// Check each neighbour to see if tree present and count number of bushes
		for (int i = 0; i < neighbours.size(); i++) {
			if (neighbours.get(i) == '+' || neighbours.get(i) == 't' || neighbours.get(i) == 'T'
					|| neighbours.get(i) == 'F' || neighbours.get(i) == 'O') {
				nextToTree = true;
			} else if (neighbours.get(i) == 'b' || neighbours.get(i) == 'B') {
				bushCount++;
			}
		}

		// If not next to tree and less than 2 bushes nearby: 1% chance to grow bush
		// Else if not next to tree and 2 or more bushes nearby: 10% chance to grow bush
		if (!nextToTree && bushCount < 2 && Util.eventSuccess(1, 100)) {
			location.setGround(new Bush());
		} else if (!nextToTree && bushCount >= 2 && Util.eventSuccess(1, 10)) {
			location.setGround(new Bush());
		}
	}
}
