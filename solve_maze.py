import pygame
import sys
import random
from typing import List, Tuple, Set
from collections import deque
from Kruskal import KruskalMaze
from prim import PrimMaze
from search import bfs, dfs, uniform_cost_search, astar, manhattan
from visualization import initialize_pygame, visualize_exploration, show_stats

# Constantes
ROWS, COLS = 60, 80  # Dimensiones del laberinto
START = (1, 1)       # Entrada del laberinto
GOAL = (58, 78)      # Salida del laberinto (ajustada para estar dentro del rango)

def get_algorithm_choice():
    """Solicitar al usuario que elija un algoritmo de generación y resolución"""
    print("Seleccione el algoritmo para generar el laberinto:")
    print("1) Kruskal")
    print("2) Prim")
    gen_choice = int(input("Algoritmo de generación: "))
    
    print("\nSeleccione el algoritmo para resolver el laberinto:")
    print("1) BFS (Breadth-First Search)")
    print("2) DFS (Depth-First Search)")
    print("3) UCS (Uniform Cost Search)")
    print("4) A* (A-Star)")
    solve_choice = int(input("Algoritmo de resolución: "))
    
    return gen_choice, solve_choice

def check_connectivity(maze, start, goal):
    """Verifica si existe un camino entre el inicio y el final del laberinto"""
    rows, cols = len(maze), len(maze[0])
    visited = [[False] * cols for _ in range(rows)]
    queue = deque([start])
    visited[start[0]][start[1]] = True
    
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    while queue:
        y, x = queue.popleft()
        
        if (y, x) == goal:
            return True
            
        for dy, dx in directions:
            ny, nx = y + dy, x + dx
            if 0 <= ny < rows and 0 <= nx < cols and not visited[ny][nx] and maze[ny][nx] == 0:
                visited[ny][nx] = True
                queue.append((ny, nx))
                
    return False

def ensure_connectivity(maze, start, goal, max_attempts=100):
    """Asegura que exista al menos un camino entre el inicio y el final"""
    if check_connectivity(maze, start, goal):
        return maze
    
    # Si no hay conectividad, intentamos crear un camino
    print("No hay conectividad inicial, creando camino...")
    
    # Guardar el laberinto original
    original_maze = [row[:] for row in maze]
    
    for attempt in range(max_attempts):
        # Restaurar el laberinto original
        maze = [row[:] for row in original_maze]
        
        # Intentar crear un camino aleatorio entre inicio y fin
        current = start
        goal_reached = False
        max_steps = (ROWS + COLS) * 2  # Límite para evitar bucles infinitos
        steps = 0
        
        while current != goal and steps < max_steps:
            y, x = current
            # Calcular dirección hacia la meta
            dy = 1 if goal[0] > y else -1 if goal[0] < y else 0
            dx = 1 if goal[1] > x else -1 if goal[1] < x else 0
            
            # Lista de posibles movimientos, priorizando acercarse a la meta
            moves = []
            if dy != 0:
                moves.append((dy, 0))
            if dx != 0:
                moves.append((0, dx))
            if not moves:  # Si ya estamos alineados, agregar movimientos aleatorios
                moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]
            
            random.shuffle(moves)  # Agregar algo de aleatoriedad
            
            # Intentar mover
            moved = False
            for dy, dx in moves:
                ny, nx = y + dy, x + dx
                if 0 < ny < ROWS-1 and 0 < nx < COLS-1:  # Mantener distancia del borde
                    maze[ny][nx] = 0  # Abrir camino
                    current = (ny, nx)
                    moved = True
                    break
            
            if not moved:
                # Si no podemos movernos, intentar otra dirección aleatoria
                directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
                random.shuffle(directions)
                for dy, dx in directions:
                    ny, nx = y + dy, x + dx
                    if 0 < ny < ROWS-1 and 0 < nx < COLS-1:
                        maze[ny][nx] = 0
                        current = (ny, nx)
                        moved = True
                        break
            
            if not moved:
                break  # Si no podemos movernos en ninguna dirección
            
            steps += 1
            
            # Verificar si hemos llegado a la meta o estamos adyacentes
            if abs(current[0] - goal[0]) + abs(current[1] - goal[1]) <= 1:
                maze[goal[0]][goal[1]] = 0
                goal_reached = True
                break
        
        # Verificar si el nuevo laberinto tiene conectividad
        if check_connectivity(maze, start, goal):
            print(f"Conectividad establecida después de {attempt+1} intentos.")
            return maze
    
    print("No se pudo establecer conectividad después de múltiples intentos.")
    return maze

