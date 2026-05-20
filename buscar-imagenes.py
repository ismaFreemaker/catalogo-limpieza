import os
import re
import pandas as pd
from icrawler.builtin import BingImageCrawler

# =========================
# CONFIGURACIÓN
# =========================

EXCEL_FILE = "productos-limpieza.xlsx"
IMAGE_FOLDER = "imagenes"

# Nombre exacto de la columna del Excel
PRODUCT_COLUMN = "Descripcion"

# =========================
# CREAR CARPETA  DE IMÁGENES
# =========================

os.makedirs(IMAGE_FOLDER, exist_ok=True)

# =========================
# LEER EXCEL
# =========================

df = pd.read_excel(EXCEL_FILE)

# Crear columna Imagen si no existe
if "Imagen" not in df.columns:
    df["Imagen"] = ""

# =========================
# FUNCIÓN PARA LIMPIAR NOMBRES
# =========================

def limpiar_nombre(nombre):
    nombre = str(nombre).lower()
    nombre = re.sub(r'[^a-zA-Z0-9]+', '-', nombre)
    return nombre.strip("-")

# =========================
# DESCARGAR IMÁGENES
# =========================

for i, row in df.iterrows():

    producto = str(row[PRODUCT_COLUMN]).strip()

    if not producto:
        continue

    nombre_archivo = limpiar_nombre(producto)
    ruta_imagen = os.path.join(IMAGE_FOLDER, f"{nombre_archivo}.jpg")

    # Si ya existe, no descargar de nuevo
    if os.path.exists(ruta_imagen):
        print(f"Ya existe: {producto}")
        df.at[i, "Imagen"] = ruta_imagen
        continue

    print(f"Buscando imagen para: {producto}")

    try:

        crawler = BingImageCrawler(
            storage={"root_dir": IMAGE_FOLDER}
        )

        crawler.crawl(
            keyword=f"{producto} envase producto limpieza supermercado botella",
            max_num=3
        )

        # Buscar la imagen descargada más reciente
        archivos = sorted(
            [os.path.join(IMAGE_FOLDER, f) for f in os.listdir(IMAGE_FOLDER)],
            key=os.path.getmtime,
            reverse=True
        )

        if archivos:
            ultima = archivos[0]

            # Renombrar
            os.rename(ultima, ruta_imagen)

            # Guardar ruta en Excel
            df.at[i, "Imagen"] = ruta_imagen

            print(f"OK -> {ruta_imagen}")

    except Exception as e:
        print(f"Error con {producto}: {e}")

# =========================
# GUARDAR EXCEL NUEVO
# =========================

OUTPUT_FILE = "productos-limpieza-con-imagenes.xlsx"

df.to_excel(OUTPUT_FILE, index=False)

print("\nProceso terminado.")
print(f"Nuevo archivo guardado como: {OUTPUT_FILE}")
