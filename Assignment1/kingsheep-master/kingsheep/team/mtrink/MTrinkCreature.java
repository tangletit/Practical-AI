package kingsheep.team.mtrink;

import kingsheep.Creature;
import kingsheep.Simulator;
import kingsheep.Type;

import java.util.*;



public abstract class MTrinkCreature extends Creature {

    private Type map[][];
    private Queue<Square> movementQueue;
    private Queue<Square> visitedSquares;

    Type otherWolf;
    Type otherSheep;
    Type myWolf;
    Type mySheep;
    String myWolfID;
    Map<Type, Integer> valueMap;
    Map<Move, Integer> alignXMap;
    Map<Move, Integer> alignYMap;

    public MTrinkCreature(Type type, Simulator parent, int playerID, int x, int y) {
        super(type, parent, playerID, x, y);
        movementQueue = new PriorityQueue<Square>(new MyComparator());
        visitedSquares = new LinkedList<Square>();
        myWolfID = "WOLF" + this.getPlayerId();
        setupVariables(myWolfID);
        setupValueMap();
        setupAlignXMap();
        setupAlignYMap();
    }

    private void setupAlignXMap() {
        alignXMap = new HashMap<>();
        alignXMap.put(Move.RIGHT, 1);
        alignXMap.put(Move.LEFT, -1);
        alignXMap.put(Move.UP, 0);
        alignXMap.put(Move.DOWN, 0);
    }

    private void setupAlignYMap() {
        alignYMap = new HashMap<>();
        alignYMap.put(Move.RIGHT, 0);
        alignYMap.put(Move.LEFT, 0);
        alignYMap.put(Move.UP, -1);
        alignYMap.put(Move.DOWN, 1);
    }

    private void setupValueMap() {
        valueMap = new HashMap<>();
        valueMap.put(Type.WOLF2, -2);
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

        Square threat  = find(Type.WOLF2);
        int distance = distance(root, threat);

        if(distance < 4) {
            stepAway(root, threat);
        }else {
            tryToMove2(x, y-1, 0, root, Move.UP);
            tryToMove2(x-1, y, 0, root, Move.LEFT);
            tryToMove2(x+1, y, 0, root, Move.RIGHT);
            tryToMove2(x, y + 1, 0, root, Move.DOWN);
        }

        if(!movementQueue.isEmpty()) {
            //check if field is empty and if we find a better move through firstdepthsearch
            if (movementQueue.element().type.equals(Type.EMPTY)) {
                Queue<Square> food = findFood(root);
                if (!food.isEmpty()) {
                    Square s = nearest(food);
                    suggestNextMove(root, s);
                }
            }

            Move move = movementQueue.poll().move;
            movementQueue.clear();
            return move;
        }
        return Move.WAIT;
    }

    protected Move runAwayOrTrap(Type map[][], Type threatType) {
        this.map = map;
        Square root = new Square(x, y, map[y][x], 0, null, null);
        Square threat  = find(threatType);
        int distance = distance(root, threat);

        if(distance < 4) {
            stepAway(root, threat);
        }else{
            //trap
            Square s = findOtherSheep(root, Type.SHEEP2);
            suggestNextMove(root, s);
        }

        if(!movementQueue.isEmpty()) {
            Move move = movementQueue.poll().move;
            movementQueue.clear();
            return move;
        }

        return Move.WAIT;
    }

    private int distance(Square root, Square target) {
        return Math.abs(root.x - target.x) + Math.abs(root.y - target.y);
    }

    protected Square find(Type type) {
        for(int i=0;i < map.length; i++) {
            for(int j=0; j < map[i].length; j++) {
                if(map[i][j] == type) {
                    return new Square(j, i, type, valueMap.get(type), null, null);
                }
            }
        }
        return null;
    }

    protected boolean anyFood(Type map[][]) {
        this.map = map;
        Square root = new Square(x, y, map[y][x], 0, null, null);
        Queue<Square> food = findFood(root);
        return food.isEmpty() ? false : true;
    }

    private void tryStrategy(Square root, Move m1,  Move m2, Move m3, Move m4){
        int alignedX = x + alignXMap.get(m1);
        int alignedY = y + alignYMap.get(m1);
        tryToMove2(alignedX, alignedY, 40, root, m1);

        alignedX = x + alignXMap.get(m2);
        alignedY = y + alignYMap.get(m2);
        tryToMove2(alignedX, alignedY, 30, root, m2);

        alignedX = x + alignXMap.get(m3);
        alignedY = y + alignYMap.get(m3);
        tryToMove2(alignedX, alignedY, 20, root, m3);

        alignedX = x + alignXMap.get(m4);
        alignedY = y + alignYMap.get(m4);
        tryToMove2(alignedX, alignedY, 10, root, m4);
    }


