from config import *
import heapq


def get_class_name():
    return 'myPlayer'


class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]


class myPlayer():
    """Greedy Kingsheep player. Sheep flee from the wolf or go to the nearest food
    in a straight line, wolves go to sheep in a straight line."""

    def __init__(self):
        self.name = "myPlayer"
        self.uzh_shortname = "yuezzh"

    def get_player_position(self, figure, field):
        x = [x for x in field if figure in x][0]
        return (field.index(x), x.index(figure))

    # defs for sheep
    def food_present(self, field):
        food_present = False

        for line in field:
            for item in line:
                if item == CELL_RHUBARB or item == CELL_GRASS:
                    food_present = True
                    break
        return food_present


    def heuristic(self,a,b):
        (x1, y1) = a
        (x2, y2) = b
        return abs(x1 - x2) + abs(y1 - y2)

# 找到吃最近的草的最优路径，start就是羊的当前位置，可通过position来获得，goal来自于closet-goal的方程


    def to_eat(self, figure, start, goal, field):
        food = PriorityQueue()
        food.put(start, 0)
        came_from = {}
        cost_so_far = {}
        all_cost = {}
        came_from[start] = None
        cost_so_far[start] = 0
        all_cost[start] = abs(goal[0] - start[0]) + abs(goal[1] - start[1])

        # goal_x = goal[1]
        # goal_y = goal[0]
        while not food.empty():
                current = food.get()

                if current == goal:
                    break

                for next in self.get_neighbors_position(figure, current, field):
                   # print(next)
                    new_cost = cost_so_far[current] + self.cost(figure, current, next, field)
                    if next not in cost_so_far or new_cost < cost_so_far[next]:
                        cost_so_far[next] = new_cost
                        priority = new_cost + self.heuristic(goal, next)
                        all_cost[next] = priority
                        food.put(next, priority)
                        came_from[next] = current


        now = goal
        path = []
        if now not in came_from.keys():
            return MOVE_NONE
        else:
            while now != start:
                path.append(now)
                now = came_from[now]
            next_move = path[-1]
            if next_move[0] == start[0]:
                if next_move[1] > start[1]:
                    return MOVE_RIGHT
                else:
                    return MOVE_LEFT
            if next_move[1] == start[1]:
                if next_move[0] > start[0]:
                    return MOVE_DOWN
                else:
                    return MOVE_UP

    # 获取邻居的位置
    def get_neighbors_position(self,figure,node,field): # 获取邻居的位置
        (x,y)=node
        res = [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]
        results = []
        for item in res:
            (i, j) = item
            if self.valid_move(figure,i,j,field):
                results.append(item)
        return results



# 获取两个点之间的权重，所以现在需要考虑两个点之间的权重是由什么决定的
    def cost(self, figure, node, next_node, field):
        empty = self.which_food(CELL_EMPTY,field)
        grass = self.which_food(CELL_GRASS,field)
        barb = self.which_food(CELL_RHUBARB,field)

        if figure == CELL_SHEEP_1:
            sheep_1 = empty + grass + barb +[self.get_player_position(CELL_SHEEP_1,field)]+[self.get_player_position(CELL_WOLF_2,field)]
            dis_1 =[5]*len(empty)+[4]*len(grass)+[0]*len(barb)+[5]+[10]
            weight_s1 = dict(zip(sheep_1,dis_1))

            return weight_s1.get(next_node)

        elif figure == CELL_SHEEP_2:
            sheep_2 = empty + grass + barb +[self.get_player_position(CELL_SHEEP_2,field)]+[self.get_player_position(CELL_WOLF_1,field)]
            dis_2 =[5]*len(empty)+[4]*len(grass)+[0]*len(barb)+[5]+[10]
            weight_s2 = dict(zip(sheep_2,dis_2))

            return weight_s2.get(next_node)

        elif figure == CELL_WOLF_2:
            wolf_2 = empty + grass + barb +[self.get_player_position(CELL_WOLF_2,field)]+[self.get_player_position(CELL_SHEEP_1,field)]
            dis_2 =[5]*len(empty)+[4]*len(grass)+[7]*len(barb)+[20]+[10]+[20]
            weight_w1 = dict(zip(wolf_2,dis_2))

            return weight_w1.get(next_node)

        elif figure == CELL_WOLF_1:
            wolf_1 = empty + grass + barb +[self.get_player_position(CELL_WOLF_1,field)]+[self.get_player_position(CELL_SHEEP_2,field)]
            dis_1 =[5]*len(empty)+[4]*len(grass)+[7]*len(barb)+[20]+[10]+[20]
            weight_w2 = dict(zip(wolf_1,dis_1))

            return weight_w2.get(next_node)