def generate_maze(choice: int):
    """Generar un laberinto usando el algoritmo seleccionado"""
    if choice == 1:
        generator = KruskalMaze(ROWS, COLS).generate()
    else:
        generator = PrimMaze(ROWS, COLS).generate()
    
    # Consumir todos los pasos de generación hasta tener el laberinto completo
    area = None
    for area in generator:
        pass
    
    # Asegurar que la entrada y salida sean celdas libres
    area[START[0]][START[1]] = 0
    area[GOAL[0]][GOAL[1]] = 0
    
    # Asegurar que hay un camino desde el inicio hasta la salida
    # Crear caminos desde puntos cercanos a START y GOAL
    # Verificar que hay celdas libres adyacentes a START
    for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        ny, nx = START[0] + dy, START[1] + dx
        if 0 <= ny < ROWS and 0 <= nx < COLS:
            area[ny][nx] = 0  # Asegurar al menos un camino desde START
            break
    
    # Verificar que hay celdas libres adyacentes a GOAL
    for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        ny, nx = GOAL[0] + dy, GOAL[1] + dx
        if 0 <= ny < ROWS and 0 <= nx < COLS:
            area[ny][nx] = 0  # Asegurar al menos un camino hacia GOAL
            break
    
    # Verificar y asegurar la conectividad entre inicio y fin
    area = ensure_connectivity(area, START, GOAL)
    
    return area

def track_exploration(algorithm, area, start, goal):
    """Ejecuta el algoritmo de búsqueda y rastrea los nodos explorados"""
    rows, cols = len(area), len(area[0])
    explored = set()
    
    if algorithm == "bfs":
        # BFS con rastreo de nodos explorados
        from collections import deque
        visited = [[False] * cols for _ in range(rows)]
        parent = {}
        queue = deque([start])
        visited[start[0]][start[1]] = True
        nodes_explored = 0
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        while queue:
            current = queue.popleft()
            nodes_explored += 1
            explored.add(current)
            
            if current == goal:
                return parent, explored, nodes_explored
                
            for dy, dx in directions:
                ny, nx = current[0] + dy, current[1] + dx
                if 0 <= ny < rows and 0 <= nx < cols and not visited[ny][nx] and area[ny][nx] == 0:
                    visited[ny][nx] = True
                    parent[(ny, nx)] = current
                    queue.append((ny, nx))
        
        return parent, explored, nodes_explored
        
    elif algorithm == "dfs":
        # DFS con rastreo de nodos explorados
        visited = [[False] * cols for _ in range(rows)]
        parent = {}
        stack = [start]
        visited[start[0]][start[1]] = True
        nodes_explored = 0
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        while stack:
            current = stack.pop()
            nodes_explored += 1
            explored.add(current)
            
            if current == goal:
                return parent, explored, nodes_explored
                
            for dy, dx in directions:
                ny, nx = current[0] + dy, current[1] + dx
                if 0 <= ny < rows and 0 <= nx < cols and not visited[ny][nx] and area[ny][nx] == 0:
                    visited[ny][nx] = True
                    parent[(ny, nx)] = current
                    stack.append((ny, nx))
        
        return parent, explored, nodes_explored
        
    elif algorithm == "ucs":
        # UCS con rastreo de nodos explorados
        import heapq
        parent = {}
        g_score = {start: 0}
        visited = set()
        heap = [(0, 0, start)]  # (costo, tiebreaker, nodo)
        nodes_explored = 0
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        counter = 1  # Para desempatar elementos con el mismo costo
        
        while heap:
            cost, _, current = heapq.heappop(heap)
            if current in visited:
                continue
                
            visited.add(current)
            nodes_explored += 1
            explored.add(current)
            
            if current == goal:
                return parent, explored, nodes_explored
                
            for dy, dx in directions:
                ny, nx = current[0] + dy, current[1] + dx
                neighbor = (ny, nx)
                if 0 <= ny < rows and 0 <= nx < cols and area[ny][nx] == 0:
                    new_cost = cost + 1
                    if neighbor not in g_score or new_cost < g_score[neighbor]:
                        g_score[neighbor] = new_cost
                        parent[neighbor] = current
                        heapq.heappush(heap, (new_cost, counter, neighbor))
                        counter += 1
        
        return parent, explored, nodes_explored
        
    elif algorithm == "astar":
        # A* con rastreo de nodos explorados
        import heapq
        open_heap = []
        g_score = {start: 0}
        f_score = {start: manhattan(start, goal)}
        parent = {}
        visited = set()
        nodes_explored = 0
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        counter = 0  # Para desempatar elementos con el mismo f_score
        
        heapq.heappush(open_heap, (f_score[start], counter, start))
        counter += 1
        
        while open_heap:
            _, _, current = heapq.heappop(open_heap)
            if current in visited:
                continue
                
            visited.add(current)
            nodes_explored += 1
            explored.add(current)
            
            if current == goal:
                return parent, explored, nodes_explored
                
            for dy, dx in directions:
                ny, nx = current[0] + dy, current[1] + dx
                neighbor = (ny, nx)
                if 0 <= ny < rows and 0 <= nx < cols and area[ny][nx] == 0:
                    tentative_g = g_score[current] + 1
                    if neighbor not in g_score or tentative_g < g_score[neighbor]:
                        g_score[neighbor] = tentative_g
                        f_score[neighbor] = tentative_g + manhattan(neighbor, goal)
                        parent[neighbor] = current
                        heapq.heappush(open_heap, (f_score[neighbor], counter, neighbor))
                        counter += 1
        
        return parent, explored, nodes_explored

