import streamlit as st
import pandas as pd

from rapidfuzz import fuzz

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
# CARGAR CSS
# =========================================

def cargar_css():

    with open("styles/styles.css") as f:

        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

cargar_css()

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
# TITULO
# =========================================

st.markdown(
    """
    <div class="main-title">
        LA DIAGONAL
        <br><span class="distribuidora">DISTRIBUIDORA</span>
    </div>
    <br><span class="lista-precios">Lista de Precios</span>
    """,
    unsafe_allow_html=True
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
# FILTRAR RUBRO
# =========================================

if rubro_seleccionado != "TODOS":

    df = df[
        df["rubro"]
        == rubro_seleccionado
    ]

# =========================================
# BUSCADOR
# =========================================

busqueda = st.text_input(
    "",
    placeholder="🔍 Buscar producto..."
)

# =========================================
# BÚSQUEDA INTELIGENTE
# =========================================

if busqueda.strip() != "":

    texto_busqueda = (
        busqueda
        .strip()
        .upper()
    )

    resultados = []

    for _, row in df.iterrows():

        descripcion = str(
            row["descripcion"]
        ).upper()

        rubro = str(
            row["rubro"]
        ).upper()

        score_descripcion = fuzz.partial_ratio(
            texto_busqueda,
            descripcion
        )

        score_rubro = fuzz.partial_ratio(
            texto_busqueda,
            rubro
        )

        score = max(
            score_descripcion,
            score_rubro
        )

        if score >= 60:

            resultados.append({

                "score": score,

                "descripcion":
                row["descripcion"],

                "precio_venta":
                row["precio_venta"],

                "rubro":
                row["rubro"]
            })

    df = pd.DataFrame(
        resultados
    )

    if not df.empty:

        df = df.sort_values(
            by="score",
            ascending=False
        )

else:

    df = df.sort_values(
        by=[
            "rubro",
            "descripcion"
        ]
    )

# =========================================
# TABLA CLIENTE
# =========================================

if not df.empty:

    st.dataframe(

        df[
            [
                "descripcion",
                "precio_venta"
            ]
        ],

        column_config={

            "descripcion":
            "Descripción",

            "precio_venta":
            st.column_config.NumberColumn(

                "Precio",

                format="$ %.0f"
            )
        },

        use_container_width=True,

        hide_index=True,

        height=700
    )

else:

    st.warning(
        "No se encontraron productos"
    )

# =========================================
# TOTAL PRODUCTOS
# =========================================

st.caption(
    f"Productos encontrados: {len(df)}"
)
