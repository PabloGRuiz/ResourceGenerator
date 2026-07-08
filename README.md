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

## Ejecución con Docker (GUI en Windows)

Dado que es una aplicación de interfaz gráfica (GUI), el contenedor Docker necesita comunicarse con el servidor de pantalla de tu host (Windows).

### Opción A: Usando VcXsrv (X Server para Windows)

1. Descarga e instala [VcXsrv](https://sourceforge.net/projects/vcxsrv/).
2. Inicia **XLaunch** con la siguiente configuración:
   - Elige **Multiple windows**.
   - Configura Display number como `0`.
   - Deja en **Start no client**.
   - **IMPORTANTE**: Marca la casilla **"Disable access control"** (esto permite que Docker se conecte).
3. Asegúrate de tener el archivo `.env` configurado en la raíz del proyecto.
4. Levanta el contenedor:
   ```bash
   docker-compose up --build
   ```

### Opción B: Usando WSLg (si ejecutas Docker Desktop con backend WSL2)

Si ejecutas los comandos desde dentro de tu terminal de WSL2 (Ubuntu, Debian, etc.), WSLg mapea la pantalla automáticamente:

Modifica tu `docker-compose.yml` para compartir el socket X11 de WSL:
```yaml
    environment:
      - DISPLAY=${DISPLAY}
    volumes:
      - /tmp/.X11-unix:/tmp/.X11-unix
      - ./.env:/app/.env
```
Y ejecuta:
```bash
docker-compose up --build
```

