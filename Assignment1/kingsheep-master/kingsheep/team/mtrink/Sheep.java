package kingsheep.team.mtrink;

import kingsheep.Simulator;
import kingsheep.Type;

public class Sheep extends MTrinkCreature {

    public Sheep(Type type, Simulator parent, int playerID, int x, int y) {
        super(type, parent, playerID, x, y);
    }


    protected void think(Type map[][]) {
        move =  doAction(map);

        if(!anyFood(map)) {
            move = runAwayOrTrap(map, Type.WOLF2);
        }
    }
}