# 判断每一个点到底是草还是空还是仙人掌
    def which_food(self,food,field):
        road = []
        grass = []
        rhu = []

        y_position = 0
        for line in field:
            x_position = 0
            for item in line:
                if item == CELL_RHUBARB:
                    rhu.append((y_position,x_position))
                if item == CELL_GRASS:
                    grass.append((y_position,x_position))
                if item == CELL_EMPTY:
                    road.append((y_position,x_position))
                x_position += 1
            y_position += 1
        if food == CELL_GRASS:
            return grass
        if food == CELL_RHUBARB:
            return rhu
        if food == CELL_EMPTY:
            return road



    def closest_goal(self,player_number,field):
        possible_goals = []

        if player_number == 1:
            sheep_position = self.get_player_position(CELL_SHEEP_1,field)
        else:
            sheep_position = self.get_player_position(CELL_SHEEP_2,field)

        # make list of possible goals

        y_position = 0
        for line in field:
            x_position = 0
            for item in line:
                if item == CELL_RHUBARB or item == CELL_GRASS:
                    possible_goals.append((y_position,x_position))
                x_position += 1
            y_position += 1

        # determine closest item and return
        distance = 1000
        for possible_goal in possible_goals:
            if (abs(possible_goal[0]-sheep_position[0])+abs(possible_goal[1]-sheep_position[1])) < distance:
                distance = abs(possible_goal[0]-sheep_position[0])+abs(possible_goal[1]-sheep_position[1])
                final_goal = (possible_goal)

        return final_goal



    def wolf_close(self,player_number,field):
        if player_number == 1:
            sheep_position = self.get_player_position(CELL_SHEEP_1,field)
            wolf_position = self.get_player_position(CELL_WOLF_2,field)
        else:
            sheep_position = self.get_player_position(CELL_SHEEP_2,field)
            wolf_position = self.get_player_position(CELL_WOLF_1,field)

        if (abs(sheep_position[0]-wolf_position[0]) <= 2 and abs(sheep_position[1]-wolf_position[1]) <= 2):
            # print('wolf is close')
            return True
        return False

    def valid_move(self, figure, x_new, y_new, field):
         # Neither the sheep nor the wolf, can step on a square outside the map. Imagine the map is surrounded by fences.
        if x_new > FIELD_HEIGHT - 1:
            return False
        elif x_new < 0:
            return False
        elif y_new > FIELD_WIDTH -1:
            return False
        elif y_new < 0:
            return False

        # Neither the sheep nor the wolf, can enter a square with a fence on.
        if field[x_new][y_new] == CELL_FENCE:
            return False

        # Wolfs can not step on squares occupied by the opponents wolf (wolfs block each other).
        # Wolfs can not step on squares occupied by the sheep of the same player .
        if figure == CELL_WOLF_1:
            if field[x_new][y_new] == CELL_WOLF_2:
                return False
            elif field[x_new][y_new] == CELL_SHEEP_1:
                return False
        elif figure == CELL_WOLF_2:
            if field[x_new][y_new] == CELL_WOLF_1:
                return False
            elif field[x_new][y_new] == CELL_SHEEP_2:
                return False


        # Sheep can not step on squares occupied by the wolf of the same player.
        # Sheep can not step on squares occupied by the opposite sheep.
        if figure == CELL_SHEEP_1:
            if field[x_new][y_new] == CELL_SHEEP_2 or \
                field[x_new][y_new] == CELL_WOLF_1:
                return False
        elif figure == CELL_SHEEP_2:
            if field[x_new][y_new] == CELL_SHEEP_1 or \
                    field[x_new][y_new] == CELL_WOLF_2:
                return False

        return True

    def run_from_wolf(self,player_number,field):
        if player_number == 1:
            sheep_position = self.get_player_position(CELL_SHEEP_1,field)
            wolf_position = self.get_player_position(CELL_WOLF_2,field)
            sheep = CELL_SHEEP_1
        else:
            sheep_position = self.get_player_position(CELL_SHEEP_2,field)
            wolf_position = self.get_player_position(CELL_WOLF_1,field)
            sheep = CELL_SHEEP_2

        distance_x = sheep_position[1] - wolf_position[1]
        abs_distance_x = abs(sheep_position[1] - wolf_position[1])
        distance_y = sheep_position[0] - wolf_position[0]
        abs_distance_y = abs(sheep_position[0] - wolf_position[0])

        # print('player_number %i' %player_number)
        # print('running from wolf')
        # if the wolf is close vertically
        if abs_distance_y == 1 and distance_x == 0:
            # print('wolf is close vertically')
            # if it's above the sheep, move down if possible
            if distance_y > 0:
                if self.valid_move(sheep,sheep_position[0]+1,sheep_position[1], field):
                    return MOVE_DOWN
            else: #it's below the sheep, move up if possible
                if self.valid_move(sheep,sheep_position[0]-1,sheep_position[1], field):
                    return MOVE_UP
            # if this is not possible, flee to the right or left
            if self.valid_move(sheep,sheep_position[0],sheep_position[1]+1, field):
                return MOVE_RIGHT
            elif self.valid_move(sheep,sheep_position[0],sheep_position[1]-1, field):
                return MOVE_LEFT
            else: #nowhere to go
                return MOVE_NONE

        # else if the wolf is close horizontally
        elif abs_distance_x == 1 and distance_y == 0:
            # print('wolf is close horizontally')
            # if it's to the left, move to the right if possible
            if distance_x > 0:
                if self.valid_move(sheep,sheep_position[0],sheep_position[1]-1, field):
                    return MOVE_RIGHT
            else: #it's to the right, move left if possible
                if self.valid_move(sheep,sheep_position[0],sheep_position[1]+1, field):
                    return MOVE_RIGHT
            # if this is not possible, flee up or down
            if self.valid_move(sheep,sheep_position[0]-1,sheep_position[1], field):
                return MOVE_UP
            elif self.valid_move(sheep,sheep_position[0]+1,sheep_position[1], field):
                return MOVE_DOWN
            else: #nowhere to go
                return MOVE_NONE

        elif abs_distance_x == 1 and abs_distance_y == 1:
            # print('wolf is in my surroundings')
            # wolf is left and up
            if distance_x > 0 and distance_y > 0:
                # move right or down
                if self.valid_move(sheep,sheep_position[0],sheep_position[1]+1, field):
                    return MOVE_RIGHT
                else:
                    return MOVE_DOWN
            # wolf is left and down
            if distance_x > 0 and distance_y < 0:
                # move right or up
                if self.valid_move(sheep,sheep_position[0],sheep_position[1]+1, field):
                    return MOVE_RIGHT
                else:
                    return MOVE_UP
            # wolf is right and up
            if distance_x < 0 and distance_y > 0:
                # move left or down
                if self.valid_move(sheep,sheep_position[0],sheep_position[1]-1, field):
                    return MOVE_LEFT
                else:
                    return MOVE_DOWN
            # wolf is right and down
            if distance_x < 0 and distance_y < 0:
                # move left and up
                if self.valid_move(sheep,sheep_position[0],sheep_position[1]-1, field):
                    return MOVE_LEFT
                else:
                    return MOVE_UP


        else: #this method was wrongly called
            return MOVE_NONE

    def move_sheep(self, player_number, field):
        if player_number == 1:
            figure = CELL_SHEEP_1
        else:
            figure = CELL_SHEEP_2

        if self.wolf_close(player_number, field):
            # print('wolf close move')
            return self.run_from_wolf(player_number, field)
        elif self.food_present(field):
            # 这里需要改，用astar去吃草
            return self.to_eat(figure,self.get_player_position(figure,field), self.closest_goal(player_number, field), field)
        else:
            return MOVE_NONE

    # defs for wolf
    # 贪心算法里面，狼吃羊的算法也就是贪心算法，但是用了astar之后，最好把狼吃羊的算法也改成astar
    def move_wolf(self,player_number,field):
        if player_number == 1:
            figure = CELL_WOLF_1
            sheep_position = self.get_player_position(CELL_SHEEP_2,field)
            return self.to_eat(figure,self.get_player_position(figure,field),sheep_position,field)
        else:
            figure = CELL_WOLF_2
            sheep_position = self.get_player_position(CELL_SHEEP_1,field)
            return self.to_eat(figure,self.get_player_position(figure,field),sheep_position,field)
