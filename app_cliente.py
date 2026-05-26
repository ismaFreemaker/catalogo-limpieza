import streamlit as st
import pandas as pd

from database import (
    crear_tabla,
    obtener_productos
)

# =========================================
# CONFIG
# =========================================

st.set_page_config(
    page_title="La Diagonal Distribuidora",
    layout="wide"
)

# =========================================
# CREAR TABLA
# =========================================

crear_tabla()

# =========================================
# OBTENER PRODUCTOS
# =========================================

productos = obtener_productos()

df = pd.DataFrame(

    productos,

    columns=[
        "id",
        "rubro",
        "descripcion",
        "precio_lista",
        "precio_venta"
    ]
)

# =========================================
# TÍTULO
# =========================================

st.markdown(
    st.markdown(
    """
    <h1 style='text-align: center;'>

    La Diagonal Distribuidora
    <br>
    <span style='font-size: 40px;'>
    Lista de Precios
    </span>

    </h1>
    """,

    unsafe_allow_html=True
    )
)

# =========================================
# FILTRO RUBRO
# =========================================

rubros = sorted(
    df["rubro"]
    .dropna()
    .unique()
)

rubros.insert(0, "TODOS")

rubro_seleccionado = st.selectbox(
    "Filtrar por rubro",
    rubros
)

# =========================================
# BUSCADOR
# =========================================

busqueda = st.text_input(
    "Buscar producto"
)

# =========================================
# FILTRAR RUBRO
# =========================================

if rubro_seleccionado != "TODOS":

    df = df[
        df["rubro"]
        == rubro_seleccionado
    ]

# =========================================
# FILTRAR BÚSQUEDA
# =========================================

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
# ORDENAR
# =========================================

df = df.sort_values(
    by=[
        "rubro",
        "descripcion"
    ]
)

# =========================================
# TABLA CLIENTE
# =========================================

st.dataframe(

    df[
        [
            "rubro",
            "descripcion",
            "precio_venta"
        ]
    ],

    column_config={

        "rubro": "Rubro",

        "descripcion":
        "Descripción",

        "precio_venta":
        st.column_config.NumberColumn(

            "Precio",

            format="$ %.0f"
        )
    },

    use_container_width=True,

    hide_index=True
)

# =========================================
# TOTAL PRODUCTOS
# =========================================

st.caption(
    f"Productos encontrados: {len(df)}"
)