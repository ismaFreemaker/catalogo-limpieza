import sqlite3

DB_FILE = "productos.db"

# =========================================
# CONEXIÓN
# =========================================

def conectar():

    conn = sqlite3.connect(DB_FILE)

    return conn

# =========================================
# CREAR TABLA
# =========================================

def crear_tabla():

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute("""

        CREATE TABLE IF NOT EXISTS productos (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            rubro TEXT NOT NULL,

            descripcion TEXT NOT NULL,

            precio_lista REAL,

            precio_venta REAL NOT NULL,

            proveedor TEXT,

            fecha_importacion TEXT,

            activo INTEGER DEFAULT 1
        )

    """)

    conn.commit()

    conn.close()

# =========================================
# OBTENER PRODUCTOS
# =========================================

def obtener_productos():

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT
            id,
            rubro,
            descripcion,
            precio_lista,
            precio_venta

        FROM productos

        WHERE activo = 1

        ORDER BY descripcion

    """)

    productos = cursor.fetchall()

    conn.close()

    return productos

# =========================================
# BUSCAR PRODUCTO
# =========================================

def buscar_producto_por_descripcion(
    descripcion
):

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT id

        FROM productos

        WHERE LOWER(descripcion)
        = LOWER(?)

        LIMIT 1

    """, (descripcion,))

    resultado = cursor.fetchone()

    conn.close()

    return resultado

# =========================================
# ACTUALIZAR PRODUCTO
# =========================================

def actualizar_producto(

    rubro,
    descripcion,
    precio_lista,
    precio_venta,
    proveedor=""

):

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute("""

        UPDATE productos

        SET

            rubro = ?,
            precio_lista = ?,
            precio_venta = ?,
            proveedor = ?,
            activo = 1

        WHERE LOWER(descripcion)
        = LOWER(?)

    """, (

        rubro,
        precio_lista,
        precio_venta,
        proveedor,
        descripcion

    ))

    conn.commit()

    conn.close()

# =========================================
# INSERTAR PRODUCTO
# =========================================

def insertar_producto(

    rubro,
    descripcion,
    precio_lista,
    precio_venta,
    proveedor=""

):

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute("""

        INSERT INTO productos (

            rubro,
            descripcion,
            precio_lista,
            precio_venta,
            proveedor

        )

        VALUES (?, ?, ?, ?, ?)

    """, (

        rubro,
        descripcion,
        precio_lista,
        precio_venta,
        proveedor

    ))

    conn.commit()

    conn.close()

# =========================================
# GUARDAR O ACTUALIZAR
# =========================================

def guardar_o_actualizar_producto(

    rubro,
    descripcion,
    precio_lista,
    precio_venta,
    proveedor=""

):

    producto_existente = (
        buscar_producto_por_descripcion(
            descripcion
        )
    )

    # =====================================
    # SI EXISTE
    # =====================================

    if producto_existente:

        actualizar_producto(

            rubro,
            descripcion,
            precio_lista,
            precio_venta,
            proveedor

        )

    # =====================================
    # SI NO EXISTE
    # =====================================

    else:

        insertar_producto(

            rubro,
            descripcion,
            precio_lista,
            precio_venta,
            proveedor

        )

# =========================================
# DESACTIVAR PRODUCTO
# =========================================

def desactivar_producto(
    id_producto
):

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute("""

        UPDATE productos

        SET activo = 0

        WHERE id = ?

    """, (id_producto,))

    conn.commit()

    conn.close()    


# =========================================
# OBTENER PROVEEDORES
# =========================================

def obtener_proveedores():

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT DISTINCT proveedor

        FROM productos

        WHERE activo = 1

        AND proveedor IS NOT NULL

        AND proveedor != ''

        ORDER BY proveedor

    """)

    proveedores = [

        fila[0]

        for fila in cursor.fetchall()
    ]

    conn.close()

    return proveedores