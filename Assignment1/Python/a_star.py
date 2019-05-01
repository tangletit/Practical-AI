import PriorityQueue


class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]


def heuristic(a, b):
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)

#找到吃最近的草的最优路径，start就是羊的当前位置，可通过position来获得，goal来自于closet-goal的方程
def food_get(self,field, start, goal):
    food = PriorityQueue()
    food.put(start, 0)
    came_from = {}
    cost_so_far = {}
    all_cost = {}
    came_from[start] = None
    cost_so_far[start] = 0
    all_cost[start] = abs(goal[0]-start[0])+abs(goal[1]-start[1])

    goal_x = goal[1]
    goal_y = goal[0]


    while not food.empty():
        current = food.get()

        if current == goal:
            break

        for next in field.neighbors(current):
            new_cost = cost_so_far[current] + field.cost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(goal, next)
                all_cost[next] = priority
                food.put(next, priority)
                came_from[next] = current

    return came_from, cost_so_far,all_cost
    # 获取邻居的位置
    def neighbors(self,figure,node,field): # 获取邻居的位置
    neighbors = []
    (x,y)=node
    results = [(x + 1, y), (x, y - 1), (x - 1, y), (x, y + 1)]
    for iterm in results:
        (i, j) = iterm
        if self.valid_move(figure, i, j, field):
            neighbors.append(iterm)
        return neighbors


# 获取两个点之间的权重，所以现在需要考虑两个点之间的权重是由什么决定的
    def cost(self, figure, next_node, field):
        empty = self.food_position(CELL_EMPTY,field)
        grass = self.food_position(CELL_GRASS,field)
        rub = self.food_position(CELL_RHUBARB,field)

        if figure = CELL_SHEEP_1:
            sheep_1 = empty + grass + rub +[self.get_play_position(CELL_SHEEP_1,field)]+[self.get_play_position(CELL_WOLF_2,field)]
            len_sheep_1 =[5]*len(empty)+[4]*len(grass)+[0]len(rhu)+[5]+[20]
            weight = dict(zip(sheep,len_sheep_1))

            return self.weight.get(next_node)

        elif figure = CELL_SHEEP_2:
            sheep_2 = empty + grass + rub +[self.get_play_position(CELL_SHEEP_2,field)]+[self.get_play_position(CELL_WOLF_1,field)]
            len_sheep_2 =[5]*len(empty)+[4]*len(grass)+[0]len(rhu)+[5]+[20]
            weight = dict(zip(sheep_2,len_sheep_2))

            return self.weights.get(next_node)

        elif figure = CELL_WOLF_2:
            wolf_2 = empty + grass + rub +[self.get_play_position(CELL_WOLF_2,field)]+[self.get_play_position(CELL_SHEEP_1,field)]
            len_wolf_2 =[5]*len(empty)+[4]*len(grass)+[0]len(rhu)+[5]+[20]
            weight = dict(zip(wolf_2,len_wolf_2))

            return self.weights.get(next_node)

        elif figure = CELL_WOLF_1:
            wolf_1 = empty + grass + rub +[self.get_play_position(CELL_WOLF_1,field)]+[self.get_play_position(CELL_SHEEP_2,field)]
            len_wolf_1 =[5]*len(empty)+[4]*len(grass)+[0]len(rhu)+[5]+[20]
            weight = dict(zip(wolf_1,len_wolf_1))

            return self.weights.get(next_node)

#判断每一个点到底是草还是空还是仙人掌
    def food_position(self,food,field):
        road = []
        grass = []
        ruh = []

        y_position = 0
        for line in field:
            x_position = 0
            for item in line:
                if item == CELL_RHUBARB:
                    rub.append((y_position,x_position))
                if item == CELL_GRASS:
                    grass.append((y_position,x_position))
                if item == CELL_EMPTY:
                    road.append((y_position,x_position))
                x_position += 1
            y_position += 1


        if food = CELL_GRASS:
            return grass
        if food = CELL_RHUBARB:
            return ruh
        if food = CELL_EMPTY:
            return road


