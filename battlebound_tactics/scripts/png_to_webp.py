import os
from PIL import Image

# Rutas a procesar
RUTAS = [
    "static/resources",
    "media/resources"
]

def convertir_png_a_webp_y_eliminar(directorio):
    for root, _, files in os.walk(directorio):
        for file in files:
            if file.lower().endswith(".png"):
                ruta_original = os.path.join(root, file)
                ruta_webp = ruta_original[:-4] + ".webp"

                try:
                    with Image.open(ruta_original) as img:
                        img.save(ruta_webp, "webp", quality=85, method=6)

                    os.remove(ruta_original)  # 🔥 Elimina el PNG original solo si la conversión fue exitosa
                    print(f"✅ Convertido y eliminado: {ruta_original} → {ruta_webp}")
                except Exception as e:
                    print(f"❌ Error con {ruta_original}: {e}")

if __name__ == "__main__":
    for ruta in RUTAS:
        if os.path.exists(ruta):
            convertir_png_a_webp_y_eliminar(ruta)
        else:
            print(f"⚠️ Ruta no encontrada: {ruta}")