import random
import time
from typing import List, Tuple, Dict
import statistics

from Kruskal import KruskalMaze
from search import bfs, dfs, uniform_cost_search, astar, manhattan


# Número de escenarios
K = 25
ROWS, COLS = 45, 55


def random_positions(area: List[List[int]]) -> Tuple[Tuple[int,int], Tuple[int,int]]:
    """
    Selecciona start y goal al azar en celdas libres (0) que estén a Manhattan >= 10.
    """
    libres = [(y,x) for y,row in enumerate(area) for x,v in enumerate(row) if v == 0]
    while True:
        a = random.choice(libres)
        b = random.choice(libres)
        if abs(a[0] - b[0]) + abs(a[1] - b[1]) >= 10:
            return a, b


def run_comparison():
    # Estructura para resultados
    results: List[Dict] = []
    algos = [
        ('BFS', bfs),
        ('DFS', dfs),
        ('UCS', uniform_cost_search),
        ('A*', lambda grid, s, g: astar(grid, s, g, manhattan))
    ]

    for i in range(1, K+1):
        # Generar laberinto final
        maze = KruskalMaze(ROWS, COLS)
        area = None
        for area in maze.generate():
            pass  # consumimos todos los pasos, nos quedamos con el laberinto completo

        start, goal = random_positions(area)

        # Ejecutar cada algoritmo
        for name, fn in algos:
            t0 = time.perf_counter()
            path, nodes = fn(area, start, goal)
            t1 = time.perf_counter()
            results.append({
                'escenario': i,
                'algoritmo': name,
                'nodos': nodes,
                'tiempo': t1 - t0,
                'longitud': len(path)
            })
        print(f"Escenario {i} completado.")

    # Resumen de métricas promedio
    print("\n=== Resumen promedio de métricas ===")
    for name, _ in algos:
        subset = [r for r in results if r['algoritmo'] == name]
        mean_nodos = statistics.mean(r['nodos'] for r in subset)
        mean_tiempo = statistics.mean(r['tiempo'] for r in subset)
        mean_long = statistics.mean(r['longitud'] for r in subset)
        print(f"{name}: nodos={mean_nodos:.1f}, tiempo={mean_tiempo:.4f}s, longitud={mean_long:.1f}")

    # Ranking por tiempo promedio
    ranking = sorted(
        [(name, statistics.mean(r['tiempo'] for r in results if r['algoritmo']==name))
         for name, _ in algos],
        key=lambda x: x[1]
    )
    print("\nRanking por tiempo (mejor -> peor):", [r[0] for r in ranking])


if __name__ == '__main__':
    random.seed(123)
    run_comparison()
