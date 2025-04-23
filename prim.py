import random

class PrimMaze:
    def __init__(self, rows, cols):
        self.rows, self.cols = rows, cols
        self.area = [[1]*cols for _ in range(rows)]
        self.frontiers = []

    def mark(self, y, x):
        self.area[y][x] = 0
        yield self.area
        for dy, dx in [(-2,0),(2,0),(0,-2),(0,2)]:
            ny, nx = y+dy, x+dx
            if 0 < ny < self.rows-1 and 0 < nx < self.cols-1 and self.area[ny][nx] == 1:
                self.area[ny][nx] = 2
                self.frontiers.append((ny, nx))
                yield self.area

    def generate(self):
        sy = random.randrange(1, self.rows-1, 2)
        sx = random.randrange(1, self.cols-1, 2)
        yield from self.mark(sy, sx)

        while self.frontiers:
            idx = random.randrange(len(self.frontiers))
            y, x = self.frontiers.pop(idx)
            vecinos = []
            for dy, dx in [(-2,0),(2,0),(0,-2),(0,2)]:
                ny, nx = y+dy, x+dx
                if 0 <= ny < self.rows and 0 <= nx < self.cols and self.area[ny][nx] == 0:
                    vecinos.append((dy, dx))
            if not vecinos:
                continue

            dy, dx = random.choice(vecinos)
            self.area[y + dy//2][x + dx//2] = 0
            self.area[y][x] = 0
            yield self.area
            yield from self.mark(y, x)
