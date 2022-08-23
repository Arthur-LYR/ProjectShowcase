package libs.demo.conwayslife;

import java.util.List;

import libs.engine.GameMap;
import libs.engine.GroundFactory;
import libs.engine.Location;

public class ConwayGameMap extends GameMap {

	public ConwayGameMap(GroundFactory groundFactory, List<String> lines) {
		super(groundFactory, lines);
	}
	
	@Override
	protected Location makeNewLocation(int x, int y) {
		return new ConwayLocation(this, x, y);
	}
}
