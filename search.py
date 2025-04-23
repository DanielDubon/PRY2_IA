from collections import deque
from typing import List, Tuple, Dict, Callable


def bfs(
    grid: List[List[int]],
    start: Tuple[int, int],
    goal: Tuple[int, int]
) -> Tuple[List[Tuple[int, int]], int]:
    """
    Breadth-First Search en un grid binario.

    Args:
        grid: matriz 2D donde 0 = espacio libre, 1 = pared.
        start: coordenada (fila, columna) de inicio.
        goal: coordenada (fila, columna) objetivo.

    Returns:
        path: lista de coordenadas desde start hasta goal (vacía si no hay camino).
        nodes_explored: número de nodos extraídos del frontier.
    """
    rows, cols = len(grid), len(grid[0])
    visited = [[False] * cols for _ in range(rows)]
    parent: Dict[Tuple[int, int], Tuple[int, int]] = {}
    queue = deque([start])
    visited[start[0]][start[1]] = True
    nodes_explored = 0

    # Movimientos en 4 direcciones: arriba, abajo, izquierda, derecha
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while queue:
        current = queue.popleft()
        nodes_explored += 1

        if current == goal:
            path = reconstruct_path(parent, start, goal)
            return path, nodes_explored

        for dy, dx in directions:
            ny, nx = current[0] + dy, current[1] + dx
            if (
                0 <= ny < rows
                and 0 <= nx < cols
                and not visited[ny][nx]
                and grid[ny][nx] == 0
            ):
                visited[ny][nx] = True
                parent[(ny, nx)] = current
                queue.append((ny, nx))

    # Si no se encuentra camino
    return [], nodes_explored


def dfs(
    grid: List[List[int]],
    start: Tuple[int, int],
    goal: Tuple[int, int]
) -> Tuple[List[Tuple[int, int]], int]:
    """
    Depth-First Search en un grid binario (iterativo con pila).

    Args:
        grid: matriz 2D donde 0 = espacio libre, 1 = pared.
        start: coordenada (fila, columna) de inicio.
        goal: coordenada (fila, columna) objetivo.

    Returns:
        path: lista de coordenadas desde start hasta goal (vacía si no hay camino).
        nodes_explored: número de nodos extraídos de la pila.
    """
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
            path = reconstruct_path(parent, start, goal)
            return path, nodes_explored

        for dy, dx in directions:
            ny, nx = current[0] + dy, current[1] + dx
            if (
                0 <= ny < rows
                and 0 <= nx < cols
                and not visited[ny][nx]
                and grid[ny][nx] == 0
            ):
                visited[ny][nx] = True
                parent[(ny, nx)] = current
                stack.append((ny, nx))

    return [], nodes_explored


def uniform_cost_search(
    grid: List[List[int]],
    start: Tuple[int, int],
    goal: Tuple[int, int]
) -> Tuple[List[Tuple[int, int]], int]:
    # Por implementar
    pass


def astar(
    grid: List[List[int]],
    start: Tuple[int, int],
    goal: Tuple[int, int],
    heuristic: Callable[[Tuple[int, int], Tuple[int, int]], float]
) -> Tuple[List[Tuple[int, int]], int]:
    # Por implementar
    pass


def reconstruct_path(
    parent: Dict[Tuple[int, int], Tuple[int, int]],
    start: Tuple[int, int],
    goal: Tuple[int, int]
) -> List[Tuple[int, int]]:
    """
    Reconstruye el camino desde goal hasta start usando el diccionario parent.
    """
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
