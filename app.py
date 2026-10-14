"""BiblioTec — aplicación web. NO MODIFICAR durante la actividad.

Ejecutar:   python app.py            -> abre http://127.0.0.1:5000
Reiniciar los datos de ejemplo:  python app.py --reiniciar

La app llama a las funciones de modulos/libros.py, modulos/socios.py y
modulos/prestamos.py. Mientras una función no esté implementada, su
sección muestra "Pendiente" en lugar de romper la página.
"""

import sys
from pathlib import Path
from types import SimpleNamespace

from flask import Flask, flash, redirect, render_template, request, url_for

from modulos import libros, prestamos, socios
from nucleo.config import CATEGORIAS, ORDENES_LIBRO
from nucleo.repositorio import Repositorio
from nucleo.semilla import datos_semilla

RUTA_DATOS = Path(__file__).parent / "datos" / "biblioteca.json"

app = Flask(__name__)
app.secret_key = "bibliotec-psp"


def obtener_repo():
    return Repositorio.desde_archivo(RUTA_DATOS, datos_semilla)


def llamar(funcion, *args, **kwargs):
    """Ejecuta una función de los módulos y atrapa sus errores."""
    try:
        return SimpleNamespace(ok=True, valor=funcion(*args, **kwargs), pendiente=False, error=None)
    except NotImplementedError:
        return SimpleNamespace(ok=False, valor=None, pendiente=True,
                               error=f"{funcion.__name__}() aún está pendiente")
    except ValueError as e:
        return SimpleNamespace(ok=False, valor=None, pendiente=False, error=str(e))
    except Exception as e:  # error inesperado en el código del módulo
        return SimpleNamespace(ok=False, valor=None, pendiente=False,
                               error=f"Error inesperado en {funcion.__name__}(): "
                                     f"{type(e).__name__}: {e}")


def avisar(resultado, mensaje_ok):
    if resultado.ok:
        flash(mensaje_ok, "exito")
    elif resultado.pendiente:
        flash(resultado.error, "pendiente")
    else:
        flash(resultado.error, "error")


@app.context_processor
def globales():
    return {"CATEGORIAS": CATEGORIAS, "ORDENES_LIBRO": ORDENES_LIBRO}


# ---------------------------------------------------------------- inicio
@app.route("/")
def inicio():
    repo = obtener_repo()
    return render_template(
        "inicio.html",
        libros=llamar(libros.listar_libros, repo),
        stats=llamar(socios.estadisticas_socios, repo),
        reporte=llamar(prestamos.reporte_prestamos, repo),
        vencidos=llamar(prestamos.prestamos_vencidos, repo),
    )


# ---------------------------------------------------------------- libros
@app.route("/libros")
def ver_libros():
    repo = obtener_repo()
    q = request.args.get("q", "")
    categoria = request.args.get("categoria", "")
    orden = request.args.get("orden", "")
    if q:
        lista = llamar(libros.buscar_libros, repo, q)
        modo = "buscar_libros()"
    elif categoria or orden:
        lista = llamar(libros.libros_por_categoria, repo, categoria or None, orden or "titulo")
        modo = "libros_por_categoria()"
    else:
        lista = llamar(libros.listar_libros, repo)
        modo = "listar_libros()"
    return render_template("libros.html", lista=lista, modo=modo,
                           q=q, categoria=categoria, orden=orden)


@app.post("/libros/agregar")
def agregar_libro():
    f = request.form
    r = llamar(libros.agregar_libro, obtener_repo(), f.get("titulo", ""), f.get("autor", ""),
               f.get("isbn", ""), f.get("anio", ""), f.get("categoria", ""))
    avisar(r, f"Libro agregado con id {r.valor}")
    return redirect(url_for("ver_libros"))


@app.route("/libros/<int:libro_id>/editar", methods=["GET", "POST"])
def editar_libro(libro_id):
    repo = obtener_repo()
    if request.method == "POST":
        cambios = {k: v for k, v in request.form.items() if k in ("titulo", "autor", "anio", "categoria")}
        r = llamar(libros.editar_libro, repo, libro_id, cambios)
        avisar(r, "Libro actualizado")
        if r.ok:
            return redirect(url_for("ver_libros"))
    libro = repo.obtener("libros", libro_id)
    if libro is None:
        flash("Ese libro no existe", "error")
        return redirect(url_for("ver_libros"))
    return render_template("libro_editar.html", libro=libro)


