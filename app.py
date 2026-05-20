import streamlit as st
import pandas as pd
import os

from streamlit_paste_button import paste_image_button

# =========================================
# CONFIGURACIÓN
# =========================================

EXCEL_FILE = "productos-limpieza.xlsx"

IMAGE_FOLDER = "imagenes"

os.makedirs(
    IMAGE_FOLDER,
    exist_ok=True
)

# =========================================
# CONFIG STREAMLIT
# =========================================

st.set_page_config(
    page_title="Catálogo de Productos",
    layout="wide"
)

# =========================================
# CARGAR EXCEL
# =========================================

try:

    df = pd.read_excel(
        EXCEL_FILE
    )

except FileNotFoundError:

    df = pd.DataFrame(
        columns=[
            "Rubro",
            "Descripcion",
            "Precio Compra",
            "Precio Venta",
            "Imagen",
            "Link"
        ]
    )

# =========================================
# ASEGURAR COLUMNAS
# =========================================

columnas_necesarias = [
    "Rubro",
    "Descripcion",
    "Precio Compra",
    "Precio Venta",
    "Imagen",
    "Link"
]

for col in columnas_necesarias:

    if col not in df.columns:

        df[col] = ""

# =========================================
# FORZAR COLUMNAS A TEXTO
# =========================================

df["Imagen"] = df["Imagen"].astype(str)

df["Link"] = df["Link"].astype(str)

# =========================================
# PANEL ADMIN
# =========================================

st.sidebar.title(
    "Panel Administrador"
)

password = st.sidebar.text_input(
    "Contraseña",
    type="password"
)

ADMIN_PASSWORD = "1234"

modo_admin = (
    password == ADMIN_PASSWORD
)

if modo_admin:

    st.sidebar.success(
        "Modo administrador activado"
    )

# =========================================
# AGREGAR PRODUCTO
# =========================================

if modo_admin:

    with st.sidebar.expander(
        "Agregar Producto"
    ):

        with st.form(
            "nuevo_producto"
        ):

            rubro = st.text_input(
                "Rubro"
            )

            descripcion = st.text_input(
                "Descripción"
            )

            precio_compra = st.text_input(
                "Precio Compra"
            )

            precio_venta = st.text_input(
                "Precio Venta"
            )

            link = st.text_input(
                "Link del producto"
            )

            submitted = (
                st.form_submit_button(
                    "Guardar Producto"
                )
            )

            if submitted:

                nueva_fila = {

                    "Rubro": rubro,

                    "Descripcion":
                    descripcion,

                    "Precio Compra":
                    precio_compra,

                    "Precio Venta":
                    precio_venta,

                    "Imagen": "",

                    "Link": link
                }

                df = pd.concat(

                    [
                        df,
                        pd.DataFrame(
                            [nueva_fila]
                        )
                    ],

                    ignore_index=True
                )

                df.to_excel(
                    EXCEL_FILE,
                    index=False
                )

                st.success(
                    "Producto agregado"
                )

# =========================================
# TÍTULO
# =========================================

st.title(
    "Catálogo de Productos"
)

# =========================================
# BUSCADOR
# =========================================

busqueda = st.text_input(
    "Buscar producto"
)

# =========================================
# FILTRAR
# =========================================

if busqueda:

    df_filtrado = df[

        df["Descripcion"]
        .astype(str)
        .str.contains(
            busqueda,
            case=False,
            na=False
        )
    ]

else:

    df_filtrado = df

# =========================================
# MOSTRAR PRODUCTOS
# =========================================

