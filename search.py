from collections import deque
from typing import List, Tuple, Dict, Callable
import heapq


def bfs(
    grid: List[List[int]],
    start: Tuple[int, int],
    goal: Tuple[int, int]
) -> Tuple[List[Tuple[int, int]], int]:
    rows, cols = len(grid), len(grid[0])
    visited = [[False] * cols for _ in range(rows)]
    parent: Dict[Tuple[int, int], Tuple[int, int]] = {}
    queue = deque([start])
    visited[start[0]][start[1]] = True
    nodes_explored = 0
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while queue:
        current = queue.popleft()
        nodes_explored += 1
        if current == goal:
            return reconstruct_path(parent, start, goal), nodes_explored
        for dy, dx in directions:
            ny, nx = current[0] + dy, current[1] + dx
            if 0 <= ny < rows and 0 <= nx < cols and not visited[ny][nx] and grid[ny][nx] == 0:
                visited[ny][nx] = True
                parent[(ny, nx)] = current
                queue.append((ny, nx))
    return [], nodes_explored


def dfs(
    grid: List[List[int]],
    start: Tuple[int, int],
    goal: Tuple[int, int]
) -> Tuple[List[Tuple[int, int]], int]:
    rows, cols = len(grid), len(grid[0])
    visited = [[False] * cols for _ in range(rows)]
    parent: Dict[Tuple[int, int], Tuple[int, int]] = {}
    stack = [start]
    visited[start[0]][start[1]] = True
    nodes_explored = 0
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while stack:
        current = stack.pop()
        nodes_explored += 1
        if current == goal:
            return reconstruct_path(parent, start, goal), nodes_explored
        for dy, dx in directions:
            ny, nx = current[0] + dy, current[1] + dx
            if 0 <= ny < rows and 0 <= nx < cols and not visited[ny][nx] and grid[ny][nx] == 0:
                visited[ny][nx] = True
                parent[(ny, nx)] = current
                stack.append((ny, nx))
    return [], nodes_explored


def uniform_cost_search(
    grid: List[List[int]],
    start: Tuple[int, int],
    goal: Tuple[int, int]
) -> Tuple[List[Tuple[int, int]], int]:
    """
    Uniform Cost Search (Dijkstra) en un grid donde cada paso cuesta 1.
    """
    rows, cols = len(grid), len(grid[0])
    parent: Dict[Tuple[int, int], Tuple[int, int]] = {}
    g_score: Dict[Tuple[int, int], int] = {start: 0}
    visited = set()
    # Min-heap de (costo acumulado, nodo)
    heap = [(0, start)]
    nodes_explored = 0
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while heap:
        cost, current = heapq.heappop(heap)
        if current in visited:
            continue
        visited.add(current)
        nodes_explored += 1
        if current == goal:
            return reconstruct_path(parent, start, goal), nodes_explored
        for dy, dx in directions:
            ny, nx = current[0] + dy, current[1] + dx
            neighbor = (ny, nx)
            if 0 <= ny < rows and 0 <= nx < cols and grid[ny][nx] == 0:
                new_cost = cost + 1
                if neighbor not in g_score or new_cost < g_score[neighbor]:
                    g_score[neighbor] = new_cost
                    parent[neighbor] = current
                    heapq.heappush(heap, (new_cost, neighbor))
    return [], nodes_explored


def astar(
    grid: List[List[int]],
    start: Tuple[int, int],
    goal: Tuple[int, int],
    heuristic: Callable[[Tuple[int, int], Tuple[int, int]], float]
) -> Tuple[List[Tuple[int, int]], int]:
    # Por implementar en el siguiente paso
    pass


def reconstruct_path(
    parent: Dict[Tuple[int, int], Tuple[int, int]],
    start: Tuple[int, int],
    goal: Tuple[int, int]
) -> List[Tuple[int, int]]:
    path: List[Tuple[int, int]] = []
    current = goal
    while current != start:
        path.append(current)
        current = parent.get(current)
        if current is None:
            return []
    path.append(start)
    path.reverse()
    return path


if __name__ == "__main__":
    sample = [
        [0, 1, 0, 0],
        [0, 1, 0, 1],
        [0, 0, 0, 0],
    ]
    s, e = (0, 0), (2, 3)

    path_bfs, exp_bfs = bfs(sample, s, e)
    print("BFS Path:", path_bfs)
    print("BFS Nodes explored:", exp_bfs)

    path_dfs, exp_dfs = dfs(sample, s, e)
    print("DFS Path:", path_dfs)
    print("DFS Nodes explored:", exp_dfs)

    path_ucs, exp_ucs = uniform_cost_search(sample, s, e)
    print("UCS Path:", path_ucs)
    print("UCS Nodes explored:", exp_ucs)
