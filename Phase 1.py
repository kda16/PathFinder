SHAPE = (10, 10)
STARTING_POINT = (0, 0)
DELIVERY_POINT = (9, 9)
OBSTACLES = ((9, 7), (8, 7), (6, 7), (6, 8))
# goes anywhere - 8 adjacent squares


class Color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


class Cell:

    def __init__(self, pos, n):
        self.pos = pos
        self.n = n


def grid(here, path, start=STARTING_POINT, finish=DELIVERY_POINT, obst=OBSTACLES):
    print()
    for y in range(10):
        for x in range(10):
            if (x, y) == start:
                print(Color.BOLD + Color.GREEN + f"[S{here[(x, y)]}]" + Color.END, end="")
            elif (x, y) == finish:
                print(Color.BOLD + Color.GREEN + f"[D{here[(x, y)]}]" + Color.END, end="")
            elif (x, y) in path:
                print(Color.GREEN + f"[W{here[(x, y)]}]" + Color.END, end="")
            elif (x, y) in here:
                print(Color.YELLOW + f"[ {here[(x, y)]}]" + Color.END, end="")
            elif (x, y) in obst:
                print(Color.BOLD + "[**]" + Color.END, end="")
            else:
                print("[  ]", end="")
        print()


def distance(a, b):
    return ((a[0]-b[0])**2 + (a[1]-b[1])**2)**(1/2)


def distance_close(a, b):
    x, y = abs(a[0]-b[0]), abs(a[1]-b[1])
    if x > 1 or y > 1:
        return int(distance(a, b)*10)
    d = x + y
    if d == 0:
        return 0
    elif d == 1:
        return 10
    else:
        return 14


def in_border(point, dim=SHAPE):
    n, m = dim
    x, y = point
    flag = False
    if -1 < x < n and -1 < y < m:
        flag = True
    return flag


def find_adjacent(center, obsts=OBSTACLES, parents=False):
    if parents:
        x, y, n = center
    else:
        x, y = center

    adj = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            (x_new, y_new) = (x + i, y + j)
            cell = (x_new, y_new)
            if (i, j) != (0, 0) and in_border(cell) and not(cell in obsts):
                if parents:
                    adj.append((x_new, y_new, n + 1))
                else:
                    adj.append((x_new, y_new))
    return adj


def wide_algo(start=STARTING_POINT, finish=DELIVERY_POINT):
    queue_old = [(start[0], start[1], 0)]
    queue_new = queue_old[:]
    found = False
    while not found:
        for current in queue_old:
            adjacent_all = find_adjacent(current, parents=True)
            adjacent_new = []
            x, y = list(zip(*queue_new))[0:2]
            for each in adjacent_all:
                if (each[0], each[1]) == finish:
                    found = True
                if (each[0], each[1]) not in set(zip(x, y)):
                    adjacent_new.append(each)
            if len(adjacent_new) != 0:
                queue_new.extend(adjacent_new)
        queue_old = queue_new[:]
    x_pos, y_pos, ns = list(zip(*queue_new))
    cells = dict(zip((zip(x_pos, y_pos)), ns))
    return cells


def reverse(k, current, start=STARTING_POINT):
    if k == 0:
        return [start]
    path = []
    adjs = find_adjacent(current, parents=False)
    dist_points = [(distance_close(each, current), each) for each in adjs if points[each] == k - 1]
    el = min(dist_points, key=lambda x: x[0])
    path = [current]
    path.extend(reverse(k-1, el[1]))
    return path


def check_logic(start=STARTING_POINT, finish=DELIVERY_POINT, obst=OBSTACLES):
    if start in obst or finish in obst:
        raise(ValueError("Impossible situation: Finish or Start is at the obstacles"))
    return None


check_logic()
points = wide_algo()
k = points[DELIVERY_POINT]
way = reverse(k, DELIVERY_POINT)
grid(here=points, path=way)
print(f"\n{k} steps: {way[::-1]}")
