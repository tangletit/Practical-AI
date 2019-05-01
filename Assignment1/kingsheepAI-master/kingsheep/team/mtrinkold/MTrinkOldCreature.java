package kingsheep.team.mtrinkold;

import kingsheep.Creature;
import kingsheep.Simulator;
import kingsheep.Type;

import java.util.*;

/**
 * Created by kama on 04.03.16.
 */
public abstract class MTrinkOldCreature extends Creature {

    private Type map[][];
    private Queue<Square> movementQueue;
    private Queue<Square> visitedSquares;

    Type otherWolf;
    Type otherSheep;
    Type myWolf;
    Type mySheep;
    String myWolfID;
    Map<Type, Integer> valueMap;

    public MTrinkOldCreature(Type type, Simulator parent, int playerID, int x, int y) {
        super(type, parent, playerID, x, y);
        movementQueue = new PriorityQueue<Square>(new MyComparator());
        visitedSquares = new LinkedList<Square>();
        myWolfID = "WOLF" + this.getPlayerId();
        setupVariables(myWolfID);
        setupValueMap();
    }

    private void setupValueMap() {
        valueMap = new HashMap<>();
        valueMap.put(Type.EMPTY, 0);
        valueMap.put(Type.GRASS, 1);
        valueMap.put(Type.RHUBARB, 5);
    }

    private void setupVariables(String myWolfID) {
        if (myWolfID.equals("WOLF1")) {
            otherWolf = Type.WOLF2;
            otherSheep = Type.SHEEP2;
            myWolf = Type.WOLF1;
            mySheep = Type.SHEEP1;
        } else {
            otherWolf = Type.WOLF1;
            otherSheep = Type.SHEEP1;
            myWolf = Type.WOLF2;
            mySheep = Type.SHEEP2;
        }
    }
    public String getNickname(){
        return "montron";
    }

    public int getPlayerId() {
        return playerID;
    }

    public int getX() {
        return x;
    }

    public int getY() {
        return y;
    }

    protected Move doAction(Type map[][]){
        this.map = map;
        Square root = new Square(x, y, map[y][x], 0, null, null);
        visitedSquares.add(root);

        tryToMove2(x, y-1, 0, root, Move.UP);
        tryToMove2(x-1, y, 0, root, Move.LEFT);
        tryToMove2(x+1, y, 0, root, Move.RIGHT);
        tryToMove2(x, y + 1, 0, root, Move.DOWN);

        while(!movementQueue.isEmpty()) {
            if(alreadyVisited(movementQueue.element())) {
                movementQueue.poll();
            }else{
                //check if field is empty and if we find a better move through firstdepthsearch
                if(movementQueue.element().type.equals(Type.EMPTY)) {
                 Queue<Square> food = findFood(root);
                    if(!food.isEmpty()) {
                        Square s = nearest(food);
                        suggestNextMove(root, s);
                    }
                }
                visitedSquares.add(movementQueue.element());
                Move move = movementQueue.poll().move;
                movementQueue.clear();
                return move;
            }
        }

        return Move.WAIT;
    }

    private void suggestNextMove(Square root, Square s) {
        if(s != null) {
            //s is on same y but right from me
            if(s.y == y && s.x > x) {
                tryToMove2(x+1, y, 40, root, Move.RIGHT);
                tryToMove2(x, y-1, 30, root, Move.UP);
                tryToMove2(x, y + 1, 20, root, Move.DOWN);
                tryToMove2(x-1, y, 10, root, Move.LEFT);
            }else if(s.y == y && s.x < x) {
                //s is on same y but left from me
                tryToMove2(x-1, y, 40, root, Move.LEFT);
                tryToMove2(x, y-1, 30, root, Move.UP);
                tryToMove2(x, y + 1, 20, root, Move.DOWN);
                tryToMove2(x+1, y, 10, root, Move.RIGHT);
            }else if(s.y < y && s.x == x){
                //s is on same x but above me, so try to go up
                tryToMove2(x, y-1, 40, root, Move.UP);
                tryToMove2(x-1, y, 30, root, Move.LEFT);
                tryToMove2(x+1, y, 20, root, Move.RIGHT);
                tryToMove2(x, y + 1, 10, root, Move.DOWN);
            }else if(s.y > y && s.x == x) {
                //s is on same x but below me, so try to go down
                tryToMove2(x, y + 1, 40, root, Move.DOWN);
                tryToMove2(x - 1, y, 30, root, Move.LEFT);
                tryToMove2(x + 1, y, 20, root, Move.RIGHT);
                tryToMove2(x, y - 1, 10, root, Move.UP);
            }else if(s.y > y && s.x > x) {
                //s is right and below me, try to go down or right
                tryToMove2(x, y + 1, 40, root, Move.DOWN);
                tryToMove2(x + 1, y, 30, root, Move.RIGHT);
                tryToMove2(x - 1, y, 20, root, Move.LEFT);
                tryToMove2(x, y - 1, 10, root, Move.UP);
            }else if(s.y > y && s.x < x) {
                //s is left and below me, try to go down or left
                tryToMove2(x, y + 1, 40, root, Move.DOWN);
                tryToMove2(x - 1, y, 30, root, Move.LEFT);
                tryToMove2(x + 1, y, 20, root, Move.RIGHT);
                tryToMove2(x, y - 1, 10, root, Move.UP);
            }else if(s.y < y && s.x < x) {
                //s is left and above me, try to go up or left
                tryToMove2(x, y - 1, 40, root, Move.UP);
                tryToMove2(x - 1, y, 30, root, Move.LEFT);
                tryToMove2(x, y + 1, 20, root, Move.DOWN);
                tryToMove2(x + 1, y, 10, root, Move.RIGHT);
            }else if(s.y > y && s.x < x) {
                //s is left and below me, try to go down or left
                tryToMove2(x, y - 1, 40, root, Move.UP);
                tryToMove2(x - 1, y, 30, root, Move.LEFT);
                tryToMove2(x, y + 1, 20, root, Move.DOWN);
                tryToMove2(x + 1, y, 10, root, Move.RIGHT);
            }else if(s.y < y && s.x > x) {
                //s is right and above me, try to go up or right
                tryToMove2(x, y - 1, 40, root, Move.UP);
                tryToMove2(x + 1, y, 30, root, Move.RIGHT);
                tryToMove2(x - 1, y, 20, root, Move.LEFT);
                tryToMove2(x, y + 1, 10, root, Move.DOWN);
            }

            }
    }

