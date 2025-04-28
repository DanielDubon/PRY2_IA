# Solución de Laberintos

Este proyecto genera y resuelve laberintos aleatorios utilizando diferentes algoritmos.

## Algoritmos implementados

### Generación de laberintos:
- **Kruskal**: Genera un laberinto mediante el algoritmo de Kruskal adaptado.
- **Prim**: Genera un laberinto mediante el algoritmo de Prim adaptado.

### Resolución de laberintos:
- **BFS (Breadth-First Search)**: Encuentra la ruta más corta, explorando en anchura.
- **DFS (Depth-First Search)**: Explora a lo largo de una rama lo más profundo posible.
- **UCS (Uniform Cost Search)**: Similar a BFS, pero considerando costos uniformes.
- **A* (A-Star)**: Algoritmo de búsqueda informada que utiliza heurística de distancia Manhattan.

## Requisitos

- Python 3.6 o superior
- Pygame

```bash
pip install pygame
```

## Uso paea visualizar laberinto

1. Ejecute el archivo principal para iniciar la aplicación:

```bash
python resolver_laberinto.py
```

2. Siga las instrucciones en la pantalla:
   - Elija un algoritmo para generar el laberinto (Kruskal o Prim)
   - Elija un algoritmo para resolver el laberinto (BFS, DFS, UCS, A*)

3. Observe la visualización:
   - **Negro**: Paredes del laberinto
   - **Blanco**: Caminos transitables
   - **Amarillo**: Nodos explorados durante la búsqueda
   - **Azul**: Camino encontrado de entrada a salida
   - **Rojo**: Punto de entrada
   - **Verde**: Punto de salida

4. Al finalizar, se muestran estadísticas:
   - Longitud del camino encontrado
   - Número de nodos explorados durante la búsqueda

## Estructura del proyecto

- `main.py`: Archivo principal que gestiona la interfaz gráfica
- `Kruskal.py`: Implementación del algoritmo de Kruskal para generación de laberintos
- `prim.py`: Implementación del algoritmo de Prim para generación de laberintos
- `search.py`: Implementación de algoritmos de búsqueda (BFS, DFS, UCS, A*)
- `visualization.py`: Funciones para visualizar el laberinto y la solución
- `solve_maze.py`: Integra generación y resolución de laberintos
- `resolver_laberinto.py`: Script para ejecutar la solución con una interfaz amigable

## Comparación de algoritmos

Para comparar el rendimiento de los diferentes algoritmos, puedes ejecutar múltiples veces la aplicación con diferentes configuraciones. Los algoritmos de búsqueda tienen diferentes características:

- **BFS**: Garantiza la ruta más corta, pero puede explorar muchos nodos.
- **DFS**: No garantiza la ruta más corta, pero puede ser más eficiente en memoria.
- **UCS**: Similar a BFS en laberintos con costos uniformes.
- **A***: Generalmente más eficiente que BFS al utilizar heurística.