from config import *
import heapq

def get_class_name():
    return 'AstarPlayer'

class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]


class AstarPlayer():
    """Greedy Kingsheep player. Sheep flee from the wolf or go to the nearest food
    in a straight line, wolves go to sheep in a straight line."""

    def __init__(self):
        self.name = "Astar Player"
        self.uzh_shortname = "aplayer"

    def get_player_position(self, figure, field):
        x = [x for x in field if figure in x][0]
        return (field.index(x), x.index(figure))

    def heuristic(self,a,b):
        (x1, y1) = a
        (x2, y2) = b
        return abs(x1 - x2) + abs(y1 - y2)

    # defs for sheep
    def food_present(self, field):
        food_present = False

        for line in field:
            for item in line:
                if item == CELL_RHUBARB or item == CELL_GRASS:
                    food_present = True
                    break
        return food_present

    def get_food_position(self,food,field):
        rhu_goals = []
        grass_goals = []
        empty = []
        y_position = 0
        for line in field:
            x_position = 0
            for item in line:
                if item == CELL_RHUBARB:
                    rhu_goals.append((y_position, x_position))
                if item == CELL_GRASS:
                    grass_goals.append((y_position, x_position))
                if item == CELL_EMPTY:
                    empty.append((y_position,x_position))
                x_position += 1
            y_position += 1

        if food == CELL_GRASS:
            return grass_goals
        if food == CELL_RHUBARB:
            return rhu_goals
        if food == CELL_EMPTY:
            return empty

    def valid_move(self, figure, x_new, y_new, field):
        # Neither the sheep nor the wolf, can step on a square outside the map. Imagine the map is surrounded by fences.
        if x_new > FIELD_HEIGHT - 1:
            return False
        elif x_new < 0:
            return False
        elif y_new > FIELD_WIDTH - 1:
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
                            field[x_new][y_new] == CELL_WOLF_1 or field[x_new][y_new] == CELL_WOLF_2 or \
                            field[x_new][y_new] == CELL_SHEEP_2_d:
                return False
        elif figure == CELL_SHEEP_2:
            if field[x_new][y_new] == CELL_SHEEP_1 or \
                            field[x_new][y_new] == CELL_WOLF_2 or field[x_new][y_new] == CELL_WOLF_1 or \
                            field[x_new][y_new] == CELL_SHEEP_1_d:
                return False
        return True

    def neighbors(self,figure, node,field):
        (x,y)=node
        res = [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]
        results = []
        for item in res:
            (a, b) = item
            if self.valid_move(figure,a,b,field):
                results.append(item)
        return results

    def cost(self,figure,node,new_node, field):
        
        empty = self.get_food_position(CELL_EMPTY,field)
        grass = self.get_food_position(CELL_GRASS,field)
        rhu = self.get_food_position(CELL_RHUBARB,field)
        #sur_sheep_1 = self.neighbors(CELL_SHEEP_1, self.get_player_position(CELL_SHEEP_1,field),field)
        #sur_sheep_2 = self.neighbors(CELL_SHEEP_2,self.get_player_position(CELL_SHEEP_2,field),field)
        #sur_wolf_1 = self.neighbors(CELL_WOLF_1,self.get_player_position(CELL_WOLF_1,field),field)
        #sur_wolf_2 = self.neighbors(CELL_WOLF_2,self.get_player_position(CELL_WOLF_1,field),field)
        #empty = list(set(empty).difference(sur_sheep_1).difference(sur_sheep_2).difference(sur_wolf_1).difference(sur_wolf_2))

        if figure == CELL_SHEEP_1:
            for_sheep_1 = empty + grass + rhu + [self.get_player_position(CELL_SHEEP_1,field)] + \
                          [self.get_player_position(CELL_WOLF_2,field)]
            len_sheep_1 = [5]*len(empty) + [4]*len(grass) + [0]*len(rhu) + [5] + [10]
                            #  [10]*(len(sur_sheep_2)+len(sur_wolf_1)+len(sur_wolf_2))
            weights_sheep_1 = dict(zip(for_sheep_1,len_sheep_1))
            return weights_sheep_1.get(new_node)

        elif figure == CELL_SHEEP_2:
            for_sheep_2 = empty + grass + rhu + [self.get_player_position(CELL_SHEEP_2,field)] + \
                          [self.get_player_position(CELL_WOLF_1,field)]
            len_sheep_2 = [5]*len(empty) + [4]*len(grass) + [0]*len(rhu) + [5] + [10]
                          #  [10]*(len(sur_sheep_1)+len(sur_wolf_1)+len(sur_wolf_2))
            weights_sheep_2 = dict(zip(for_sheep_2,len_sheep_2))
            return weights_sheep_2.get(new_node)

        if figure == CELL_WOLF_1:
            for_wolf_1 = empty + grass + rhu + [self.get_player_position(CELL_SHEEP_2,field)] + \
                          [self.get_player_position(figure,field)]
            len_wolf_1 = [5]*len(empty) + [6]*len(grass) + [7]*len(rhu) + [5] + [5] + [5]
            weights_wolf_1 = dict(zip(for_wolf_1,len_wolf_1))
            return weights_wolf_1.get(new_node)

        elif figure == CELL_WOLF_2:
            for_wolf_2 = empty + grass + rhu + [self.get_player_position(figure,field)] + \
                         [self.get_player_position(CELL_SHEEP_1,field)]
            len_wolf_2 = [5]*len(empty) + [6]*len(grass) + [7]*len(rhu)+ [5] + [5] + [5]
            weights_wolf_2 = dict(zip(for_wolf_2,len_wolf_2))
            return weights_wolf_2.get(new_node)

    def closest_goal(self, player_number, field):
        grass = self.get_food_position(CELL_GRASS, field)
        rhu = self.get_food_position(CELL_RHUBARB, field)
        rhu_goals = []
        grass_goals = []

        if player_number == 1:
            figure = CELL_SHEEP_1
            sheep_position = self.get_player_position(figure, field)

        else:
            figure = CELL_SHEEP_2
            sheep_position = self.get_player_position(figure, field)

        for rhu_goal in rhu:
            if self.neighbors(figure, rhu_goal, field):
                rhu_goals.append(rhu_goal)

        for grass_goal in grass:
            if self.neighbors(figure, grass_goal, field):
                grass_goals.append(grass_goal)

        # make list of possible goals
        value_rhu = []
        for rhu_goal in rhu_goals:
            dist = abs(rhu_goal[0] - sheep_position[0]) + abs(rhu_goal[1] - sheep_position[1])
            value_rhu.append(dist)

        value_grass = []
        for grass_goal in grass_goals:
            value_grass.append(abs(grass_goal[0] - sheep_position[0]) + abs(grass_goal[1] - sheep_position[1]))

        if value_grass:
            if value_rhu:
                if min(value_rhu) <= min(value_grass):
                    ind = value_rhu.index(min(value_rhu))
                    final_goal = rhu_goals[ind]
                else:
                    ind = value_grass.index(min(value_grass))
                    final_goal = grass_goals[ind]
            else:
                ind = value_grass.index(min(value_grass))
                final_goal = grass_goals[ind]
        else:
            ind = value_rhu.index(min(value_rhu))
            final_goal = rhu_goals[ind]

        return final_goal

    #A* star search for sheep
    def a_star_sheep(self,figure, start, goal,field):

        frontier = PriorityQueue()
        frontier.put(start, 0)
        came_from = {}
        cost_so_far = {}
        all_cost = {}
        came_from[start] = None
        cost_so_far[start] = 0
        all_cost[start] = abs(goal[0]-start[0])+abs(goal[1]-start[1])

        while not frontier.empty():
            current = frontier.get()

            if current == goal:
                break

            for next in self.neighbors(figure, current, field):
               # print(next)
                new_cost = cost_so_far[current] + self.cost(figure, current,next,field)
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + self.heuristic(goal, next)
                    all_cost[next] = priority
                    frontier.put(next, priority)
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

        # A* star search for wolf
    def a_star_wolf(self, figure, start, goal, field):
        frontier = PriorityQueue()
        frontier.put(start, 0)
        came_from = {}
        cost_so_far = {}
        all_cost = {}
        came_from[start] = None
        cost_so_far[start] = 0
        all_cost[start] = abs(goal[0] - start[0]) + abs(goal[1] - start[1])

        while not frontier.empty():
            current = frontier.get()

            if current == goal:
                break

            for next in self.neighbors(figure, current, field):

                new_cost = cost_so_far[current] + self.cost(figure, current, next, field)
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + self.heuristic(goal, next)
                    all_cost[next] = priority
                    frontier.put(next, priority)
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


    def wolf_close(self, player_number, field):
        if player_number == 1:
            sheep_position = self.get_player_position(CELL_SHEEP_1, field)
            wolf_position = self.get_player_position(CELL_WOLF_2, field)
        else:
            sheep_position = self.get_player_position(CELL_SHEEP_2, field)
            wolf_position = self.get_player_position(CELL_WOLF_1, field)

        if (abs(sheep_position[0] - wolf_position[0]) <= 1 and abs(sheep_position[1] - wolf_position[1]) <= 1) or \
            (abs(sheep_position[0] - wolf_position[0]) <= 2 and abs(sheep_position[1] - wolf_position[1]) == 0) or \
            (abs(sheep_position[0] - wolf_position[0]) == 0 and abs(sheep_position[1] - wolf_position[1]) <= 2):
            # print('wolf is close')
            return True
        return False


    def run_from_wolf(self, player_number, field):
        if player_number == 1:
            sheep_position = self.get_player_position(CELL_SHEEP_1, field)
            wolf_position = self.get_player_position(CELL_WOLF_2, field)
            sheep = CELL_SHEEP_1
        else:
            sheep_position = self.get_player_position(CELL_SHEEP_2, field)
            wolf_position = self.get_player_position(CELL_WOLF_1, field)
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
                if self.valid_move(sheep, sheep_position[0] + 1, sheep_position[1], field):
                    return MOVE_DOWN
            else:  # it's below the sheep, move up if possible
                if self.valid_move(sheep, sheep_position[0] - 1, sheep_position[1], field):
                    return MOVE_UP
                    # if this is not possible, flee to the right or left
            if self.valid_move(sheep, sheep_position[0], sheep_position[1] + 1, field):
                return MOVE_RIGHT
            elif self.valid_move(sheep, sheep_position[0], sheep_position[1] - 1, field):
                return MOVE_LEFT
            else:  # nowhere to go
                return MOVE_NONE

        # else if the wolf is close horizontally
        elif abs_distance_x == 1 and distance_y == 0:
            # print('wolf is close horizontally')
            # if it's to the left, move to the right if possible
            if distance_x > 0:
                if self.valid_move(sheep, sheep_position[0], sheep_position[1] - 1, field):
                    return MOVE_RIGHT
            else:  # it's to the right, move left if possible
                if self.valid_move(sheep, sheep_position[0], sheep_position[1] + 1, field):
                    return MOVE_RIGHT
            # if this is not possible, flee up or down
            if self.valid_move(sheep, sheep_position[0] - 1, sheep_position[1], field):
                return MOVE_UP
            elif self.valid_move(sheep, sheep_position[0] + 1, sheep_position[1], field):
                return MOVE_DOWN
            else:  # nowhere to go
                return MOVE_NONE

        elif abs_distance_x == 1 and abs_distance_y == 1:
            # print('wolf is in my surroundings')
            # wolf is left and up
            if distance_x > 0 and distance_y > 0:
                # move right or down
                if self.valid_move(sheep, sheep_position[0], sheep_position[1] + 1, field):
                    return MOVE_RIGHT
                else:
                    return MOVE_DOWN
            # wolf is left and down
            if distance_x > 0 and distance_y < 0:
                # move right or up
                if self.valid_move(sheep, sheep_position[0], sheep_position[1] + 1, field):
                    return MOVE_RIGHT
                else:
                    return MOVE_UP
            # wolf is right and up
            if distance_x < 0 and distance_y > 0:
                # move left or down
                if self.valid_move(sheep, sheep_position[0], sheep_position[1] - 1, field):
                    return MOVE_LEFT
                else:
                    return MOVE_DOWN
            # wolf is right and down
            if distance_x < 0 and distance_y < 0:
                # move left and up
                if self.valid_move(sheep, sheep_position[0], sheep_position[1] - 1, field):
                    return MOVE_LEFT
                else:
                    return MOVE_UP

        else:  # this method was wrongly called
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
            # print('gather food move')
            return self.a_star_sheep(figure,self.get_player_position(figure,field),self.closest_goal(player_number, field), field)
        else:
            return MOVE_NONE

    # defs for wolf
    def move_wolf(self, player_number, field):
        if player_number == 1:
            figure = CELL_WOLF_1
            sheep_position = self.get_player_position(CELL_SHEEP_2, field)
            return self.a_star_wolf(figure,self.get_player_position(figure,field),sheep_position,field)
        else:
            figure = CELL_WOLF_2
            sheep_position = self.get_player_position(CELL_SHEEP_1, field)
            return self.a_star_wolf(figure, self.get_player_position(figure, field), sheep_position, field)