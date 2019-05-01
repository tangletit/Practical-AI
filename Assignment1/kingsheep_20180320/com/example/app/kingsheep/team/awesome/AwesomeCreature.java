package com.example.app.kingsheep.team.awesome;

import com.example.app.kingsheep.Creature;
import com.example.app.kingsheep.Simulator;
import com.example.app.kingsheep.Type;

/**
 * Created by kama on 04.03.16.
 */
public abstract class AwesomeCreature extends Creature {

    public AwesomeCreature(Type type, Simulator parent, int playerID, int x, int y) {
        super(type, parent, playerID, x, y);
    }

    public String getNickname(){
        //TODO change this to any nickname you like. This should not be your uzh_shortname. That way you can stay anonymous on the ranking list.
        return "my_nickname";
    }
}
