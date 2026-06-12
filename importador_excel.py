import pandas as pd
import re

from database import (
    guardar_o_actualizar_producto
)

# =========================================
# CONFIG DESCUENTO
# =========================================

DESCUENTO_COMERCIO = 0.20

# =========================================
# LIMPIAR PRECIO
# =========================================

def limpiar_precio(valor):

    texto = (
        str(valor)
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
# NORMALIZAR TEXTO
# =========================================

def normalizar_texto(texto):

    texto = (
        str(texto)
        .lower()
        .strip()
    )

    texto = texto.replace(
        " ",
        "_"
    )

    return texto

# =========================================
# NORMALIZAR DESCRIPCION
# =========================================

def normalizar_descripcion(texto):

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
# IMPORTAR EXCEL
# =========================================

def importar_excel(
    archivo_excel,
    proveedor=""
):

    productos = []

    # =====================================
    # LEER EXCEL
    # =====================================

    df = pd.read_excel(
        archivo_excel,
        engine="xlrd"
    )

    # =====================================
    # NORMALIZAR COLUMNAS
    # =====================================

    df.columns = [

        normalizar_texto(col)

        for col in df.columns
    ]

    # =====================================
    # POSIBLES COLUMNAS
    # =====================================

    posibles_rubros = [

        "rubro",
        "categoria",
        "tipo"

    ]

    posibles_descripciones = [

        "descripcion",
        "producto",
        "articulo",
        "detalle"

    ]

    posibles_precio_lista = [

        "precio_lista",
        "precio_costo",
        "lista",
        "lista_1",
        "lista1",
        "precio_lista_1",
        "precio_publico"

    ]

    # =====================================
    # DETECTAR COLUMNAS
    # =====================================

    col_rubro = next(

        (
            c for c in posibles_rubros
            if c in df.columns
        ),

        None
    )

    col_descripcion = next(

        (
            c for c in posibles_descripciones
            if c in df.columns
        ),

        None
    )

    col_precio_lista = next(

        (
            c for c in posibles_precio_lista
            if c in df.columns
        ),

        None
    )

    # =====================================
    # VALIDACIONES
    # =====================================

    if not col_descripcion:

        raise Exception(
            "No se encontró columna descripción"
        )

    if not col_precio_lista:

        raise Exception(
            "No se encontró columna LISTA 1"
        )

    # =====================================
    # RECORRER FILAS
    # =====================================

    for _, row in df.iterrows():

        # =================================
        # RUBRO
        # =================================

        rubro = ""

        if col_rubro:

            rubro = str(
                row[col_rubro]
            ).strip()

        # =================================
        # DESCRIPCION
        # =================================

        descripcion = (
            normalizar_descripcion(
                row[col_descripcion]
            )
        )

        # =================================
        # PRECIO LISTA
        # =================================

        precio_lista = limpiar_precio(
            row[col_precio_lista]
        )

        # =================================
        # PRECIO COMERCIO
        # =================================

        precio_venta = round(

            precio_lista
            * (1 - DESCUENTO_COMERCIO),

            2
        )

        # =================================
        # VALIDAR
        # =================================

        if (

            descripcion == ""

            or precio_lista <= 0

        ):

            continue

        # =================================
        # AGREGAR PRODUCTO
        # =================================

        productos.append({

            "rubro":
            rubro,

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

def guardar_productos_excel(
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
