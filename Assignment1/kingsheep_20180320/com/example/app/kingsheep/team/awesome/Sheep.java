package com.example.app.kingsheep.team.awesome;

import com.example.app.kingsheep.*;

public class Sheep extends AwesomeCreature {

    public Sheep(Type type, Simulator parent, int playerID, int x, int y) {
        super(type, parent, playerID, x, y);
    }

    protected void think(Type map[][]) {

        int t = (int)(Math.random() * 4);

        switch (t) {
        case 0:
            move = Move.UP;
            break;
        case 1:
            move = Move.DOWN;
            break;
        case 2:
            move = Move.LEFT;
            break;
        case 3:
            move = Move.RIGHT;
            break;
        default:
            move = Move.WAIT;
            break;
        }
    }
}