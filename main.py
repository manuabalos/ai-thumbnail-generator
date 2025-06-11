from image_generator import generate_image
from helpers import convert_rgba_to_rgb_tuple, add_text, resize_to_1280x720
import gradio as gr

def create_thumbnail(title, description, use_custom_image, uploaded_image,
                     text_position, text_size, text_color):
    text_color = convert_rgba_to_rgb_tuple(text_color)
    if use_custom_image and uploaded_image is not None:
        base_image = uploaded_image
    else:
        prompt = description
        base_image = generate_image(prompt)

    image_with_text = add_text(base_image.copy(), 
                               text=title, 
                               position=text_position, 
                               size=text_size, 
                               color=text_color)

    # resized_image = resize_to_1280x720(image_with_text.copy())
    return base_image, image_with_text

gr.Interface(
    fn=create_thumbnail,
    inputs=[
        gr.Textbox(label="Título del video"),  # Solo para el texto en la imagen
        gr.Textbox(label="Descripción para la imagen (prompt)"),  # Solo para el prompt
        gr.Checkbox(label="¿Usar imagen personalizada como fondo?"),
        gr.Image(label="Sube tu imagen", type="pil"),
        gr.Radio(["arriba", "medio", "abajo"], label="Ubicación del texto", value="arriba"),
        gr.Radio(["pequeño", "medio", "grande"], label="Tamaño del texto", value="medio"),
        gr.ColorPicker(label="Color del texto", value="#FFFFFF")
    ],
    outputs=[
        gr.Image(type="pil", label="Imagen base generada"),
        gr.Image(type="pil", label="Imagen con texto"),
        # gr.Image(type="pil", label="Imagen redimensionada (1280x720)")
    ],
    title="📸 Generador de Miniaturas con IA"
).launch()