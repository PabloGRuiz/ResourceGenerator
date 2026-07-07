from huggingface_hub import InferenceClient
from PIL import Image

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

    def generate_image(self, prompt: str) -> Image.Image:
        """
        Genera una imagen a partir de un prompt (Llamada bloqueante de red).
        
        Args:
            prompt (str): Descripción de la imagen a generar.
            
        Returns:
            Image.Image: La imagen generada devuelta por la API.
        """
        # Se añade un modificador al prompt para fomentar estilo pixel art por defecto
        enhanced_prompt = f"{prompt}, pixel art style, sprite, clean background, high contrast"
        
        # text_to_image devuelve un objeto PIL.Image
        image = self.client.text_to_image(enhanced_prompt)
        return image