def reconstruct_path(parent, start, goal):
    """Reconstruye el camino desde el inicio hasta la meta"""
    if goal not in parent and goal != start:
        # No hay camino hasta la meta
        print("¡No se encontró un camino hasta la meta!")
        return []
    
    path = []
    current = goal
    
    while current != start:
        path.append(current)
        if current not in parent:
            print(f"Error: Nodo {current} no tiene padre en el diccionario de padres")
            return []
        current = parent[current]
    
    path.append(start)
    path.reverse()
    return path

def solve_maze(area: List[List[int]], choice: int):
    """Resolver el laberinto usando el algoritmo seleccionado"""
    if choice == 1:
        algorithm = "bfs"
        algo_name = "BFS"
    elif choice == 2:
        algorithm = "dfs"
        algo_name = "DFS"
    elif choice == 3:
        algorithm = "ucs"
        algo_name = "UCS"
    else:
        algorithm = "astar"
        algo_name = "A*"
    
    # Verificar conectividad antes de resolver
    if not check_connectivity(area, START, GOAL):
        print("ADVERTENCIA: No existe un camino desde el inicio hasta la meta. Estableciendo conectividad...")
        area = ensure_connectivity(area, START, GOAL)
    
    # Ejecutar algoritmo y rastrear exploración
    parent, explored, nodes_explored = track_exploration(algorithm, area, START, GOAL)
    
    # Reconstruir camino
    path = reconstruct_path(parent, START, GOAL)
    
    return path, explored, nodes_explored, algo_name

def main():
    # Opciones de algoritmo
    gen_choice, solve_choice = get_algorithm_choice()
    
    # Generar laberinto
    maze = generate_maze(gen_choice)
    
    # Inicializar pygame y visualización
    screen = initialize_pygame(ROWS, COLS)
    
    # Resolver el laberinto
    path, explored, nodes_explored, algo_name = solve_maze(maze, solve_choice)
    
    # Visualizar exploración y camino
    visualize_exploration(screen, maze, START, GOAL, explored, path)
    
    # Mostrar estadísticas
    show_stats(screen, len(path), nodes_explored, algo_name)
    
    # Mantener la ventana abierta hasta que el usuario la cierre
    while True:
        for evt in pygame.event.get():
            if evt.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

if __name__ == "__main__":
    main() 