@app.post("/libros/<int:libro_id>/eliminar")
def eliminar_libro(libro_id):
    r = llamar(libros.eliminar_libro, obtener_repo(), libro_id)
    avisar(r, "Libro eliminado")
    return redirect(url_for("ver_libros"))


# ---------------------------------------------------------------- socios
@app.route("/socios")
def ver_socios():
    repo = obtener_repo()
    q = request.args.get("q", "")
    solo_activos = request.args.get("solo_activos") == "1"
    if q:
        lista = llamar(socios.buscar_socios, repo, q)
        modo = "buscar_socios()"
    else:
        lista = llamar(socios.listar_socios, repo, solo_activos)
        modo = "listar_socios()"
    return render_template("socios.html", lista=lista, modo=modo, q=q, solo_activos=solo_activos,
                           stats=llamar(socios.estadisticas_socios, repo))


@app.post("/socios/registrar")
def registrar_socio():
    f = request.form
    r = llamar(socios.registrar_socio, obtener_repo(), f.get("nombre", ""),
               f.get("correo", ""), f.get("telefono", ""))
    avisar(r, f"Socio registrado con número {r.valor}")
    return redirect(url_for("ver_socios"))


@app.route("/socios/<int:socio_id>/editar", methods=["GET", "POST"])
def editar_socio(socio_id):
    repo = obtener_repo()
    if request.method == "POST":
        cambios = {k: v for k, v in request.form.items() if k in ("nombre", "correo", "telefono")}
        r = llamar(socios.editar_socio, repo, socio_id, cambios)
        avisar(r, "Socio actualizado")
        if r.ok:
            return redirect(url_for("ver_socios"))
    socio = repo.obtener("socios", socio_id)
    if socio is None:
        flash("Ese socio no existe", "error")
        return redirect(url_for("ver_socios"))
    return render_template("socio_editar.html", socio=socio)


@app.post("/socios/<int:socio_id>/estado")
def cambiar_estado(socio_id):
    activar = request.form.get("activo") == "1"
    r = llamar(socios.cambiar_estado_socio, obtener_repo(), socio_id, activar)
    avisar(r, "Socio reactivado" if activar else "Socio suspendido")
    return redirect(url_for("ver_socios"))


# ---------------------------------------------------------------- préstamos
@app.route("/prestamos")
def ver_prestamos():
    repo = obtener_repo()
    multa = None
    if request.args.get("limite") and request.args.get("devolucion"):
        multa = llamar(prestamos.calcular_multa, request.args["limite"], request.args["devolucion"])
    return render_template(
        "prestamos.html",
        activos=llamar(prestamos.listar_prestamos_activos, repo),
        vencidos=llamar(prestamos.prestamos_vencidos, repo),
        reporte=llamar(prestamos.reporte_prestamos, repo),
        multa=multa,
        limite=request.args.get("limite", ""),
        devolucion=request.args.get("devolucion", ""),
        libros_disp=repo.filtrar("libros", lambda l: l["disponible"]),
        socios_act=repo.filtrar("socios", lambda s: s["activo"]),
    )


@app.post("/prestamos/registrar")
def registrar_prestamo():
    try:
        libro_id = int(request.form.get("libro_id", ""))
        socio_id = int(request.form.get("socio_id", ""))
    except ValueError:
        flash("Selecciona un libro y un socio", "error")
        return redirect(url_for("ver_prestamos"))
    r = llamar(prestamos.registrar_prestamo, obtener_repo(), libro_id, socio_id)
    avisar(r, f"Préstamo registrado con folio {r.valor}")
    return redirect(url_for("ver_prestamos"))


@app.post("/prestamos/<int:prestamo_id>/devolver")
def devolver(prestamo_id):
    r = llamar(prestamos.registrar_devolucion, obtener_repo(), prestamo_id)
    if r.ok:
        flash(f"Devolución registrada. Multa: ${r.valor:.2f}", "exito")
    else:
        avisar(r, "")
    return redirect(url_for("ver_prestamos"))


# ---------------------------------------------------------------- utilidades
@app.post("/reiniciar")
def reiniciar():
    RUTA_DATOS.unlink(missing_ok=True)
    flash("Datos de ejemplo restaurados", "exito")
    return redirect(request.referrer or url_for("inicio"))


if __name__ == "__main__":
    if "--reiniciar" in sys.argv:
        RUTA_DATOS.unlink(missing_ok=True)
        print("Datos de ejemplo restaurados.")
    app.run(debug=True)