for start in range(
    0,
    len(df_filtrado),
    3
):

    cols = st.columns(3)

    bloque = df_filtrado.iloc[
        start:start + 3
    ]

    for col, (idx, row) in zip(
        cols,
        bloque.iterrows()
    ):

        with col:

            # =========================================
            # IMAGEN
            # =========================================

            imagen = str(
                row["Imagen"]
            ).strip()

            link = str(
                row["Link"]
            ).strip()

            imagen_final = ""

            # =========================================
            # PRIORIZAR IMAGEN LOCAL
            # =========================================

            if (
                imagen
                and imagen.lower() != "nan"
            ):

                imagen_final = imagen

            # =========================================
            # USAR LINK COMO IMAGEN
            # =========================================

            elif (
                link.startswith("http")
                and any(
                    ext in link.lower()
                    for ext in [
                        ".jpg",
                        ".jpeg",
                        ".png",
                        ".webp"
                    ]
                )
            ):

                imagen_final = link

            # =========================================
            # MOSTRAR IMAGEN
            # =========================================

            if imagen_final:

                try:

                    st.image(
                        imagen_final,
                        use_container_width=True
                    )

                except:

                    st.warning(
                        "Error cargando imagen"
                    )

            else:

                st.info(
                    "Sin imagen"
                )

            # =========================================
            # INFORMACIÓN
            # =========================================

            st.subheader(
                row["Descripcion"]
            )

            st.write(
                f"Rubro: {row['Rubro']}"
            )

            st.write(
                f"Precio Venta: "
                f"${row['Precio Venta']}"
            )

            # =========================================
            # LINK PRODUCTO
            # =========================================

            if (
                link
                and link.lower() != "nan"
                and not any(
                    ext in link.lower()
                    for ext in [
                        ".jpg",
                        ".jpeg",
                        ".png",
                        ".webp"
                    ]
                )
            ):

                st.caption(link)

            # =========================================
            # ADMIN TARJETA
            # =========================================

            if modo_admin:

                st.markdown(
                    "### Editar Producto"
                )

                nuevo_link = st.text_input(
                    "Link",
                    value=link,
                    key=f"link_{idx}"
                )

                # =========================================
                # PEGAR IMAGEN
                # =========================================

                st.markdown(
                    "### 📋 Pegá imagen "
                    "(Ctrl + V)"
                )

                paste_result = (
                    paste_image_button(
                        label=
                        "Pegar imagen",
                        key=f"paste_{idx}"
                    )
                )

                nueva_imagen = None

                if (
                    paste_result.image_data
                    is not None
                ):

                    nueva_imagen = (
                        paste_result
                        .image_data
                    )

                    st.success(
                        "Imagen pegada"
                    )

                # =========================================
                # GUARDAR CAMBIOS
                # =========================================

                if st.button(
                    "Guardar Cambios",
                    key=f"save_{idx}"
                ):

                    # =========================================
                    # GUARDAR LINK
                    # =========================================

                    df.at[
                        idx,
                        "Link"
                    ] = nuevo_link

                    # =========================================
                    # GUARDAR IMAGEN
                    # =========================================

                    if (
                        nueva_imagen
                        is not None
                    ):

                        nombre_archivo = (

                            str(
                                row[
                                    "Descripcion"
                                ]
                            )

                            .lower()

                            .replace(
                                " ",
                                "_"
                            )

                            .replace(
                                "/",
                                "_"
                            )

                            .replace(
                                "\\",
                                "_"
                            )
                        )

                        nombre_final = (
                            f"{nombre_archivo}.png"
                        )

                        ruta_imagen = (
                            os.path.join(
                                IMAGE_FOLDER,
                                nombre_final
                            )
                        )

                        # =========================================
                        # GUARDAR IMAGEN
                        # =========================================

                        nueva_imagen.save(
                            ruta_imagen
                        )

                        # =========================================
                        # GUARDAR RUTA
                        # =========================================

                        df.at[
                            idx,
                            "Imagen"
                        ] = ruta_imagen

                    # =========================================
                    # GUARDAR EXCEL
                    # =========================================

                    df.to_excel(
                        EXCEL_FILE,
                        index=False
                    )

                    st.success(
                        "Producto actualizado"
                    )

            st.markdown("---")

# =========================================
# TABLA COMPLETA
# =========================================

with st.expander(
    "Ver tabla completa"
):

    st.dataframe(df)