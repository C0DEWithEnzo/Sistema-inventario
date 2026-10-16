import os
from contextlib import contextmanager
from decimal import Decimal, InvalidOperation

import mysql.connector
from flask import (Flask, abort, flash, redirect, render_template, request,
                   url_for)

from db import get_connection

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "cambia-esta-clave-en-produccion")

# Por debajo de este número de unidades un producto se considera con stock bajo
STOCK_BAJO = 5

# Columnas por las que se permite ordenar (lista blanca para evitar inyección SQL)
COLUMNAS_ORDEN = {
    "id": "id",
    "nombre": "nombre",
    "precio": "precio",
    "cantidad": "cantidad",
    "valor": "precio * cantidad",
}

FILTROS_ESTADO = ("todos", "disponible", "bajo", "agotado")


# ---------------------------------------------------------------------------
# Utilidades
# ---------------------------------------------------------------------------
@contextmanager
def cursor(dictionary=True):
    """Abre conexión + cursor, confirma los cambios y siempre cierra."""
    conn = get_connection()
    cur = conn.cursor(dictionary=dictionary)
    try:
        yield cur
        conn.commit()
    finally:
        cur.close()
        conn.close()


def leer_formulario():
    """Valida el formulario de producto. Devuelve (datos, errores)."""
    datos = {
        "nombre": request.form.get("nombre", "").strip(),
        "descripcion": request.form.get("descripcion", "").strip(),
        "precio": request.form.get("precio", "").strip(),
        "cantidad": request.form.get("cantidad", "").strip(),
    }
    errores = []

    if not datos["nombre"]:
        errores.append("El nombre del producto es obligatorio.")
    elif len(datos["nombre"]) > 150:
        errores.append("El nombre no puede superar los 150 caracteres.")

    try:
        precio = Decimal(datos["precio"])
        if precio < 0:
            raise InvalidOperation
        datos["precio"] = precio.quantize(Decimal("0.01"))
    except InvalidOperation:
        errores.append("El precio debe ser un número igual o mayor a 0.")

    try:
        cantidad = int(datos["cantidad"])
        if cantidad < 0:
            raise ValueError
        datos["cantidad"] = cantidad
    except ValueError:
        errores.append("La cantidad debe ser un número entero igual o mayor a 0.")

    return datos, errores


# ---------------------------------------------------------------------------
# Rutas
# ---------------------------------------------------------------------------
@app.route("/")
def index():
    q = request.args.get("q", "").strip()
    estado = request.args.get("estado", "todos")
    orden = request.args.get("orden", "id")
    direccion = request.args.get("dir", "desc")

    if estado not in FILTROS_ESTADO:
        estado = "todos"
    if orden not in COLUMNAS_ORDEN:
        orden = "id"
    if direccion not in ("asc", "desc"):
        direccion = "desc"

    condiciones, params = [], []
    if q:
        condiciones.append("(nombre LIKE %s OR descripcion LIKE %s)")
        params += [f"%{q}%", f"%{q}%"]
    if estado == "agotado":
        condiciones.append("cantidad = 0")
    elif estado == "bajo":
        condiciones.append("cantidad > 0 AND cantidad < %s")
        params.append(STOCK_BAJO)
    elif estado == "disponible":
        condiciones.append("cantidad >= %s")
        params.append(STOCK_BAJO)

    sql = "SELECT * FROM productos"
    if condiciones:
        sql += " WHERE " + " AND ".join(condiciones)
    sql += f" ORDER BY {COLUMNAS_ORDEN[orden]} {direccion.upper()}"
    if orden != "id":
        sql += ", id DESC"  # desempate estable

    with cursor() as cur:
        cur.execute(sql, params)
        productos = cur.fetchall()

        # Las métricas siempre reflejan TODO el inventario, no solo lo filtrado
        cur.execute(
            """
            SELECT COUNT(*)                                        AS total,
                   COALESCE(SUM(precio * cantidad), 0)             AS valor,
                   COALESCE(SUM(cantidad = 0), 0)                  AS agotados,
                   COALESCE(SUM(cantidad > 0 AND cantidad < %s), 0) AS bajos,
                   COALESCE(SUM(cantidad), 0)                      AS unidades
            FROM productos
            """,
            (STOCK_BAJO,),
        )
        fila = cur.fetchone()

    stats = {
        "total": int(fila["total"]),
        "valor": fila["valor"],
        "agotados": int(fila["agotados"]),
        "bajos": int(fila["bajos"]),
        "unidades": int(fila["unidades"]),
    }
    stats["disponibles"] = stats["total"] - stats["agotados"] - stats["bajos"]

    return render_template(
        "index.html",
        productos=productos,
        stats=stats,
        q=q,
        estado=estado,
        orden=orden,
        direccion=direccion,
        stock_bajo=STOCK_BAJO,
    )


@app.route("/agregar", methods=["GET", "POST"])
def agregar():
    producto = {"nombre": "", "descripcion": "", "precio": "", "cantidad": ""}

    if request.method == "POST":
        producto, errores = leer_formulario()
        if errores:
            for e in errores:
                flash(e, "error")
        else:
            with cursor(dictionary=False) as cur:
                cur.execute(
                    "INSERT INTO productos (nombre, descripcion, precio, cantidad) "
                    "VALUES (%s, %s, %s, %s)",
                    (producto["nombre"], producto["descripcion"],
                     producto["precio"], producto["cantidad"]),
                )
            flash(f"Producto «{producto['nombre']}» agregado al inventario.", "success")
            return redirect(url_for("index"))

    return render_template("agregar.html", producto=producto, stock_bajo=STOCK_BAJO)


@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    if request.method == "POST":
        datos, errores = leer_formulario()
        if errores:
            for e in errores:
                flash(e, "error")
            datos["id"] = id
            return render_template("editar.html", producto=datos, stock_bajo=STOCK_BAJO)

        with cursor(dictionary=False) as cur:
            cur.execute(
                "UPDATE productos SET nombre=%s, descripcion=%s, precio=%s, cantidad=%s "
                "WHERE id=%s",
                (datos["nombre"], datos["descripcion"], datos["precio"],
                 datos["cantidad"], id),
            )
        flash(f"Producto «{datos['nombre']}» actualizado correctamente.", "success")
        return redirect(url_for("index"))

    with cursor() as cur:
        cur.execute("SELECT * FROM productos WHERE id = %s", (id,))
        producto = cur.fetchone()
    if producto is None:
        abort(404)
    return render_template("editar.html", producto=producto, stock_bajo=STOCK_BAJO)


@app.route("/eliminar/<int:id>", methods=["POST"])
def eliminar(id):
    with cursor() as cur:
        cur.execute("SELECT nombre FROM productos WHERE id = %s", (id,))
        producto = cur.fetchone()
        if producto is None:
            abort(404)
        cur.execute("DELETE FROM productos WHERE id = %s", (id,))
    flash(f"Producto «{producto['nombre']}» eliminado.", "success")
    return redirect(url_for("index"))


# ---------------------------------------------------------------------------
# Errores
# ---------------------------------------------------------------------------
@app.errorhandler(404)
def no_encontrado(_e):
    return render_template(
        "error.html",
        codigo=404,
        titulo="Página no encontrada",
        mensaje="El producto o la página que buscas no existe o fue eliminado.",
    ), 404


@app.errorhandler(mysql.connector.Error)
def error_db(_e):
    return render_template(
        "error.html",
        codigo=500,
        titulo="No se pudo conectar con la base de datos",
        mensaje="Verifica que MySQL esté en ejecución y que las credenciales en db.py sean correctas.",
    ), 500


if __name__ == "__main__":
    app.run(debug=True)
