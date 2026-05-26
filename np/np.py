import streamlit as st
import pandas as pd
import os
from PIL import Image

# =========================================
# CONFIGURACIÓN
# =========================================

EXCEL_FILE = "productos-limpieza.xlsx"
IMAGE_FOLDER = "imagenes"

os.makedirs(IMAGE_FOLDER, exist_ok=True)

# =========================================
# CARGAR EXCEL
# =========================================

try:
    df = pd.read_excel(EXCEL_FILE)

except FileNotFoundError:

    df = pd.DataFrame(columns=[
        "Rubro",
        "Descripcion",
        "Precio Compra",
        "Precio Venta",
        "Imagen",
        "Link"
    ])

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
# SIDEBAR ADMIN
# =========================================

st.title("Catálogo de Productos")

st.subheader("Acceso Administrador")

password = st.text_input(
    "Contraseña",
    type="password"
)

ADMIN_PASSWORD = "1234"

modo_admin = password == ADMIN_PASSWORD

# =========================================
# PANEL ADMIN
# =========================================

if modo_admin:

    st.sidebar.success("Modo administrador activado")

    st.header("Agregar Producto")

    with st.form("form_producto"):

        rubro = st.text_input("Rubro")

        descripcion = st.text_input("Descripción")

        precio_compra = st.text_input("Precio Compra")

        precio_venta = st.text_input("Precio Venta")

        link = st.text_input("Link del producto")

        imagen = st.file_uploader(
            "Subir imagen",
            type=["png", "jpg", "jpeg", "webp"]
        )

        submitted = st.form_submit_button("Guardar Producto")

        if submitted:

            ruta_imagen = ""

            # =========================================
            # GUARDAR IMAGEN
            # =========================================

            if imagen is not None:

                nombre_archivo = (
                    descripcion
                    .lower()
                    .replace(" ", "_")
                    .replace("/", "_")
                )

                extension = imagen.name.split(".")[-1]

                nombre_final = f"{nombre_archivo}.{extension}"

                ruta_imagen = os.path.join(
                    IMAGE_FOLDER,
                    nombre_final
                )

                with open(ruta_imagen, "wb") as f:
                    f.write(imagen.getbuffer())

            # =========================================
            # AGREGAR FILA
            # =========================================

            nueva_fila = {
                "Rubro": rubro,
                "Descripcion": descripcion,
                "Precio Compra": precio_compra,
                "Precio Venta": precio_venta,
                "Imagen": ruta_imagen,
                "Link": link
            }

            df = pd.concat(
                [df, pd.DataFrame([nueva_fila])],
                ignore_index=True
            )

            # =========================================
            # GUARDAR EXCEL
            # =========================================

            df.to_excel(EXCEL_FILE, index=False)

            st.success("Producto guardado correctamente")

# =========================================
# CATÁLOGO PÚBLICO
# =========================================

st.title("Catálogo de Productos")

busqueda = st.text_input("Buscar producto")

# =========================================
# FILTRAR
# =========================================

if busqueda:

    df_filtrado = df[
        df["Descripcion"]
        .astype(str)
        .str.contains(busqueda, case=False, na=False)
    ]

else:

    df_filtrado = df

# =========================================
# MOSTRAR PRODUCTOS
# =========================================

for start in range(0, len(df_filtrado), 3):

    cols = st.columns(3)

    bloque = df_filtrado.iloc[start:start + 3]

    for col, (_, row) in zip(cols, bloque.iterrows()):

        with col:

            # =========================================
            # IMAGEN
            # =========================================

            ruta = row["Imagen"]

            if isinstance(ruta, str):

                if os.path.exists(ruta):

                    try:

                        img = Image.open(ruta)

                        st.image(
                            img,
                            use_container_width=True
                        )

                    except:
                        st.warning("Error al abrir imagen")

            # =========================================
            # INFO
            # =========================================

            st.subheader(row["Descripcion"])

            st.write(f"Rubro: {row['Rubro']}")

            st.write(
                f"Precio Venta: ${row['Precio Venta']}"
            )

            # =========================================
            # LINK
            # =========================================

            if str(row["Link"]).strip():

                st.link_button(
                    "Ver Producto",
                    row["Link"]
                )

            st.markdown("---")

# =========================================
# TABLA COMPLETA
# =========================================

with st.expander("Ver tabla completa"):

    st.dataframe(df)