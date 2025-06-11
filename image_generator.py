# file: generador_imagen.py
# Script para generar una imagen desde un prompt de texto usando Stable Diffusion.

from diffusers import StableDiffusionPipeline
import torch

# Usa la GPU integrada de Mac M1
device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")

# Carga el modelo
pipe = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4")
pipe = pipe.to(device)
pipe.enable_attention_slicing()  # Mejora uso de RAM

def generate_image(prompt: str, pasos: int = 25):
    imagen = pipe(prompt, num_inference_steps=pasos).images[0]
    return imagen
