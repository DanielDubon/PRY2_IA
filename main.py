
import pygame
import random
import sys
from Kruskal import KruskalMaze
from prim    import PrimMaze

# ———— CONSTANTES ————
SEED      = 123         
CELL_SIZE = 16          # esta en px
DELAY_MS  = 30          # retardo entre frames en milisegundos
# ———————————————————

def get_dimensions():
    m = int(input("Número de filas : "))
    n = int(input("Número de columnas : "))
    print("Seleccione el algoritmo: 1) Kruskal 2) Prim ")
    algo = int(input("Algoritmo a usar: "))
    return m, n, algo

def draw(area, screen):
    cols = len(area[0])
    rows = len(area)
    for y in range(rows):
        for x in range(cols):
            v = area[y][x]
            if v == 1:      color = (  0,   0,   0)   
            elif v == 0:    color = (255, 255, 255)   
            else:           color = (200, 200, 200)   
            rect = pygame.Rect(x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, color, rect)
    pygame.display.flip()

def main():
    if SEED is not None:
        random.seed(SEED)

    rows, cols, algo = get_dimensions()
    width, height = cols*CELL_SIZE, rows*CELL_SIZE

    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Generación de laberinto")

    
    if algo == 1:
        generator = KruskalMaze(rows, cols).generate()
    else:
        generator = PrimMaze(rows, cols).generate()


    for area in generator:
      
        for evt in pygame.event.get():
            if evt.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        draw(area, screen)
        pygame.time.delay(DELAY_MS)

  
    while True:
        for evt in pygame.event.get():
            if evt.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

if __name__ == "__main__":
    main()
