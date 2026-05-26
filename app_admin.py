import streamlit as st
import pandas as pd

from database import (
    crear_tabla,
    desactivar_producto,
    obtener_productos
)

from importador_pdf import (
    importar_pdf,
    guardar_productos
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
# LOGIN SIMPLE
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
# SUBIR PDF
# =========================================

st.header(
    "Importar PDF"
)

pdf_file = st.file_uploader(
    "Subir PDF",
    type=["pdf"]
)

proveedor = st.text_input(
    "Proveedor"
)

# =========================================
# PROCESAR PDF
# =========================================

if pdf_file is not None:

    try:

        productos = importar_pdf(
            pdf_file,
            proveedor
        )

        st.success(
            f"Productos encontrados: "
            f"{len(productos)}"
        )

        # =================================
        # DATAFRAME
        # =================================

        df_preview = pd.DataFrame(
            productos
        )

        # =================================
        # RUBROS EXISTENTES
        # =================================

        rubros_existentes = [

            "LIMPIEZA",
            "PERFUMERIA",
            "QUIMICA",
            "BEBIDAS",
            "PAPELERA",
            "OTROS"
        ]

        # =================================
        # SELECT RUBRO
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
        # VISTA PREVIA
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
        # IMPORTAR
        # =================================

        if st.button(
            "Guardar en Base de Datos"
        ):

            guardar_productos(
                productos,
                proveedor
            )

            st.success(
                "Productos importados"
            )

            st.rerun()

    except Exception as e:

        st.error(
            f"Error procesando PDF: {e}"
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

        "rubro": "Rubro",

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
# DESACTIVAR PRODUCTO
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