import pdfplumber
import re

from database import insertar_producto

# =========================================
# LIMPIAR PRECIO
# =========================================

def limpiar_precio(texto):

    texto = (
        str(texto)
        .replace("$", "")
        .replace(".", "")
        .replace(",", ".")
        .strip()
    )

    try:

        return float(texto)

    except:

        return 0

# =========================================
# IMPORTAR PDF
# =========================================

def importar_pdf(
    archivo_pdf,
    proveedor=""
):

    productos = []

    # =====================================
    # ABRIR PDF
    # =====================================

    with pdfplumber.open(
        archivo_pdf
    ) as pdf:

        for pagina in pdf.pages:

            texto = pagina.extract_text()

            if not texto:
                continue

            lineas = texto.split("\n")

            # =================================
            # RECORRER LÍNEAS
            # =================================

            for linea in lineas:

                linea = linea.strip()

                # =============================
                # FILTRAR BASURA
                # =============================

                if (
                    "Listado de productos"
                    in linea
                    or "WhatsApp"
                    in linea
                    or "La Diagonal"
                    in linea
                    or linea == ""
                ):

                    continue

                # =============================
                # BUSCAR PRECIOS
                # =============================

                precios = re.findall(

                    r"\$\s?[\d\.\,]+",

                    linea
                )

                # Necesitamos 2 precios
                # Lista y comercio

                if len(precios) < 2:
                    continue

                # =============================
                # PRECIO COMERCIO
                # =============================

                precio_lista = limpiar_precio(
                    precios[-2]
                )

                precio_comercio = limpiar_precio(
                    precios[-1]
                )

                # =============================
                # QUITAR PRECIOS
                # =============================

                texto_sin_precios = linea

                for p in precios:

                    texto_sin_precios = (
                        texto_sin_precios
                        .replace(p, "")
                    )

                texto_sin_precios = (
                    texto_sin_precios.strip()
                )

                # =============================
                # DETECTAR RUBRO
                # =============================

                rubro = ""

                posibles_rubros = [
                    "QUIMICA",
                    "PERFUMERIA",
                    "LIMPIEZA"
                ]

                for r in posibles_rubros:

                    if r in texto_sin_precios:

                        rubro = r

                        texto_sin_precios = (
                            texto_sin_precios
                            .replace(r, "")
                            .strip()
                        )

                        break

                # =============================
                # DESCRIPCIÓN
                # =============================

                descripcion = (
                    texto_sin_precios
                )

                # =============================
                # VALIDAR
                # =============================

                if (
                    descripcion == ""
                    or precio_comercio <= 0
                ):

                    continue

                # =============================
                # AGREGAR A LISTA
                # =============================

                productos.append({

                    "rubro": rubro,

                    "descripcion":
                    descripcion,

                    "precio_lista":
                    precio_lista,

                    "precio_venta":
                    precio_comercio
                })

    return productos

# =========================================
# GUARDAR PRODUCTOS
# =========================================

def guardar_productos(
    productos,
    proveedor=""
):

    for p in productos:

        insertar_producto(

            rubro=p["rubro"],

            descripcion=
            p["descripcion"],

            precio_lista=
            p["precio_lista"],

            precio_venta=
            p["precio_venta"],

            proveedor=proveedor
        )