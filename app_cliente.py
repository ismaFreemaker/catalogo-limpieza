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

    """
    <h1 style='text-align: center;'>

    La Diagonal Distribuidora
    </h1>

    <h2>
    <span>
    Lista de Precios
    </span>
    </h2>

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
    "Buscar producto"
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

        # =============================
        # SCORE DESCRIPCIÓN
        # =============================

        score_descripcion = fuzz.partial_ratio(
            texto_busqueda,
            descripcion
        )

        # =============================
        # SCORE RUBRO
        # =============================

        score_rubro = fuzz.partial_ratio(
            texto_busqueda,
            rubro
        )

        # =============================
        # MEJOR SCORE
        # =============================

        score = max(
            score_descripcion,
            score_rubro
        )

        # =============================
        # FILTRAR RESULTADOS
        # =============================

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

    # =====================================
    # DATAFRAME RESULTADOS
    # =====================================

    df = pd.DataFrame(
        resultados
    )

    # =====================================
    # ORDENAR POR SIMILITUD
    # =====================================

    if not df.empty:

        df = df.sort_values(
            by="score",
            ascending=False
        )

else:

    # =====================================
    # ORDEN NORMAL
    # =====================================

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