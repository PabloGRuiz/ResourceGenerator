import sys
import os

# Añadir el directorio raíz al path de Python para que pueda importar 'src'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.ui.controller import AppController

def main():
    """
    Punto de entrada principal de la aplicación.
    Inicializa el controlador y arranca la interfaz gráfica.
    """
    try:
        app = AppController()
        app.run()
    except ValueError as e:
        print(f"Error de Configuración: {e}")
        print("Por favor, asegúrate de configurar el archivo .env correctamente.")
    except Exception as e:
        print(f"Error inesperado: {e}")

if __name__ == "__main__":
    main()
