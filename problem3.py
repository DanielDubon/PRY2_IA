
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
import random
import time
import pygame
import statistics
from typing import List, Tuple, Dict

from Kruskal import KruskalMaze
from search import bfs, dfs, uniform_cost_search, astar, manhattan
from visualization import (
    initialize_pygame,
    visualize_exploration,
    show_stats
)


# Número de escenarios
K = 25
ROWS, COLS = 45, 55

# Carpeta de salida para capturas
OUT_DIR = "problem3_vis"
os.makedirs(OUT_DIR, exist_ok=True)

def random_positions(area: List[List[int]]) -> Tuple[Tuple[int,int], Tuple[int,int]]:
    """Selecciona start y goal al azar en celdas libres (0) que estén a Manhattan >= 10."""
    libres = [(y,x) for y,row in enumerate(area) for x,v in enumerate(row) if v == 0]
    while True:
        a = random.choice(libres)
        b = random.choice(libres)
        if abs(a[0] - b[0]) + abs(a[1] - b[1]) >= 10:
            return a, b

def run_comparison():
    results: List[Dict] = []
    algos = [
        ('BFS', bfs),
        ('DFS', dfs),
        ('UCS', uniform_cost_search),
        ('A*', lambda g,s,t: astar(g,s,t,manhattan))
    ]

    for i in range(1, K+1):
        # 1) Generar laberinto
        maze = KruskalMaze(ROWS, COLS)
        for area in maze.generate(): pass  # agotamos el generator
        start, goal = random_positions(area)

        # 2) Para cada algoritmo:
        for name, fn in algos:
            # — Ejecutar algoritmo y medir
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

            # — Visualizar escenario
            screen = initialize_pygame(ROWS, COLS)
            from solve_maze import track_exploration

            # Determinar la clave correcta para track_exploration
            if name == 'A*':
                key = 'astar'
            else:
                key = name.lower()
            
            parent, explored, _ = track_exploration(
                key, area, start, goal
            )
            # Reconstruimos path con tus funciones
            from solve_maze import reconstruct_path
            real_path = reconstruct_path(parent, start, goal)

            visualize_exploration(screen, area, start, goal, explored, real_path)
            show_stats(screen, len(real_path), nodes, name)

            # — Guardar captura y cerrar ventana
            filename = os.path.join(
                OUT_DIR, f"esc{i}_{name.replace('*','star')}.png"
            )
            pygame.image.save(screen, filename)
            pygame.quit()

        print(f"Escenario {i} completado.")

    # 3) Resumen promedio
    print("\n=== Resumen promedio de métricas ===")
    for name, _ in algos:
        subset = [r for r in results if r['algoritmo'] == name]
        mn = statistics.mean(r['nodos'] for r in subset)
        mt = statistics.mean(r['tiempo'] for r in subset)
        ml = statistics.mean(r['longitud'] for r in subset)
        print(f"{name}: nodos={mn:.1f}, tiempo={mt:.4f}s, longitud={ml:.1f}")

    ranking = sorted(
        [(name, statistics.mean(r['tiempo'] for r in results if r['algoritmo']==name))
         for name, _ in algos],
        key=lambda x: x[1]
    )
    print("\nRanking por tiempo (mejor -> peor):", [r[0] for r in ranking])

if __name__ == '__main__':
    random.seed(123)
    run_comparison()
