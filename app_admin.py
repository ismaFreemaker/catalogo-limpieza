import streamlit as st
import pandas as pd
import os

from database import (
    crear_tabla,
    desactivar_producto,
    obtener_productos
    obtener_proveedores,
)

from importador_pdf import (
    importar_pdf,
    guardar_productos
)

from importador_excel import (
    importar_excel,
    guardar_productos_excel
)

# =========================================
# CONFIG
# =========================================

st.set_page_config(
    page_title="Administrador",
    layout="wide"
)

# =========================================
# CREAR TABLA
# =========================================

crear_tabla()

# =========================================
# LOGIN
# =========================================

st.title(
    "Panel Administrador"
)

password = st.text_input(
    "Contraseña",
    type="password"
)

ADMIN_PASSWORD = "1234"

if password != ADMIN_PASSWORD:

    st.warning(
        "Ingresá contraseña"
    )

    st.stop()

# =========================================
# IMPORTADOR
# =========================================

st.header(
    "Importar Archivo"
)

archivo = st.file_uploader(

    "Subir PDF o Excel",

    type=[
        "pdf",
        "xlsx",
        "xls"
    ]
)

proveedor = st.text_input(
    "Proveedor"
)

# =========================================
# PROCESAR ARCHIVO
# =========================================

if archivo is not None:

    try:

        extension = (
            os.path.splitext(
                archivo.name
            )[1]
            .lower()
        )

        productos = []

        # =================================
        # PDF
        # =================================

        if extension == ".pdf":

            productos = importar_pdf(
                archivo,
                proveedor
            )

        # =================================
        # EXCEL
        # =================================

        elif extension in [
            ".xlsx",
            ".xls"
        ]:

            productos = importar_excel(
                archivo,
                proveedor
            )

        # =================================
        # SIN PRODUCTOS
        # =================================

        if len(productos) == 0:

            st.warning(
                "No se encontraron productos"
            )

            st.stop()

        st.success(
            f"Productos encontrados: "
            f"{len(productos)}"
        )

        # =================================
        # DATAFRAME PREVIEW
        # =================================

        df_preview = pd.DataFrame(
            productos
        )

        # =================================
        # RUBROS
        # =================================

        rubros_existentes = [

            "LIMPIEZA",
            "PERFUMERIA",
            "QUIMICA",
            "BEBIDAS",
            "PAPELERA",
            "ALMACEN",
            "OTROS"

        ]

        # =================================
        # RUBRO EXISTENTE
        # =================================

        rubro_seleccionado = st.selectbox(

            "Seleccionar rubro existente",

            [""] + rubros_existentes
        )

        # =================================
        # NUEVO RUBRO
        # =================================

        nuevo_rubro = st.text_input(
            "O escribir nuevo rubro"
        )

        # =================================
        # RUBRO FINAL
        # =================================

        rubro_general = ""

        if nuevo_rubro.strip() != "":

            rubro_general = (
                nuevo_rubro
                .strip()
                .upper()
            )

        else:

            rubro_general = (
                rubro_seleccionado
            )

        # =================================
        # APLICAR RUBRO
        # =================================

        if rubro_general != "":

            df_preview["rubro"] = (
                rubro_general
            )

            for producto in productos:

                producto["rubro"] = (
                    rubro_general
                )

        # =================================
        # PREVIEW
        # =================================

        st.subheader(
            "Vista previa"
        )

        st.data_editor(

            df_preview,

            use_container_width=True,

            hide_index=True
        )

        # =================================
        # GUARDAR
        # =================================

        if st.button(
            "Guardar en Base de Datos"
        ):

            # =============================
            # PDF
            # =============================

            if extension == ".pdf":

                guardar_productos(
                    productos,
                    proveedor
                )

            # =============================
            # EXCEL
            # =============================

            elif extension in [
                ".xlsx",
                ".xls"
            ]:

                guardar_productos_excel(
                    productos,
                    proveedor
                )

            st.success(
                "Base de datos actualizada"
            )

            st.rerun()

    except Exception as e:

        st.error(
            f"Error procesando archivo: {e}"
        )

# =========================================
# PRODUCTOS ACTUALES
# =========================================

st.header(
    "Productos actuales"
)

productos_db = obtener_productos()

df = pd.DataFrame(

    productos_db,

    columns=[
        "id",
        "rubro",
        "descripcion",
        "precio_lista",
        "precio_venta"
    ]
)

# =========================================
# FILTRO PROVEEDOR
# =========================================

proveedores = obtener_proveedores()

proveedor_filtro = st.selectbox(

    "Filtrar por proveedor",

    ["TODOS"] + proveedores
)


# =========================================
# FILTRAR PROVEEDOR
# =========================================

if proveedor_filtro != "TODOS":

    conn_df = pd.read_sql_query(

        f"""

        SELECT
            id,
            rubro,
            descripcion,
            precio_lista,
            precio_venta

        FROM productos

        WHERE activo = 1

        AND proveedor = ?

        """,

        con=__import__("sqlite3")
        .connect("productos.db"),

        params=[proveedor_filtro]
    )

    df = conn_df
# =========================================
# BUSCADOR
# =========================================

busqueda = st.text_input(
    "Buscar producto"
)

if busqueda:

    filtro_descripcion = (

        df["descripcion"]
        .astype(str)
        .str.contains(
            busqueda,
            case=False,
            na=False
        )
    )

    filtro_rubro = (

        df["rubro"]
        .astype(str)
        .str.contains(
            busqueda,
            case=False,
            na=False
        )
    )

    df = df[
        filtro_descripcion
        | filtro_rubro
    ]

# =========================================
# TABLA
# =========================================

st.dataframe(

    df[
        [
            "rubro",
            "descripcion",
            "precio_lista",
            "precio_venta"
        ]
    ],

    column_config={

        "rubro":
        "Rubro",

        "descripcion":
        "Descripción",

        "precio_lista":
        st.column_config.NumberColumn(

            "Precio Lista",

            format="$ %.0f"
        ),

        "precio_venta":
        st.column_config.NumberColumn(

            "Precio Venta",

            format="$ %.0f"
        )
    },

    use_container_width=True,

    hide_index=True
)

# =========================================
# DESACTIVAR
# =========================================

st.subheader(
    "Desactivar producto"
)

id_producto = st.number_input(

    "ID del producto",

    min_value=1,

    step=1
)

if st.button(
    "Desactivar"
):

    desactivar_producto(
        id_producto
    )

    st.success(
        "Producto desactivado"
    )

    st.rerun()