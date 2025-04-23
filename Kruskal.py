import random

HORIZONTAL = 0
VERTICAL   = 1

class KruskalMaze:
    def __init__(self, rows, cols):
        self.rows, self.cols = rows, cols
        self.area = [[1]*cols for _ in range(rows)]
        self.sets = [[0]*cols for _ in range(rows)]

    def generate(self):
        edges, set_id = [], 1
        for y in range(1, self.rows-1, 2):
            for x in range(1, self.cols-1, 2):
                self.sets[y][x] = set_id; set_id += 1
                if y+2 < self.rows-1: edges.append((y, x, VERTICAL))
                if x+2 < self.cols-1: edges.append((y, x, HORIZONTAL))
        random.shuffle(edges)

        yield self.area

        for y, x, ori in edges:
            if ori == HORIZONTAL:
                y2, x2 = y, x+2
                if self.sets[y][x] != self.sets[y2][x2]:
                    old, new = self.sets[y2][x2], self.sets[y][x]
                    for yy in range(1, self.rows-1, 2):
                        for xx in range(1, self.cols-1, 2):
                            if self.sets[yy][xx] == old:
                                self.sets[yy][xx] = new
                    for dx in range(3):
                        self.area[y][x+dx] = 0
                    yield self.area

            else:
                y2, x2 = y+2, x
                if self.sets[y][x] != self.sets[y2][x2]:
                    old, new = self.sets[y2][x2], self.sets[y][x]
                    for yy in range(1, self.rows-1, 2):
                        for xx in range(1, self.cols-1, 2):
                            if self.sets[yy][xx] == old:
                                self.sets[yy][xx] = new
                    for dy in range(3):
                        self.area[y+dy][x] = 0
                    yield self.area
