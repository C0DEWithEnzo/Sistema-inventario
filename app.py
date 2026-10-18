import csv
import io
import os
from contextlib import contextmanager
from decimal import Decimal, InvalidOperation

import mysql.connector
from flask import (Flask, Response, abort, flash, redirect, render_template,
                   request, url_for)

from db import get_connection

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-prod")

STOCK_BAJO = 5
POR_PAGINA = 8

COLUMNAS_ORDEN = {
    "id": "p.id",
    "nombre": "p.nombre",
    "precio": "p.precio",
    "cantidad": "p.cantidad",
    "valor": "p.precio * p.cantidad",
    "categoria": "c.nombre",
}

FILTROS_ESTADO = ("todos", "disponible", "bajo", "agotado")


@contextmanager
def cursor(dictionary=True):
    conn = get_connection()
    cur = conn.cursor(dictionary=dictionary)
    try:
        yield cur
        conn.commit()
    finally:
        cur.close()
        conn.close()


def obtener_categorias():
    with cursor() as cur:
        cur.execute("SELECT * FROM categorias ORDER BY nombre ASC")
        return cur.fetchall()


def leer_formulario():
    datos = {
        "nombre": request.form.get("nombre", "").strip(),
        "descripcion": request.form.get("descripcion", "").strip(),
        "precio": request.form.get("precio", "").strip(),
        "cantidad": request.form.get("cantidad", "").strip(),
        "categoria_id": request.form.get("categoria_id", "").strip(),
    }
    errores = []

    if not datos["nombre"]:
        errores.append("El nombre del producto es obligatorio.")

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
        errores.append("La cantidad debe ser un número entero mayor o igual a 0.")

    datos["categoria_id"] = int(datos["categoria_id"]) if datos["categoria_id"].isdigit() else None
    return datos, errores


@app.route("/")
def index():
    q = request.args.get("q", "").strip()
    estado = request.args.get("estado", "todos")
    categoria_id = request.args.get("categoria_id", "")
    orden = request.args.get("orden", "id")
    direccion = request.args.get("dir", "desc")
    pagina = max(1, request.args.get("pagina", 1, type=int))

    condiciones, params = [], []
    if q:
        condiciones.append("(p.nombre LIKE %s OR p.descripcion LIKE %s)")
        params += [f"%{q}%", f"%{q}%"]
    if estado == "agotado":
        condiciones.append("p.cantidad = 0")
    elif estado == "bajo":
        condiciones.append("p.cantidad > 0 AND p.cantidad < %s")
        params.append(STOCK_BAJO)
    elif estado == "disponible":
        condiciones.append("p.cantidad >= %s")
        params.append(STOCK_BAJO)

    if categoria_id.isdigit():
        condiciones.append("p.categoria_id = %s")
        params.append(int(categoria_id))

    where_clause = (" WHERE " + " AND ".join(condiciones)) if condiciones else ""
    order_col = COLUMNAS_ORDEN.get(orden, "p.id")
    dir_sql = "ASC" if direccion == "asc" else "DESC"

    with cursor() as cur:
        # Paginación
        cur.execute(f"SELECT COUNT(*) as total FROM productos p{where_clause}", params)
        total_filtrados = cur.fetchone()["total"]
        total_paginas = max(1, (total_filtrados + POR_PAGINA - 1) // POR_PAGINA)
        pagina = min(pagina, total_paginas)
        offset = (pagina - 1) * POR_PAGINA

        sql = f"""
            SELECT p.*, c.nombre AS categoria_nombre 
            FROM productos p
            LEFT JOIN categorias c ON p.categoria_id = c.id
            {where_clause}
            ORDER BY {order_col} {dir_sql}, p.id DESC
            LIMIT %s OFFSET %s
        """
        cur.execute(sql, params + [POR_PAGINA, offset])
        productos = cur.fetchall()

        # Métricas Generales
        cur.execute("""
            SELECT COUNT(*) AS total,
                   COALESCE(SUM(precio * cantidad), 0) AS valor,
                   COALESCE(SUM(cantidad = 0), 0) AS agotados,
                   COALESCE(SUM(cantidad > 0 AND cantidad < %s), 0) AS bajos,
                   COALESCE(SUM(cantidad), 0) AS unidades
            FROM productos
        """, (STOCK_BAJO,))
        stats = cur.fetchone()

    stats["disponibles"] = stats["total"] - stats["agotados"] - stats["bajos"]

    return render_template(
        "index.html",
        productos=productos,
        stats=stats,
        categorias=obtener_categorias(),
        q=q,
        estado=estado,
        categoria_id=categoria_id,
        orden=orden,
        direccion=direccion,
        pagina=pagina,
        total_paginas=total_paginas,
        stock_bajo=STOCK_BAJO,
    )


@app.route("/exportar/csv")
def exportar_csv():
    with cursor() as cur:
        cur.execute("""
            SELECT p.id, p.nombre, c.nombre AS categoria, p.precio, p.cantidad, (p.precio * p.cantidad) AS valor_total
            FROM productos p
            LEFT JOIN categorias c ON p.categoria_id = c.id
            ORDER BY p.id ASC
        """)
        productos = cur.fetchall()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "Producto", "Categoría", "Precio ($)", "Stock", "Valor Total ($)"])

    for p in productos:
        writer.writerow([p["id"], p["nombre"], p["categoria"] or "Sin categoría", p["precio"], p["cantidad"], p["valor_total"]])

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=inventario.csv"}
    )


@app.route("/agregar", methods=["GET", "POST"])
def agregar():
    producto = {"nombre": "", "descripcion": "", "precio": "", "cantidad": "", "categoria_id": ""}
    if request.method == "POST":
        producto, errores = leer_formulario()
        if errores:
            for e in errores:
                flash(e, "error")
        else:
            with cursor(dictionary=False) as cur:
                cur.execute(
                    "INSERT INTO productos (nombre, descripcion, precio, cantidad, categoria_id) "
                    "VALUES (%s, %s, %s, %s, %s)",
                    (producto["nombre"], producto["descripcion"], producto["precio"], producto["cantidad"], producto["categoria_id"]),
                )
            flash(f"Producto «{producto['nombre']}» agregado.", "success")
            return redirect(url_for("index"))

    return render_template("agregar.html", producto=producto, categorias=obtener_categorias(), stock_bajo=STOCK_BAJO)


@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    if request.method == "POST":
        datos, errores = leer_formulario()
        if errores:
            for e in errores:
                flash(e, "error")
            datos["id"] = id
            return render_template("editar.html", producto=datos, categorias=obtener_categorias(), stock_bajo=STOCK_BAJO)

        with cursor(dictionary=False) as cur:
            cur.execute(
                "UPDATE productos SET nombre=%s, descripcion=%s, precio=%s, cantidad=%s, categoria_id=%s WHERE id=%s",
                (datos["nombre"], datos["descripcion"], datos["precio"], datos["cantidad"], datos["categoria_id"], id),
            )
        flash(f"Producto «{datos['nombre']}» actualizado.", "success")
        return redirect(url_for("index"))

    with cursor() as cur:
        cur.execute("SELECT * FROM productos WHERE id = %s", (id,))
        producto = cur.fetchone()

    if not producto:
        abort(404)
    return render_template("editar.html", producto=producto, categorias=obtener_categorias(), stock_bajo=STOCK_BAJO)


@app.route("/eliminar/<int:id>", methods=["POST"])
def eliminar(id):
    with cursor() as cur:
        cur.execute("DELETE FROM productos WHERE id = %s", (id,))
    flash("Producto eliminado correctamente.", "success")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)