import pandas as pd

from database import insertar_producto

# =========================================
# IMPORTAR EXCEL
# =========================================

def importar_excel(
    archivo_excel,
    proveedor=""
):

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
        "articulo"
    ]

    posibles_precios = [
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

    col_precio = next(
        (
            c for c in posibles_precios
            if c in df.columns
        ),
        None
    )

    # =====================================
    # VALIDAR
    # =====================================

    if not col_descripcion:

        raise Exception(
            "No se encontró columna descripción"
        )

    if not col_precio:

        raise Exception(
            "No se encontró columna precio"
        )

    # =====================================
    # IMPORTAR FILAS
    # =====================================

    for _, row in df.iterrows():

        rubro = ""

        if col_rubro:

            rubro = str(
                row[col_rubro]
            )

        descripcion = str(
            row[col_descripcion]
        )

        precio = row[col_precio]

        # =================================
        # LIMPIAR
        # =================================

        if (
            descripcion.strip() == ""
            or str(precio).strip() == ""
        ):

            continue

        # =================================
        # INSERTAR
        # =================================

        insertar_producto(

            rubro=rubro,

            descripcion=descripcion,

            precio_venta=precio,

            proveedor=proveedor
        )
        