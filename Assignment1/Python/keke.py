from config import *
import heapq

def get_class_name():
    return 'newPlayer'

class PriorityQueue:
    def __init__(self):
        self.elements = []

    def no_food(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]


class newPlayer():
    """Greedy Kingsheep player. Sheep flee from the wolf or go to the nearest food
    in a straight line, wolves go to sheep in a straight line."""

    def __init__(self):
        self.name = "newPlayer"
        self.uzh_shortname = "aplayer"

    def get_player_position(self, figure, field):
        x = [x for x in field if figure in x][0]
        return (field.index(x), x.index(figure))

    def to_evaluate(self,i,j):

        (x, y) = i
        (x0, y0) = j
        distance = abs(x - x0) + abs(y - y0)

        return distance

    # defs for sheep
    def food_present(self, field):
        food_present = False

        for line in field:
            for item in line:
                if item == CELL_RHUBARB or item == CELL_GRASS:
                    food_present = True
                    break
        return food_present

    def search_goal(self,food,field):
        r_goal = []
        g_goal = []
        no_food = []

# it is necessary to identify whether the point is grass or rhu or empty
        y_position = 0
        for line in field:
            x_position = 0
            for item in line:
                if item == CELL_RHUBARB:
                    r_goal.append((y_position, x_position))
                if item == CELL_GRASS:
                    g_goal.append((y_position, x_position))
                if item == CELL_EMPTY:
                    no_food.append((y_position,x_position))
                x_position += 1
            y_position += 1

        if food == CELL_GRASS:
            return g_goal
        if food == CELL_RHUBARB:
            return r_goal
        if food == CELL_EMPTY:
            return no_food

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

    def around_me(self,figure, node,field):
        (x,y)=node
        my_neib = [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]
        around_point = []
        for i in my_neib:
            (a, b) = i
            if self.valid_move(figure,a,b,field):
                around_point.append(i)
        return around_point

    def weight_caculate(self,figure,node,new_node, field):
 #need to figure out each pointfor grass or empty
        no_food = self.search_goal(CELL_EMPTY,field)
        grass = self.search_goal(CELL_GRASS,field)
        rhu = self.search_goal(CELL_RHUBARB,field)

        #no_food = self.goal(CELL_no_food,field)
        #grass = self.goal(CELL_GRASS,field)
        #rhu = self.goal(CELL_RHUBARB,field)

        if figure == CELL_SHEEP_1:
            first_s = no_food + grass + rhu + [self.get_player_position(CELL_SHEEP_1,field)] + \
                          [self.get_player_position(CELL_WOLF_2,field)]
            first_s_dis = [5]*len(no_food) + [4]*len(grass) + [0]*len(rhu) + [5] + [10]

            weights_s_1 = dict(zip(first_s,first_s_dis))
            return weights_s_1.get(new_node)

        elif figure == CELL_SHEEP_2:
            second_s = no_food + grass + rhu + [self.get_player_position(CELL_SHEEP_2,field)] + \
                          [self.get_player_position(CELL_WOLF_1,field)]
            second_s_dis = [5]*len(no_food) + [4]*len(grass) + [0]*len(rhu) + [5] + [10]
                          #  [10]*(len(sur_sheep_1)+len(sur_wolf_1)+len(sur_wolf_2))
            weights_s_2 = dict(zip(second_s,second_s_dis))
            return weights_s_2.get(new_node)

        if figure == CELL_WOLF_1:
            first_w = no_food + grass + rhu + [self.get_player_position(CELL_SHEEP_2,field)] + \
                          [self.get_player_position(figure,field)]
            first_w_dis = [5]*len(no_food) + [6]*len(grass) + [7]*len(rhu) + [100] + [20] + [35]
            weights_wolf_1 = dict(zip(first_w,first_w_dis))
            return weights_w_1.get(new_node)

        elif figure == CELL_WOLF_2:
            second_w = no_food + grass + rhu + [self.get_player_position(figure,field)] + \
                         [self.get_player_position(CELL_SHEEP_1,field)]
            second_w_dis = [5]*len(no_food) + [6]*len(grass) + [7]*len(rhu)+ [100] + [20] + [35]
            weights_w_2 = dict(zip(second_w,second_w_dis))
            return weights_w_2.get(new_node)


    #to get the closest goal by greedy algorithmus
    def closest_goal(self, player_number, field):
        possible_goals = []

        if player_number == 1:
            sheep_position = self.get_player_position(CELL_SHEEP_1,field)
        else:
            sheep_position = self.get_player_position(CELL_SHEEP_2,field)

        #make list of possible goals

        y_position = 0
        for line in field:
            x_position = 0
            for item in line:
                if item == CELL_RHUBARB or item == CELL_GRASS:
                    possible_goals.append((y_position,x_position))
                x_position += 1
            y_position += 1

        #determine closest item and return
        distance = 1000
        for possible_goal in possible_goals:
            if (abs(possible_goal[0]-sheep_position[0])+abs(possible_goal[1]-sheep_position[1])) < distance:
                distance = abs(possible_goal[0]-sheep_position[0])+abs(possible_goal[1]-sheep_position[1])
                final_goal = (possible_goal)

        return final_goal

    #A* star search for sheep
    def get_goal_by_astar(self,figure, start, goal,field):

        goals = PriorityQueue()
        goals.put(start, 0)
        came_from = {}


        #weight_caculate_so_far = {}
        #all_weight_caculate = {}
        #came_from[start] = None
        #weight_caculate_so_far[start] = 0

        weight_caculate_so_far = {}
        all_weight_caculate = {}
        came_from[start] = None
        weight_caculate_so_far[start] = 0


        all_weight_caculate[start] = abs(goal[0]-start[0])+abs(goal[1]-start[1])

        while not goals.no_food():
            current = goals.get()

            if current == goal:
                break

            for next in self.around_me(figure, current, field):
               # print(next)
                new_weight_caculate = weight_caculate_so_far[current] + self.weight_caculate(figure, current,next,field)
                if next not in weight_caculate_so_far or new_weight_caculate < weight_caculate_so_far[next]:
                    weight_caculate_so_far[next] = new_weight_caculate
                    priority = new_weight_caculate + self.to_evaluate(goal, next)
                    all_weight_caculate[next] = priority
                    goals.put(next, priority)
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
            return self.get_goal_by_astar(figure,self.get_player_position(figure,field),self.closest_goal(player_number, field), field)
        else:
            return MOVE_NONE

    # defs for wolf
    def move_wolf(self, player_number, field):
        if player_number == 1:
            figure = CELL_WOLF_1
            sheep_position = self.get_player_position(CELL_SHEEP_2, field)
            return self.get_goal_by_astar(figure,self.get_player_position(figure,field),sheep_position,field)
        else:
            figure = CELL_WOLF_2
            sheep_position = self.get_player_position(CELL_SHEEP_1, field)
            return self.get_goal_by_astar(figure, self.get_player_position(figure, field), sheep_position, field)
