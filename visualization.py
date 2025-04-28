import pygame
import sys
from typing import List, Tuple, Set

# Constantes
CELL_SIZE = 8  # Tamaño de celda en píxeles (reducido para que quepa un laberinto más grande)
DELAY_EXPLORATION = 0  # Milisegundos entre la visualización de cada nodo explorado
DELAY_PATH = 10  # Milisegundos entre la visualización de cada paso del camino

# Colores
BLACK = (0, 0, 0)         # Pared
WHITE = (255, 255, 255)   # Camino libre
RED = (255, 0, 0)         # Punto inicial
GREEN = (0, 255, 0)       # Punto final
BLUE = (0, 0, 255)        # Camino encontrado
YELLOW = (255, 255, 0)    # Nodos explorados
GRAY = (200, 200, 200)    # Frontera (si se usa Prim)
ORANGE = (255, 165, 0)    # Color alternativo

def initialize_pygame(rows: int, cols: int):
    """Inicializa pygame y devuelve la superficie de dibujo"""
    pygame.init()
    width, height = cols * CELL_SIZE, rows * CELL_SIZE
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Resolución de Laberinto")
    return screen

def visualize_exploration(
    screen, 
    area: List[List[int]], 
    start: Tuple[int, int], 
    goal: Tuple[int, int], 
    explored: Set[Tuple[int, int]],
    path: List[Tuple[int, int]]
):
    """Visualiza la exploración y el camino encontrado"""
    # Dibujar el laberinto base
    for y in range(len(area)):
        for x in range(len(area[0])):
            v = area[y][x]
            if v == 1:
                color = BLACK
            elif v == 0:
                color = WHITE
            else:
                color = GRAY
            rect = pygame.Rect(x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, color, rect)
    pygame.display.flip()
    
    # Dibujar nodos explorados
    count = 0
    for y, x in explored:
        if (y, x) != start and (y, x) != goal and (y, x) not in path:
            rect = pygame.Rect(x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, YELLOW, rect)
            count += 1
            if count % 50 == 0:  # Actualizar cada 50 nodos para acelerar la visualización
                pygame.display.flip()
                pygame.time.delay(DELAY_EXPLORATION)
                # Manejar eventos para permitir salir
                for evt in pygame.event.get():
                    if evt.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
    
    pygame.display.flip()
    pygame.time.delay(300)  # Pausa para apreciar la exploración completa
    
    # Verificar si se encontró un camino
    if not path:
        print("No se encontró un camino entre el inicio y la meta.")
        # Dibujar solo puntos de inicio y fin
        start_rect = pygame.Rect(start[1]*CELL_SIZE, start[0]*CELL_SIZE, CELL_SIZE, CELL_SIZE)
        goal_rect = pygame.Rect(goal[1]*CELL_SIZE, goal[0]*CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, RED, start_rect)
        pygame.draw.rect(screen, GREEN, goal_rect)
        pygame.display.flip()
        return
    
    # Dibujar camino encontrado
    print(f"Camino encontrado con longitud: {len(path)}")
    
    # Crear un camino visual más grueso para que sea más visible
    for y, x in path:
        if (y, x) != start and (y, x) != goal:  # No dibujar sobre inicio y fin
            rect = pygame.Rect(x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, ORANGE, rect)
            pygame.display.flip()
            pygame.time.delay(DELAY_PATH)
            # Manejar eventos para permitir salir
            for evt in pygame.event.get():
                if evt.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
    
    # Dibujar punto inicial y final
    start_rect = pygame.Rect(start[1]*CELL_SIZE, start[0]*CELL_SIZE, CELL_SIZE, CELL_SIZE)
    goal_rect = pygame.Rect(goal[1]*CELL_SIZE, goal[0]*CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, RED, start_rect)
    pygame.draw.rect(screen, GREEN, goal_rect)
    pygame.display.flip()

def show_stats(screen, path_length, nodes_explored, algorithm_name):
    """Muestra estadísticas en pantalla"""
    try:
        font = pygame.font.SysFont('Arial', 18)
    except:
        font = pygame.font.Font(None, 22)  # Fuente por defecto si Arial no está disponible
    
    # Crear un rectángulo para el fondo de las estadísticas
    stats_rect = pygame.Rect(10, 10, 300, 100)
    s = pygame.Surface((stats_rect.width, stats_rect.height))
    s.set_alpha(200)  # Semi-transparente
    s.fill((220, 220, 220))
    screen.blit(s, stats_rect)
    
    # Crear textos
    text1 = font.render(f"Algoritmo: {algorithm_name}", True, BLACK)
    text2 = font.render(f"Longitud del camino: {path_length}", True, BLACK)
    text3 = font.render(f"Nodos explorados: {nodes_explored}", True, BLACK)
    
    # Posicionar textos
    screen.blit(text1, (20, 20))
    screen.blit(text2, (20, 45))
    screen.blit(text3, (20, 70))
    
    pygame.display.flip()