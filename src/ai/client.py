from huggingface_hub import InferenceClient
from PIL import Image
from deep_translator import GoogleTranslator

class AIClient:
    """
    Cliente para comunicarse con la API de Hugging Face de forma serverless.
    """
    def __init__(self, token: str, model_id: str):
        """
        Inicializa el cliente de Inferencia.
        
        Args:
            token (str): Token de Hugging Face.
            model_id (str): ID del modelo a utilizar.
        """
        self.model_id = model_id
        # Inicializa el cliente serverless de Hugging Face
        self.client = InferenceClient(model=self.model_id, token=token)

    def translate_prompt(self, prompt: str) -> str:
        """
        Traduce el prompt de entrada al inglés si está en otro idioma.
        
        Args:
            prompt (str): Prompt original.
            
        Returns:
            str: Prompt en inglés.
        """
        try:
            # Traduce de forma automática (detectando el idioma de origen) al inglés
            translated = GoogleTranslator(source='auto', target='en').translate(prompt)
            # En caso de que devuelva None o vacío, usamos el original
            return translated if translated else prompt
        except Exception as e:
            # Fallback al prompt original si la traducción falla (ej. sin conexión)
            print(f"Advertencia: Falló la traducción automática ({e}). Usando prompt original.")
            return prompt

    def generate_image(self, prompt: str) -> Image.Image:
        """
        Genera una imagen a partir de un prompt (Llamada bloqueante de red).
        
        Args:
            prompt (str): Descripción de la imagen a generar (soporta español/inglés).
            
        Returns:
            Image.Image: La imagen generada devuelta por la API.
        """
        # Traducir automáticamente al inglés para asegurar la calidad de SDXL
        english_prompt = self.translate_prompt(prompt)
        print(f"Prompt traducido/procesado: '{english_prompt}'")
        
        # Se añade un modificador al prompt para fomentar estilo pixel art por defecto
        enhanced_prompt = f"{english_prompt}, pixel art style, sprite, clean background, high contrast"
        
        # text_to_image devuelve un objeto PIL.Image
        image = self.client.text_to_image(enhanced_prompt)
        return image
