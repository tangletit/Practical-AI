package kingsheep.team.mtrink;

import kingsheep.Simulator;
import kingsheep.Type;

public class Wolf extends MTrinkCreature {

    public Wolf(Type type, Simulator parent, int playerID, int x, int y) {
        super(type, parent, playerID, x, y);
    }

    protected void think(Type map[][]) {

        move =  doWolfAction(map);

    }
}
