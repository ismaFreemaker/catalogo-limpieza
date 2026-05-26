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

    """)

    productos = cursor.fetchall()

    conn.close()

    return productos

# =========================================
# VERIFICAR SI EXISTE
# =========================================

def producto_existe(
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

    return resultado is not None

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

    # =====================================
    # EVITAR DUPLICADOS
    # =====================================

    if producto_existe(
        descripcion
    ):

        return

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