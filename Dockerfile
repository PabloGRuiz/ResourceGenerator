# Usamos una imagen oficial de Python basada en Debian Bookworm (que facilita la instalación de dependencias de GUI)
FROM python:3.10-slim-bookworm

# Evitar que Python escriba archivos .pyc y habilitar el buffer de salida para logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instalar dependencias del sistema necesarias para Tkinter/CustomTkinter y X11
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-tk \
    tk-dev \
    libx11-6 \
    libxext6 \
    libxrender1 \
    libxtst6 \
    libxi6 \
    && rm -rf /var/lib/apt/lists/*

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivo de requerimientos
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente del proyecto
COPY src/ ./src/

# Comando por defecto para arrancar la aplicación
CMD ["python", "src/main.py"]