    private void tryToMove2(int x, int y, int value, Square root, Move move) {
        try{
            addToQueueIfFieldIsFree(new Square(x,y,map[y][x], value, root, move));

        }catch (ArrayIndexOutOfBoundsException e){
            //continue
        }catch (NullPointerException e){
            e.fillInStackTrace();
        }
    }


    private Square nearest(Queue<Square> s) {
        int minDistanceX = map[0].length;
        int minDistanceY = map.length;
        Square nearestSquare = null;

        for(Square sq : s) {
            if(sq.x < minDistanceX && sq.y < minDistanceY) {
                nearestSquare = sq;
            }
        }

        return nearestSquare;
    }


    private Queue<Square> findFood(Square root) {
        Queue<Square> nearestSquare = new LinkedList<Square>();

        //search from me away to the left
        for(int i=root.y; i >= 0; --i) {
            for(int j=root.x; j >=0; --j) {
                if(map[i][j] == Type.RHUBARB || map[i][j] == Type.GRASS) {
                    nearestSquare.add(new Square(j, i, map[i][j], valueMap.get(map[i][j]), null,null));
                }
            }
            //search from me away to the right
            for(int j=root.x; j < map[i].length; j++) {
                if(map[i][j] == Type.RHUBARB || map[i][j] == Type.GRASS) {
                    nearestSquare.add(new Square(j, i, map[i][j], valueMap.get(map[i][j]), null,null));
                }
            }
        }

        //search from me away to the right
        for(int i=root.y; i < map.length; ++i) {
            for(int j=root.x; j >=0; --j) {
                if(map[i][j] == Type.RHUBARB || map[i][j] == Type.GRASS) {
                    nearestSquare.add(new Square(j, i, map[i][j], valueMap.get(map[i][j]), null,null));
                }
            }
            //search from me away to the right
            for(int j=root.x; j < map[i].length; j++) {
                if(map[i][j] == Type.RHUBARB || map[i][j] == Type.GRASS) {
                    nearestSquare.add(new Square(j, i, map[i][j], valueMap.get(map[i][j]), null,null));
                }
            }
        }

        return nearestSquare;

    }

    private Square findOtherSheep(Square root, Type targetType) {
        for(int i=0;i < map.length; i++) {
            for(int j=0; j < map[i].length; j++) {
                if(map[i][j] == targetType) {
                    return new Square(j, i, targetType, 100, null, null);
                }
            }
        }
        return null;
    }

    public Move doWolfAction(Type[][] map) {
        this.map = map;
        Square root = new Square(x, y, map[y][x], 0, null, null);
        visitedSquares.add(root);

        Square s = findOtherSheep(root, Type.SHEEP2);
        suggestNextMove(root, s);

        while(!movementQueue.isEmpty()) {
            if(alreadyVisited(movementQueue.element())) {
                movementQueue.poll();
            }else{
                visitedSquares.add(movementQueue.element());
                Move move = movementQueue.poll().move;
                movementQueue.clear();
                return move;
            }
        }

        return Move.WAIT;

    }

    private boolean alreadyVisited(Square target) {

        for(Square s : visitedSquares) {
            if(s.x == target.x && s.y == target.y) {
                return true;
            }
        }

        return false;
    }

    private void addToQueueIfFieldIsFree(Square field) {
        if(     field.type != Type.FENCE &&
                field.type != Type.WOLF2 &&
                field.type != Type.SHEEP2) {

                if(field.value == 0) {
                    field.setValue(valueMap.get(field.type));
                }
                movementQueue.add(field);
        }

    }


    private class Square {
        int x;
        int y;
        Type type;
        int value;
        boolean visited;
        Square parent;
        Move move;

        public Square(int x, int y, Type type, int value, Square parent, Move move){
            this.x = x;
            this.y = y;
            this.type = type;
            this.value = value;
            this.visited = false;
            this.parent = parent;
            this.move = move;
        }

        public void setValue(int val) {
            this.value = val;
        }

    }

    private class MyComparator implements Comparator<Square> {
        @Override
        public int compare(Square s1, Square s2) {
            return  Integer.compare(s2.value, s1.value);
        }
    }
}
