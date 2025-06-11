import re
from PIL import Image, ImageStat, ImageDraw, ImageFont

def resize_to_1280x720(image: Image.Image) -> Image.Image:
    return image.resize((1280, 720), resample=Image.Resampling.LANCZOS)

def es_fondo_oscuro(image: Image.Image, box: tuple) -> bool:
    """
    Determina si una zona es oscura basándose en su brillo promedio:
    1. Analizar la zona donde se colocará el texto.
    2. Calcular su brillo promedio.
    3. Elegir automáticamente blanco o negro para el texto principal y su sombra.
    """
    area = image.crop(box).convert("L")  # Convert to grayscale
    stat = ImageStat.Stat(area)
    avg_brightness = stat.mean[0]  # 0 (black) to 255 (white)
    return avg_brightness < 127  # Threshold: 127 = middle

def convert_rgba_to_rgb_tuple(color_rgba):
    # If hexadecimal.
    if isinstance(color_rgba, str) and color_rgba.startswith("#"):
        color_hex = color_rgba.lstrip('#')
        r, g, b = tuple(int(color_hex[i:i+2], 16) for i in (0, 2, 4))
        return (r, g, b, 255)
    # If string like "rgba(r, g, b, a)".
    if isinstance(color_rgba, str) and color_rgba.startswith("rgba"):
        # Extract numbers using regex.
        values = re.findall(r"[\d.]+", color_rgba)
        r, g, b = [int(float(x)) for x in values[:3]]
        a = int(float(values[3]) * 255) if len(values) > 3 else 255
        return (r, g, b, a)
    # If tuple/list like (r, g, b, a).
    if isinstance(color_rgba, (tuple, list)):
        r, g, b = [int(float(x)) for x in color_rgba[:3]]
        a = int(float(color_rgba[3]) * 255) if len(color_rgba) > 3 and color_rgba[3] <= 1 else int(color_rgba[3]) if len(color_rgba) > 3 else 255
        return (r, g, b, a)
    # Any other case, default to white.
    return (255, 255, 255, 255)

def add_text(image: Image.Image, text: str, position: str = "arriba", 
                  size: str = "medio", color: str = "white") -> Image.Image:
    draw = ImageDraw.Draw(image)
    w, h = image.size

    # Tamaño de fuente según selección.
    scale_size = {
        "pequeño": 0.03,
        "medio": 0.045,
        "grande": 0.06
    }
    font_size = int(w * scale_size.get(size, 0.045))

    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", font_size)
    except:
        font = ImageFont.load_default(size=font_size)

    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]

    x = (w - tw) // 2
    y = {
        "arriba": int(h * 0.05),
        "medio": (h - th) // 2,
        "abajo": int(h * 0.85 - th)
    }.get(position, int(h * 0.05))

    # Fondo translúcido detrás del texto.
    padding = 20
    background = Image.new("RGBA", image.size, (0, 0, 0, 0))
    background_draw = ImageDraw.Draw(background)
    background_draw.rectangle(
        [
            x + bbox[0] - padding,
            y + bbox[1] - padding,
            x + bbox[2] + padding,
            y + bbox[3] + padding
        ],
        fill=(0, 0, 0, 180)
    )
    image = image.convert("RGBA")
    image = Image.alpha_composite(image, background)

    # Sombra + texto principal.
    draw = ImageDraw.Draw(image)
    draw.text((x+2, y+2), text, font=font, fill="black" if color != "black" else "white")
    draw.text((x, y), text, font=font, fill=color)

    return image.convert("RGB")