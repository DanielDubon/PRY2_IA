import sys
from solve_maze import main

if __name__ == "__main__":
    print("-" * 50)
    print("Solución de Laberinto 60x80")
    print("-" * 50)
    print("Este programa genera un laberinto aleatorio y lo resuelve")
    print("usando el algoritmo de búsqueda que elijas.")
    print()
    print("Visualizará el proceso de exploración y el camino encontrado,")
    print("además de mostrar estadísticas sobre el rendimiento.")
    print("-" * 50)
    
    try:
        main()
    except KeyboardInterrupt:
        print("\nPrograma interrumpido por el usuario.")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {str(e)}")
        sys.exit(1) 