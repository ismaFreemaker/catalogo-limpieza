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

    try:

        with open(
            "styles/styles.css",
            encoding="utf-8"
        ) as f:

            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True
            )

    except:
        pass

cargar_css()

# =========================================
# CREAR TABLA
# =========================================

crear_tabla()

# =========================================
# PRODUCTOS
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
    <div style="
        text-align:center;
        margin-bottom:10px;
    ">

        <h1 style="
            margin-bottom:0;
        ">
            LA DIAGONAL
        </h1>

        <h3 style="
            margin-top:0;
            color:#666;
        ">
            DISTRIBUIDORA
        </h3>

    </div>

    <h2>
        Lista de Precios
    </h2>

    <div style="
        color:#666;
        margin-bottom:20px;
    ">
        Precios especiales para comercios.
    </div>
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

rubros.insert(
    0,
    "TODOS"
)

rubro_seleccionado = st.selectbox(
    "Filtrar por rubro",
    rubros
)

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
# BUSQUEDA INTELIGENTE
# =========================================

if busqueda.strip() != "":

    texto_busqueda = (
        busqueda
        .upper()
        .strip()
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

                "id":
                row["id"],

                "rubro":
                row["rubro"],

                "descripcion":
                row["descripcion"],

                "precio_lista":
                row["precio_lista"],

                "precio_venta":
                row["precio_venta"]
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
# LISTA PRODUCTOS
# =========================================

if not df.empty:

    contenedor = st.container(height=650)

    with contenedor:

        for _, row in df.iterrows():

            descripcion = str(
                row["descripcion"]
            )

            precio_actual = float(
                row["precio_venta"]
            )

            precio_anterior = round(
                precio_actual * 1.20
            )

            with st.container(border=True):

                col1, col2 = st.columns(
                    [4, 1]
                )

                with col1:

                    st.markdown(
                        f"**{descripcion}**"
                    )

                with col2:

                    st.markdown(
                        f"### $ {precio_actual:,.0f}"
                    )
                    st.markdown(
                        f"~~$ {precio_anterior:,.0f}~~"
                    )


else:

    st.warning(
        "No se encontraron productos"
    )
# =========================================
# TOTAL
# =========================================

st.caption(
    f"Productos encontrados: {len(df)}"
)