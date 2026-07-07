# Generador de Assets para Videojuegos

Aplicación de escritorio para la generación de sprites e iconos de videojuegos utilizando IA generativa, optimizada para resoluciones de pixel art.

## Requisitos
- Python 3.10+

## Instalación

1. Clona el repositorio.
2. Crea un entorno virtual e instala las dependencias:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Linux/Mac
   venv\Scripts\activate     # En Windows
   pip install -r requirements.txt
   ```
3. Copia el archivo `.env.example` a `.env` y añade tu token de Hugging Face.

## Ejecución

```bash
python src/main.py
```
