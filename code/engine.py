import torch
from diffusers import StableDiffusionPipeline
import time

class ImageGeneratorEngine:
    """Класс для управления жизненным циклом и инференсом нейросети."""
    
    def __init__(self):
        self.device = "cpu"
        self.model_id = "runwayml/stable-diffusion-v1-5"
        self.pipe = None

    def initialize_model(self):
        """Загрузка весов и настройка оптимизаций."""
        try:
            self.pipe = StableDiffusionPipeline.from_pretrained(
                self.model_id, 
                torch_dtype=torch.float32,
                use_safetensors=True
            )
            self.pipe.to(self.device)
            # Оптимизация памяти (теория в п. 2.5)
            self.pipe.enable_attention_slicing()
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    def generate_image(self, prompt, steps=20):
        """Метод генерации изображения."""
        if self.pipe is None:
            return None
            
        start_time = time.time()
        # Выполнение обратной диффузии
        result = self.pipe(prompt, num_inference_steps=steps)
        image = result.images[0]
        
        elapsed = int(time.time() - start_time)
        return image, elapsed