    private void suggestNextMove(Square root, Square s) {
        if(s != null) {
            //s is on same y but right from me
            if(s.y == y && s.x > x) {
                tryStrategy(root, Move.RIGHT, Move.UP, Move.DOWN, Move.LEFT);
            }else if(s.y == y && s.x < x) {
                //s is on same y but left from me
                tryStrategy(root, Move.LEFT, Move.UP, Move.DOWN, Move.RIGHT);
            }else if(s.y < y && s.x == x){
                //s is on same x but above me, so try to go up
                tryStrategy(root, Move.UP, Move.LEFT, Move.RIGHT, Move.DOWN);
            }else if(s.y > y && s.x == x) {
                //s is on same x but below me, so try to go down
                tryStrategy(root, Move.DOWN, Move.LEFT, Move.RIGHT, Move.UP);
            }else if(s.y > y && s.x > x) {
                //s is right and below me, try to go down or right
                tryStrategy(root, Move.DOWN, Move.RIGHT, Move.UP, Move.LEFT);
            }else if(s.y > y && s.x < x) {
                //s is left and below me, try to go down or left
                tryStrategy(root, Move.DOWN, Move.LEFT, Move.UP, Move.RIGHT);
            }else if(s.y < y && s.x < x) {
                //s is left and above me, try to go up or left
                tryStrategy(root, Move.UP, Move.LEFT, Move.DOWN, Move.RIGHT);
            }else if(s.y > y && s.x < x) {
                //s is left and below me, try to go down or left
                tryStrategy(root, Move.DOWN, Move.LEFT, Move.UP, Move.RIGHT);
            }else if(s.y < y && s.x > x) {
                //s is right and above me, try to go up or right
                tryStrategy(root, Move.UP, Move.RIGHT, Move.DOWN, Move.LEFT);
            }

        }
    }

    private void stepAway(Square root, Square s) {
        if(s != null) {
            //s is on same y but right from me
            if(s.y == y && s.x > x) {
                tryStrategy(root, Move.LEFT, Move.UP, Move.DOWN, Move.RIGHT);
            }else if(s.y == y && s.x < x) {
                //s is on same y but left from me
                tryStrategy(root, Move.RIGHT, Move.UP, Move.DOWN, Move.LEFT);
            }else if(s.y < y && s.x == x){
                //s is on same x but above me, so try to go up
                tryStrategy(root, Move.DOWN, Move.LEFT, Move.RIGHT, Move.UP);
            }else if(s.y > y && s.x == x) {
                //s is on same x but below me, so try to go down
                tryStrategy(root, Move.UP, Move.LEFT, Move.RIGHT, Move.DOWN);
            }else if(s.y > y && s.x > x) {
                //s is right and below me, try to go down or right
                tryStrategy(root, Move.UP, Move.LEFT, Move.DOWN, Move.RIGHT);
            }else if(s.y > y && s.x < x) {
                //s is left and below me, try to go down or left
                tryStrategy(root, Move.UP, Move.RIGHT, Move.DOWN, Move.LEFT);
            }else if(s.y < y && s.x < x) {
                //s is left and above me, try to go up or left
                tryStrategy(root, Move.DOWN, Move.RIGHT, Move.UP, Move.LEFT);
            }else if(s.y > y && s.x < x) {
                //s is left and below me, try to go down or left
                tryStrategy(root, Move.UP, Move.RIGHT, Move.DOWN, Move.LEFT);
            }else if(s.y < y && s.x > x) {
                //s is right and above me, try to go up or right
                tryStrategy(root, Move.DOWN, Move.LEFT, Move.UP, Move.RIGHT);
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

        if(!movementQueue.isEmpty()) {
//            if(alreadyVisited(movementQueue.element())) {
//                movementQueue.poll();
//            }else{
//                visitedSquares.add(movementQueue.element());
                Move move = movementQueue.poll().move;
                movementQueue.clear();
                return move;
//            }
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
        if(map[y][x] == Type.SHEEP1) {
            if(     field.type != Type.FENCE &&
                    field.type != Type.WOLF2 &&
                    field.type != Type.SHEEP2 &&
                    field.type != Type.WOLF1) {

                if(field.value == 0) {
                    field.setValue(valueMap.get(field.type));
                }
                movementQueue.add(field);
            }
        }else{ //in wolf case
            if(     field.type != Type.FENCE &&
                    field.type != Type.GRASS &&
                    field.type != Type.RHUBARB &&
                    field.type != Type.SHEEP1) {

                if(field.value == 0) {
                    field.setValue(valueMap.get(field.type));
                }
                movementQueue.add(field);
            }

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
