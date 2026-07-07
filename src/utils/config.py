import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

class Config:
    """
    Clase centralizada para gestionar la configuración de la aplicación.
    """
    HUGGINGFACE_TOKEN: str = os.getenv("HUGGINGFACE_TOKEN", "")
    MODEL_ID: str = os.getenv("MODEL_ID", "stabilityai/stable-diffusion-xl-base-1.0")

    @classmethod
    def validate(cls) -> None:
        """
        Valida que las variables de entorno críticas estén configuradas.
        """
        if not cls.HUGGINGFACE_TOKEN:
            raise ValueError("HUGGINGFACE_TOKEN no está configurado en el archivo .env")

# Validar la configuración al importar el módulo
# Config.validate() # Se puede descomentar o llamar en el main para validar en el arranque.
