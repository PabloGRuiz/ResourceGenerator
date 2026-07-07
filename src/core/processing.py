from PIL import Image

class ImageProcessor:
    """
    Clase encargada de procesar las imágenes generadas, adaptándolas
    a resoluciones de pixel art, reduciendo colores y manejando transparencia.
    """
    
    @staticmethod
    def process_pixel_art(
        image: Image.Image, 
        target_size: tuple[int, int], 
        colors: int = 32
    ) -> Image.Image:
        """
        Procesa una imagen para darle un estilo pixel art estricto.
        
        Args:
            image (Image.Image): La imagen original generada.
            target_size (tuple[int, int]): La resolución objetivo (ej: (32, 32)).
            colors (int): Número de colores a indexar en la paleta.
            
        Returns:
            Image.Image: La imagen post-procesada.
        """
        # 1. Redimensionar usando interpolación Nearest Neighbor (estricto para pixel art)
        resized_img = image.resize(target_size, resample=Image.Resampling.NEAREST)
        
        # 2. Cuantización de color (Reducir la paleta)
        quantized_img = resized_img.quantize(colors=colors)
        
        # Convertir de vuelta a RGBA si se necesita manipular canal alfa más adelante
        final_img = quantized_img.convert("RGBA")
        
        return final_img

    @staticmethod
    def remove_background_simple(image: Image.Image, bg_color: tuple[int, int, int] = (255, 255, 255)) -> Image.Image:
        """
        Elimina el fondo de una imagen basado en un color sólido de fondo,
        convirtiéndolo a transparente.
        
        Args:
            image (Image.Image): La imagen a procesar (debe estar en modo RGBA).
            bg_color (tuple): Color de fondo a remover (R, G, B).
            
        Returns:
            Image.Image: Imagen con fondo transparente.
        """
        img = image.convert("RGBA")
        datas = img.getdata()
        
        new_data = []
        for item in datas:
            # Si el pixel coincide con el color de fondo (ignorando alfa por ahora)
            if item[:3] == bg_color:
                # Cambiar a transparente
                new_data.append((255, 255, 255, 0))
            else:
                new_data.append(item)
                
        img.putdata(new_data)
        return img
