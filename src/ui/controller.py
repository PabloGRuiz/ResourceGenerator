import threading
import customtkinter as ctk
from PIL import Image
from src.ai.client import AIClient
from src.core.processing import ImageProcessor
from src.utils.config import Config
from src.ui.app import AppView

class AppController:
    """
    Controlador que orquesta la vista y la lógica de negocio.
    Maneja el threading para evitar congelar la UI de CustomTkinter.
    """
    def __init__(self):
        # Validar la configuración
        Config.validate()
        
        # Inicializar cliente IA
        self.ai_client = AIClient(token=Config.HUGGINGFACE_TOKEN, model_id=Config.MODEL_ID)
        
        # Inicializar Vista
        self.view = AppView(controller=self)
        
    def run(self):
        """Inicia el mainloop de la UI."""
        self.view.mainloop()
        
    def handle_generate_request(self, prompt: str, target_size: tuple[int, int], colors: int):
        """
        Inicia el proceso de generación en un hilo secundario.
        """
        # Actualizar UI a estado de carga
        self.view.set_loading_state()
        
        # Crear y arrancar el hilo
        # Se pasa `daemon=True` para que el hilo muera si se cierra la app
        thread = threading.Thread(
            target=self._generate_task,
            args=(prompt, target_size, colors),
            daemon=True
        )
        thread.start()
        
    def _generate_task(self, prompt: str, target_size: tuple[int, int], colors: int):
        """
        Tarea pesada que corre en el hilo secundario.
        Realiza la llamada de red y el post-procesamiento.
        """
        try:
            # 1. Llamada a la IA (Bloqueante, pero está en otro hilo)
            raw_image = self.ai_client.generate_image(prompt)
            
            # 2. Post-procesamiento local
            processed_image = ImageProcessor.process_pixel_art(
                image=raw_image,
                target_size=target_size,
                colors=colors
            )
            
            # (Opcional) 3. Remoción de fondo
            final_image = ImageProcessor.remove_background_simple(processed_image)
            
            # 4. Actualizar la UI (Thread-safe)
            # CustomTkinter soporta la actualización de propiedades desde hilos, 
            # pero el método recomendado es usar `after` si se altera fuertemente el árbol de widgets.
            self.view.after(0, self._on_generate_success, final_image)
            
        except Exception as e:
            # Enviar el error a la UI principal
            self.view.after(0, self._on_generate_error, str(e))
            
    def _on_generate_success(self, image: Image.Image):
        """Callback llamado desde el hilo principal al terminar con éxito."""
        self.view.set_normal_state()
        self.view.show_status("¡Asset generado con éxito!")
        
        # Escalar la imagen visualmente para que no se vea minúscula en la UI
        # (ej. un sprite de 32x32 lo mostramos a 256x256 en la pantalla usando NEAREST)
        display_img = image.resize((256, 256), resample=Image.Resampling.NEAREST)
        
        # Convertir a formato compatible con CustomTkinter
        ctk_img = ctk.CTkImage(light_image=display_img, dark_image=display_img, size=(256, 256))
        self.view.display_image(ctk_img)

    def _on_generate_error(self, error_message: str):
        """Callback llamado desde el hilo principal si ocurre un error."""
        self.view.set_normal_state()
        self.view.show_status(f"Error: {error_message}", error=True)
