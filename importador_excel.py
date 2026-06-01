import pandas as pd
import re

from database import (
    guardar_o_actualizar_producto
)

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
        archivo_excel
    )

    # =====================================
    # NORMALIZAR COLUMNAS
    # =====================================

    df.columns = [

        str(col)
        .strip()
        .lower()
        .replace(" ", "_")

        for col in df.columns
    ]

    # =====================================
    # MAPEO FLEXIBLE
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
        "Lista1"
        

    ]

    posibles_precio_venta = [

        "precio_venta",
        "precio",
        "precio_final",
        "pventa"

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

    col_precio_venta = next(

        (
            c for c in posibles_precio_venta
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

    if not col_precio_venta:

        raise Exception(
            "No se encontró columna precio"
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
        # DESCRIPCIÓN
        # =================================

        descripcion = (
            normalizar_descripcion(
                row[col_descripcion]
            )
        )

        # =================================
        # PRECIOS
        # =================================

        precio_lista = 0

        if col_precio_lista:

            precio_lista = limpiar_precio(
                row[col_precio_lista]
            )

        precio_venta = limpiar_precio(
            row[col_precio_venta]
        )

        # =================================
        # VALIDAR
        # =================================

        if (

            descripcion == ""

            or precio_venta <= 0

        ):

            continue

        # =================================
        # AGREGAR A LISTA
        # =================================

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