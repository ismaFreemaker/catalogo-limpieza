import pdfplumber
import re

from database import (
    guardar_o_actualizar_producto
)

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
# NORMALIZAR DESCRIPCIÓN
# =========================================

def normalizar_descripcion(
    texto
):

    texto = (
        str(texto)
        .upper()
        .strip()
    )

    texto = re.sub(
        r"\s+",
        " ",
        texto
    )

    return texto

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

                # Necesitamos mínimo 2 precios

                if len(precios) < 2:
                    continue

                # =============================
                # PRECIOS
                # =============================

                precio_lista = limpiar_precio(
                    precios[-2]
                )

                precio_venta = limpiar_precio(
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
                # RUBROS
                # =============================

                rubro = ""

                posibles_rubros = [

                    "QUIMICA",
                    "PERFUMERIA",
                    "LIMPIEZA",
                    "BEBIDAS",
                    "PAPELERA",
                    "ALMACEN"

                ]

                for r in posibles_rubros:

                    if r in texto_sin_precios.upper():

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
                    normalizar_descripcion(
                        texto_sin_precios
                    )
                )

                # =============================
                # VALIDAR
                # =============================

                if (

                    descripcion == ""

                    or precio_venta <= 0

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
                    precio_venta
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

        guardar_o_actualizar_producto(

            rubro=p["rubro"],

            descripcion=
            p["descripcion"],

            precio_lista=
            p["precio_lista"],

            precio_venta=
            p["precio_venta"],

            proveedor=proveedor
        )