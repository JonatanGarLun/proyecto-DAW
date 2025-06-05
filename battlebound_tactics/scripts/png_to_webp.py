from PIL import Image
import os

def convert_to_webp(image_path):
    if image_path.endswith('.png'):
        im = Image.open(image_path).convert("RGBA")
        webp_path = image_path.replace(".png", ".webp")
        im.save(webp_path, "WEBP", quality=75, lossless=True)
        print(f"Converted: {webp_path}")
