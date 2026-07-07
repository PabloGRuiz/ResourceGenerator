import customtkinter as ctk
from PIL import Image

class AppView(ctk.CTk):
    """
    Vista principal de la aplicación.
    Solo se encarga de definir la UI, no contiene lógica de negocio.
    """
    def __init__(self, controller):
        super().__init__()
        
        self.controller = controller
        
        # Configuración básica de la ventana
        self.title("Generador de Assets de Videojuegos")
        self.geometry("600x700")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self._build_ui()
        
    def _build_ui(self):
        """Construye todos los elementos de la interfaz."""
        
        # Título
        self.title_label = ctk.CTkLabel(self, text="Generador de Assets IA", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.pack(pady=(20, 10))
        
        # Prompt Entry
        self.prompt_entry = ctk.CTkTextbox(self, height=100)
        self.prompt_entry.pack(padx=20, pady=10, fill="x")
        self.prompt_entry.insert("0.0", "Escribe tu prompt aquí... (Ej: un cofre del tesoro de oro)")
        
        # Opciones Frame
        self.options_frame = ctk.CTkFrame(self)
        self.options_frame.pack(padx=20, pady=10, fill="x")
        
        # Resolución
        self.res_label = ctk.CTkLabel(self.options_frame, text="Resolución:")
        self.res_label.grid(row=0, column=0, padx=10, pady=10)
        
        self.resolution_var = ctk.StringVar(value="32x32")
        self.res_menu = ctk.CTkOptionMenu(
            self.options_frame, 
            values=["16x16", "32x32", "64x64", "128x128"],
            variable=self.resolution_var
        )
        self.res_menu.grid(row=0, column=1, padx=10, pady=10)
        
        # Colores (Cuantización)
        self.color_label = ctk.CTkLabel(self.options_frame, text="Max Colores:")
        self.color_label.grid(row=0, column=2, padx=10, pady=10)
        
        self.color_var = ctk.StringVar(value="32")
        self.color_menu = ctk.CTkOptionMenu(
            self.options_frame, 
            values=["8", "16", "32", "64", "256"],
            variable=self.color_var
        )
        self.color_menu.grid(row=0, column=3, padx=10, pady=10)
        
        # Botón de Generar
        self.generate_btn = ctk.CTkButton(
            self, 
            text="Generar Asset", 
            command=self._on_generate_click,
            height=40,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.generate_btn.pack(pady=20)
        
        # Barra de progreso (indeterminada) para mostrar actividad
        self.progress_bar = ctk.CTkProgressBar(self, mode="indeterminate")
        self.progress_bar.pack(padx=40, pady=10, fill="x")
        self.progress_bar.set(0)
        self.progress_bar.pack_forget() # Ocultar por defecto
        
        # Label de Estado
        self.status_label = ctk.CTkLabel(self, text="Listo.", text_color="gray")
        self.status_label.pack(pady=5)
        
        # Contenedor de Imagen de Resultado
        self.image_label = ctk.CTkLabel(self, text="Sin imagen generada", width=256, height=256, fg_color=("gray75", "gray25"))
        self.image_label.pack(pady=20)
        
    def _on_generate_click(self):
        """Manejador del botón que delega al controlador."""
        prompt = self.prompt_entry.get("0.0", "end").strip()
        if not prompt or prompt == "Escribe tu prompt aquí... (Ej: un cofre del tesoro de oro)":
            self.show_status("Por favor, ingresa un prompt válido.", error=True)
            return
            
        resolution_str = self.resolution_var.get()
        colors = int(self.color_var.get())
        
        # Parsear resolución "32x32" -> (32, 32)
        w, h = map(int, resolution_str.split("x"))
        
        # Delegar al controlador (que maneja el multihilo)
        self.controller.handle_generate_request(prompt, (w, h), colors)
        
    def set_loading_state(self):
        """Actualiza la UI para mostrar que está cargando."""
        self.generate_btn.configure(state="disabled")
        self.progress_bar.pack(padx=40, pady=10, fill="x", before=self.status_label)
        self.progress_bar.start()
        self.show_status("Generando asset... (esto puede tomar hasta 30s)")
        
    def set_normal_state(self):
        """Restaura la UI a su estado normal."""
        self.generate_btn.configure(state="normal")
        self.progress_bar.stop()
        self.progress_bar.pack_forget()
        
    def show_status(self, message: str, error: bool = False):
        """Muestra un mensaje de estado en la UI."""
        color = "red" if error else "green"
        self.status_label.configure(text=message, text_color=color)
        
    def display_image(self, ctk_image: ctk.CTkImage):
        """Muestra la imagen generada en la UI."""
        self.image_label.configure(image=ctk_image, text="")
